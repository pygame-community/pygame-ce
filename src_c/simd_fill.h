#define NO_PYGAME_C_API
#include "_surface.h"
#include "simd_shared.h"

// AVX2 functions
#ifdef PG_HAS_AVX2
int
surface_fill_blend_add_avx2(SDL_Surface *surface, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_add_avx2(SDL_Surface *surface, SDL_Rect *rect,
                                 Uint32 color);

int
surface_fill_blend_sub_avx2(SDL_Surface *surface, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_sub_avx2(SDL_Surface *surface, SDL_Rect *rect,
                                 Uint32 color);
int
surface_fill_blend_mult_avx2(SDL_Surface *surface, SDL_Rect *rect,
                             Uint32 color);
int
surface_fill_blend_rgba_mult_avx2(SDL_Surface *surface, SDL_Rect *rect,
                                  Uint32 color);
int
surface_fill_blend_min_avx2(SDL_Surface *surface, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_min_avx2(SDL_Surface *surface, SDL_Rect *rect,
                                 Uint32 color);
int
surface_fill_blend_max_avx2(SDL_Surface *surface, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_max_avx2(SDL_Surface *surface, SDL_Rect *rect,
                                 Uint32 color);
#endif

// SSE2 functions
#ifdef PG_HAS_SSE2_OR_NEON
int
surface_fill_blend_add_sse2(SDL_Surface *surface, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_add_sse2(SDL_Surface *surface, SDL_Rect *rect,
                                 Uint32 color);
int
surface_fill_blend_sub_sse2(SDL_Surface *surface, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_sub_sse2(SDL_Surface *surface, SDL_Rect *rect,
                                 Uint32 color);
int
surface_fill_blend_mult_sse2(SDL_Surface *surface, SDL_Rect *rect,
                             Uint32 color);
int
surface_fill_blend_rgba_mult_sse2(SDL_Surface *surface, SDL_Rect *rect,
                                  Uint32 color);
int
surface_fill_blend_min_sse2(SDL_Surface *surface, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_min_sse2(SDL_Surface *surface, SDL_Rect *rect,
                                 Uint32 color);
int
surface_fill_blend_max_sse2(SDL_Surface *surface, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_max_sse2(SDL_Surface *surface, SDL_Rect *rect,
                                 Uint32 color);
#endif
