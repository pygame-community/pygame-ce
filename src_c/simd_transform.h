#define NO_PYGAME_C_API
#include "_surface.h"

#if !defined(PG_ENABLE_ARM_NEON) && defined(__aarch64__)
// arm64 has neon optimisations enabled by default, even when fpu=neon is not
// passed
#define PG_ENABLE_ARM_NEON 1
#endif

#define SURF_GET_AT(p_color, p_surf, p_x, p_y, p_pixels, p_format, p_pix)     \
    switch (p_format->BytesPerPixel) {                                        \
        case 1:                                                               \
            p_color = (Uint32) *                                              \
                      ((Uint8 *)(p_pixels) + (p_y)*p_surf->pitch + (p_x));    \
            break;                                                            \
        case 2:                                                               \
            p_color = (Uint32) *                                              \
                      ((Uint16 *)((p_pixels) + (p_y)*p_surf->pitch) + (p_x)); \
            break;                                                            \
        case 3:                                                               \
            p_pix = ((Uint8 *)(p_pixels + (p_y)*p_surf->pitch) + (p_x)*3);    \
            p_color = (SDL_BYTEORDER == SDL_LIL_ENDIAN)                       \
                          ? (p_pix[0]) + (p_pix[1] << 8) + (p_pix[2] << 16)   \
                          : (p_pix[2]) + (p_pix[1] << 8) + (p_pix[0] << 16);  \
            break;                                                            \
        default: /* case 4: */                                                \
            p_color = *((Uint32 *)(p_pixels + (p_y)*p_surf->pitch) + (p_x));  \
            break;                                                            \
    }

#if (SDL_BYTEORDER == SDL_LIL_ENDIAN)

#define SURF_SET_AT(p_color, p_surf, p_x, p_y, p_pixels, p_format,            \
                    p_byte_buf)                                               \
    switch (p_format->BytesPerPixel) {                                        \
        case 1:                                                               \
            *((Uint8 *)p_pixels + (p_y)*p_surf->pitch + (p_x)) =              \
                (Uint8)p_color;                                               \
            break;                                                            \
        case 2:                                                               \
            *((Uint16 *)(p_pixels + (p_y)*p_surf->pitch) + (p_x)) =           \
                (Uint16)p_color;                                              \
            break;                                                            \
        case 3:                                                               \
            p_byte_buf = (Uint8 *)(p_pixels + (p_y)*p_surf->pitch) + (p_x)*3; \
            *(p_byte_buf + (p_format->Rshift >> 3)) =                         \
                (Uint8)(p_color >> p_format->Rshift);                         \
            *(p_byte_buf + (p_format->Gshift >> 3)) =                         \
                (Uint8)(p_color >> p_format->Gshift);                         \
            *(p_byte_buf + (p_format->Bshift >> 3)) =                         \
                (Uint8)(p_color >> p_format->Bshift);                         \
            break;                                                            \
        default:                                                              \
            *((Uint32 *)(p_pixels + (p_y)*p_surf->pitch) + (p_x)) = p_color;  \
            break;                                                            \
    }

#else

#define SURF_SET_AT(p_color, p_surf, p_x, p_y, p_pixels, p_format,            \
                    p_byte_buf)                                               \
    switch (p_format->BytesPerPixel) {                                        \
        case 1:                                                               \
            *((Uint8 *)p_pixels + (p_y)*p_surf->pitch + (p_x)) =              \
                (Uint8)p_color;                                               \
            break;                                                            \
        case 2:                                                               \
            *((Uint16 *)(p_pixels + (p_y)*p_surf->pitch) + (p_x)) =           \
                (Uint16)p_color;                                              \
            break;                                                            \
        case 3:                                                               \
            p_byte_buf = (Uint8 *)(p_pixels + (p_y)*p_surf->pitch) + (p_x)*3; \
            *(p_byte_buf + 2 - (p_format->Rshift >> 3)) =                     \
                (Uint8)(p_color >> p_format->Rshift);                         \
            *(p_byte_buf + 2 - (p_format->Gshift >> 3)) =                     \
                (Uint8)(p_color >> p_format->Gshift);                         \
            *(p_byte_buf + 2 - (p_format->Bshift >> 3)) =                     \
                (Uint8)(p_color >> p_format->Bshift);                         \
            break;                                                            \
        default:                                                              \
            *((Uint32 *)(p_pixels + (p_y)*p_surf->pitch) + (p_x)) = p_color;  \
            break;                                                            \
    }

#endif

int
pg_sse2_at_runtime_but_uncompiled();
int
pg_neon_at_runtime_but_uncompiled();
int
pg_avx2_at_runtime_but_uncompiled();


void
grayscale_sse2(SDL_Surface *src, SDL_Surface * newsurf);


int
pg_has_avx2();
void
grayscale_avx2(SDL_Surface *src, SDL_Surface * newsurf);
