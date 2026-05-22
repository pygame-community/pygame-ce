#ifndef PGCOMPAT_RECT_H
#define PGCOMPAT_RECT_H
#ifdef PG_SDL3
#include <SDL3/SDL.h>
#else
#include <SDL.h>
#endif
/* SDL_IntersectFRectAndLine (available since SDL 2.0.22) has the same -1
 * boundary bug for float rects with small dimensions, so we always use our
 * custom implementation instead of delegating to SDL. */
SDL_bool
PG_IntersectFRectAndLine(SDL_FRect *rect, float *X1, float *Y1, float *X2,
                         float *Y2);
#define pg_PyFloat_FromFloat(x) (PyFloat_FromDouble((double)x))
#endif /* PGCOMPAT_RECT_H */
