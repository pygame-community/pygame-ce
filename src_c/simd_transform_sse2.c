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

void
grayscale_sse2(SDL_Surface *src, SDL_Surface *newsurf)
{
    int n;
    int width = src->w;
    int height = src->h;

    Uint32 *srcp = (Uint32 *)src->pixels;
    Uint32 *dstp = (Uint32 *)newsurf->pixels;

    int skip = (src->pitch - width * src->format->BytesPerPixel) >> 2;
    int pxskip = src->format->BytesPerPixel >> 2;

    __m128i mm_src, mm_dst, mm_zero, mm_two_five_fives, mm_rgb_weights;

    mm_zero = _mm_setzero_si128();
    mm_two_five_fives = _mm_set_epi64x(0x00FF00FF00FF00FF, 0x00FF00FF00FF00FF);
    mm_rgb_weights = _mm_set_epi64x(0xFF4C961DFF4C961D, 0xFF4C961DFF4C961D);

    while (height--) {
        LOOP_UNROLLED4(
            {
                mm_src = _mm_cvtsi32_si128(*srcp);
                /*mm_src = 0x000000000000000000000000AARRGGBB*/
                mm_src = _mm_unpacklo_epi8(mm_src, mm_zero);
                /*mm_src = 0x000000000000000000AA00RR00GG00BB*/

                mm_dst = _mm_unpacklo_epi8(mm_rgb_weights, mm_zero);
                /*mm_dst = 0x000000000000000000AA00RR00GG00BB*/

                mm_dst = _mm_mullo_epi16(mm_src, mm_dst);
                /*mm_dst = 0x0000000000000000AAAARRRRGGGGBBBB*/
                mm_dst = _mm_add_epi16(mm_dst, mm_two_five_fives);
                /*mm_dst = 0x0000000000000000AAAARRRRGGGGBBBB*/
                mm_dst = _mm_srli_epi16(mm_dst, 8);
                /*mm_dst = 0x000000000000000000AA00RR00GG00BB*/

                /* red & alpha */
                mm_dst = _mm_add_epi16(
                    _mm_add_epi16(
                        _mm_shufflelo_epi16(mm_dst, _MM_SHUFFLE(3, 0, 0, 0)),
                        _mm_shufflelo_epi16(mm_dst, _MM_SHUFFLE(-1, 1, 1, 1))),
                    _mm_shufflelo_epi16(mm_dst, _MM_SHUFFLE(-1, 2, 2, 2)));

                mm_dst = _mm_packus_epi16(mm_dst, mm_dst);
                /*mm_dst = 0x00000000AARRGGBB00000000AARRGGBB*/
                *dstp = _mm_cvtsi128_si32(mm_dst);
                /*dstp = 0xAARRGGBB*/
                srcp += pxskip;
                dstp += pxskip;
            },
            n, width);

        srcp += skip;
        dstp += skip;
    }
}
