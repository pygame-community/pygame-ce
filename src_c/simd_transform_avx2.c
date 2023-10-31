#include "simd_transform.h"

#if defined(HAVE_IMMINTRIN_H) && !defined(SDL_DISABLE_IMMINTRIN_H)
#include <immintrin.h>
#endif /* defined(HAVE_IMMINTRIN_H) && !defined(SDL_DISABLE_IMMINTRIN_H) */

#define BAD_AVX2_FUNCTION_CALL                                               \
    printf(                                                                  \
        "Fatal Error: Attempted calling an AVX2 function when both compile " \
        "time and runtime support is missing. If you are seeing this "       \
        "message, you have stumbled across a pygame bug, please report it "  \
        "to the devs!");                                                     \
    PG_EXIT(1)

/* helper function that does a runtime check for AVX2. It has the added
 * functionality of also returning 0 if compile time support is missing */
int
pg_has_avx2()
{
#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
    return SDL_HasAVX2();
#else
    return 0;
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */
}

/* This returns 1 when avx2 is available at runtime but support for it isn't
 * compiled in, 0 in all other cases */
int
pg_avx2_at_runtime_but_uncompiled()
{
    if (SDL_HasAVX2()) {
#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
        return 0;
#else
        return 1;
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */
    }
    return 0;
}

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
invert_avx2(SDL_Surface *src, SDL_Surface *newsurf)
{
    int s_row_skip = (src->pitch - src->w * 4) / 4;

    // generate number of batches of pixels we need to loop through
    int pixel_batch_length = src->w * src->h;
    int num_batches = 1;
    if (s_row_skip > 0) {
        pixel_batch_length = src->w;
        num_batches = src->h;
    }

    int remaining_pixels = pixel_batch_length % 8;
    int perfect_8_pixels = pixel_batch_length / 8;

    int perfect_8_pixels_batch_counter = perfect_8_pixels;
    int remaining_pixels_batch_counter = remaining_pixels;

    Uint32 *srcp = (Uint32 *)src->pixels;
    Uint32 *dstp = (Uint32 *)newsurf->pixels;

    Uint32 rgbmask =
        (src->format->Rmask | src->format->Gmask | src->format->Bmask);
    Uint32 amask = ~rgbmask;

    __m256i *srcp256 = (__m256i *)src->pixels;
    __m256i *dstp256 = (__m256i *)newsurf->pixels;

    __m256i mm256_src, mm256_dst, mm256_rgb_invert_mask, mm256_alpha,
        mm256_alpha_mask;

    mm256_rgb_invert_mask = _mm256_set1_epi32(rgbmask);
    mm256_alpha_mask = _mm256_set1_epi32(amask);

    __m256i _partial8_mask =
        _mm256_set_epi32(0x00, (remaining_pixels > 6) ? 0x80000000 : 0x00,
                         (remaining_pixels > 5) ? 0x80000000 : 0x00,
                         (remaining_pixels > 4) ? 0x80000000 : 0x00,
                         (remaining_pixels > 3) ? 0x80000000 : 0x00,
                         (remaining_pixels > 2) ? 0x80000000 : 0x00,
                         (remaining_pixels > 1) ? 0x80000000 : 0x00,
                         (remaining_pixels > 0) ? 0x80000000 : 0x00);

    while (num_batches--) {
        perfect_8_pixels_batch_counter = perfect_8_pixels;
        remaining_pixels_batch_counter = remaining_pixels;
        while (perfect_8_pixels_batch_counter--) {
            mm256_src = _mm256_loadu_si256(srcp256);

            /* pull out the alpha */
            mm256_alpha = _mm256_and_si256(mm256_src, mm256_alpha_mask);

            /* do the invert */
            mm256_dst = _mm256_andnot_si256(mm256_src, mm256_rgb_invert_mask);

            /* put the alpha back in*/
            mm256_dst = _mm256_or_si256(mm256_dst, mm256_alpha);

            _mm256_storeu_si256(dstp256, mm256_dst);

            srcp256++;
            dstp256++;
        }
        srcp = (Uint32 *)srcp256;
        dstp = (Uint32 *)dstp256;
        if (remaining_pixels_batch_counter > 0) {
            mm256_src = _mm256_maskload_epi32((int *)srcp, _partial8_mask);

            /* pull out the alpha */
            mm256_alpha = _mm256_and_si256(mm256_src, mm256_alpha_mask);

            /* do the invert */
            mm256_dst = _mm256_andnot_si256(mm256_src, mm256_rgb_invert_mask);

            /* put the alpha back in*/
            mm256_dst = _mm256_or_si256(mm256_dst, mm256_alpha);

            _mm256_maskstore_epi32((int *)dstp, _partial8_mask, mm256_dst);

            srcp += remaining_pixels_batch_counter;
            dstp += remaining_pixels_batch_counter;
        }
        srcp += s_row_skip;
        srcp256 = (__m256i *)srcp;
    }
}
#else
void
invert_avx2(SDL_Surface *src, SDL_Surface *newsurf)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */
