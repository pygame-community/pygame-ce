#include "simd_shared.h"
/* On Platforms with AVX2 support this file will be compiled with AV2 compiler
 * flags enabled.
 */

/* This returns True if either SSE2 or NEON is present at runtime.
 * Relevant because they use the same codepaths. Only the relevant runtime
 * SDL cpu feature check is compiled in.*/
int
pg_HasSSE_NEON()
{
#if defined(__SSE2__)
    return SDL_HasSSE2();
#elif PG_ENABLE_ARM_NEON
    return SDL_HasNEON();
#else
    return 0;
#endif
}

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
