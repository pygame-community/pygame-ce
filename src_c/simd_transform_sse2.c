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
invert_sse2(SDL_Surface *src, SDL_Surface *newsurf)
{
    int s_row_skip = (src->pitch - src->w * 4) / 4;

    // generate number of batches of pixels we need to loop through
    int pixel_batch_length = src->w * src->h;
    int num_batches = 1;
    if (s_row_skip > 0) {
        pixel_batch_length = src->w;
        num_batches = src->h;
    }
    int remaining_pixels = pixel_batch_length % 4;
    int perfect_4_pixels = pixel_batch_length / 4;

    int perfect_4_pixels_batch_counter = perfect_4_pixels;
    int remaining_pixels_batch_counter = remaining_pixels;

    Uint32 *srcp = (Uint32 *)src->pixels;
    Uint32 *dstp = (Uint32 *)newsurf->pixels;

    Uint32 rgbmask =
        (src->format->Rmask | src->format->Gmask | src->format->Bmask);
    Uint64 rgbmask64 = ((Uint64)rgbmask << 32) | rgbmask;
    Uint64 amask64 = ~rgbmask64;

    __m128i mm_src, mm_dst, mm_alpha, mm_rgb_invert_mask, mm_alpha_mask;

    __m128i *srcp128 = (__m128i *)src->pixels;
    __m128i *dstp128 = (__m128i *)newsurf->pixels;

    mm_rgb_invert_mask = _mm_set1_epi64x(rgbmask64);
    mm_alpha_mask = _mm_set1_epi64x(amask64);

    while (num_batches--) {
        perfect_4_pixels_batch_counter = perfect_4_pixels;
        remaining_pixels_batch_counter = remaining_pixels;
        while (perfect_4_pixels_batch_counter--) {
            mm_src = _mm_loadu_si128(srcp128);
            /*mm_src = 0xAARRGGBBAARRGGBBAARRGGBBAARRGGBB*/

            /* pull out the alpha */
            mm_alpha = _mm_and_si128(mm_src, mm_alpha_mask);

            /* do the invert */
            mm_dst = _mm_andnot_si128(mm_src, mm_rgb_invert_mask);

            /* put the alpha back in*/
            mm_dst = _mm_or_si128(mm_dst, mm_alpha);

            _mm_storeu_si128(dstp128, mm_dst);
            /*dstp = 0xAARRGGBBAARRGGBBAARRGGBBAARRGGBB*/
            srcp128++;
            dstp128++;
        }
        srcp = (Uint32 *)srcp128;
        dstp = (Uint32 *)dstp128;
        if (remaining_pixels_batch_counter > 0) {
            mm_src = _mm_cvtsi32_si128(*srcp);
            /*mm_src = 0x000000000000000000000000AARRGGBB*/

            /* pull out the alpha */
            mm_alpha = _mm_and_si128(mm_src, mm_alpha_mask);

            /* do the invert */
            mm_dst = _mm_andnot_si128(mm_src, mm_rgb_invert_mask);

            /* put the alpha back in*/
            mm_dst = _mm_or_si128(mm_dst, mm_alpha);

            *dstp = _mm_cvtsi128_si32(mm_dst);
            /*dstp = 0xAARRGGBB*/
            srcp++;
            dstp++;
        }
        srcp += s_row_skip;
        srcp128 = (__m128i *)srcp;
    }
}
#endif /* __SSE2__ || PG_ENABLE_ARM_NEON*/
