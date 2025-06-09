#define NO_PYGAME_C_API
#include "_surface.h"

/* TODO: This compat code should probably go in some place like simd_shared.h
 * That header file however is inconsistently used at the moment and not
 * included wherever it should be.
 * this block will be needed by simd_blitters and simd_fill */

#if PG_SDL3
// SDL3 no longer includes intrinsics by default, we need to do it explicitly
#include <SDL3/SDL_intrin.h>

/* If SDL_AVX2_INTRINSICS is defined by SDL3, we need to set macros that our
 * code checks for avx2 build time support */
#ifdef SDL_AVX2_INTRINSICS
#ifndef HAVE_IMMINTRIN_H
#define HAVE_IMMINTRIN_H 1
#endif /* HAVE_IMMINTRIN_H*/
#endif /* SDL_AVX2_INTRINSICS*/
#endif /* PG_SDL3 */

/**
 * MACRO borrowed from SSE2NEON - useful for making the shuffling family of
 * intrinsics easier to understand by indicating clearly what will go where.
 *
 * SSE2Neon description follows...
 * MACRO for shuffle parameter for _mm_shuffle_ps().
 * Argument fp3 is a digit[0123] that represents the fp from argument "b"
 * of mm_shuffle_ps that will be placed in fp3 of result. fp2 is the same
 * for fp2 in result. fp1 is a digit[0123] that represents the fp from
 * argument "a" of mm_shuffle_ps that will be places in fp1 of result.
 * fp0 is the same for fp0 of result.
 */
#define _PG_SIMD_SHUFFLE(fp3, fp2, fp1, fp0) \
    (((fp3) << 6) | ((fp2) << 4) | ((fp1) << 2) | ((fp0)))

#if !defined(PG_ENABLE_ARM_NEON) && defined(__aarch64__)
// arm64 has neon optimisations enabled by default, even when fpu=neon is not
// passed
#define PG_ENABLE_ARM_NEON 1
#endif

// SSE2 functions
#if defined(__SSE2__) || defined(PG_ENABLE_ARM_NEON)

void
grayscale_sse2(SDL_Surface *src, PG_PixelFormat *src_fmt,
               SDL_Surface *newsurf);
// smoothscale filters
void
filter_shrink_X_SSE2(Uint8 *srcpix, Uint8 *dstpix, int height, int srcpitch,
                     int dstpitch, int srcwidth, int dstwidth);
void
filter_shrink_Y_SSE2(Uint8 *srcpix, Uint8 *dstpix, int width, int srcpitch,
                     int dstpitch, int srcheight, int dstheight);
void
filter_expand_X_SSE2(Uint8 *srcpix, Uint8 *dstpix, int height, int srcpitch,
                     int dstpitch, int srcwidth, int dstwidth);
void
filter_expand_Y_SSE2(Uint8 *srcpix, Uint8 *dstpix, int width, int srcpitch,
                     int dstpitch, int srcheight, int dstheight);
void
invert_sse2(SDL_Surface *src, PG_PixelFormat *src_fmt, SDL_Surface *newsurf);

#endif /* (defined(__SSE2__) || defined(PG_ENABLE_ARM_NEON)) */

// AVX2 functions
void
grayscale_avx2(SDL_Surface *src, PG_PixelFormat *src_fmt,
               SDL_Surface *newsurf);
void
invert_avx2(SDL_Surface *src, PG_PixelFormat *src_fmt, SDL_Surface *newsurf);
