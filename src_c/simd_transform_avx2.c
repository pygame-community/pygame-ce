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

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
grayscale_avx2(SDL_Surface *src, SDL_Surface *newsurf)
{

    // Current AVX2 process
    // ------------------
    // - pre loop: Load weights into register x8
    // - in loop:
    //     1. Load 8 pixels into register
    //     2. multiply weights by pixels using standard shuffle to 2x 16bit
    //        register, mul + 255 then left shift
    //     3. pack it back together
    //     3. shuffle again into three channel registers
    //        (red & alpha together, then blue and finally green)
    //     4. add the shuffled channels together

    // Things to fix:
    //     1. Currently this assumes and ARGB pixel layout, ideally we need to
    //        make it 32bit pixel format agnostic.
    //     2. SSE2 single pixel version - see current single pixel path.
    //     2. Would be nice to only use AVX2 stuff for the single pixel stuff.
    //     3. Get inspiration from Starbuck's AVX2 macros


    int n;
    int width = src->w;
    int height = src->h;

    Uint32 *srcp = (Uint32 *)src->pixels;
    Uint32 *dstp = (Uint32 *)newsurf->pixels;

    int skip = (src->pitch - width * src->format->BytesPerPixel) >> 2;
    int pxskip = src->format->BytesPerPixel >> 2;

    int pre_8_width = width % 8;
    int post_8_width = (width - pre_8_width) / 8;

    __m256i *srcp256 = (__m256i *)src->pixels;
    __m256i *dstp256 = (__m256i *)newsurf->pixels;

    __m128i mm_src, mm_dst, mm_zero, mm_two_five_fives, mm_rgb_weights;
    __m256i mm256_src, mm256_srcA, mm256_srcB, mm256_dst, mm256_dstA,
        mm256_dstB, mm256_shuff_mask_A, mm256_shuff_mask_B,
        mm256_two_five_fives, mm256_rgb_weights, mm256_shuff_mask_red_alpha,
        mm256_shuff_mask_green, mm256_shuff_mask_blue;

    mm256_shuff_mask_A =
        _mm256_set_epi8(0x80, 23, 0x80, 22, 0x80, 21, 0x80, 20, 0x80, 19, 0x80,
                        18, 0x80, 17, 0x80, 16, 0x80, 7, 0x80, 6, 0x80, 5,
                        0x80, 4, 0x80, 3, 0x80, 2, 0x80, 1, 0x80, 0);
    mm256_shuff_mask_B =
        _mm256_set_epi8(0x80, 31, 0x80, 30, 0x80, 29, 0x80, 28, 0x80, 27, 0x80,
                        26, 0x80, 25, 0x80, 24, 0x80, 15, 0x80, 14, 0x80, 13,
                        0x80, 12, 0x80, 11, 0x80, 10, 0x80, 9, 0x80, 8);

    mm256_shuff_mask_red_alpha =
        _mm256_set_epi8(31, 28, 28, 28, 27, 24, 24, 24,
                        23, 20, 20, 20, 19, 16, 16, 16,
                        15, 12, 12, 12, 11, 8, 8, 8,
                        7, 4, 4, 4, 3, 0, 0, 0);

    mm256_shuff_mask_green =
        _mm256_set_epi8(0x80, 29, 29, 29, 0x80, 25, 25, 25,
                        0x80, 21, 21, 21, 0x80, 17, 17, 17,
                        0x80, 13, 13, 13, 0x80, 9, 9, 9,
                        0x80, 5, 5, 5, 0x80, 1, 1, 1);

    mm256_shuff_mask_blue =
        _mm256_set_epi8(0x80, 30, 30, 30, 0x80, 26, 26, 26,
                        0x80, 22, 22, 22, 0x80, 18, 18, 18,
                        0x80, 14, 14, 14, 0x80, 10, 10, 10,
                        0x80, 6, 6, 6, 0x80, 2, 2, 2);

    mm_zero = _mm_setzero_si128();
    mm_two_five_fives = _mm_set_epi64x(0x00FF00FF00FF00FF, 0x00FF00FF00FF00FF);
    mm_rgb_weights = _mm_set_epi64x(0xFF4C961DFF4C961D, 0xFF4C961DFF4C961D);

    mm256_two_five_fives = _mm256_set_epi8(
        0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF,
        0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF,
        0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF);

    mm256_rgb_weights = _mm256_set_epi8(
        0xFF, 0x4C, 0x96, 0x1D,
        0xFF, 0x4C, 0x96, 0x1D,
        0xFF, 0x4C, 0x96, 0x1D,
        0xFF, 0x4C, 0x96, 0x1D,
        0xFF, 0x4C, 0x96, 0x1D,
        0xFF, 0x4C, 0x96, 0x1D,
        0xFF, 0x4C, 0x96, 0x1D,
        0xFF, 0x4C, 0x96, 0x1D);


    while (height--) {
        if (pre_8_width > 0) {
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
                        _mm_add_epi16(_mm_shufflelo_epi16(mm_dst, _MM_SHUFFLE( 3,0,0,0)),
                                      _mm_shufflelo_epi16(mm_dst, _MM_SHUFFLE(-1,1,1,1))),
                                      _mm_shufflelo_epi16(mm_dst, _MM_SHUFFLE(-1,2,2,2)));

                    mm_dst = _mm_packus_epi16(mm_dst, mm_dst);
                    /*mm_dst = 0x00000000AARRGGBB00000000AARRGGBB*/
                    *dstp = _mm_cvtsi128_si32(mm_dst);
                    /*dstp = 0xAARRGGBB*/
                    srcp += pxskip;
                    dstp += pxskip;
                },
                n, pre_8_width);
        }
        srcp256 = (__m256i *)srcp;
        dstp256 = (__m256i *)dstp;
        if (post_8_width > 0) {
            LOOP_UNROLLED4(
                {
                    mm256_src = _mm256_loadu_si256(srcp256);

                    mm256_srcA =
                        _mm256_shuffle_epi8(mm256_src, mm256_shuff_mask_A);
                    mm256_srcB =
                        _mm256_shuffle_epi8(mm256_src, mm256_shuff_mask_B);

                    mm256_dstA =
                        _mm256_shuffle_epi8(mm256_rgb_weights, mm256_shuff_mask_A);
                    mm256_dstB =
                        _mm256_shuffle_epi8(mm256_rgb_weights, mm256_shuff_mask_B);

                    mm256_dstA = _mm256_mullo_epi16(mm256_srcA, mm256_dstA);
                    mm256_dstA =
                        _mm256_add_epi16(mm256_dstA, mm256_two_five_fives);
                    mm256_dstA = _mm256_srli_epi16(mm256_dstA, 8);

                    mm256_dstB = _mm256_mullo_epi16(mm256_srcB, mm256_dstB);
                    mm256_dstB =
                        _mm256_add_epi16(mm256_dstB, mm256_two_five_fives);
                    mm256_dstB = _mm256_srli_epi16(mm256_dstB, 8);

                    mm256_dst = _mm256_packus_epi16(mm256_dstA, mm256_dstB);

                    mm256_dstA = _mm256_shuffle_epi8(mm256_dst, mm256_shuff_mask_red_alpha);

                    mm256_dstB = _mm256_shuffle_epi8(mm256_dst, mm256_shuff_mask_green);

                    mm256_dst = _mm256_shuffle_epi8(mm256_dst, mm256_shuff_mask_blue);

                    mm256_dst = _mm256_adds_epu8(mm256_dst, mm256_dstB);
                    mm256_dst = _mm256_adds_epu8(mm256_dst, mm256_dstA);


                    _mm256_storeu_si256(dstp256, mm256_dst);

                    srcp256++;
                    dstp256++;
                },
                n, post_8_width);
        }
        srcp = (Uint32 *)srcp256 + skip;
        dstp = (Uint32 *)dstp256 + skip;
    }
}
#else
void
grayscale_avx2(SDL_Surface *src, SDL_Surface *newsurf)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */
