/*

SDL_gfxPrimitives - Graphics primitives for SDL surfaces

LGPL (c) A. Schiffler

*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#include "SDL_gfxPrimitives.h"
// #include "SDL_rotozoom.h"

/* -===================- */

#define DEFAULT_ALPHA_PIXEL_ROUTINE
#undef EXPERIMENTAL_ALPHA_PIXEL_ROUTINE

/* ----- Defines for pixel clipping tests */

#define clip_xmin(surface) surface->clip_rect.x
#define clip_xmax(surface) surface->clip_rect.x + surface->clip_rect.w - 1
#define clip_ymin(surface) surface->clip_rect.y
#define clip_ymax(surface) surface->clip_rect.y + surface->clip_rect.h - 1

/*!
\brief Internal pixel drawing function with alpha blending where input color in
in destination format.

Contains two alternative 32 bit alpha blending routines which can be enabled at
the source level with the defines DEFAULT_ALPHA_PIXEL_ROUTINE or
EXPERIMENTAL_ALPHA_PIXEL_ROUTINE. Only the bits up to the surface depth are
significant in the color value.

\param dst The surface to draw on.
\param x The horizontal coordinate of the pixel.
\param y The vertical position of the pixel.
\param color The color value of the pixel to draw.
\param alpha The blend factor to apply while drawing.

\returns Returns 0 on success, -1 on failure.
*/
int
_putPixelAlpha(SDL_Surface *dst, Sint16 x, Sint16 y, Uint32 color, Uint8 alpha)
{
    SDL_PixelFormat *format;
    Uint32 Rmask, Gmask, Bmask, Amask;
    Uint32 Rshift, Gshift, Bshift, Ashift;
    Uint32 R, G, B, A;

    if (dst == NULL) {
        return (-1);
    }

    if (x >= clip_xmin(dst) && x <= clip_xmax(dst) && y >= clip_ymin(dst) &&
        y <= clip_ymax(dst)) {
        format = dst->format;

        switch (GFX_FORMAT_BytesPerPixel(format)) {
            case 1: { /* Assuming 8-bpp */
                if (alpha == 255) {
                    *((Uint8 *)dst->pixels + y * dst->pitch + x) = color;
                }
                else {
                    Uint8 *pixel = (Uint8 *)dst->pixels + y * dst->pitch + x;
                    SDL_Palette *palette = format->palette;
                    SDL_Color *colors = palette->colors;
                    SDL_Color dColor = colors[*pixel];
                    SDL_Color sColor = colors[color];
                    Uint8 dR = dColor.r;
                    Uint8 dG = dColor.g;
                    Uint8 dB = dColor.b;
                    Uint8 sR = sColor.r;
                    Uint8 sG = sColor.g;
                    Uint8 sB = sColor.b;

                    dR = dR + ((sR - dR) * alpha >> 8);
                    dG = dG + ((sG - dG) * alpha >> 8);
                    dB = dB + ((sB - dB) * alpha >> 8);

                    *pixel = SDL_MapRGB(format, dR, dG, dB);
                }
            } break;

            case 2: { /* Probably 15-bpp or 16-bpp */
                if (alpha == 255) {
                    *((Uint16 *)dst->pixels + y * dst->pitch / 2 + x) = color;
                }
                else {
                    Uint16 *pixel =
                        (Uint16 *)dst->pixels + y * dst->pitch / 2 + x;
                    Uint32 dc = *pixel;

                    Rmask = format->Rmask;
                    Gmask = format->Gmask;
                    Bmask = format->Bmask;
                    Amask = format->Amask;
                    R = ((dc & Rmask) +
                         (((color & Rmask) - (dc & Rmask)) * alpha >> 8)) &
                        Rmask;
                    G = ((dc & Gmask) +
                         (((color & Gmask) - (dc & Gmask)) * alpha >> 8)) &
                        Gmask;
                    B = ((dc & Bmask) +
                         (((color & Bmask) - (dc & Bmask)) * alpha >> 8)) &
                        Bmask;
                    *pixel = R | G | B;
                    if (Amask != 0) {
                        A = ((dc & Amask) +
                             (((color & Amask) - (dc & Amask)) * alpha >> 8)) &
                            Amask;
                        *pixel |= A;
                    }
                }
            } break;

            case 3: {
                /* Slow 24-bpp mode. This is patched on the pygame end because
                 * the original code failed on big endian */
                Uint8 *pixel = (Uint8 *)dst->pixels + y * dst->pitch + x * 3;
                Uint8 *dR, *dG, *dB;
                Uint8 sR, sG, sB;

                SDL_GetRGB(color, format, &sR, &sG, &sB);

#if (SDL_BYTEORDER == SDL_LIL_ENDIAN)
                dR = pixel + (format->Rshift >> 3);
                dG = pixel + (format->Gshift >> 3);
                dB = pixel + (format->Bshift >> 3);
#else
                dR = pixel + 2 - (format->Rshift >> 3);
                dG = pixel + 2 - (format->Gshift >> 3);
                dB = pixel + 2 - (format->Bshift >> 3);
#endif

                if (alpha == 255) {
                    *dR = sR;
                    *dG = sG;
                    *dB = sB;
                }
                else {
                    *dR = *dR + ((sR - *dR) * alpha >> 8);
                    *dG = *dG + ((sG - *dG) * alpha >> 8);
                    *dB = *dB + ((sB - *dB) * alpha >> 8);
                }
            } break;

#ifdef DEFAULT_ALPHA_PIXEL_ROUTINE

            case 4: { /* Probably :-) 32-bpp */
                if (alpha == 255) {
                    *((Uint32 *)dst->pixels + y * dst->pitch / 4 + x) = color;
                }
                else {
                    Uint32 *pixel =
                        (Uint32 *)dst->pixels + y * dst->pitch / 4 + x;
                    Uint32 dc = *pixel;

                    Rmask = format->Rmask;
                    Gmask = format->Gmask;
                    Bmask = format->Bmask;
                    Amask = format->Amask;

                    Rshift = format->Rshift;
                    Gshift = format->Gshift;
                    Bshift = format->Bshift;
                    Ashift = format->Ashift;

                    R = ((dc & Rmask) +
                         (((((color & Rmask) - (dc & Rmask)) >> Rshift) *
                               alpha >>
                           8)
                          << Rshift)) &
                        Rmask;
                    G = ((dc & Gmask) +
                         (((((color & Gmask) - (dc & Gmask)) >> Gshift) *
                               alpha >>
                           8)
                          << Gshift)) &
                        Gmask;
                    B = ((dc & Bmask) +
                         (((((color & Bmask) - (dc & Bmask)) >> Bshift) *
                               alpha >>
                           8)
                          << Bshift)) &
                        Bmask;
                    *pixel = R | G | B;
                    if (Amask != 0) {
                        A = ((dc & Amask) +
                             (((((color & Amask) - (dc & Amask)) >> Ashift) *
                                   alpha >>
                               8)
                              << Ashift)) &
                            Amask;
                        *pixel |= A;
                    }
                }
            } break;
#endif

#ifdef EXPERIMENTAL_ALPHA_PIXEL_ROUTINE

            case 4: { /* Probably :-) 32-bpp */
                if (alpha == 255) {
                    *((Uint32 *)dst->pixels + y * dst->pitch / 4 + x) = color;
                }
                else {
                    Uint32 *pixel =
                        (Uint32 *)dst->pixels + y * dst->pitch / 4 + x;
                    Uint32 dR, dG, dB, dA;
                    Uint32 dc = *pixel;

                    Uint32 surfaceAlpha, preMultR, preMultG, preMultB;
                    Uint32 aTmp;

                    Rmask = format->Rmask;
                    Gmask = format->Gmask;
                    Bmask = format->Bmask;
                    Amask = format->Amask;

                    dR = (color & Rmask);
                    dG = (color & Gmask);
                    dB = (color & Bmask);
                    dA = (color & Amask);

                    Rshift = format->Rshift;
                    Gshift = format->Gshift;
                    Bshift = format->Bshift;
                    Ashift = format->Ashift;

                    preMultR = (alpha * (dR >> Rshift));
                    preMultG = (alpha * (dG >> Gshift));
                    preMultB = (alpha * (dB >> Bshift));

                    surfaceAlpha = ((dc & Amask) >> Ashift);
                    aTmp = (255 - alpha);
                    if (A = 255 - ((aTmp * (255 - surfaceAlpha)) >> 8)) {
                        aTmp *= surfaceAlpha;
                        R = (preMultR +
                             ((aTmp * ((dc & Rmask) >> Rshift)) >> 8)) /
                                    A
                                << Rshift &
                            Rmask;
                        G = (preMultG +
                             ((aTmp * ((dc & Gmask) >> Gshift)) >> 8)) /
                                    A
                                << Gshift &
                            Gmask;
                        B = (preMultB +
                             ((aTmp * ((dc & Bmask) >> Bshift)) >> 8)) /
                                    A
                                << Bshift &
                            Bmask;
                    }
                    *pixel = R | G | B | (A << Ashift & Amask);
                }
            } break;
#endif
        }
    }

    return (0);
}

/*!
\brief Pixel draw with blending enabled if a<255.

\param dst The surface to draw on.
\param x X (horizontal) coordinate of the pixel.
\param y Y (vertical) coordinate of the pixel.
\param color The color value of the pixel to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
pixelColor(SDL_Surface *dst, Sint16 x, Sint16 y, Uint32 color)
{
    Uint8 alpha;
    Uint32 mcolor;
    int result = 0;

    /*
     * Lock the surface
     */
    if (SDL_MUSTLOCK(dst)) {
        if (SDL_LockSurface(dst) < 0) {
            return (-1);
        }
    }

    /*
     * Setup color
     */
    alpha = color & 0x000000ff;
    mcolor = SDL_MapRGBA(dst->format, (color & 0xff000000) >> 24,
                         (color & 0x00ff0000) >> 16, (color & 0x0000ff00) >> 8,
                         alpha);

    /*
     * Draw
     */
    result = _putPixelAlpha(dst, x, y, mcolor, alpha);

    /*
     * Unlock the surface
     */
    if (SDL_MUSTLOCK(dst)) {
        SDL_UnlockSurface(dst);
    }

    return (result);
}

/*!
\brief Pixel draw with blending enabled if a<255 - no surface locking.

\param dst The surface to draw on.
\param x X (horizontal) coordinate of the pixel.
\param y Y (vertical) coordinate of the pixel.
\param color The color value of the pixel to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
pixelColorNolock(SDL_Surface *dst, Sint16 x, Sint16 y, Uint32 color)
{
    Uint8 alpha;
    Uint32 mcolor;
    int result = 0;

    /*
     * Setup color
     */
    alpha = color & 0x000000ff;
    mcolor = SDL_MapRGBA(dst->format, (color & 0xff000000) >> 24,
                         (color & 0x00ff0000) >> 16, (color & 0x0000ff00) >> 8,
                         alpha);

    /*
     * Draw
     */
    result = _putPixelAlpha(dst, x, y, mcolor, alpha);

    return (result);
}

/*!
\brief Internal function to draw filled rectangle with alpha blending.

Assumes color is in destination format.

\param dst The surface to draw on.
\param x1 X coordinate of the first corner (upper left) of the rectangle.
\param y1 Y coordinate of the first corner (upper left) of the rectangle.
\param x2 X coordinate of the second corner (lower right) of the rectangle.
\param y2 Y coordinate of the second corner (lower right) of the rectangle.
\param color The color value of the rectangle to draw (0xRRGGBBAA).
\param alpha Alpha blending amount for pixels.

\returns Returns 0 on success, -1 on failure.
*/
int
_filledRectAlpha(SDL_Surface *dst, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2,
                 Uint32 color, Uint8 alpha)
{
    SDL_PixelFormat *format;
    Uint32 Rmask, Bmask, Gmask, Amask;
    Uint32 Rshift, Bshift, Gshift, Ashift;
    Uint8 sR, sG, sB, sA;
    Uint32 R, G, B, A;
    Sint16 x, y;

    format = dst->format;
    switch (GFX_FORMAT_BytesPerPixel(format)) {
        case 1: { /* Assuming 8-bpp */
            Uint8 *row, *pixel;
            Uint8 dR, dG, dB;
            SDL_Palette *palette = format->palette;
            SDL_Color *colors = palette->colors;
            sR = colors[color].r;
            sG = colors[color].g;
            sB = colors[color].b;

            for (y = y1; y <= y2; y++) {
                row = (Uint8 *)dst->pixels + y * dst->pitch;
                for (x = x1; x <= x2; x++) {
                    pixel = row + x;

                    dR = colors[*pixel].r;
                    dG = colors[*pixel].g;
                    dB = colors[*pixel].b;

                    dR = dR + ((sR - dR) * alpha >> 8);
                    dG = dG + ((sG - dG) * alpha >> 8);
                    dB = dB + ((sB - dB) * alpha >> 8);

                    *pixel = SDL_MapRGB(format, dR, dG, dB);
                }
            }
        } break;

        case 2: { /* Probably 15-bpp or 16-bpp */
            Uint16 *row, *pixel;
            Uint32 dR, dG, dB, dA;
            Rmask = format->Rmask;
            Gmask = format->Gmask;
            Bmask = format->Bmask;
            Amask = format->Amask;

            dR = (color & Rmask);
            dG = (color & Gmask);
            dB = (color & Bmask);
            dA = (color & Amask);

            for (y = y1; y <= y2; y++) {
                row = (Uint16 *)dst->pixels + y * dst->pitch / 2;
                for (x = x1; x <= x2; x++) {
                    pixel = row + x;

                    R = ((*pixel & Rmask) +
                         ((dR - (*pixel & Rmask)) * alpha >> 8)) &
                        Rmask;
                    G = ((*pixel & Gmask) +
                         ((dG - (*pixel & Gmask)) * alpha >> 8)) &
                        Gmask;
                    B = ((*pixel & Bmask) +
                         ((dB - (*pixel & Bmask)) * alpha >> 8)) &
                        Bmask;
                    *pixel = R | G | B;
                    if (Amask != 0) {
                        A = ((*pixel & Amask) +
                             ((dA - (*pixel & Amask)) * alpha >> 8)) &
                            Amask;
                        *pixel |= A;
                    }
                }
            }
        } break;

        case 3: {
            /* Slow 24-bpp mode. This is patched on the pygame end because the
             * original code failed on big endian */
            Uint8 *row, *pix;
            Uint8 *dR, *dG, *dB;
            Uint8 sR, sG, sB;

            SDL_GetRGB(color, format, &sR, &sG, &sB);
            for (y = y1; y <= y2; y++) {
                row = (Uint8 *)dst->pixels + y * dst->pitch;
                for (x = x1; x <= x2; x++) {
                    pix = row + x * 3;

#if (SDL_BYTEORDER == SDL_LIL_ENDIAN)
                    dR = pix + (format->Rshift >> 3);
                    dG = pix + (format->Gshift >> 3);
                    dB = pix + (format->Bshift >> 3);
#else
                    dR = pix + 2 - (format->Rshift >> 3);
                    dG = pix + 2 - (format->Gshift >> 3);
                    dB = pix + 2 - (format->Bshift >> 3);
#endif

                    *dR = *dR + ((sR - *dR) * alpha >> 8);
                    *dG = *dG + ((sG - *dG) * alpha >> 8);
                    *dB = *dB + ((sB - *dB) * alpha >> 8);
                }
            }
        } break;

#ifdef DEFAULT_ALPHA_PIXEL_ROUTINE
        case 4: { /* Probably :-) 32-bpp */
            Uint32 *row, *pixel;
            Uint32 dR, dG, dB, dA;

            Rmask = format->Rmask;
            Gmask = format->Gmask;
            Bmask = format->Bmask;
            Amask = format->Amask;

            Rshift = format->Rshift;
            Gshift = format->Gshift;
            Bshift = format->Bshift;
            Ashift = format->Ashift;

            dR = (color & Rmask);
            dG = (color & Gmask);
            dB = (color & Bmask);
            dA = (color & Amask);

            for (y = y1; y <= y2; y++) {
                row = (Uint32 *)dst->pixels + y * dst->pitch / 4;
                for (x = x1; x <= x2; x++) {
                    pixel = row + x;

                    R = ((*pixel & Rmask) +
                         ((((dR - (*pixel & Rmask)) >> Rshift) * alpha >> 8)
                          << Rshift)) &
                        Rmask;
                    G = ((*pixel & Gmask) +
                         ((((dG - (*pixel & Gmask)) >> Gshift) * alpha >> 8)
                          << Gshift)) &
                        Gmask;
                    B = ((*pixel & Bmask) +
                         ((((dB - (*pixel & Bmask)) >> Bshift) * alpha >> 8)
                          << Bshift)) &
                        Bmask;
                    *pixel = R | G | B;
                    if (Amask != 0) {
                        A = ((*pixel & Amask) +
                             ((((dA - (*pixel & Amask)) >> Ashift) * alpha >>
                               8)
                              << Ashift)) &
                            Amask;
                        *pixel |= A;
                    }
                }
            }
        } break;
#endif

#ifdef EXPERIMENTAL_ALPHA_PIXEL_ROUTINE
        case 4: { /* Probably :-) 32-bpp */
            Uint32 *row, *pixel;
            Uint32 dR, dG, dB, dA;
            Uint32 dc;
            Uint32 surfaceAlpha, preMultR, preMultG, preMultB;
            Uint32 aTmp;

            Rmask = format->Rmask;
            Gmask = format->Gmask;
            Bmask = format->Bmask;
            Amask = format->Amask;

            dR = (color & Rmask);
            dG = (color & Gmask);
            dB = (color & Bmask);
            dA = (color & Amask);

            Rshift = format->Rshift;
            Gshift = format->Gshift;
            Bshift = format->Bshift;
            Ashift = format->Ashift;

            preMultR = (alpha * (dR >> Rshift));
            preMultG = (alpha * (dG >> Gshift));
            preMultB = (alpha * (dB >> Bshift));

            for (y = y1; y <= y2; y++) {
                row = (Uint32 *)dst->pixels + y * dst->pitch / 4;
                for (x = x1; x <= x2; x++) {
                    pixel = row + x;
                    dc = *pixel;

                    surfaceAlpha = ((dc & Amask) >> Ashift);
                    aTmp = (255 - alpha);
                    if (A = 255 - ((aTmp * (255 - surfaceAlpha)) >> 8)) {
                        aTmp *= surfaceAlpha;
                        R = (preMultR +
                             ((aTmp * ((dc & Rmask) >> Rshift)) >> 8)) /
                                    A
                                << Rshift &
                            Rmask;
                        G = (preMultG +
                             ((aTmp * ((dc & Gmask) >> Gshift)) >> 8)) /
                                    A
                                << Gshift &
                            Gmask;
                        B = (preMultB +
                             ((aTmp * ((dc & Bmask) >> Bshift)) >> 8)) /
                                    A
                                << Bshift &
                            Bmask;
                    }
                    *pixel = R | G | B | (A << Ashift & Amask);
                }
            }
        } break;
#endif
    }

    return (0);
}

/*!
\brief Draw filled rectangle of RGBA color with alpha blending.

\param dst The surface to draw on.
\param x1 X coordinate of the first corner (upper left) of the rectangle.
\param y1 Y coordinate of the first corner (upper left) of the rectangle.
\param x2 X coordinate of the second corner (lower right) of the rectangle.
\param y2 Y coordinate of the second corner (lower right) of the rectangle.
\param color The color value of the rectangle to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
filledRectAlpha(SDL_Surface *dst, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2,
                Uint32 color)
{
    Uint8 alpha;
    Uint32 mcolor;
    int result = 0;

    /*
     * Lock the surface
     */
    if (SDL_MUSTLOCK(dst)) {
        if (SDL_LockSurface(dst) < 0) {
            return (-1);
        }
    }

    /*
     * Setup color
     */
    alpha = color & 0x000000ff;
    mcolor = SDL_MapRGBA(dst->format, (color & 0xff000000) >> 24,
                         (color & 0x00ff0000) >> 16, (color & 0x0000ff00) >> 8,
                         alpha);

    /*
     * Draw
     */
    result = _filledRectAlpha(dst, x1, y1, x2, y2, mcolor, alpha);

    /*
     * Unlock the surface
     */
    if (SDL_MUSTLOCK(dst)) {
        SDL_UnlockSurface(dst);
    }

    return (result);
}

/*!
\brief Internal function to draw horizontal line of RGBA color with alpha
blending.

\param dst The surface to draw on.
\param x1 X coordinate of the first point (i.e. left) of the line.
\param x2 X coordinate of the second point (i.e. right) of the line.
\param y Y coordinate of the points of the line.
\param color The color value of the line to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
_HLineAlpha(SDL_Surface *dst, Sint16 x1, Sint16 x2, Sint16 y, Uint32 color)
{
    return (filledRectAlpha(dst, x1, y, x2, y, color));
}

/*!
\brief Internal function to draw vertical line of RGBA color with alpha
blending.

\param dst The surface to draw on.
\param x X coordinate of the points of the line.
\param y1 Y coordinate of the first point (top) of the line.
\param y2 Y coordinate of the second point (bottom) of the line.
\param color The color value of the line to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
_VLineAlpha(SDL_Surface *dst, Sint16 x, Sint16 y1, Sint16 y2, Uint32 color)
{
    return (filledRectAlpha(dst, x, y1, x, y2, color));
}

/*!
\brief Pixel draw with blending enabled and using alpha weight on color - no
locking.

\param dst The surface to draw on.
\param x The horizontal coordinate of the pixel.
\param y The vertical position of the pixel.
\param color The color value of the pixel to draw (0xRRGGBBAA).
\param weight The weight multiplied into the alpha value of the pixel.

\returns Returns 0 on success, -1 on failure.
*/
int
pixelColorWeightNolock(SDL_Surface *dst, Sint16 x, Sint16 y, Uint32 color,
                       Uint32 weight)
{
    Uint32 a;

    /*
     * Get alpha
     */
    a = (color & (Uint32)0x000000ff);

    /*
     * Modify Alpha by weight
     */
    a = ((a * weight) >> 8);

    return (
        pixelColorNolock(dst, x, y, (color & (Uint32)0xffffff00) | (Uint32)a));
}

/*!
\brief Draw horizontal line with blending.

\param dst The surface to draw on.
\param x1 X coordinate of the first point (i.e. left) of the line.
\param x2 X coordinate of the second point (i.e. right) of the line.
\param y Y coordinate of the points of the line.
\param color The color value of the line to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
hlineColor(SDL_Surface *dst, Sint16 x1, Sint16 x2, Sint16 y, Uint32 color)
{
    Sint16 left, right, top, bottom;
    Uint8 *pixel, *pixellast;
    int dx;
    int pixx, pixy;
    Sint16 xtmp;
    int result = -1;
    Uint8 *colorptr;
    Uint8 color3[3];

    /*
     * Check visibility of clipping rectangle
     */
    if ((dst->clip_rect.w == 0) || (dst->clip_rect.h == 0)) {
        return (0);
    }

    /*
     * Swap x1, x2 if required to ensure x1<=x2
     */
    if (x1 > x2) {
        xtmp = x1;
        x1 = x2;
        x2 = xtmp;
    }

    /*
     * Get clipping boundary and
     * check visibility of hline
     */
    left = dst->clip_rect.x;
    if (x2 < left) {
        return (0);
    }
    right = dst->clip_rect.x + dst->clip_rect.w - 1;
    if (x1 > right) {
        return (0);
    }
    top = dst->clip_rect.y;
    bottom = dst->clip_rect.y + dst->clip_rect.h - 1;
    if ((y < top) || (y > bottom)) {
        return (0);
    }

    /*
     * Clip x
     */
    if (x1 < left) {
        x1 = left;
    }
    if (x2 > right) {
        x2 = right;
    }

    /*
     * Calculate width difference
     */
    dx = x2 - x1;

    /*
     * Alpha check
     */
    if ((color & 255) == 255) {
        /*
         * No alpha-blending required
         */

        /*
         * Setup color
         */
        colorptr = (Uint8 *)&color;
        if (SDL_BYTEORDER == SDL_BIG_ENDIAN) {
            color = SDL_MapRGBA(dst->format, colorptr[0], colorptr[1],
                                colorptr[2], colorptr[3]);
        }
        else {
            color = SDL_MapRGBA(dst->format, colorptr[3], colorptr[2],
                                colorptr[1], colorptr[0]);
        }

        /*
         * Lock the surface
         */
        if (SDL_MUSTLOCK(dst)) {
            if (SDL_LockSurface(dst) < 0) {
                return (-1);
            }
        }

        /*
         * More variable setup
         */
        pixx = GFX_SURF_BytesPerPixel(dst);
        pixy = dst->pitch;
        pixel = ((Uint8 *)dst->pixels) + pixx * (int)x1 + pixy * (int)y;

        /*
         * Draw
         */
        switch (GFX_SURF_BytesPerPixel(dst)) {
            case 1:
                memset(pixel, color, dx + 1);
                break;
            case 2:
                pixellast = pixel + dx + dx;
                for (; pixel <= pixellast; pixel += pixx) {
                    *(Uint16 *)pixel = color;
                }
                break;
            case 3:
                pixellast = pixel + dx + dx + dx;
                if (SDL_BYTEORDER == SDL_BIG_ENDIAN) {
                    color3[0] = (color >> 16) & 0xff;
                    color3[1] = (color >> 8) & 0xff;
                    color3[2] = color & 0xff;
                }
                else {
                    color3[0] = color & 0xff;
                    color3[1] = (color >> 8) & 0xff;
                    color3[2] = (color >> 16) & 0xff;
                }
                for (; pixel <= pixellast; pixel += pixx) {
                    memcpy(pixel, color3, 3);
                }
                break;
            default: /* case 4 */
                dx = dx + dx;
                pixellast = pixel + dx + dx;
                for (; pixel <= pixellast; pixel += pixx) {
                    *(Uint32 *)pixel = color;
                }
                break;
        }

        /*
         * Unlock surface
         */
        if (SDL_MUSTLOCK(dst)) {
            SDL_UnlockSurface(dst);
        }

        /*
         * Set result code
         */
        result = 0;
    }
    else {
        /*
         * Alpha blending blit
         */
        result = _HLineAlpha(dst, x1, x1 + dx, y, color);
    }

    return (result);
}

/*!
\brief Draw vertical line with blending.

\param dst The surface to draw on.
\param x X coordinate of the points of the line.
\param y1 Y coordinate of the first point (i.e. top) of the line.
\param y2 Y coordinate of the second point (i.e. bottom) of the line.
\param color The color value of the line to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
vlineColor(SDL_Surface *dst, Sint16 x, Sint16 y1, Sint16 y2, Uint32 color)
{
    Sint16 left, right, top, bottom;
    Uint8 *pixel, *pixellast;
    int dy;
    int pixx, pixy;
    Sint16 h;
    Sint16 ytmp;
    int result = -1;
    Uint8 *colorptr;

    /*
     * Check visibility of clipping rectangle
     */
    if ((dst->clip_rect.w == 0) || (dst->clip_rect.h == 0)) {
        return (0);
    }

    /*
     * Swap y1, y2 if required to ensure y1<=y2
     */
    if (y1 > y2) {
        ytmp = y1;
        y1 = y2;
        y2 = ytmp;
    }

    /*
     * Get clipping boundary and
     * check visibility of vline
     */
    left = dst->clip_rect.x;
    right = dst->clip_rect.x + dst->clip_rect.w - 1;
    if ((x < left) || (x > right)) {
        return (0);
    }
    top = dst->clip_rect.y;
    if (y2 < top) {
        return (0);
    }
    bottom = dst->clip_rect.y + dst->clip_rect.h - 1;
    if (y1 > bottom) {
        return (0);
    }

    /*
     * Clip x
     */
    if (y1 < top) {
        y1 = top;
    }
    if (y2 > bottom) {
        y2 = bottom;
    }

    /*
     * Calculate height
     */
    h = y2 - y1;

    /*
     * Alpha check
     */
    if ((color & 255) == 255) {
        /*
         * No alpha-blending required
         */

        /*
         * Setup color
         */
        colorptr = (Uint8 *)&color;
        if (SDL_BYTEORDER == SDL_BIG_ENDIAN) {
            color = SDL_MapRGBA(dst->format, colorptr[0], colorptr[1],
                                colorptr[2], colorptr[3]);
        }
        else {
            color = SDL_MapRGBA(dst->format, colorptr[3], colorptr[2],
                                colorptr[1], colorptr[0]);
        }

        /*
         * Lock the surface
         */
        if (SDL_MUSTLOCK(dst)) {
            if (SDL_LockSurface(dst) < 0) {
                return (-1);
            }
        }

        /*
         * More variable setup
         */
        dy = h;
        pixx = GFX_SURF_BytesPerPixel(dst);
        pixy = dst->pitch;
        pixel = ((Uint8 *)dst->pixels) + pixx * (int)x + pixy * (int)y1;
        pixellast = pixel + pixy * dy;

        /*
         * Draw
         */
        switch (GFX_SURF_BytesPerPixel(dst)) {
            case 1:
                for (; pixel <= pixellast; pixel += pixy) {
                    *(Uint8 *)pixel = color;
                }
                break;
            case 2:
                for (; pixel <= pixellast; pixel += pixy) {
                    *(Uint16 *)pixel = color;
                }
                break;
            case 3:
                for (; pixel <= pixellast; pixel += pixy) {
                    if (SDL_BYTEORDER == SDL_BIG_ENDIAN) {
                        pixel[0] = (color >> 16) & 0xff;
                        pixel[1] = (color >> 8) & 0xff;
                        pixel[2] = color & 0xff;
                    }
                    else {
                        pixel[0] = color & 0xff;
                        pixel[1] = (color >> 8) & 0xff;
                        pixel[2] = (color >> 16) & 0xff;
                    }
                }
                break;
            default: /* case 4 */
                for (; pixel <= pixellast; pixel += pixy) {
                    *(Uint32 *)pixel = color;
                }
                break;
        }

        /* Unlock surface */
        if (SDL_MUSTLOCK(dst)) {
            SDL_UnlockSurface(dst);
        }

        /*
         * Set result code
         */
        result = 0;
    }
    else {
        /*
         * Alpha blending blit
         */

        result = _VLineAlpha(dst, x, y1, y1 + h, color);
    }

    return (result);
}

/* --------- Clipping routines for line */

/* Clipping based heavily on code from                       */
/* http://www.ncsa.uiuc.edu/Vis/Graphics/src/clipCohSuth.c   */

#define CLIP_LEFT_EDGE 0x1
#define CLIP_RIGHT_EDGE 0x2
#define CLIP_BOTTOM_EDGE 0x4
#define CLIP_TOP_EDGE 0x8
#define CLIP_INSIDE(a) (!a)
#define CLIP_REJECT(a, b) (a & b)
#define CLIP_ACCEPT(a, b) (!(a | b))

/*!
\brief Internal clip-encoding routine.

Calculates a segment-based clipping encoding for a point against a rectangle.

\param x X coordinate of point.
\param y Y coordinate of point.
\param left X coordinate of left edge of the rectangle.
\param top Y coordinate of top edge of the rectangle.
\param right X coordinate of right edge of the rectangle.
\param bottom Y coordinate of bottom edge of the rectangle.
*/
static int
_clipEncode(Sint16 x, Sint16 y, Sint16 left, Sint16 top, Sint16 right,
            Sint16 bottom)
{
    int code = 0;

    if (x < left) {
        code |= CLIP_LEFT_EDGE;
    }
    else if (x > right) {
        code |= CLIP_RIGHT_EDGE;
    }
    if (y < top) {
        code |= CLIP_TOP_EDGE;
    }
    else if (y > bottom) {
        code |= CLIP_BOTTOM_EDGE;
    }
    return code;
}

/*!
\brief Clip line to a the clipping rectangle of a surface.

\param dst Target surface to draw on.
\param x1 Pointer to X coordinate of first point of line.
\param y1 Pointer to Y coordinate of first point of line.
\param x2 Pointer to X coordinate of second point of line.
\param y2 Pointer to Y coordinate of second point of line.
*/
static int
_clipLine(SDL_Surface *dst, Sint16 *x1, Sint16 *y1, Sint16 *x2, Sint16 *y2)
{
    Sint16 left, right, top, bottom;
    int code1, code2;
    int draw = 0;
    Sint16 swaptmp;
    float m;

    /*
     * Get clipping boundary
     */
    left = dst->clip_rect.x;
    right = dst->clip_rect.x + dst->clip_rect.w - 1;
    top = dst->clip_rect.y;
    bottom = dst->clip_rect.y + dst->clip_rect.h - 1;

    while (1) {
        code1 = _clipEncode(*x1, *y1, left, top, right, bottom);
        code2 = _clipEncode(*x2, *y2, left, top, right, bottom);
        if (CLIP_ACCEPT(code1, code2)) {
            draw = 1;
            break;
        }
        else if (CLIP_REJECT(code1, code2))
            break;
        else {
            if (CLIP_INSIDE(code1)) {
                swaptmp = *x2;
                *x2 = *x1;
                *x1 = swaptmp;
                swaptmp = *y2;
                *y2 = *y1;
                *y1 = swaptmp;
                swaptmp = code2;
                code2 = code1;
                code1 = swaptmp;
            }
            if (*x2 != *x1) {
                m = (float)(*y2 - *y1) / (float)(*x2 - *x1);
            }
            else {
                m = 1.0f;
            }
            if (code1 & CLIP_LEFT_EDGE) {
                *y1 += (Sint16)((left - *x1) * m);
                *x1 = left;
            }
            else if (code1 & CLIP_RIGHT_EDGE) {
                *y1 += (Sint16)((right - *x1) * m);
                *x1 = right;
            }
            else if (code1 & CLIP_BOTTOM_EDGE) {
                if (*x2 != *x1) {
                    *x1 += (Sint16)((bottom - *y1) / m);
                }
                *y1 = bottom;
            }
            else if (code1 & CLIP_TOP_EDGE) {
                if (*x2 != *x1) {
                    *x1 += (Sint16)((top - *y1) / m);
                }
                *y1 = top;
            }
        }
    }

    return draw;
}

/* ----- Line */

/* Non-alpha line drawing code adapted from routine          */
/* by Pete Shinners, pete@shinners.org                       */
/* Originally from pygame, http://pygame.seul.org            */

#define ABS(a) (((a) < 0) ? -(a) : (a))

/*!
\brief Draw line with alpha blending.

\param dst The surface to draw on.
\param x1 X coordinate of the first point of the line.
\param y1 Y coordinate of the first point of the line.
\param x2 X coordinate of the second point of the line.
\param y2 Y coordinate of the second point of the line.
\param color The color value of the line to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
lineColor(SDL_Surface *dst, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2,
          Uint32 color)
{
    int pixx, pixy;
    int x, y;
    int dx, dy;
    int ax, ay;
    int sx, sy;
    int swaptmp;
    Uint8 *pixel;
    Uint8 *colorptr;

    /*
     * Clip line and test if we have to draw
     */
    if (!(_clipLine(dst, &x1, &y1, &x2, &y2))) {
        return (0);
    }

    /*
     * Test for special cases of straight lines or single point
     */
    if (x1 == x2) {
        if (y1 < y2) {
            return (vlineColor(dst, x1, y1, y2, color));
        }
        else if (y1 > y2) {
            return (vlineColor(dst, x1, y2, y1, color));
        }
        else {
            return (pixelColor(dst, x1, y1, color));
        }
    }
    if (y1 == y2) {
        if (x1 < x2) {
            return (hlineColor(dst, x1, x2, y1, color));
        }
        else if (x1 > x2) {
            return (hlineColor(dst, x2, x1, y1, color));
        }
    }

    /*
     * Variable setup
     */
    dx = x2 - x1;
    dy = y2 - y1;
    sx = (dx >= 0) ? 1 : -1;
    sy = (dy >= 0) ? 1 : -1;

    /* Lock surface */
    if (SDL_MUSTLOCK(dst)) {
        if (SDL_LockSurface(dst) < 0) {
            return (-1);
        }
    }

    /*
     * Check for alpha blending
     */
    if ((color & 255) == 255) {
        /*
         * No alpha blending - use fast pixel routines
         */

        /*
         * Setup color
         */
        colorptr = (Uint8 *)&color;
        if (SDL_BYTEORDER == SDL_BIG_ENDIAN) {
            color = SDL_MapRGBA(dst->format, colorptr[0], colorptr[1],
                                colorptr[2], colorptr[3]);
        }
        else {
            color = SDL_MapRGBA(dst->format, colorptr[3], colorptr[2],
                                colorptr[1], colorptr[0]);
        }

        /*
         * More variable setup
         */
        dx = sx * dx + 1;
        dy = sy * dy + 1;
        pixx = GFX_SURF_BytesPerPixel(dst);
        pixy = dst->pitch;
        pixel = ((Uint8 *)dst->pixels) + pixx * (int)x1 + pixy * (int)y1;
        pixx *= sx;
        pixy *= sy;
        if (dx < dy) {
            swaptmp = dx;
            dx = dy;
            dy = swaptmp;
            swaptmp = pixx;
            pixx = pixy;
            pixy = swaptmp;
        }

        /*
         * Draw
         */
        x = 0;
        y = 0;
        switch (GFX_SURF_BytesPerPixel(dst)) {
            case 1:
                for (; x < dx; x++, pixel += pixx) {
                    *pixel = color;
                    y += dy;
                    if (y >= dx) {
                        y -= dx;
                        pixel += pixy;
                    }
                }
                break;
            case 2:
                for (; x < dx; x++, pixel += pixx) {
                    *(Uint16 *)pixel = color;
                    y += dy;
                    if (y >= dx) {
                        y -= dx;
                        pixel += pixy;
                    }
                }
                break;
            case 3:
                for (; x < dx; x++, pixel += pixx) {
                    if (SDL_BYTEORDER == SDL_BIG_ENDIAN) {
                        pixel[0] = (color >> 16) & 0xff;
                        pixel[1] = (color >> 8) & 0xff;
                        pixel[2] = color & 0xff;
                    }
                    else {
                        pixel[0] = color & 0xff;
                        pixel[1] = (color >> 8) & 0xff;
                        pixel[2] = (color >> 16) & 0xff;
                    }
                    y += dy;
                    if (y >= dx) {
                        y -= dx;
                        pixel += pixy;
                    }
                }
                break;
            default: /* case 4 */
                for (; x < dx; x++, pixel += pixx) {
                    *(Uint32 *)pixel = color;
                    y += dy;
                    if (y >= dx) {
                        y -= dx;
                        pixel += pixy;
                    }
                }
                break;
        }
    }
    else {
        /*
         * Alpha blending required - use single-pixel blits
         */

        ax = ABS(dx) << 1;
        ay = ABS(dy) << 1;
        x = x1;
        y = y1;
        if (ax > ay) {
            int d = ay - (ax >> 1);

            while (x != x2) {
                pixelColorNolock(dst, x, y, color);
                if (d > 0 || (d == 0 && sx == 1)) {
                    y += sy;
                    d -= ax;
                }
                x += sx;
                d += ay;
            }
        }
        else {
            int d = ax - (ay >> 1);

            while (y != y2) {
                pixelColorNolock(dst, x, y, color);
                if (d > 0 || ((d == 0) && (sy == 1))) {
                    x += sx;
                    d -= ay;
                }
                y += sy;
                d += ax;
            }
        }
        pixelColorNolock(dst, x, y, color);
    }

    /* Unlock surface */
    if (SDL_MUSTLOCK(dst)) {
        SDL_UnlockSurface(dst);
    }

    return (0);
}

/* AA Line */

#define AAlevels 256
#define AAbits 8

/*!
\brief Internal function to draw anti-aliased line with alpha blending and
endpoint control.

This implementation of the Wu antialiasing code is based on Mike Abrash's
DDJ article which was reprinted as Chapter 42 of his Graphics Programming
Black Book, but has been optimized to work with SDL and utilizes 32-bit
fixed-point arithmetic by A. Schiffler. The endpoint control allows the
suppression to draw the last pixel useful for rendering continuous aa-lines
with alpha<255.

\param dst The surface to draw on.
\param x1 X coordinate of the first point of the aa-line.
\param y1 Y coordinate of the first point of the aa-line.
\param x2 X coordinate of the second point of the aa-line.
\param y2 Y coordinate of the second point of the aa-line.
\param color The color value of the aa-line to draw (0xRRGGBBAA).
\param draw_endpoint Flag indicating if the endpoint should be drawn; draw if
non-zero.

\returns Returns 0 on success, -1 on failure.
*/
int
_aalineColor(SDL_Surface *dst, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2,
             Uint32 color, int draw_endpoint)
{
    Sint32 xx0, yy0, xx1, yy1;
    int result;
    Uint32 intshift, erracc, erradj;
    Uint32 erracctmp, wgt, wgtcompmask;
    int dx, dy, tmp, xdir, y0p1, x0pxdir;

    /*
     * Check visibility of clipping rectangle
     */
    if ((dst->clip_rect.w == 0) || (dst->clip_rect.h == 0)) {
        return (0);
    }

    /*
     * Clip line and test if we have to draw
     */
    if (!(_clipLine(dst, &x1, &y1, &x2, &y2))) {
        return (0);
    }

    /*
     * Keep on working with 32bit numbers
     */
    xx0 = x1;
    yy0 = y1;
    xx1 = x2;
    yy1 = y2;

    /*
     * Reorder points if required
     */
    if (yy0 > yy1) {
        tmp = yy0;
        yy0 = yy1;
        yy1 = tmp;
        tmp = xx0;
        xx0 = xx1;
        xx1 = tmp;
    }

    /*
     * Calculate distance
     */
    dx = xx1 - xx0;
    dy = yy1 - yy0;

    /*
     * Check for special cases
     */
    if (dx == 0) {
        /*
         * Vertical line
         */
        if (draw_endpoint) {
            return (vlineColor(dst, x1, y1, y2, color));
        }
        else {
            if (dy > 0) {
                return (vlineColor(dst, x1, yy0, yy0 + dy, color));
            }
            else {
                return (pixelColor(dst, x1, y1, color));
            }
        }
    }
    else if (dy == 0) {
        /*
         * Horizontal line
         */
        if (draw_endpoint) {
            return (hlineColor(dst, x1, x2, y1, color));
        }
        else {
            if (dx != 0) {
                return (hlineColor(dst, xx0, xx0 + dx, y1, color));
            }
            else {
                return (pixelColor(dst, x1, y1, color));
            }
        }
    }
    else if ((dx == dy) && (draw_endpoint)) {
        /*
         * Diagonal line (with endpoint)
         */
        return (lineColor(dst, x1, y1, x2, y2, color));
    }

    /*
     * Adjust for negative dx and set xdir
     */
    if (dx >= 0) {
        xdir = 1;
    }
    else {
        xdir = -1;
        dx = (-dx);
    }

    /*
     * Line is not horizontal, vertical or diagonal (with endpoint)
     */
    result = 0;

    /*
     * Zero accumulator
     */
    erracc = 0;

    /*
     * # of bits by which to shift erracc to get intensity level
     */
    intshift = 32 - AAbits;

    /*
     * Mask used to flip all bits in an intensity weighting
     */
    wgtcompmask = AAlevels - 1;

    /* Lock surface */
    if (SDL_MUSTLOCK(dst)) {
        if (SDL_LockSurface(dst) < 0) {
            return (-1);
        }
    }

    /*
     * Draw the initial pixel in the foreground color
     */
    result |= pixelColorNolock(dst, x1, y1, color);

    /*
     * x-major or y-major?
     */
    if (dy > dx) {
        /*
         * y-major.  Calculate 16-bit fixed point fractional part of a pixel
         * that X advances every time Y advances 1 pixel, truncating the result
         * so that we won't overrun the endpoint along the X axis
         */
        /*
         * Not-so-portable version: erradj = ((Uint64)dx << 32) / (Uint64)dy;
         */
        erradj = ((dx << 16) / dy) << 16;

        /*
         * draw all pixels other than the first and last
         */
        x0pxdir = xx0 + xdir;
        while (--dy) {
            erracctmp = erracc;
            erracc += erradj;
            if (erracc <= erracctmp) {
                /*
                 * rollover in error accumulator, x coord advances
                 */
                xx0 = x0pxdir;
                x0pxdir += xdir;
            }
            yy0++; /* y-major so always advance Y */

            /*
             * the AAbits most significant bits of erracc give us the intensity
             * weighting for this pixel, and the complement of the weighting
             * for the paired pixel.
             */
            wgt = (erracc >> intshift) & 255;
            result |= pixelColorWeightNolock(dst, xx0, yy0, color, 255 - wgt);
            result |= pixelColorWeightNolock(dst, x0pxdir, yy0, color, wgt);
        }
    }
    else {
        /*
         * x-major line.  Calculate 16-bit fixed-point fractional part of a
         * pixel that Y advances each time X advances 1 pixel, truncating the
         * result so that we won't overrun the endpoint along the X axis.
         */
        /*
         * Not-so-portable version: erradj = ((Uint64)dy << 32) / (Uint64)dx;
         */
        erradj = ((dy << 16) / dx) << 16;

        /*
         * draw all pixels other than the first and last
         */
        y0p1 = yy0 + 1;
        while (--dx) {
            erracctmp = erracc;
            erracc += erradj;
            if (erracc <= erracctmp) {
                /*
                 * Accumulator turned over, advance y
                 */
                yy0 = y0p1;
                y0p1++;
            }
            xx0 += xdir; /* x-major so always advance X */
            /*
             * the AAbits most significant bits of erracc give us the intensity
             * weighting for this pixel, and the complement of the weighting
             * for the paired pixel.
             */
            wgt = (erracc >> intshift) & 255;
            result |= pixelColorWeightNolock(dst, xx0, yy0, color, 255 - wgt);
            result |= pixelColorWeightNolock(dst, xx0, y0p1, color, wgt);
        }
    }

    /*
     * Do we have to draw the endpoint
     */
    if (draw_endpoint) {
        /*
         * Draw final pixel, always exactly intersected by the line and doesn't
         * need to be weighted.
         */
        result |= pixelColorNolock(dst, x2, y2, color);
    }

    /* Unlock surface */
    if (SDL_MUSTLOCK(dst)) {
        SDL_UnlockSurface(dst);
    }

    return (result);
}

/* ----- AA Ellipse */

/* Visual Studio 2015 and above define the lrint intrinsic function, but for
 * compatibility with older windows compilers, we need to define it ourselves
 */
#if defined(_MSC_VER)
#if _MSC_VER < 1900
/* Detect 64bit and use intrinsic version */
#ifdef _M_X64
#include <emmintrin.h>
static __inline long
lrint(float f)
{
    return _mm_cvtss_si32(_mm_load_ss(&f));
}
#elif defined(_M_IX86)
__inline long int
lrint(double flt)
{
    int intgr;
    _asm
        {
		fld flt
		fistp intgr
        }
    ;
    return intgr;
}
#elif defined(_M_ARM)
#include <armintr.h>
#pragma warning(push)
#pragma warning(disable : 4716)
__declspec(naked) long int
lrint(double flt)
{
    __emit(0xEC410B10);  // fmdrr  d0, r0, r1
    __emit(0xEEBD0B40);  // ftosid s0, d0
    __emit(0xEE100A10);  // fmrs   r0, s0
    __emit(0xE12FFF1E);  // bx     lr
}
#pragma warning(pop)
#else
#error lrint needed for MSVC on non X86/AMD64/ARM targets.
#endif
#endif
#endif

/*!
\brief Draw anti-aliased ellipse with blending.

Note: Based on code from Anders Lindstroem, which is based on code from sge
library, which is based on code from TwinLib.

\param dst The surface to draw on.
\param x X coordinate of the center of the aa-ellipse.
\param y Y coordinate of the center of the aa-ellipse.
\param rx Horizontal radius in pixels of the aa-ellipse.
\param ry Vertical radius in pixels of the aa-ellipse.
\param color The color value of the aa-ellipse to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
aaellipseColor(SDL_Surface *dst, Sint16 x, Sint16 y, Sint16 rx, Sint16 ry,
               Uint32 color)
{
    Sint16 left, right, top, bottom;
    Sint16 x1, y1, x2, y2;
    int i;
    int a2, b2, ds, dt, dxt, t, s, d;
    Sint16 xp, yp, xs, ys, dyt, xx, yy, xc2, yc2;
    float cp;
    double sab;
    Uint8 weight, iweight;
    int result;

    /*
     * Check visibility of clipping rectangle
     */
    if ((dst->clip_rect.w == 0) || (dst->clip_rect.h == 0)) {
        return (0);
    }

    /*
     * Sanity check radii
     */
    if ((rx < 0) || (ry < 0)) {
        return (-1);
    }

    /*
     * Special case for rx=0 - draw a vline
     */
    if (rx == 0) {
        return (vlineColor(dst, x, y - ry, y + ry, color));
    }
    /*
     * Special case for ry=0 - draw an hline
     */
    if (ry == 0) {
        return (hlineColor(dst, x - rx, x + rx, y, color));
    }

    /*
     * Get circle and clipping boundary and
     * test if bounding box of circle is visible
     */
    x2 = x + rx;
    left = dst->clip_rect.x;
    if (x2 < left) {
        return (0);
    }
    x1 = x - rx;
    right = dst->clip_rect.x + dst->clip_rect.w - 1;
    if (x1 > right) {
        return (0);
    }
    y2 = y + ry;
    top = dst->clip_rect.y;
    if (y2 < top) {
        return (0);
    }
    y1 = y - ry;
    bottom = dst->clip_rect.y + dst->clip_rect.h - 1;
    if (y1 > bottom) {
        return (0);
    }

    /* Variable setup */
    a2 = rx * rx;
    b2 = ry * ry;

    ds = 2 * a2;
    dt = 2 * b2;

    xc2 = 2 * x;
    yc2 = 2 * y;

    sab = sqrt((double)(a2 + b2));
    dxt = (Sint16)lrint((double)a2 / sab);

    t = 0;
    s = -2 * a2 * ry;
    d = 0;

    xp = x;
    yp = y - ry;

    /* Lock surface */
    if (SDL_MUSTLOCK(dst)) {
        if (SDL_LockSurface(dst) < 0) {
            return (-1);
        }
    }

    /* Draw */
    result = 0;

    /* "End points" */
    result |= pixelColorNolock(dst, xp, yp, color);
    result |= pixelColorNolock(dst, xc2 - xp, yp, color);
    result |= pixelColorNolock(dst, xp, yc2 - yp, color);
    result |= pixelColorNolock(dst, xc2 - xp, yc2 - yp, color);

    for (i = 1; i <= dxt; i++) {
        xp--;
        d += t - b2;

        if (d >= 0)
            ys = yp - 1;
        else if ((d - s - a2) > 0) {
            if ((2 * d - s - a2) >= 0)
                ys = yp + 1;
            else {
                ys = yp;
                yp++;
                d -= s + a2;
                s += ds;
            }
        }
        else {
            yp++;
            ys = yp + 1;
            d -= s + a2;
            s += ds;
        }

        t -= dt;

        /* Calculate alpha */
        if (s != 0) {
            cp = (float)abs(d) / (float)abs(s);
            if (cp > 1.0) {
                cp = 1.0;
            }
        }
        else {
            cp = 1.0;
        }

        /* Calculate weights */
        weight = (Uint8)(cp * 255);
        iweight = 255 - weight;

        /* Upper half */
        xx = xc2 - xp;
        result |= pixelColorWeightNolock(dst, xp, yp, color, iweight);
        result |= pixelColorWeightNolock(dst, xx, yp, color, iweight);

        result |= pixelColorWeightNolock(dst, xp, ys, color, weight);
        result |= pixelColorWeightNolock(dst, xx, ys, color, weight);

        /* Lower half */
        yy = yc2 - yp;
        result |= pixelColorWeightNolock(dst, xp, yy, color, iweight);
        result |= pixelColorWeightNolock(dst, xx, yy, color, iweight);

        yy = yc2 - ys;
        result |= pixelColorWeightNolock(dst, xp, yy, color, weight);
        result |= pixelColorWeightNolock(dst, xx, yy, color, weight);
    }

    /* Replaces original approximation code dyt = abs(yp - yc); */
    dyt = (Sint16)lrint((double)b2 / sab);

    for (i = 1; i <= dyt; i++) {
        yp++;
        d -= s + a2;

        if (d <= 0)
            xs = xp + 1;
        else if ((d + t - b2) < 0) {
            if ((2 * d + t - b2) <= 0)
                xs = xp - 1;
            else {
                xs = xp;
                xp--;
                d += t - b2;
                t -= dt;
            }
        }
        else {
            xp--;
            xs = xp - 1;
            d += t - b2;
            t -= dt;
        }

        s += ds;

        /* Calculate alpha */
        if (t != 0) {
            cp = (float)abs(d) / (float)abs(t);
            if (cp > 1.0) {
                cp = 1.0;
            }
        }
        else {
            cp = 1.0;
        }

        /* Calculate weight */
        weight = (Uint8)(cp * 255);
        iweight = 255 - weight;

        /* Left half */
        xx = xc2 - xp;
        yy = yc2 - yp;
        result |= pixelColorWeightNolock(dst, xp, yp, color, iweight);
        result |= pixelColorWeightNolock(dst, xx, yp, color, iweight);

        result |= pixelColorWeightNolock(dst, xp, yy, color, iweight);
        result |= pixelColorWeightNolock(dst, xx, yy, color, iweight);

        /* Right half */
        xx = xc2 - xs;
        result |= pixelColorWeightNolock(dst, xs, yp, color, weight);
        result |= pixelColorWeightNolock(dst, xx, yp, color, weight);

        result |= pixelColorWeightNolock(dst, xs, yy, color, weight);
        result |= pixelColorWeightNolock(dst, xx, yy, color, weight);
    }

    /* Unlock surface */
    if (SDL_MUSTLOCK(dst)) {
        SDL_UnlockSurface(dst);
    }

    return (result);
}

/*!
\brief Draw anti-aliased ellipse with blending.

\param dst The surface to draw on.
\param x X coordinate of the center of the aa-ellipse.
\param y Y coordinate of the center of the aa-ellipse.
\param rx Horizontal radius in pixels of the aa-ellipse.
\param ry Vertical radius in pixels of the aa-ellipse.
\param r The red value of the aa-ellipse to draw.
\param g The green value of the aa-ellipse to draw.
\param b The blue value of the aa-ellipse to draw.
\param a The alpha value of the aa-ellipse to draw.

\returns Returns 0 on success, -1 on failure.
*/
int
aaellipseRGBA(SDL_Surface *dst, Sint16 x, Sint16 y, Sint16 rx, Sint16 ry,
              Uint8 r, Uint8 g, Uint8 b, Uint8 a)
{
    /*
     * Draw
     */
    return (aaellipseColor(
        dst, x, y, rx, ry,
        ((Uint32)r << 24) | ((Uint32)g << 16) | ((Uint32)b << 8) | (Uint32)a));
}

/* ----- pie */

/*!
\brief Internal float (low-speed) pie-calc implementation by drawing polygons.

Note: Determines vertex array and uses polygon or filledPolygon drawing
routines to render.

\param dst The surface to draw on.
\param x X coordinate of the center of the pie.
\param y Y coordinate of the center of the pie.
\param rad Radius in pixels of the pie.
\param start Starting radius in degrees of the pie.
\param end Ending radius in degrees of the pie.
\param color The color value of the pie to draw (0xRRGGBBAA).
\param filled Flag indicating if the pie should be filled (=1) or not (=0).

\returns Returns 0 on success, -1 on failure.
*/
int
_pieColor(SDL_Surface *dst, Sint16 x, Sint16 y, Sint16 rad, Sint16 start,
          Sint16 end, Uint32 color, Uint8 filled)
{
    Sint16 left, right, top, bottom;
    Sint16 x1, y1, x2, y2;
    int result;
    double angle, start_angle, end_angle;
    double deltaAngle;
    double dr;
    int numpoints, i;
    Sint16 *vx, *vy;

    /*
     * Check visibility of clipping rectangle
     */
    if ((dst->clip_rect.w == 0) || (dst->clip_rect.h == 0)) {
        return (0);
    }

    /*
     * Sanity check radii
     */
    if (rad < 0) {
        return (-1);
    }

    /*
     * Fixup angles
     */
    start = start % 360;
    end = end % 360;

    /*
     * Special case for rad=0 - draw a point
     */
    if (rad == 0) {
        return (pixelColor(dst, x, y, color));
    }

    /*
     * Clip against circle, not pie (not 100% optimal).
     * Get pie's circle and clipping boundary and
     * test if bounding box of circle is visible
     */
    x2 = x + rad;
    left = dst->clip_rect.x;
    if (x2 < left) {
        return (0);
    }
    x1 = x - rad;
    right = dst->clip_rect.x + dst->clip_rect.w - 1;
    if (x1 > right) {
        return (0);
    }
    y2 = y + rad;
    top = dst->clip_rect.y;
    if (y2 < top) {
        return (0);
    }
    y1 = y - rad;
    bottom = dst->clip_rect.y + dst->clip_rect.h - 1;
    if (y1 > bottom) {
        return (0);
    }

    /*
     * Variable setup
     */
    dr = (double)rad;
    deltaAngle = 3.0 / dr;
    start_angle = (double)start * (2.0 * M_PI / 360.0);
    end_angle = (double)end * (2.0 * M_PI / 360.0);
    if (start > end) {
        end_angle += (2.0 * M_PI);
    }

    /* We will always have at least 2 points */
    numpoints = 2;

    /* Count points (rather than calculating it) */
    angle = start_angle;
    while (angle < end_angle) {
        angle += deltaAngle;
        numpoints++;
    }

    /* Allocate combined vertex array */
    vx = vy = (Sint16 *)malloc(2 * sizeof(Uint16) * numpoints);
    if (vx == NULL) {
        return (-1);
    }

    /* Update point to start of vy */
    vy += numpoints;

    /* Center */
    vx[0] = x;
    vy[0] = y;

    /* First vertex */
    angle = start_angle;
    vx[1] = x + (int)(dr * cos(angle));
    vy[1] = y + (int)(dr * sin(angle));

    if (numpoints < 3) {
        result = lineColor(dst, vx[0], vy[0], vx[1], vy[1], color);
    }
    else {
        /* Calculate other vertices */
        i = 2;
        angle = start_angle;
        while (angle < end_angle) {
            angle += deltaAngle;
            if (angle > end_angle) {
                angle = end_angle;
            }
            vx[i] = x + (int)(dr * cos(angle));
            vy[i] = y + (int)(dr * sin(angle));
            i++;
        }

        /* Draw */
        if (filled) {
            result = filledPolygonColor(dst, vx, vy, numpoints, color);
        }
        else {
            result = polygonColor(dst, vx, vy, numpoints, color);
        }
    }

    /* Free combined vertex array */
    free(vx);

    return (result);
}

/*!
\brief Draw pie (outline) with alpha blending.

\param dst The surface to draw on.
\param x X coordinate of the center of the pie.
\param y Y coordinate of the center of the pie.
\param rad Radius in pixels of the pie.
\param start Starting radius in degrees of the pie.
\param end Ending radius in degrees of the pie.
\param color The color value of the pie to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
pieColor(SDL_Surface *dst, Sint16 x, Sint16 y, Sint16 rad, Sint16 start,
         Sint16 end, Uint32 color)
{
    return (_pieColor(dst, x, y, rad, start, end, color, 0));
}

/*!
\brief Draw pie (outline) with alpha blending.

\param dst The surface to draw on.
\param x X coordinate of the center of the pie.
\param y Y coordinate of the center of the pie.
\param rad Radius in pixels of the pie.
\param start Starting radius in degrees of the pie.
\param end Ending radius in degrees of the pie.
\param r The red value of the pie to draw.
\param g The green value of the pie to draw.
\param b The blue value of the pie to draw.
\param a The alpha value of the pie to draw.

\returns Returns 0 on success, -1 on failure.
*/
int
pieRGBA(SDL_Surface *dst, Sint16 x, Sint16 y, Sint16 rad, Sint16 start,
        Sint16 end, Uint8 r, Uint8 g, Uint8 b, Uint8 a)
{
    return (_pieColor(
        dst, x, y, rad, start, end,
        ((Uint32)r << 24) | ((Uint32)g << 16) | ((Uint32)b << 8) | (Uint32)a,
        0));
}

/* ------ AA-Trigon */

/*!
\brief Draw anti-aliased trigon (triangle outline) with alpha blending.

Note: Creates vertex array and uses aapolygon routine to render.

\param dst The surface to draw on.
\param x1 X coordinate of the first point of the aa-trigon.
\param y1 Y coordinate of the first point of the aa-trigon.
\param x2 X coordinate of the second point of the aa-trigon.
\param y2 Y coordinate of the second point of the aa-trigon.
\param x3 X coordinate of the third point of the aa-trigon.
\param y3 Y coordinate of the third point of the aa-trigon.
\param color The color value of the aa-trigon to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
aatrigonColor(SDL_Surface *dst, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2,
              Sint16 x3, Sint16 y3, Uint32 color)
{
    Sint16 vx[3];
    Sint16 vy[3];

    vx[0] = x1;
    vx[1] = x2;
    vx[2] = x3;
    vy[0] = y1;
    vy[1] = y2;
    vy[2] = y3;

    return (aapolygonColor(dst, vx, vy, 3, color));
}

/*!
\brief Draw anti-aliased trigon (triangle outline) with alpha blending.

\param dst The surface to draw on.
\param x1 X coordinate of the first point of the aa-trigon.
\param y1 Y coordinate of the first point of the aa-trigon.
\param x2 X coordinate of the second point of the aa-trigon.
\param y2 Y coordinate of the second point of the aa-trigon.
\param x3 X coordinate of the third point of the aa-trigon.
\param y3 Y coordinate of the third point of the aa-trigon.
\param r The red value of the aa-trigon to draw.
\param g The green value of the aa-trigon to draw.
\param b The blue value of the aa-trigon to draw.
\param a The alpha value of the aa-trigon to draw.

\returns Returns 0 on success, -1 on failure.
*/
int
aatrigonRGBA(SDL_Surface *dst, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2,
             Sint16 x3, Sint16 y3, Uint8 r, Uint8 g, Uint8 b, Uint8 a)
{
    Sint16 vx[3];
    Sint16 vy[3];

    vx[0] = x1;
    vx[1] = x2;
    vx[2] = x3;
    vy[0] = y1;
    vy[1] = y2;
    vy[2] = y3;

    return (aapolygonRGBA(dst, vx, vy, 3, r, g, b, a));
}

/* ------ Filled Trigon */

/* ---- Polygon */

/*!
\brief Draw polygon with alpha blending.

\param dst The surface to draw on.
\param vx Vertex array containing X coordinates of the points of the polygon.
\param vy Vertex array containing Y coordinates of the points of the polygon.
\param n Number of points in the vertex array. Minimum number is 3.
\param color The color value of the polygon to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
polygonColor(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n,
             Uint32 color)
{
    int result;
    int i;
    const Sint16 *x1, *y1, *x2, *y2;

    /*
     * Check visibility of clipping rectangle
     */
    if ((dst->clip_rect.w == 0) || (dst->clip_rect.h == 0)) {
        return (0);
    }

    /*
     * Vertex array NULL check
     */
    if (vx == NULL) {
        return (-1);
    }
    if (vy == NULL) {
        return (-1);
    }

    /*
     * Sanity check
     */
    if (n < 3) {
        return (-1);
    }

    /*
     * Pointer setup
     */
    x1 = x2 = vx;
    y1 = y2 = vy;
    x2++;
    y2++;

    /*
     * Draw
     */
    result = 0;
    for (i = 1; i < n; i++) {
        result |= lineColor(dst, *x1, *y1, *x2, *y2, color);
        x1 = x2;
        y1 = y2;
        x2++;
        y2++;
    }
    result |= lineColor(dst, *x1, *y1, *vx, *vy, color);

    return (result);
}

/* ---- AA-Polygon */

/*!
\brief Draw anti-aliased polygon with alpha blending.

\param dst The surface to draw on.
\param vx Vertex array containing X coordinates of the points of the
aa-polygon. \param vy Vertex array containing Y coordinates of the points of
the aa-polygon. \param n Number of points in the vertex array. Minimum number
is 3. \param color The color value of the aa-polygon to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
aapolygonColor(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n,
               Uint32 color)
{
    int result;
    int i;
    const Sint16 *x1, *y1, *x2, *y2;

    /*
     * Check visibility of clipping rectangle
     */
    if ((dst->clip_rect.w == 0) || (dst->clip_rect.h == 0)) {
        return (0);
    }

    /*
     * Vertex array NULL check
     */
    if (vx == NULL) {
        return (-1);
    }
    if (vy == NULL) {
        return (-1);
    }

    /*
     * Sanity check
     */
    if (n < 3) {
        return (-1);
    }

    /*
     * Pointer setup
     */
    x1 = x2 = vx;
    y1 = y2 = vy;
    x2++;
    y2++;

    /*
     * Draw
     */
    result = 0;
    for (i = 1; i < n; i++) {
        result |= _aalineColor(dst, *x1, *y1, *x2, *y2, color, 0);
        x1 = x2;
        y1 = y2;
        x2++;
        y2++;
    }
    result |= _aalineColor(dst, *x1, *y1, *vx, *vy, color, 0);

    return (result);
}

/*!
\brief Draw anti-aliased polygon with alpha blending.

\param dst The surface to draw on.
\param vx Vertex array containing X coordinates of the points of the
aa-polygon. \param vy Vertex array containing Y coordinates of the points of
the aa-polygon. \param n Number of points in the vertex array. Minimum number
is 3. \param r The red value of the aa-polygon to draw. \param g The green
value of the aa-polygon to draw. \param b The blue value of the aa-polygon to
draw. \param a The alpha value of the aa-polygon to draw.

\returns Returns 0 on success, -1 on failure.
*/
int
aapolygonRGBA(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n,
              Uint8 r, Uint8 g, Uint8 b, Uint8 a)
{
    /*
     * Draw
     */
    return (aapolygonColor(
        dst, vx, vy, n,
        ((Uint32)r << 24) | ((Uint32)g << 16) | ((Uint32)b << 8) | (Uint32)a));
}

/* ---- Filled Polygon */

/*!
\brief Internal helper qsort callback functions used in filled polygon drawing.

\param a The surface to draw on.
\param b Vertex array containing X coordinates of the points of the polygon.

\returns Returns 0 if a==b, a negative number if a<b or a positive number if
a>b.
*/
int
_gfxPrimitivesCompareInt(const void *a, const void *b)
{
    return (*(const int *)a) - (*(const int *)b);
}

/*!
\brief Global vertex array to use if optional parameters are not given in
filledPolygonMT calls.

Note: Used for non-multithreaded (default) operation of filledPolygonMT.
*/
static int *gfxPrimitivesPolyIntsGlobal = NULL;

/*!
\brief Flag indicating if global vertex array was already allocated.

Note: Used for non-multithreaded (default) operation of filledPolygonMT.
*/
static int gfxPrimitivesPolyAllocatedGlobal = 0;

/*!
\brief Draw filled polygon with alpha blending (multi-threaded capable).

Note: The last two parameters are optional; but are required for multithreaded
operation.

\param dst The surface to draw on.
\param vx Vertex array containing X coordinates of the points of the filled
polygon. \param vy Vertex array containing Y coordinates of the points of the
filled polygon. \param n Number of points in the vertex array. Minimum number
is 3. \param color The color value of the filled polygon to draw (0xRRGGBBAA).
\param polyInts Preallocated, temporary vertex array used for sorting vertices.
Required for multithreaded operation; set to NULL otherwise. \param
polyAllocated Flag indicating if temporary vertex array was allocated. Required
for multithreaded operation; set to NULL otherwise.

\returns Returns 0 on success, -1 on failure.
*/
int
filledPolygonColorMT(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy,
                     int n, Uint32 color, int **polyInts, int *polyAllocated)
{
    int result;
    int i;
    int y, xa, xb;
    int miny, maxy;
    int x1, y1;
    int x2, y2;
    int ind1, ind2;
    int ints;
    int *gfxPrimitivesPolyInts = NULL;
    int *gfxPrimitivesPolyIntsNew = NULL;
    int gfxPrimitivesPolyAllocated = 0;

    /*
     * Check visibility of clipping rectangle
     */
    if ((dst->clip_rect.w == 0) || (dst->clip_rect.h == 0)) {
        return (0);
    }

    /*
     * Vertex array NULL check
     */
    if (vx == NULL) {
        return (-1);
    }
    if (vy == NULL) {
        return (-1);
    }

    /*
     * Sanity check number of edges
     */
    if (n < 3) {
        return -1;
    }

    /*
     * Map polygon cache
     */
    if ((polyInts == NULL) || (polyAllocated == NULL)) {
        /* Use global cache */
        gfxPrimitivesPolyInts = gfxPrimitivesPolyIntsGlobal;
        gfxPrimitivesPolyAllocated = gfxPrimitivesPolyAllocatedGlobal;
    }
    else {
        /* Use local cache */
        gfxPrimitivesPolyInts = *polyInts;
        gfxPrimitivesPolyAllocated = *polyAllocated;
    }

    /*
     * Allocate temp array, only grow array
     */
    if (!gfxPrimitivesPolyAllocated) {
        gfxPrimitivesPolyInts = (int *)malloc(sizeof(int) * n);
        gfxPrimitivesPolyAllocated = n;
    }
    else {
        if (gfxPrimitivesPolyAllocated < n) {
            gfxPrimitivesPolyIntsNew =
                (int *)realloc(gfxPrimitivesPolyInts, sizeof(int) * n);
            if (!gfxPrimitivesPolyIntsNew) {
                if (!gfxPrimitivesPolyInts) {
                    free(gfxPrimitivesPolyInts);
                    gfxPrimitivesPolyInts = NULL;
                }
                gfxPrimitivesPolyAllocated = 0;
            }
            else {
                gfxPrimitivesPolyInts = gfxPrimitivesPolyIntsNew;
                gfxPrimitivesPolyAllocated = n;
            }
        }
    }

    /*
     * Check temp array
     */
    if (gfxPrimitivesPolyInts == NULL) {
        gfxPrimitivesPolyAllocated = 0;
    }

    /*
     * Update cache variables
     */
    if ((polyInts == NULL) || (polyAllocated == NULL)) {
        gfxPrimitivesPolyIntsGlobal = gfxPrimitivesPolyInts;
        gfxPrimitivesPolyAllocatedGlobal = gfxPrimitivesPolyAllocated;
    }
    else {
        *polyInts = gfxPrimitivesPolyInts;
        *polyAllocated = gfxPrimitivesPolyAllocated;
    }

    /*
     * Check temp array again
     */
    if (gfxPrimitivesPolyInts == NULL) {
        return (-1);
    }

    /*
     * Determine Y maxima
     */
    miny = vy[0];
    maxy = vy[0];
    for (i = 1; (i < n); i++) {
        if (vy[i] < miny) {
            miny = vy[i];
        }
        else if (vy[i] > maxy) {
            maxy = vy[i];
        }
    }

    /*
     * Draw, scanning y
     */
    result = 0;
    for (y = miny; (y <= maxy); y++) {
        ints = 0;
        for (i = 0; (i < n); i++) {
            if (!i) {
                ind1 = n - 1;
                ind2 = 0;
            }
            else {
                ind1 = i - 1;
                ind2 = i;
            }
            y1 = vy[ind1];
            y2 = vy[ind2];
            if (y1 < y2) {
                x1 = vx[ind1];
                x2 = vx[ind2];
            }
            else if (y1 > y2) {
                y2 = vy[ind1];
                y1 = vy[ind2];
                x2 = vx[ind1];
                x1 = vx[ind2];
            }
            else {
                continue;
            }
            if (((y >= y1) && (y < y2)) ||
                ((y == maxy) && (y > y1) && (y <= y2))) {
                gfxPrimitivesPolyInts[ints++] =
                    ((65536 * (y - y1)) / (y2 - y1)) * (x2 - x1) +
                    (65536 * x1);
            }
        }

        qsort(gfxPrimitivesPolyInts, ints, sizeof(int),
              _gfxPrimitivesCompareInt);

        for (i = 0; (i < ints); i += 2) {
            xa = gfxPrimitivesPolyInts[i] + 1;
            xa = (xa >> 16) + ((xa & 32768) >> 15);
            xb = gfxPrimitivesPolyInts[i + 1] - 1;
            xb = (xb >> 16) + ((xb & 32768) >> 15);
            result |= hlineColor(dst, xa, xb, y, color);
        }
    }

    return (result);
}

/*!
\brief Draw filled polygon with alpha blending.

Note: Standard filledPolygon function is calling multithreaded version with
NULL parameters to use the global vertex cache.

\param dst The surface to draw on.
\param vx Vertex array containing X coordinates of the points of the filled
polygon. \param vy Vertex array containing Y coordinates of the points of the
filled polygon. \param n Number of points in the vertex array. Minimum number
is 3. \param color The color value of the filled polygon to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
filledPolygonColor(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n,
                   Uint32 color)
{
    /*
     * Draw
     */
    return (filledPolygonColorMT(dst, vx, vy, n, color, NULL, NULL));
}

/*!
\brief Internal function to draw a textured horizontal line.

\param dst The surface to draw on.
\param x1 X coordinate of the first point (i.e. left) of the line.
\param x2 X coordinate of the second point (i.e. right) of the line.
\param y Y coordinate of the points of the line.
\param texture The texture surface to retrieve color information from.
\param texture_dx The X offset for the texture lookup.
\param texture_dy The Y offset for the textured lookup.

\returns Returns 0 on success, -1 on failure.
*/
int
_HLineTextured(SDL_Surface *dst, Sint16 x1, Sint16 x2, Sint16 y,
               SDL_Surface *texture, int texture_dx, int texture_dy)
{
    Sint16 left, right, top, bottom;
    Sint16 w;
    Sint16 xtmp;
    int result = 0;
    int texture_x_walker;
    int texture_y_start;
    SDL_Rect source_rect, dst_rect;
    int pixels_written, write_width;

    /*
     * Check visibility of clipping rectangle
     */
    if ((dst->clip_rect.w == 0) || (dst->clip_rect.h == 0)) {
        return (0);
    }

    /*
     * Swap x1, x2 if required to ensure x1<=x2
     */
    if (x1 > x2) {
        xtmp = x1;
        x1 = x2;
        x2 = xtmp;
    }

    /*
     * Get clipping boundary and
     * check visibility of hline
     */
    left = dst->clip_rect.x;
    if (x2 < left) {
        return (0);
    }
    right = dst->clip_rect.x + dst->clip_rect.w - 1;
    if (x1 > right) {
        return (0);
    }
    top = dst->clip_rect.y;
    bottom = dst->clip_rect.y + dst->clip_rect.h - 1;
    if ((y < top) || (y > bottom)) {
        return (0);
    }

    /*
     * Clip x
     */
    if (x1 < left) {
        x1 = left;
    }
    if (x2 > right) {
        x2 = right;
    }

    /*
     * Calculate width to draw
     */
    w = x2 - x1 + 1;

    /*
     * Determine where in the texture we start drawing
     */
    texture_x_walker = (x1 - texture_dx) % texture->w;
    if (texture_x_walker < 0) {
        texture_x_walker = texture->w + texture_x_walker;
    }

    texture_y_start = (y + texture_dy) % texture->h;
    if (texture_y_start < 0) {
        texture_y_start = texture->h + texture_y_start;
    }

    // setup the source rectangle; we are only drawing one horizontal line
    source_rect.y = texture_y_start;
    source_rect.x = texture_x_walker;
    source_rect.h = 1;

    // we will draw to the current y
    dst_rect.y = y;

    // if there are enough pixels left in the current row of the texture
    // draw it all at once
    if (w <= texture->w - texture_x_walker) {
        source_rect.w = w;
        source_rect.x = texture_x_walker;
        dst_rect.x = x1;
        result = (SDL_BlitSurface(texture, &source_rect, dst, &dst_rect) == 0);
    }
    else {  // we need to draw multiple times
        // draw the first segment
        pixels_written = texture->w - texture_x_walker;
        source_rect.w = pixels_written;
        source_rect.x = texture_x_walker;
        dst_rect.x = x1;
        result |=
            (SDL_BlitSurface(texture, &source_rect, dst, &dst_rect) == 0);
        write_width = texture->w;

        // now draw the rest
        // set the source x to 0
        source_rect.x = 0;
        while (pixels_written < w) {
            if (write_width >= w - pixels_written) {
                write_width = w - pixels_written;
            }
            source_rect.w = write_width;
            dst_rect.x = x1 + pixels_written;
            result |=
                (SDL_BlitSurface(texture, &source_rect, dst, &dst_rect) == 0);
            pixels_written += write_width;
        }
    }

    return result;
}

/*!
\brief Draws a polygon filled with the given texture (Multi-Threading Capable).

This operation use internally SDL_BlitSurface for lines of the source texture.
It supports alpha drawing.

To get the best performance of this operation you need to make sure the texture
and the dst surface have the same format (see
http://docs.mandragor.org/files/Common_libs_documentation/SDL/SDL_Documentation_project_en/sdlblitsurface.html).
The last two parameters are optional, but required for multithreaded operation.
When set to NULL, uses global static temp array.

\param dst the destination surface,
\param vx array of x vector components
\param vy array of x vector components
\param n the amount of vectors in the vx and vy array
\param texture the sdl surface to use to fill the polygon
\param texture_dx the offset of the texture relative to the screen. if you
move the polygon 10 pixels to the left and want the texture to appear the same
you need to increase the texture_dx value \param texture_dy see texture_dx
\param polyInts preallocated temp array storage for vertex sorting (used for
multi-threaded operation) \param polyAllocated flag indicating if the temp
array was allocated (used for multi-threaded operation)

\returns Returns 0 on success, -1 on failure.
*/
int
texturedPolygonMT(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n,
                  SDL_Surface *texture, int texture_dx, int texture_dy,
                  int **polyInts, int *polyAllocated)
{
    int result;
    int i;
    int y, xa, xb;
    int minx, maxx, miny, maxy;
    int x1, y1;
    int x2, y2;
    int ind1, ind2;
    int ints;
    int *gfxPrimitivesPolyInts = NULL;
    int gfxPrimitivesPolyAllocated = 0;

    /*
     * Check visibility of clipping rectangle
     */
    if ((dst->clip_rect.w == 0) || (dst->clip_rect.h == 0)) {
        return (0);
    }

    /*
     * Sanity check number of edges
     */
    if (n < 3) {
        return -1;
    }

    /*
     * Map polygon cache
     */
    if ((polyInts == NULL) || (polyAllocated == NULL)) {
        /* Use global cache */
        gfxPrimitivesPolyInts = gfxPrimitivesPolyIntsGlobal;
        gfxPrimitivesPolyAllocated = gfxPrimitivesPolyAllocatedGlobal;
    }
    else {
        /* Use local cache */
        gfxPrimitivesPolyInts = *polyInts;
        gfxPrimitivesPolyAllocated = *polyAllocated;
    }

    /*
     * Allocate temp array, only grow array
     */
    if (!gfxPrimitivesPolyAllocated) {
        gfxPrimitivesPolyInts = (int *)malloc(sizeof(int) * n);
        gfxPrimitivesPolyAllocated = n;
    }
    else {
        if (gfxPrimitivesPolyAllocated < n) {
            gfxPrimitivesPolyInts =
                (int *)realloc(gfxPrimitivesPolyInts, sizeof(int) * n);
            gfxPrimitivesPolyAllocated = n;
        }
    }

    /*
     * Check temp array
     */
    if (gfxPrimitivesPolyInts == NULL) {
        gfxPrimitivesPolyAllocated = 0;
    }

    /*
     * Update cache variables
     */
    if ((polyInts == NULL) || (polyAllocated == NULL)) {
        gfxPrimitivesPolyIntsGlobal = gfxPrimitivesPolyInts;
        gfxPrimitivesPolyAllocatedGlobal = gfxPrimitivesPolyAllocated;
    }
    else {
        *polyInts = gfxPrimitivesPolyInts;
        *polyAllocated = gfxPrimitivesPolyAllocated;
    }

    /*
     * Check temp array again
     */
    if (gfxPrimitivesPolyInts == NULL) {
        return (-1);
    }

    /*
     * Determine X,Y minima,maxima
     */
    miny = vy[0];
    maxy = vy[0];
    minx = vx[0];
    maxx = vx[0];
    for (i = 1; (i < n); i++) {
        if (vy[i] < miny) {
            miny = vy[i];
        }
        else if (vy[i] > maxy) {
            maxy = vy[i];
        }
        if (vx[i] < minx) {
            minx = vx[i];
        }
        else if (vx[i] > maxx) {
            maxx = vx[i];
        }
    }
    if (maxx < 0 || minx > dst->w) {
        return -1;
    }
    if (maxy < 0 || miny > dst->h) {
        return -1;
    }

    /*
     * Draw, scanning y
     */
    result = 0;
    for (y = miny; (y <= maxy); y++) {
        ints = 0;
        for (i = 0; (i < n); i++) {
            if (!i) {
                ind1 = n - 1;
                ind2 = 0;
            }
            else {
                ind1 = i - 1;
                ind2 = i;
            }
            y1 = vy[ind1];
            y2 = vy[ind2];
            if (y1 < y2) {
                x1 = vx[ind1];
                x2 = vx[ind2];
            }
            else if (y1 > y2) {
                y2 = vy[ind1];
                y1 = vy[ind2];
                x2 = vx[ind1];
                x1 = vx[ind2];
            }
            else {
                continue;
            }
            if (((y >= y1) && (y < y2)) ||
                ((y == maxy) && (y > y1) && (y <= y2))) {
                gfxPrimitivesPolyInts[ints++] =
                    ((65536 * (y - y1)) / (y2 - y1)) * (x2 - x1) +
                    (65536 * x1);
            }
        }

        qsort(gfxPrimitivesPolyInts, ints, sizeof(int),
              _gfxPrimitivesCompareInt);

        for (i = 0; (i < ints); i += 2) {
            xa = gfxPrimitivesPolyInts[i] + 1;
            xa = (xa >> 16) + ((xa & 32768) >> 15);
            xb = gfxPrimitivesPolyInts[i + 1] - 1;
            xb = (xb >> 16) + ((xb & 32768) >> 15);
            result |= _HLineTextured(dst, xa, xb, y, texture, texture_dx,
                                     texture_dy);
        }
    }

    return (result);
}

/*!
\brief Draws a polygon filled with the given texture.

This standard version is calling multithreaded versions with NULL cache
parameters.

\param dst the destination surface,
\param vx array of x vector components
\param vy array of x vector components
\param n the amount of vectors in the vx and vy array
\param texture the sdl surface to use to fill the polygon
\param texture_dx the offset of the texture relative to the screeen. if you
move the polygon 10 pixels to the left and want the texture to appear the same
you need to increase the texture_dx value \param texture_dy see texture_dx

\returns Returns 0 on success, -1 on failure.
*/
int
texturedPolygon(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n,
                SDL_Surface *texture, int texture_dx, int texture_dy)
{
    /*
     * Draw
     */
    return (texturedPolygonMT(dst, vx, vy, n, texture, texture_dx, texture_dy,
                              NULL, NULL));
}

/* ---- Bezier curve */

/*!
\brief Internal function to calculate bezier interpolator of data array with
ndata values at position 't'.

\param data Array of values.
\param ndata Size of array.
\param t Position for which to calculate interpolated value. t should be
between [0, nstepdata]. \param nstepdata Number of steps for the interpolation
multiplied by the number of points. \returns Interpolated value at position t,
value[0] when t<0, value[n-1] when t>=n.
*/
double
_evaluateBezier(double *data, int ndata, int t, int nstepdata)
{
    double mu, result;
    int n, k, kn, nn, nkn;
    double blend, muk, munk;

    /* Sanity check bounds */
    if (t < 0) {
        return (data[0]);
    }
    if (t >= nstepdata) {
        return (data[ndata - 1]);
    }

    /* Adjust t to the range 0.0 to 1.0 */
    mu = t / (double)nstepdata;

    /* Calculate interpolate */
    n = ndata - 1;
    result = 0.0;
    muk = 1;
    munk = pow(1 - mu, (double)n);

    /* Ensure munk is not 0 which would cause coordinates to be (0, 0) */
    if (munk <= 0) {
        return (data[ndata - 1]);
    }

    for (k = 0; k <= n; k++) {
        nn = n;
        kn = k;
        nkn = n - k;
        blend = muk * munk;
        muk *= mu;
        munk /= (1 - mu);
        while (nn >= 1) {
            blend *= nn;
            nn--;
            if (kn > 1) {
                blend /= (double)kn;
                kn--;
            }
            if (nkn > 1) {
                blend /= (double)nkn;
                nkn--;
            }
        }
        result += data[k] * blend;
    }

    return (result);
}

/*!
\brief Draw a bezier curve with alpha blending.

\param dst The surface to draw on.
\param vx Vertex array containing X coordinates of the points of the bezier
curve. \param vy Vertex array containing Y coordinates of the points of the
bezier curve. \param n Number of points in the vertex array. Minimum number
is 3. \param s Number of steps for the interpolation. Minimum number is 2.
\param color The color value of the bezier curve to draw (0xRRGGBBAA).

\returns Returns 0 on success, -1 on failure.
*/
int
bezierColor(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n, int s,
            Uint32 color)
{
    int result;
    int i, steppoints;
    double *x, *y;
    Sint16 x1, y1, x2, y2;

    /*
     * Sanity check
     */
    if (n < 3) {
        return (-1);
    }
    if (s < 2) {
        return (-1);
    }

    /*
     * Variable setup
     */
    steppoints = s * n;

    /* Transfer vertices into float arrays */
    if ((x = (double *)malloc(sizeof(double) * (n + 1))) == NULL) {
        return (-1);
    }
    if ((y = (double *)malloc(sizeof(double) * (n + 1))) == NULL) {
        free(x);
        return (-1);
    }
    for (i = 0; i < n; i++) {
        x[i] = (double)vx[i];
        y[i] = (double)vy[i];
    }
    x[n] = (double)vx[0];
    y[n] = (double)vy[0];

    /*
     * Draw
     */
    result = 0;
    x1 = (Sint16)lrint(_evaluateBezier(x, n + 1, 0, steppoints));
    y1 = (Sint16)lrint(_evaluateBezier(y, n + 1, 0, steppoints));
    for (i = 1; i <= steppoints; i++) {
        x2 = (Sint16)_evaluateBezier(x, n, i, steppoints);
        y2 = (Sint16)_evaluateBezier(y, n, i, steppoints);
        result |= lineColor(dst, x1, y1, x2, y2, color);
        x1 = x2;
        y1 = y2;
    }

    /* Clean up temporary array */
    free(x);
    free(y);

    return (result);
}

/*!
\brief Draw a bezier curve with alpha blending.

\param dst The surface to draw on.
\param vx Vertex array containing X coordinates of the points of the bezier
curve. \param vy Vertex array containing Y coordinates of the points of the
bezier curve. \param n Number of points in the vertex array. Minimum number
is 3. \param s Number of steps for the interpolation. Minimum number is 2.
\param r The red value of the bezier curve to draw.
\param g The green value of the bezier curve to draw.
\param b The blue value of the bezier curve to draw.
\param a The alpha value of the bezier curve to draw.

\returns Returns 0 on success, -1 on failure.
*/
int
bezierRGBA(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n, int s,
           Uint8 r, Uint8 g, Uint8 b, Uint8 a)
{
    /*
     * Draw
     */
    return (bezierColor(
        dst, vx, vy, n, s,
        ((Uint32)r << 24) | ((Uint32)g << 16) | ((Uint32)b << 8) | (Uint32)a));
}
