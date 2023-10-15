#define NO_PYGAME_C_API
#include "_surface.h"

int
_pg_has_avx2();

// AVX2 functions
int
surface_fill_blend_add_avx2(SDL_Surface *surface, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_add_avx2(SDL_Surface *surface, SDL_Rect *rect,
                                 Uint32 color);
