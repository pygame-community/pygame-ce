#include "_surface.h"

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
_pg_has_avx2()
{
#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
    return SDL_HasAVX2();
#else
    return 0;
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */
}

#define SETUP_AVX2_FILLER(COLOR_PROCESS_CODE)                                 \
    /* initialize surface data */                                             \
    int width = rect->w, height = rect->h;                                    \
    int bpp = surface->format->BytesPerPixel;                                 \
    int skip = (surface->pitch - width * bpp) >> 2;                           \
    int pxl_skip = bpp >> 2;                                                  \
    /* indicates the number of pixels that can't be processed in 8-pixel      \
     * blocks */                                                              \
    int pxl_excess = width % 8;                                               \
    /* indicates the number of 8-pixel blocks that can be processed */        \
    int n_iters_8 = width / 8;                                                \
    int excess_skip = pxl_excess * pxl_skip, block_skip = pxl_skip * 8;       \
    int i;                                                                    \
    /* load pixel data */                                                     \
    Uint32 *pixels = (Uint32 *)surface->pixels +                              \
                     rect->y * (surface->pitch >> 2) + rect->x * pxl_skip;    \
                                                                              \
    __m256i mm256_dst;                                                        \
    __m256i mask =                                                            \
        _mm256_set_epi32(0, pxl_excess > 6 ? -1 : 0, pxl_excess > 5 ? -1 : 0, \
                         pxl_excess > 4 ? -1 : 0, pxl_excess > 3 ? -1 : 0,    \
                         pxl_excess > 2 ? -1 : 0, pxl_excess > 1 ? -1 : 0,    \
                         pxl_excess > 0 ? -1 : 0);                            \
    /* prep and load the color */                                             \
    Uint32 amask = surface->format->Amask;                                    \
    if (amask) {                                                              \
        {                                                                     \
            COLOR_PROCESS_CODE                                                \
        }                                                                     \
    }                                                                         \
    __m256i mm256_color = _mm256_set1_epi32(color);

#define MASKED_CASE(FILL_CODE)                              \
    /* load up to 7 pixels */                               \
    mm256_dst = _mm256_maskload_epi32((int *)pixels, mask); \
                                                            \
    {FILL_CODE}                                             \
                                                            \
    /* store up to 7 pixels */                              \
    _mm256_maskstore_epi32((int *)pixels, mask, mm256_dst); \
                                                            \
    pixels += excess_skip;

#define NON_MASKED_CASE(FILL_CODE)                         \
    for (i = 0; i < n_iters_8; i++) {                      \
        /* load 8 pixels */                                \
        mm256_dst = _mm256_loadu_si256((__m256i *)pixels); \
                                                           \
        {FILL_CODE}                                        \
                                                           \
        /* store 8 pixels */                               \
        _mm256_storeu_si256((__m256i *)pixels, mm256_dst); \
                                                           \
        pixels += block_skip;                              \
    }

#define AVX_FILLER_LOOP(CASE1, CASE2) \
    while (height--) {                \
        CASE1                         \
                                      \
        CASE2                         \
                                      \
        pixels += skip;               \
    }

#define RUN_AVX2_FILLER(FILL_CODE)                                          \
    /* Surface width not multiple of 8, greater than 7 */                   \
    if (pxl_excess && n_iters_8) {                                          \
        AVX_FILLER_LOOP(NON_MASKED_CASE(FILL_CODE), MASKED_CASE(FILL_CODE)) \
    }                                                                       \
    /* Surface width is between 1 and 7 */                                  \
    else if (pxl_excess) {                                                  \
        AVX_FILLER_LOOP({}, MASKED_CASE(FILL_CODE))                         \
    }                                                                       \
    /* Surface width multiple of 8 */                                       \
    else if (n_iters_8) {                                                   \
        AVX_FILLER_LOOP(NON_MASKED_CASE(FILL_CODE), {})                     \
    }                                                                       \
    /* Surface width is 0 */                                                \
    else {                                                                  \
        return -1;                                                          \
    }

/* BLEND_ADD */
#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
int
surface_fill_blend_add_avx2(SDL_Surface *surface, SDL_Rect *rect, Uint32 color)
{
    SETUP_AVX2_FILLER({ color &= ~amask; })
    RUN_AVX2_FILLER({ mm256_dst = _mm256_adds_epu8(mm256_dst, mm256_color); });
    return 0;
}
#else
int
surface_fill_blend_add_avx2(SDL_Surface *surface, SDL_Rect *rect, Uint32 color)
{
    BAD_AVX2_FUNCTION_CALL;
    return -1;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
 !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
int
surface_fill_blend_rgba_add_avx2(SDL_Surface *surface, SDL_Rect *rect,
                                 Uint32 color)
{
    SETUP_AVX2_FILLER({})
    RUN_AVX2_FILLER({ mm256_dst = _mm256_adds_epu8(mm256_dst, mm256_color); });
    return 0;
}
#else
int
surface_fill_blend_rgba_add_avx2(SDL_Surface *surface, SDL_Rect *rect,
                                 Uint32 color)
{
    BAD_AVX2_FUNCTION_CALL;
    return -1;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
 !defined(SDL_DISABLE_IMMINTRIN_H) */
