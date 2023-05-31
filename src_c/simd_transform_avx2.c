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
    //     2. remove the alpha channel for every pixel and save it.
    //     3. multiply weights by pixels using standard shuffle to 2x 16bit
    //        register, mul + 255 then left shift. See multiply blitter mode
    //        for this operation in isolation.
    //     4. pack pixels back together from A & B while adding with a
    //        horizontal add (e.g. adds A+R and G+B in a ARGB layout)
    //     5. shift and add to make final grey pixel colour in 0th
    //        8Bit channel in each 'pixel'
    //     6. shuffle again to push the grey from the 0th channel into every
    //        channel of every pixel.
    //     7. add the alpha channel back in.

    // Things to fix:
    //     1. Would be nice to only use AVX2 stuff for the single pixel stuff.
    //     2. Get inspiration from Starbuck's AVX2 macros

    int s_row_skip = (src->pitch - src->w * src->format->BytesPerPixel) >> 2;

    // generate number of batches of pixels we need to loop through
    int pixel_batch_length = src->w * src->h;
    int num_batches = 1;
    if (s_row_skip > 0) {
        pixel_batch_length = src->w;
        num_batches = src->h;
    }

    int remaining_pixels = pixel_batch_length % 8;
    int perfect_8_pixels = (pixel_batch_length - remaining_pixels) / 8;

    int perfect_8_pixels_batch_counter = perfect_8_pixels;
    int remaining_pixels_batch_counter = remaining_pixels;

    Uint32 *srcp = (Uint32 *)src->pixels;
    Uint32 *dstp = (Uint32 *)newsurf->pixels;

    Uint32 rgbmask =
        (src->format->Rmask | src->format->Gmask | src->format->Bmask);
    Uint32 amask = ~rgbmask;

    int rgb_weights =
        ((0x4C << src->format->Rshift) | (0x96 << src->format->Gshift) |
         (0x1D << src->format->Bshift));

    __m256i *srcp256 = (__m256i *)src->pixels;
    __m256i *dstp256 = (__m256i *)newsurf->pixels;

    __m128i mm_src, mm_dst, mm_alpha, mm_zero, mm_two_five_fives,
        mm_rgb_weights, mm_alpha_mask, mm_rgb_mask;
    __m256i mm256_src, mm256_srcA, mm256_srcB, mm256_dst, mm256_dstA,
        mm256_dstB, mm256_shuff_mask_A, mm256_shuff_mask_B,
        mm256_two_five_fives, mm256_rgb_weights, mm256_shuff_mask_gray,
        mm256_alpha, mm256_rgb_mask, mm256_alpha_mask;

    mm256_shuff_mask_A =
        _mm256_set_epi8(0x80, 23, 0x80, 22, 0x80, 21, 0x80, 20, 0x80, 19, 0x80,
                        18, 0x80, 17, 0x80, 16, 0x80, 7, 0x80, 6, 0x80, 5,
                        0x80, 4, 0x80, 3, 0x80, 2, 0x80, 1, 0x80, 0);
    mm256_shuff_mask_B =
        _mm256_set_epi8(0x80, 31, 0x80, 30, 0x80, 29, 0x80, 28, 0x80, 27, 0x80,
                        26, 0x80, 25, 0x80, 24, 0x80, 15, 0x80, 14, 0x80, 13,
                        0x80, 12, 0x80, 11, 0x80, 10, 0x80, 9, 0x80, 8);

    mm256_shuff_mask_gray = _mm256_set_epi8(
        28, 28, 28, 28, 24, 24, 24, 24, 20, 20, 20, 20, 16, 16, 16, 16, 12, 12,
        12, 12, 8, 8, 8, 8, 4, 4, 4, 4, 0, 0, 0, 0);

    mm_zero = _mm_setzero_si128();
    mm_alpha_mask = _mm_cvtsi32_si128(amask);
    mm_rgb_mask = _mm_cvtsi32_si128(rgbmask);
    mm_two_five_fives = _mm_set_epi64x(0x00FF00FF00FF00FF, 0x00FF00FF00FF00FF);
    mm_rgb_weights =
        _mm_unpacklo_epi8(_mm_cvtsi32_si128(rgb_weights), mm_zero);

    mm256_two_five_fives = _mm256_set1_epi16(0x00FF);
    mm256_rgb_weights = _mm256_set1_epi32(rgb_weights);
    mm256_rgb_mask = _mm256_set1_epi32(rgbmask);
    mm256_alpha_mask = _mm256_set1_epi32(amask);

    while (num_batches--) {
        perfect_8_pixels_batch_counter = perfect_8_pixels;
        remaining_pixels_batch_counter = remaining_pixels;
        while (perfect_8_pixels_batch_counter--) {
            mm256_src = _mm256_loadu_si256(srcp256);
            mm256_alpha = _mm256_subs_epu8(mm256_src, mm256_rgb_mask);

            mm256_srcA = _mm256_shuffle_epi8(mm256_src, mm256_shuff_mask_A);
            mm256_srcB = _mm256_shuffle_epi8(mm256_src, mm256_shuff_mask_B);

            mm256_dstA =
                _mm256_shuffle_epi8(mm256_rgb_weights, mm256_shuff_mask_A);
            mm256_dstB =
                _mm256_shuffle_epi8(mm256_rgb_weights, mm256_shuff_mask_B);

            mm256_dstA = _mm256_mullo_epi16(mm256_srcA, mm256_dstA);
            mm256_dstA = _mm256_add_epi16(mm256_dstA, mm256_two_five_fives);
            mm256_dstA = _mm256_srli_epi16(mm256_dstA, 8);

            mm256_dstB = _mm256_mullo_epi16(mm256_srcB, mm256_dstB);
            mm256_dstB = _mm256_add_epi16(mm256_dstB, mm256_two_five_fives);
            mm256_dstB = _mm256_srli_epi16(mm256_dstB, 8);

            mm256_dst = _mm256_hadd_epi16(mm256_dstA, mm256_dstB);
            mm256_dst =
                _mm256_add_epi16(mm256_dst, _mm256_srli_epi32(mm256_dst, 16));
            mm256_dst = _mm256_shuffle_epi8(mm256_dst, mm256_shuff_mask_gray);

            mm256_dst = _mm256_subs_epu8(mm256_dst, mm256_alpha_mask);
            mm256_dst = _mm256_adds_epu8(mm256_dst, mm256_alpha);

            _mm256_storeu_si256(dstp256, mm256_dst);

            srcp256++;
            dstp256++;
        }
        srcp = (Uint32 *)srcp256;
        dstp = (Uint32 *)dstp256;
        while (remaining_pixels_batch_counter--) {
            mm_src = _mm_cvtsi32_si128(*srcp);
            /*mm_src = 0x000000000000000000000000AARRGGBB*/
            mm_alpha = _mm_subs_epu8(mm_src, mm_rgb_mask);
            /*mm_src = 0x00000000000000000000000000RRGGBB*/
            mm_src = _mm_unpacklo_epi8(mm_src, mm_zero);
            /*mm_src = 0x0000000000000000000000RR00GG00BB*/

            mm_dst = _mm_mullo_epi16(mm_src, mm_rgb_weights);
            /*mm_dst = 0x00000000000000000000RRRRGGGGBBBB*/
            mm_dst = _mm_add_epi16(mm_dst, mm_two_five_fives);
            /*mm_dst = 0x00000000000000000000RRRRGGGGBBBB*/
            mm_dst = _mm_srli_epi16(mm_dst, 8);
            /*mm_dst = 0x0000000000000000000000RR00GG00BB*/

            mm_dst = _mm_hadd_epi16(mm_dst, mm_dst);  // This requires SSE3
            mm_dst = _mm_shufflelo_epi16(_mm_hadd_epi16(mm_dst, mm_dst),
                                         _MM_SHUFFLE(0, 0, 0, 0));
            /*mm_dst = 0x000000000000000000GrGr00GrGr00GrGr00GrGr*/

            mm_dst = _mm_packus_epi16(mm_dst, mm_dst);
            /*mm_dst = 0x000000000000000000000000GrGrGrGrGrGrGrGr*/
            mm_dst = _mm_subs_epu8(mm_dst, mm_alpha_mask);
            mm_dst = _mm_add_epi16(mm_dst, mm_alpha);
            /*mm_dst = 0x000000000000000000000000AAGrGrGrGrGrGr*/
            *dstp = _mm_cvtsi128_si32(mm_dst);
            /*dstp = 0xAARRGGBB*/
            srcp++;
            dstp++;
        }
        srcp += s_row_skip;
        srcp256 = (__m256i *)srcp;
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
