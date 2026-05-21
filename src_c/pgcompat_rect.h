#ifndef PGCOMPAT_RECT_H
#define PGCOMPAT_RECT_H

#ifdef PG_SDL3
#include <SDL3/SDL.h>
#else
#include <SDL.h>
#endif

/* SDL 2.0.22 provides some utility functions for FRects */
/* SDL_IntersectFRectAndLine has the same -1 boundary bug for small float
 * rects, so we always use our custom implementation for SDL2. */
#if !SDL_VERSION_ATLEAST(3, 0, 0)
#if !SDL_VERSION_ATLEAST(3, 0, 0)

SDL_bool
PG_IntersectFRectAndLine(SDL_FRect *rect, float *X1, float *Y1, float *X2,
                         float *Y2);
#else
#define PG_IntersectFRectAndLine SDL_IntersectFRectAndLine
#endif /* !(SDL_VERSION_ATLEAST(2, 0, 22)) || SDL_VERSION_ATLEAST(3, 0, 0) */

#define pg_PyFloat_FromFloat(x) (PyFloat_FromDouble((double)x))

#endif /* PGCOMPAT_RECT_H */
