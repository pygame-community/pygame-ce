#define NO_PYGAME_C_API
#ifndef SIMD_SHARED_H
#define SIMD_SHARED_H

#include "_surface.h"

int
pg_sse2_at_runtime_but_uncompiled();
int
pg_neon_at_runtime_but_uncompiled();
int
pg_avx2_at_runtime_but_uncompiled();

#if !defined(PG_ENABLE_ARM_NEON) && defined(__aarch64__)
// arm64 has neon optimisations enabled by default, even when fpu=neon is not
// passed
#define PG_ENABLE_ARM_NEON 1
#endif

/* See if we are compiled 64 bit on GCC or MSVC */
#if _WIN32 || _WIN64
#if _WIN64
#define ENV64BIT
#endif
#endif

// Check GCC
#if __GNUC__
#if __x86_64__ || __ppc64__ || __aarch64__
#define ENV64BIT
#endif
#endif

#if defined(__EMSCRIPTEN__) || SDL_BYTEORDER != SDL_LIL_ENDIAN
#define PG_SIMD_DISABLED 1
#endif /* PG_SIMD_DISABLED */

#ifndef PG_SIMD_DISABLED

#ifdef __SSE2__
#define PG_HAS_SSE2_OR_NEON SDL_HasSSE2
#elif PG_ENABLE_ARM_NEON
// sse2neon.h is from here: https://github.com/DLTcollab/sse2neon
#include "include/sse2neon.h"
#define PG_HAS_SSE2_OR_NEON SDL_HasNEON
#endif /* PG_ENABLE_ARM_NEON */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
#include <immintrin.h>
#define PG_HAS_AVX2 SDL_HasAVX2
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
        * !defined(SDL_DISABLE_IMMINTRIN_H) */

#endif /* PG_SIMD_DISABLED */

#endif  // SIMD_SHARED_H
