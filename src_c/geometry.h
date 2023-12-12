#ifndef PYGAME_CE_GEOMETRY_H
#define PYGAME_CE_GEOMETRY_H

#include "pygame.h"
#include "pgcompat.h"

typedef struct {
    double x, y, r;
} pgCircleBase;

typedef struct {
    PyObject_HEAD pgCircleBase circle;
    PyObject *weakreflist;
} pgCircleObject;

#define pgCircle_CAST(o) ((pgCircleObject *)(o))
#define pgCircle_AsCircle(o) (pgCircle_CAST(o)->circle)
#define pgCircle_GETX(self) (pgCircle_CAST(self)->circle.x)
#define pgCircle_GETY(self) (pgCircle_CAST(self)->circle.y)
#define pgCircle_GETR(self) (pgCircle_CAST(self)->circle.r)
#define pgCircle_Check(o) ((o)->ob_type == &pgCircle_Type)

static PyTypeObject pgCircle_Type;

static int
pgCircle_FromObject(PyObject *obj, pgCircleBase *out);

static int
pgCircle_FromObjectFastcall(PyObject *const *args, Py_ssize_t nargs,
                            pgCircleBase *out);
/* Constants */

/* PI */
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/* 2PI */
#ifndef M_TWOPI
#define M_TWOPI 6.28318530717958647692
#endif

#endif  // PYGAME_CE_GEOMETRY_H
