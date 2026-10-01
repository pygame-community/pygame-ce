/*
  pygame-ce - Python Game Library

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Library General Public
  License as published by the Free Software Foundation; either
  version 2 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Library General Public License for more details.

  You should have received a copy of the GNU Library General Public
  License along with this library; if not, write to the Free
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

/* Global SIMD CPU layer: the single authoritative source of CPU/ISA
 * capability and compile-time availability knowledge.
 *
 * This header owns two questions:
 *   1. "Was ISA X compiled into this binary?" (the intrinsic bootstrap and
 *      the PG_ENABLE_* / __AVX2__ / __SSE2__ / HAVE_IMMINTRIN_H macros)
 *   2. "Can this CPU execute ISA X, and is it also compiled in?" (the
 *      pg_* query API, defined once in pg_simd_cpu.c)
 *
 * Dependency direction: modules (surface, transform, ...) depend on
 * simd/cpu; simd/cpu must NEVER depend on any module header (surface/*, ...)
 * or the pygame/Python C API. The SIMD module headers include this header
 * directly to get the bootstrap and detection API. Keep this header free of
 * pygame/Python API.
 *
 * NOTE: this is deliberately a narrow CPU/ISA capability + compile-environment
 * header, not a general SIMD configuration header. It owns facts that every
 * SIMD translation unit must agree on (ISA compile-availability, and the
 * ENV64BIT pointer-width flag the load/store kernels key off). Genuinely
 * module-specific helpers (e.g. the differing per-module LOAD_64_INTO_M128
 * calling conventions) stay with the code that uses them.
 */

#ifndef PG_SIMD_CPU_H
#define PG_SIMD_CPU_H

/* --- SDL3 intrinsic / compile-time ISA availability bootstrap ---
 * SDL3 no longer includes intrinsics by default, so we include them
 * explicitly and set the macros our SIMD code checks for build-time ISA
 * support. */
#if PG_SDL3
#include <SDL3/SDL_intrin.h>

/* If SDL_AVX2_INTRINSICS is defined by SDL3, we need to set macros that our
 * code checks for avx2 build time support */
#ifdef SDL_AVX2_INTRINSICS
#ifndef HAVE_IMMINTRIN_H
#define HAVE_IMMINTRIN_H 1
#endif /* HAVE_IMMINTRIN_H*/
#ifndef __AVX2__
#define __AVX2__
#endif /* __AVX2__*/
#endif /* SDL_AVX2_INTRINSICS*/

// TODO reenable this to test best
#ifdef SDL_SSE2_INTRINSICS
#ifndef __SSE2__
#define __SSE2__
#endif /* __SSE2__*/
#endif /* SDL_SSE2_INTRINSICS*/
#endif /* PG_SDL3 */

/* Whether this is a 64-bit build, derived from the compiler's predefined
 * macros. This is purely a pygame-computed flag -- the OS, compiler, and build
 * system never define ENV64BIT themselves; only these blocks do. Centralized
 * here so every SIMD translation unit derives it consistently. (It used to be
 * defined only in some surface sources, so transform's SSE2 kernels -- which
 * key off ENV64BIT for a 64-bit movq load/store path -- never saw it and were
 * stuck on the 32-bit fallback.) These predefined macros exist from the start
 * of compilation, so this is include-order independent. */
#if _WIN32 || _WIN64
#if _WIN64
#define ENV64BIT
#endif
#endif
#if __GNUC__
#if __x86_64__ || __ppc64__ || __aarch64__
#define ENV64BIT
#endif
#endif

/* Pull in the x86 wide-intrinsics header once, here, when it is available,
 * rather than repeating this block in every per-ISA source. On SDL3 the
 * SDL_intrin.h include above may already have included it; immintrin.h's own
 * include guard makes this idempotent. */
#if defined(HAVE_IMMINTRIN_H) && !defined(SDL_DISABLE_IMMINTRIN_H)
#include <immintrin.h>
#endif /* defined(HAVE_IMMINTRIN_H) && !defined(SDL_DISABLE_IMMINTRIN_H) */

/* True (1) when the AVX2 kernels are compiled into this binary: the compiler
 * targets AVX2 and the x86 wide-intrinsics header is available. Named to match
 * pygame's existing PG_COMPILE_* convention (cf. PG_COMPILE_SSE4_2 in
 * pgplatform.h) and used to gate the per-ISA AVX2 sources and the AVX2
 * capability queries, replacing the three-part condition they used to repeat.
 *
 * This is a frozen 0/1, so any translation unit that includes this header must
 * already have __AVX2__ and HAVE_IMMINTRIN_H in their final state: the
 * bootstrap above provides them on SDL3; on SDL2 they come from the SDL
 * headers, so include SDL before this header (as pg_simd_cpu.c and the module
 * SIMD headers both do). */
#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
#define PG_COMPILE_AVX2 1
#else
#define PG_COMPILE_AVX2 0
#endif

#if !defined(PG_ENABLE_ARM_NEON) && defined(__aarch64__)
// arm64 has neon optimisations enabled by default, even when fpu=neon is not
// passed
#define PG_ENABLE_ARM_NEON 1
#endif

/* This defines PG_ENABLE_SSE_NEON as True if either SSE or NEON is available
 * at compile time. Since we do compile time translation of SSE2->NEON, they
 * have the same code paths, so this reduces code duplication of those paths.
 */
#if defined(__SSE2__)
#define PG_ENABLE_SSE_NEON 1
#elif PG_ENABLE_ARM_NEON
#define PG_ENABLE_SSE_NEON 1
#else
#define PG_ENABLE_SSE_NEON 0
#endif

/* --- CPU capability / compile-availability query API ---
 * Single authoritative declarations. The definitions live once in
 * pg_simd_cpu.c, replacing the per-module duplicated copies. Each helper
 * fuses "runtime CPU support" with "compiled backend availability" (it
 * returns true only when the CPU supports the ISA AND the ISA was compiled
 * in). Signatures are intentionally left exactly as they were historically;
 * any renaming/redesign belongs to a later stage. */
int
pg_sse2_at_runtime_but_uncompiled();
int
pg_neon_at_runtime_but_uncompiled();
int
pg_avx2_at_runtime_but_uncompiled();
int
pg_has_avx2();

/* This returns True if either SSE2 or NEON is present at runtime.
 * Relevant because they use the same codepaths. Only the relevant runtime
 * SDL cpu feature check is compiled in.*/
int
pg_HasSSE_NEON();

/* --- Uncompiled-backend fallback diagnostics ---
 * A backend's kernels are declared unconditionally so the module dispatch
 * always has a symbol to link against, but when that ISA was not compiled in
 * the body is a stub that must never actually run (runtime dispatch gates it
 * behind pg_has_avx2() / pg_HasSSE_NEON()). Reaching one of these is a pygame
 * bug, so the stub aborts. These live here (rather than being copied into
 * every per-ISA source) because "was this backend compiled in?" is exactly
 * the compile-availability concern this header owns.
 *
 * NOTE: unlike the rest of this header, these macros reference pygame's
 * PG_EXIT (and printf); they are only ever *expanded* inside module SIMD
 * sources that already have those available. pg_simd_cpu.c itself never
 * expands them, so this translation unit stays free of the pygame/Python API.
 */
#define BAD_AVX2_FUNCTION_CALL                                               \
    printf(                                                                  \
        "Fatal Error: Attempted calling an AVX2 function when both compile " \
        "time and runtime support is missing. If you are seeing this "       \
        "message, you have stumbled across a pygame bug, please report it "  \
        "to the devs!");                                                     \
    PG_EXIT(1)

#define BAD_SSE2_FUNCTION_CALL                                               \
    printf(                                                                  \
        "Fatal Error: Attempted calling an SSE2 function when both compile " \
        "time and runtime support is missing. If you are seeing this "       \
        "message, you have stumbled across a pygame bug, please report it "  \
        "to the devs!");                                                     \
    PG_EXIT(1)

#endif /* PG_SIMD_CPU_H */
