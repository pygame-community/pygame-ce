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

#if defined(ENV64BIT)
#define LOAD_64_INTO_M128(num, reg) *reg = _mm_cvtsi64_si128(*num)
#define STORE_M128_INTO_64(reg, num) *num = _mm_cvtsi128_si64(*reg)
#else
#define LOAD_64_INTO_M128(num, reg) \
    *reg = _mm_loadl_epi64((const __m128i *)num)
#define STORE_M128_INTO_64(reg, num) _mm_storel_epi64((__m128i *)num, *reg)
#endif

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
    int remaining_pixels = pixel_batch_length % 2;
    int perfect_2_pixels = pixel_batch_length / 2;

    int perfect_2_pixels_batch_counter = perfect_2_pixels;
    int remaining_pixels_batch_counter = remaining_pixels;

    Uint32 *srcp = (Uint32 *)src->pixels;
    Uint32 *dstp = (Uint32 *)newsurf->pixels;

    Uint32 rgbmask =
        (src->format->Rmask | src->format->Gmask | src->format->Bmask);
    Uint64 rgbmask64 = ((Uint64)rgbmask << 32) | rgbmask;
    Uint64 amask64 = ~rgbmask64;

    Uint64 *srcp64 = (Uint64 *)src->pixels;
    Uint64 *dstp64 = (Uint64 *)newsurf->pixels;

    __m128i mm_src, mm_dst, mm_alpha, mm_two_five_fives,
        mm_alpha_mask, mm_rgb_mask;

    LOAD_64_INTO_M128(&amask64, &mm_alpha_mask);
    LOAD_64_INTO_M128(&rgbmask64, &mm_rgb_mask);
    mm_two_five_fives = _mm_set1_epi64x(0xFFFFFFFFFFFFFFFF);

    while (num_batches--) {
        perfect_2_pixels_batch_counter = perfect_2_pixels;
        remaining_pixels_batch_counter = remaining_pixels;
        while (perfect_2_pixels_batch_counter--) {
            LOAD_64_INTO_M128(srcp64, &mm_src);
            /*mm_src = 0x0000000000000000AARRGGBBAARRGGBB*/
            /* First we strip out the alpha so we have one of our 4 channels
               empty for the rest of the calculation */
            mm_alpha = _mm_subs_epu8(mm_src, mm_rgb_mask);
            /*mm_src = 0x000000000000000000RRGGBB00RRGGBB*/

            /*invert the colours*/
            mm_dst = _mm_subs_epu8(mm_two_five_fives, mm_src);

            /*add the alpha channel back*/
            mm_dst = _mm_subs_epu8(mm_dst, mm_alpha_mask);
            mm_dst = _mm_adds_epu8(mm_dst, mm_alpha);
            /*mm_dst = 0x0000000000000000AAGrGrGrGrGrGrAAGrGrGrGrGrGr*/
            STORE_M128_INTO_64(&mm_dst, dstp64);
            /*dstp = 0xAARRGGBB*/
            srcp64++;
            dstp64++;
        }
        srcp = (Uint32 *)srcp64;
        dstp = (Uint32 *)dstp64;
        if (remaining_pixels_batch_counter > 0) {
            mm_src = _mm_cvtsi32_si128(*srcp);
            /*mm_src = 0x000000000000000000000000AARRGGBB*/
            /* First we strip out the alpha so we have one of our 4 channels
               empty for the rest of the calculation */
            mm_alpha = _mm_subs_epu8(mm_src, mm_rgb_mask);
            /*mm_src = 0x00000000000000000000000000RRGGBB*/

             /*invert the colours*/
            mm_dst = _mm_subs_epu8(mm_two_five_fives, mm_src);

            /*add the alpha channel back*/
            mm_dst = _mm_subs_epu8(mm_dst, mm_alpha_mask);
            mm_dst = _mm_adds_epu8(mm_dst, mm_alpha);
            /*mm_dst = 0x000000000000000000000000AAGrGrGrGrGrGr*/
            *dstp = _mm_cvtsi128_si32(mm_dst);
            /*dstp = 0xAARRGGBB*/
            srcp++;
            dstp++;
        }
        srcp += s_row_skip;
        srcp64 = (Uint64 *)srcp;
    }
}
#endif /* __SSE2__ || PG_ENABLE_ARM_NEON*/
