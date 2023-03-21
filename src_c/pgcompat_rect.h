#ifndef PGCOMPAT_RECT_H
#define PGCOMPAT_RECT_H

#include <SDL.h>

#if !(SDL_VERSION_ATLEAST(2, 0, 10))
typedef struct SDL_FRect {
    float x, y;
    float w, h;
} SDL_FRect;
#endif /* !(SDL_VERSION_ATLEAST(2, 0, 10)) */

/* SDL 2.0.22 provides some utility functions for FRects */
#if !(SDL_VERSION_ATLEAST(2, 0, 22))

SDL_bool
SDL_IntersectFRectAndLine(SDL_FRect *rect, float *X1, float *Y1, float *X2,
                          float *Y2);
#endif /* !(SDL_VERSION_ATLEAST(2, 0, 22)) */

#define pg_PyFloat_FromFloat(x) (PyFloat_FromDouble((double)x))

#endif /* PGCOMPAT_RECT_H */
