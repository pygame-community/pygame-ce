#define NO_PYGAME_C_API
#include "surface/surface.h"
#include "simd/cpu/pg_simd_cpu.h"

// AVX2 functions
int
surface_fill_blend_add_avx2(SDL_Surface *surface,
                            PG_PixelFormat *surface_format, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_add_avx2(SDL_Surface *surface,
                                 PG_PixelFormat *surface_format,
                                 SDL_Rect *rect, Uint32 color);

int
surface_fill_blend_sub_avx2(SDL_Surface *surface,
                            PG_PixelFormat *surface_format, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_sub_avx2(SDL_Surface *surface,
                                 PG_PixelFormat *surface_format,
                                 SDL_Rect *rect, Uint32 color);
int
surface_fill_blend_mult_avx2(SDL_Surface *surface,
                             PG_PixelFormat *surface_format, SDL_Rect *rect,
                             Uint32 color);
int
surface_fill_blend_rgba_mult_avx2(SDL_Surface *surface,
                                  PG_PixelFormat *surface_format,
                                  SDL_Rect *rect, Uint32 color);
int
surface_fill_blend_min_avx2(SDL_Surface *surface,
                            PG_PixelFormat *surface_format, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_min_avx2(SDL_Surface *surface,
                                 PG_PixelFormat *surface_format,
                                 SDL_Rect *rect, Uint32 color);
int
surface_fill_blend_max_avx2(SDL_Surface *surface,
                            PG_PixelFormat *surface_format, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_max_avx2(SDL_Surface *surface,
                                 PG_PixelFormat *surface_format,
                                 SDL_Rect *rect, Uint32 color);
// SSE2 functions
int
surface_fill_blend_add_sse2(SDL_Surface *surface,
                            PG_PixelFormat *surface_format, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_add_sse2(SDL_Surface *surface,
                                 PG_PixelFormat *surface_format,
                                 SDL_Rect *rect, Uint32 color);
int
surface_fill_blend_sub_sse2(SDL_Surface *surface,
                            PG_PixelFormat *surface_format, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_sub_sse2(SDL_Surface *surface,
                                 PG_PixelFormat *surface_format,
                                 SDL_Rect *rect, Uint32 color);
int
surface_fill_blend_mult_sse2(SDL_Surface *surface,
                             PG_PixelFormat *surface_format, SDL_Rect *rect,
                             Uint32 color);
int
surface_fill_blend_rgba_mult_sse2(SDL_Surface *surface,
                                  PG_PixelFormat *surface_format,
                                  SDL_Rect *rect, Uint32 color);
int
surface_fill_blend_min_sse2(SDL_Surface *surface,
                            PG_PixelFormat *surface_format, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_min_sse2(SDL_Surface *surface,
                                 PG_PixelFormat *surface_format,
                                 SDL_Rect *rect, Uint32 color);
int
surface_fill_blend_max_sse2(SDL_Surface *surface,
                            PG_PixelFormat *surface_format, SDL_Rect *rect,
                            Uint32 color);
int
surface_fill_blend_rgba_max_sse2(SDL_Surface *surface,
                                 PG_PixelFormat *surface_format,
                                 SDL_Rect *rect, Uint32 color);
