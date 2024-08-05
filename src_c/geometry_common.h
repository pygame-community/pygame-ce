#ifndef PYGAME_CE_GEOMETRY_COMMON_H
#define PYGAME_CE_GEOMETRY_COMMON_H

#include "geometry.h"

int
_pg_circle_set_radius(PyObject *value, pgCircleBase *circle);

int
pgCircle_FromObject(PyObject *obj, pgCircleBase *out);

int
pgCircle_FromObjectFastcall(PyObject *const *args, Py_ssize_t nargs,
                            pgCircleBase *out);

/* === Collision Functions === */

static inline int
pgCollision_CirclePoint(pgCircleBase *circle, double Cx, double Cy)
{
    double dx = circle->x - Cx;
    double dy = circle->y - Cy;
    return dx * dx + dy * dy <= circle->r * circle->r;
}

static inline int
pgCollision_CircleCircle(pgCircleBase *A, pgCircleBase *B)
{
    double dx, dy;
    double sum_radii;

    dx = A->x - B->x;
    dy = A->y - B->y;
    sum_radii = A->r + B->r;

    return dx * dx + dy * dy <= sum_radii * sum_radii;
}

static inline int
pgCollision_RectCircle(double rx, double ry, double rw, double rh,
                       pgCircleBase *circle)
{
    const double cx = circle->x, cy = circle->y;
    const double r_bottom = ry + rh, r_right = rx + rw;

    const double test_x = (cx < rx) ? rx : ((cx > r_right) ? r_right : cx);
    const double test_y = (cy < ry) ? ry : ((cy > r_bottom) ? r_bottom : cy);

    return pgCollision_CirclePoint(circle, test_x, test_y);
}

#endif  // PYGAME_CE_GEOMETRY_COMMON_H
