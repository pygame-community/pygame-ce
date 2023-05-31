#define NO_PYGAME_C_API
#include "_surface.h"

#if !defined(PG_ENABLE_ARM_NEON) && defined(__aarch64__)
// arm64 has neon optimisations enabled by default, even when fpu=neon is not
// passed
#define PG_ENABLE_ARM_NEON 1
#endif

// SSE2 functions
#if defined(__SSE2__) || defined(PG_ENABLE_ARM_NEON)
#endif /* (defined(__SSE2__) || defined(PG_ENABLE_ARM_NEON)) */

// AVX2 functions
