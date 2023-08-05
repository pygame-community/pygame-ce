#define NO_PYGAME_C_API

#ifndef SIMD_FILL_H
#define SIMD_FILL_H
#include "_surface.h"

// AVX2 functions
int
_pg_has_avx2();

int
surface_fill_blend_add_avx2(SDL_Surface *surface, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_add_avx2(SDL_Surface *surface, SDL_Rect *rect,
                                 Uint32 color);
#endif  // SIMD_FILL_H
