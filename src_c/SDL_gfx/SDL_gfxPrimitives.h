/*

SDL_gfxPrimitives: graphics primitives for SDL

LGPL (c) A. Schiffler

*/

#ifndef _SDL_gfxPrimitives_h
#define _SDL_gfxPrimitives_h

#include <math.h>
#ifndef M_PI
#define M_PI 3.1415926535897932384626433832795
#endif

#include "SDL.h"

/* Set up for C function definitions, even when using C++ */
#ifdef __cplusplus
extern "C" {
#endif

/* ----- Versioning */

#define SDL_GFXPRIMITIVES_MAJOR 2
#define SDL_GFXPRIMITIVES_MINOR 0
#define SDL_GFXPRIMITIVES_MICRO 23

/* ---- Compatibility */

#if SDL_VERSION_ATLEAST(3, 0, 0)
#define GFX_SURF_BitsPerPixel(surf) surf->format->bits_per_pixel
#define GFX_SURF_BytesPerPixel(surf) surf->format->bytes_per_pixel
#define GFX_FORMAT_BitsPerPixel(format) format->bits_per_pixel
#define GFX_FORMAT_BytesPerPixel(format) format->bytes_per_pixel
#else
#define GFX_SURF_BitsPerPixel(surf) surf->format->BitsPerPixel
#define GFX_SURF_BytesPerPixel(surf) surf->format->BytesPerPixel
#define GFX_FORMAT_BitsPerPixel(format) format->BitsPerPixel
#define GFX_FORMAT_BytesPerPixel(format) format->BytesPerPixel
#endif

/* ---- Function Prototypes */

#ifdef _MSC_VER
#if defined(DLL_EXPORT) && !defined(LIBSDL_GFX_DLL_IMPORT)
#define SDL_GFXPRIMITIVES_SCOPE __declspec(dllexport)
#else
#ifdef LIBSDL_GFX_DLL_IMPORT
#define SDL_GFXPRIMITIVES_SCOPE __declspec(dllimport)
#endif
#endif
#endif
#ifndef SDL_GFXPRIMITIVES_SCOPE
#define SDL_GFXPRIMITIVES_SCOPE extern
#endif

/* Note: all ___Color routines expect the color to be in format 0xRRGGBBAA */

/* Pixel */

/* Horizontal line */

SDL_GFXPRIMITIVES_SCOPE int
hlineColor(SDL_Surface *dst, Sint16 x1, Sint16 x2, Sint16 y, Uint32 color);

/* Vertical line */

SDL_GFXPRIMITIVES_SCOPE int
vlineColor(SDL_Surface *dst, Sint16 x, Sint16 y1, Sint16 y2, Uint32 color);

/* Line */

SDL_GFXPRIMITIVES_SCOPE int
lineColor(SDL_Surface *dst, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2,
          Uint32 color);

/* AA Ellipse */

SDL_GFXPRIMITIVES_SCOPE int
aaellipseColor(SDL_Surface *dst, Sint16 x, Sint16 y, Sint16 rx, Sint16 ry,
               Uint32 color);
SDL_GFXPRIMITIVES_SCOPE int
aaellipseRGBA(SDL_Surface *dst, Sint16 x, Sint16 y, Sint16 rx, Sint16 ry,
              Uint8 r, Uint8 g, Uint8 b, Uint8 a);

/* Pie */

SDL_GFXPRIMITIVES_SCOPE int
pieColor(SDL_Surface *dst, Sint16 x, Sint16 y, Sint16 rad, Sint16 start,
         Sint16 end, Uint32 color);
SDL_GFXPRIMITIVES_SCOPE int
pieRGBA(SDL_Surface *dst, Sint16 x, Sint16 y, Sint16 rad, Sint16 start,
        Sint16 end, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

/* AA-Trigon */

SDL_GFXPRIMITIVES_SCOPE int
aatrigonColor(SDL_Surface *dst, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2,
              Sint16 x3, Sint16 y3, Uint32 color);
SDL_GFXPRIMITIVES_SCOPE int
aatrigonRGBA(SDL_Surface *dst, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2,
             Sint16 x3, Sint16 y3, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

/* Filled Trigon */

SDL_GFXPRIMITIVES_SCOPE int
filledTrigonColor(SDL_Surface *dst, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2,
                  Sint16 x3, Sint16 y3, Uint32 color);
SDL_GFXPRIMITIVES_SCOPE int
filledTrigonRGBA(SDL_Surface *dst, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2,
                 Sint16 x3, Sint16 y3, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

/* Polygon */

SDL_GFXPRIMITIVES_SCOPE int
polygonColor(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n,
             Uint32 color);

/* AA-Polygon */

SDL_GFXPRIMITIVES_SCOPE int
aapolygonColor(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n,
               Uint32 color);
SDL_GFXPRIMITIVES_SCOPE int
aapolygonRGBA(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n,
              Uint8 r, Uint8 g, Uint8 b, Uint8 a);

/* Filled Polygon */

SDL_GFXPRIMITIVES_SCOPE int
filledPolygonColor(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n,
                   Uint32 color);
SDL_GFXPRIMITIVES_SCOPE int
texturedPolygon(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n,
                SDL_Surface *texture, int texture_dx, int texture_dy);

/* (Note: These MT versions are required for multi-threaded operation.) */

SDL_GFXPRIMITIVES_SCOPE int
filledPolygonColorMT(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy,
                     int n, Uint32 color, int **polyInts, int *polyAllocated);
SDL_GFXPRIMITIVES_SCOPE int
texturedPolygonMT(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n,
                  SDL_Surface *texture, int texture_dx, int texture_dy,
                  int **polyInts, int *polyAllocated);

/* Bezier */

SDL_GFXPRIMITIVES_SCOPE int
bezierColor(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n, int s,
            Uint32 color);
SDL_GFXPRIMITIVES_SCOPE int
bezierRGBA(SDL_Surface *dst, const Sint16 *vx, const Sint16 *vy, int n, int s,
           Uint8 r, Uint8 g, Uint8 b, Uint8 a);

/* Ends C function definitions when using C++ */
#ifdef __cplusplus
}
#endif

#endif /* _SDL_gfxPrimitives_h */
