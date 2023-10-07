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
