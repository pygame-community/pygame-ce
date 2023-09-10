#include "simd_transform.h"

#if PG_ENABLE_ARM_NEON
// sse2neon.h is from here: https://github.com/DLTcollab/sse2neon
#include "include/sse2neon.h"
#endif /* PG_ENABLE_ARM_NEON */

/* This returns 1 when sse2 is available at runtime but support for it isn't
 * compiled in, 0 in all other cases */
int
pg_sse2_at_runtime_but_uncompiled()
{
    if (SDL_HasSSE2()) {
#ifdef __SSE2__
        return 0;
#else
        return 1;
#endif /* __SSE2__ */
    }
    return 0;
}

/* This returns 1 when neon is available at runtime but support for it isn't
 * compiled in, 0 in all other cases */
int
pg_neon_at_runtime_but_uncompiled()
{
    if (SDL_HasNEON()) {
#if PG_ENABLE_ARM_NEON
        return 0;
#else
        return 1;
#endif /* PG_ENABLE_ARM_NEON */
    }
    return 0;
}

#if (defined(__SSE2__) || defined(PG_ENABLE_ARM_NEON))
void
grayscale_sse2(SDL_Surface *src, SDL_Surface *newsurf)
{
    /* For the SSE2 SIMD version of grayscale we do one pixel at a time
     * Thus we can calculate the number of loops (and pixels) by multiplying
     * the width of the surface to be grayscaled, by the height of that
     * surface.
     *
     * We also need to calculate a 'skip value' in case our surface's rows are
     * not contiguous in memory. For surfaces, a single row's worth of pixel
     * data is always contiguous (i.e. each pixel is next to each other).
     * However, a surface's rows may be seperated from one another in memory,
     * most commonly this happens with sub surfaces.
     * The vast majority of surfaces used in applications will probably also
     * have contiguous rows as that is what happens when you create a standard
     * 32bit surface with pygame.Surface. SIMD Transform algorithms,
     * should treat this 'most normal' case as the critical path to maximise
     * performance.
     */
    int s_row_skip = (src->pitch - src->w * src->format->BytesPerPixel) >> 2;

    // generate number of batches of pixels we need to loop through
    int pixel_batch_length = src->w * src->h;
    int num_batches = 1;
    if (s_row_skip > 0) {
        pixel_batch_length = src->w;
        num_batches = src->h;
    }
    int pixel_batch_counter = pixel_batch_length;

    Uint32 *srcp = (Uint32 *)src->pixels;
    Uint32 *dstp = (Uint32 *)newsurf->pixels;

    Uint32 rgbmask =
        (src->format->Rmask | src->format->Gmask | src->format->Bmask);
    Uint32 amask = ~rgbmask;

    int rgb_weights =
        ((0x4C << src->format->Rshift) | (0x96 << src->format->Gshift) |
         (0x1D << src->format->Bshift));

    __m128i mm_src, mm_dst, mm_alpha, mm_zero, mm_two_five_fives,
        mm_rgb_weights, mm_alpha_mask, mm_rgb_mask;

    mm_zero = _mm_setzero_si128();
    mm_alpha_mask = _mm_cvtsi32_si128(amask);
    mm_rgb_mask = _mm_cvtsi32_si128(rgbmask);
    mm_two_five_fives = _mm_set1_epi64x(0x00FF00FF00FF00FF);
    mm_rgb_weights =
        _mm_unpacklo_epi8(_mm_cvtsi32_si128(rgb_weights), mm_zero);

    while (num_batches--) {
        pixel_batch_counter = pixel_batch_length;
        while (pixel_batch_counter--) {
            mm_src = _mm_cvtsi32_si128(*srcp);
            /*mm_src = 0x000000000000000000000000AARRGGBB*/
            /* First we strip out the alpha so we have one of our 4 channels
               empty for the rest of the calculation */
            mm_alpha = _mm_subs_epu8(mm_src, mm_rgb_mask);
            /*mm_src = 0x00000000000000000000000000RRGGBB*/

            /* This is where we do the efficient 8bit 'floating point multiply'
               operation of each channel by the weights - using a 16bit integer
               multiply, an add and a bitshift. We use this trick repeatedly
               for multiplication by a 0 to 1 value in SIMD code.
            */
            mm_src = _mm_unpacklo_epi8(mm_src, mm_zero);
            /*mm_src = 0x0000000000000000000000RR00GG00BB*/
            mm_dst = _mm_mullo_epi16(mm_src, mm_rgb_weights);
            /*mm_dst = 0x00000000000000000000RRRRGGGGBBBB*/
            mm_dst = _mm_add_epi16(mm_dst, mm_two_five_fives);
            /*mm_dst = 0x00000000000000000000RRRRGGGGBBBB*/
            mm_dst = _mm_srli_epi16(mm_dst, 8);
            /*mm_dst = 0x0000000000000000000000RR00GG00BB*/

            /* now we have the multiplied channels we 'shuffle them out' one
             * at a time so there are four copies of red, four copies of green,
             * four copies of blue etc. Then we add all these together
             * so each of channels contains R+G+B.
             */
            mm_dst = _mm_adds_epu8(
                _mm_adds_epu8(
                    _mm_shufflelo_epi16(mm_dst, _PG_SIMD_SHUFFLE(0, 0, 0, 0)),
                    _mm_shufflelo_epi16(mm_dst, _PG_SIMD_SHUFFLE(1, 1, 1, 1))),
                _mm_adds_epu8(
                    _mm_shufflelo_epi16(mm_dst, _PG_SIMD_SHUFFLE(2, 2, 2, 2)),
                    _mm_shufflelo_epi16(mm_dst,
                                        _PG_SIMD_SHUFFLE(3, 3, 3, 3))));
            /* Gr here stands for 'Gray' as we've now added all the channels
             * back together after multiplying them above.
             * mm_dst = 0x000000000000000000GrGr00GrGr00GrGr00GrGr
             */

            /* The rest is just packing the grayscale back to the original
             * 8bit pixel layout and adding the alpha we removed earlier back
             * in again
             */
            mm_dst = _mm_packus_epi16(mm_dst, mm_dst);
            /*mm_dst = 0x000000000000000000000000GrGrGrGrGrGrGrGr*/
            mm_dst = _mm_subs_epu8(mm_dst, mm_alpha_mask);
            mm_dst = _mm_adds_epu8(mm_dst, mm_alpha);
            /*mm_dst = 0x000000000000000000000000AAGrGrGrGrGrGr*/
            *dstp = _mm_cvtsi128_si32(mm_dst);
            /*dstp = 0xAARRGGBB*/
            srcp++;
            dstp++;
        }
        srcp += s_row_skip;
    }
}
#endif /* __SSE2__ || PG_ENABLE_ARM_NEON*/
