#define NO_PYGAME_C_API
#include "_surface.h"
#include "_blit_info.h"
#include "simd_shared.h"

#ifdef PG_HAS_SSE2_OR_NEON
void
alphablit_alpha_sse2_argb_surf_alpha(SDL_BlitInfo *info);
void
alphablit_alpha_sse2_argb_no_surf_alpha(SDL_BlitInfo *info);
void
alphablit_alpha_sse2_argb_no_surf_alpha_opaque_dst(SDL_BlitInfo *info);
void
blit_blend_rgba_mul_sse2(SDL_BlitInfo *info);
void
blit_blend_rgb_mul_sse2(SDL_BlitInfo *info);
void
blit_blend_rgba_add_sse2(SDL_BlitInfo *info);
void
blit_blend_rgb_add_sse2(SDL_BlitInfo *info);
void
blit_blend_rgba_sub_sse2(SDL_BlitInfo *info);
void
blit_blend_rgb_sub_sse2(SDL_BlitInfo *info);
void
blit_blend_rgba_max_sse2(SDL_BlitInfo *info);
void
blit_blend_rgb_max_sse2(SDL_BlitInfo *info);
void
blit_blend_rgba_min_sse2(SDL_BlitInfo *info);
void
blit_blend_rgb_min_sse2(SDL_BlitInfo *info);
void
blit_blend_premultiplied_sse2(SDL_BlitInfo *info);
void
premul_surf_color_by_alpha_sse2(SDL_Surface *src, SDL_Surface *dst);
#endif /* PG_HAS_SSE2_OR_NEON */

#ifdef PG_HAS_AVX2
void
alphablit_alpha_avx2_argb_no_surf_alpha_opaque_dst(SDL_BlitInfo *info);
void
alphablit_alpha_avx2_argb_no_surf_alpha(SDL_BlitInfo *info);
void
alphablit_alpha_avx2_argb_surf_alpha(SDL_BlitInfo *info);
void
blit_blend_rgba_mul_avx2(SDL_BlitInfo *info);
void
blit_blend_rgb_mul_avx2(SDL_BlitInfo *info);
void
blit_blend_rgba_add_avx2(SDL_BlitInfo *info);
void
blit_blend_rgb_add_avx2(SDL_BlitInfo *info);
void
blit_blend_rgba_sub_avx2(SDL_BlitInfo *info);
void
blit_blend_rgb_sub_avx2(SDL_BlitInfo *info);
void
blit_blend_rgba_max_avx2(SDL_BlitInfo *info);
void
blit_blend_rgb_max_avx2(SDL_BlitInfo *info);
void
blit_blend_rgba_min_avx2(SDL_BlitInfo *info);
void
blit_blend_rgb_min_avx2(SDL_BlitInfo *info);
void
blit_blend_premultiplied_avx2(SDL_BlitInfo *info);
void
premul_surf_color_by_alpha_avx2(SDL_Surface *src, SDL_Surface *dst);
#endif
