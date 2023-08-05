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

#define SETUP_AVX2_FILLER                                               \
    /* initialize surface data */                                       \
    int width = rect->w, height = rect->h;                              \
    int skip =                                                          \
        (surface->pitch - width * surface->format->BytesPerPixel) >> 2; \
    int pxl_skip = surface->format->BytesPerPixel >> 2;                 \
    int pre_8_width = width % 8;                                        \
    int post_8_width = (width - pre_8_width) / 8;                       \
                                                                        \
    /* load pixel data */                                               \
    Uint32 *pixels = (Uint32 *)surface->pixels +                        \
                     (Uint64)rect->y * (surface->pitch >> 2) +          \
                     (Uint64)rect->x * pxl_skip;                        \
                                                                        \
    __m256i *mm256_pixels = (__m256i *)pixels;                          \
                                                                        \
    /* load color data */                                               \
    __m256i mm256_color = _mm256_set1_epi32(color);                     \
    __m128i mm_color = _mm_cvtsi32_si128(color);                        \
                                                                        \
    __m128i mm_src;                                                     \
    __m256i mm256_src;                                                  \
    int n;

#define RUN_AVX2_FILLER(CODE_1, CODE_8)                           \
    while (height--) {                                            \
        if (pre_8_width > 0) {                                    \
            LOOP_UNROLLED4(                                       \
                {                                                 \
                    /* load 1 pixel */                            \
                    mm_src = _mm_cvtsi32_si128(*pixels);          \
                                                                  \
                    CODE_1                                        \
                                                                  \
                    /* store 1 pixel */                           \
                    *pixels = _mm_cvtsi128_si32(mm_src);          \
                                                                  \
                    pixels += pxl_skip;                           \
                },                                                \
                n, pre_8_width);                                  \
        }                                                         \
        mm256_pixels = (__m256i *)pixels;                         \
        if (post_8_width > 0) {                                   \
            LOOP_UNROLLED4(                                       \
                {                                                 \
                    /* load 8 pixels */                           \
                    mm256_src = _mm256_loadu_si256(mm256_pixels); \
                                                                  \
                    CODE_8                                        \
                                                                  \
                    /* store 8 pixels */                          \
                    _mm256_storeu_si256(mm256_pixels, mm256_src); \
                                                                  \
                    mm256_pixels++;                               \
                },                                                \
                n, post_8_width);                                 \
        }                                                         \
                                                                  \
        pixels = (Uint32 *)mm256_pixels + skip;                   \
    }

/* BLEND_ADD */
#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
int
surface_fill_blend_add_avx2(SDL_Surface *surface, SDL_Rect *rect, Uint32 color)
{
    SETUP_AVX2_FILLER
    Uint32 amask = surface->format->Amask;

    if (amask) {
        /* if Amask is set, subtract the alpha value from the color*/
        mm256_color = _mm256_subs_epu8(mm256_color, _mm256_set1_epi32(amask));
        mm_color = _mm_subs_epu8(mm_color, _mm_cvtsi32_si128(amask));
    }

    RUN_AVX2_FILLER({ mm_src = _mm_adds_epu8(mm_src, mm_color); },
                    { mm256_src = _mm256_adds_epu8(mm256_src, mm256_color); });

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
    SETUP_AVX2_FILLER

    RUN_AVX2_FILLER({ mm_src = _mm_adds_epu8(mm_src, mm_color); },
                    { mm256_src = _mm256_adds_epu8(mm256_src, mm256_color); });

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
