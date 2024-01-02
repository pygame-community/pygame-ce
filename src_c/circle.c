#include "geometry.h"
#include "doc/geometry_doc.h"

static PyObject *
_pg_circle_subtype_new(PyTypeObject *type, pgCircleBase *circle)
{
    pgCircleObject *circle_obj =
        (pgCircleObject *)pgCircle_Type.tp_new(type, NULL, NULL);

    if (circle_obj) {
        circle_obj->circle = *circle;
    }
    return (PyObject *)circle_obj;
}

static int
_pg_circle_set_radius(PyObject *value, pgCircleBase *circle)
{
    double radius = 0;
    if (!pg_DoubleFromObj(value, &radius) || radius <= 0) {
        return 0;
    }
    circle->r = radius;

    return 1;
}

static int
pgCircle_FromObject(PyObject *obj, pgCircleBase *out)
{
    Py_ssize_t length;

    if (pgCircle_Check(obj)) {
        *out = pgCircle_AsCircle(obj);
        return 1;
    }

    /* Paths for sequences */
    if (pgSequenceFast_Check(obj)) {
        PyObject **f_arr = PySequence_Fast_ITEMS(obj);
        length = PySequence_Fast_GET_SIZE(obj);

        if (length == 3) {
            if (!pg_DoubleFromObj(f_arr[0], &out->x) ||
                !pg_DoubleFromObj(f_arr[1], &out->y) ||
                !_pg_circle_set_radius(f_arr[2], out)) {
                return 0;
            }
            return 1;
        }
        else if (length == 1) {
            if (!pgCircle_FromObject(f_arr[0], out)) {
                return 0;
            }
            return 1;
        }
        else if (length == 2) {
            if (!pg_TwoDoublesFromObj(f_arr[0], &out->x, &out->y) ||
                !_pg_circle_set_radius(f_arr[1], out)) {
                return 0;
            }
            return 1;
        }
        else {
            /* Sequences of size other than 3 or 1 are not supported
            (don't wanna support infinite sequence nesting anymore)*/
            return 0;
        }
    }
    else if (PySequence_Check(obj)) {
        PyObject *tmp = NULL;
        length = PySequence_Length(obj);
        if (length == 3) {
            /*These are to be substituted with better pg_DoubleFromSeqIndex()
             * implementations*/
            tmp = PySequence_ITEM(obj, 0);
            if (!pg_DoubleFromObj(tmp, &out->x)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);

            tmp = PySequence_ITEM(obj, 1);
            if (!pg_DoubleFromObj(tmp, &out->y)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);

            tmp = PySequence_ITEM(obj, 2);
            if (!_pg_circle_set_radius(tmp, out)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);

            return 1;
        }
        else if (length == 2) {
            tmp = PySequence_ITEM(obj, 0);
            if (!pg_TwoDoublesFromObj(tmp, &out->x, &out->y)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);

            tmp = PySequence_ITEM(obj, 1);
            if (!_pg_circle_set_radius(tmp, out)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);

            return 1;
        }
        else if (length == 1) {
            tmp = PySequence_ITEM(obj, 0);
            if (PyUnicode_Check(obj) || !pgCircle_FromObject(tmp, out)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            return 1;
        }
        else {
            /* Sequences of size other than 3 or 1 are not supported
            (don't wanna support infinite sequence nesting anymore)*/
            return 0;
        }
    }

    /* Path for objects that have a circle attribute */
    PyObject *circleattr;
    if (!(circleattr = PyObject_GetAttrString(obj, "circle"))) {
        PyErr_Clear();
        return 0;
    }

    if (PyCallable_Check(circleattr)) /*call if it's a method*/
    {
        PyObject *circleresult = PyObject_CallObject(circleattr, NULL);
        Py_DECREF(circleattr);
        if (!circleresult) {
            PyErr_Clear();
            return 0;
        }
        circleattr = circleresult;
    }

    if (!pgCircle_FromObject(circleattr, out)) {
        PyErr_Clear();
        Py_DECREF(circleattr);
        return 0;
    }

    Py_DECREF(circleattr);

    return 1;
}

static int
pgCircle_FromObjectFastcall(PyObject *const *args, Py_ssize_t nargs,
                            pgCircleBase *out)
{
    if (nargs == 1) {
        return pgCircle_FromObject(args[0], out);
    }
    else if (nargs == 2) {
        if (!pg_TwoDoublesFromObj(args[0], &out->x, &out->y) ||
            !_pg_circle_set_radius(args[1], out)) {
            return 0;
        }
        return 1;
    }
    else if (nargs == 3) {
        if (!pg_DoubleFromObj(args[0], &out->x) ||
            !pg_DoubleFromObj(args[1], &out->y) ||
            !_pg_circle_set_radius(args[2], out)) {
            return 0;
        }
        return 1;
    }
    return 0;
}

static PyObject *
pg_circle_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    pgCircleObject *self = (pgCircleObject *)type->tp_alloc(type, 0);

    if (self) {
        self->circle.x = self->circle.y = 0;
        self->circle.r = 1;
        self->weakreflist = NULL;
    }
    return (PyObject *)self;
}

static int
pg_circle_init(pgCircleObject *self, PyObject *args, PyObject *kwds)
{
    if (!pgCircle_FromObject(args, &self->circle)) {
        PyErr_SetString(
            PyExc_TypeError,
            "Arguments must be a Circle, a sequence of length 3 or 2, or an "
            "object with an attribute called 'circle'");
        return -1;
    }
    return 0;
}

static void
pg_circle_dealloc(pgCircleObject *self)
{
    if (self->weakreflist) {
        PyObject_ClearWeakRefs((PyObject *)self);
    }

    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
pg_circle_copy(pgCircleObject *self, PyObject *_null)
{
    return _pg_circle_subtype_new(Py_TYPE(self), &self->circle);
}

static PyObject *
pg_circle_repr(pgCircleObject *self)
{
    PyObject *x, *y, *r;

    x = PyFloat_FromDouble(self->circle.x);
    if (!x) {
        return NULL;
    }
    y = PyFloat_FromDouble(self->circle.y);
    if (!y) {
        Py_DECREF(x);
        return NULL;
    }
    r = PyFloat_FromDouble(self->circle.r);
    if (!r) {
        Py_DECREF(x);
        Py_DECREF(y);
        return NULL;
    }

    PyObject *result = PyUnicode_FromFormat("<Circle((%R, %R), %R)>", x, y, r);

    Py_DECREF(x);
    Py_DECREF(y);
    Py_DECREF(r);

    return result;
}

static PyObject *
pg_circle_str(pgCircleObject *self)
{
    return pg_circle_repr(self);
}

static PyObject *
pg_circle_update(pgCircleObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    if (!pgCircle_FromObjectFastcall(args, nargs, &self->circle)) {
        PyErr_SetString(
            PyExc_TypeError,
            "Circle.update requires a circle or CircleLike object");
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_circle_collidepoint(pgCircleObject *self, PyObject *const *args,
                       Py_ssize_t nargs)
{
    double px, py;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &px, &py)) {
        return RAISE(
            PyExc_TypeError,
            "Circle.collidepoint requires a point or PointLike object");
    }

    return PyBool_FromLong(pgCollision_CirclePoint(&self->circle, px, py));
}

static PyObject *
pg_circle_collidecircle(pgCircleObject *self, PyObject *const *args,
                        Py_ssize_t nargs)
{
    pgCircleBase other_circle;

    if (!pgCircle_FromObjectFastcall(args, nargs, &other_circle)) {
        return RAISE(PyExc_TypeError, "A CircleType object was expected");
    }

    return PyBool_FromLong(
        pgCollision_CircleCircle(&self->circle, &other_circle));
}

static PyObject *
pg_circle_colliderect(pgCircleObject *self, PyObject *const *args,
                      Py_ssize_t nargs)
{
    double x, y, w, h;

    if (nargs == 1) {
        SDL_FRect temp, *tmp;
        if (!(tmp = pgFRect_FromObject(args[0], &temp))) {
            return RAISE(PyExc_TypeError,
                         "Invalid rect, must be RectType or sequence of 4 "
                         "numbers");
        }
        x = (double)tmp->x;
        y = (double)tmp->y;
        w = (double)tmp->w;
        h = (double)tmp->h;
    }
    else if (nargs == 2) {
        if (!pg_TwoDoublesFromObj(args[0], &x, &y) ||
            !pg_TwoDoublesFromObj(args[1], &w, &h)) {
            return RAISE(PyExc_TypeError,
                         "Invalid rect, all 4 fields must be numeric");
        }
    }
    else if (nargs == 4) {
        if (!pg_DoubleFromObj(args[0], &x) || !pg_DoubleFromObj(args[1], &y) ||
            !pg_DoubleFromObj(args[2], &w) || !pg_DoubleFromObj(args[3], &h)) {
            return RAISE(PyExc_TypeError,
                         "Invalid rect, all 4 fields must be numeric");
        }
    }
    else {
        PyErr_Format(
            PyExc_TypeError,
            "Invalid number of arguments, expected 1, 2 or 4 (got %zd)",
            nargs);
        return NULL;
    }

    return PyBool_FromLong(pgCollision_RectCircle(x, y, w, h, &self->circle));
}

static struct PyMethodDef pg_circle_methods[] = {
    {"collidepoint", (PyCFunction)pg_circle_collidepoint, METH_FASTCALL,
     DOC_CIRCLE_COLLIDEPOINT},
    {"collidecircle", (PyCFunction)pg_circle_collidecircle, METH_FASTCALL,
     DOC_CIRCLE_COLLIDECIRCLE},
    {"colliderect", (PyCFunction)pg_circle_colliderect, METH_FASTCALL,
     DOC_CIRCLE_COLLIDERECT},
    {"update", (PyCFunction)pg_circle_update, METH_FASTCALL,
     DOC_CIRCLE_UPDATE},
    {"__copy__", (PyCFunction)pg_circle_copy, METH_NOARGS, DOC_CIRCLE_COPY},
    {"copy", (PyCFunction)pg_circle_copy, METH_NOARGS, DOC_CIRCLE_COPY},
    {NULL, NULL, 0, NULL}};

#define GETTER_SETTER(name)                                                   \
    static PyObject *pg_circle_get##name(pgCircleObject *self, void *closure) \
    {                                                                         \
        return PyFloat_FromDouble(self->circle.name);                         \
    }                                                                         \
    static int pg_circle_set##name(pgCircleObject *self, PyObject *value,     \
                                   void *closure)                             \
    {                                                                         \
        double val;                                                           \
        DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);                          \
        if (!pg_DoubleFromObj(value, &val)) {                                 \
            PyErr_Format(PyExc_TypeError, "Expected a number, got '%s'",      \
                         Py_TYPE(value)->tp_name);                            \
            return -1;                                                        \
        }                                                                     \
        self->circle.name = val;                                              \
        return 0;                                                             \
    }

GETTER_SETTER(x)
GETTER_SETTER(y)

#undef GETTER_SETTER

static PyObject *
pg_circle_getr(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(self->circle.r);
}

static int
pg_circle_setr(pgCircleObject *self, PyObject *value, void *closure)
{
    double radius;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_DoubleFromObj(value, &radius)) {
        PyErr_Format(PyExc_TypeError, "Expected a number, got '%s'",
                     Py_TYPE(value)->tp_name);
        return -1;
    }

    if (radius <= 0) {
        PyErr_SetString(PyExc_ValueError, "Radius must be positive");
        return -1;
    }

    self->circle.r = radius;

    return 0;
}

static PyObject *
pg_circle_getr_sqr(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(self->circle.r * self->circle.r);
}

static int
pg_circle_setr_sqr(pgCircleObject *self, PyObject *value, void *closure)
{
    double radius_squared;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_DoubleFromObj(value, &radius_squared)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid type for radius squared, must be numeric");
        return -1;
    }

    if (radius_squared <= 0) {
        PyErr_SetString(PyExc_ValueError,
                        "Invalid radius squared value, must be > 0");
        return -1;
    }

    self->circle.r = sqrt(radius_squared);

    return 0;
}

static PyObject *
pg_circle_getcenter(pgCircleObject *self, void *closure)
{
    return pg_tuple_couple_from_values_double(self->circle.x, self->circle.y);
}

static int
pg_circle_setcenter(pgCircleObject *self, PyObject *value, void *closure)
{
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_TwoDoublesFromObj(value, &self->circle.x, &self->circle.y)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
        return -1;
    }
    return 0;
}

static PyObject *
pg_circle_getarea(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(M_PI * self->circle.r * self->circle.r);
}

static int
pg_circle_setarea(pgCircleObject *self, PyObject *value, void *closure)
{
    double area;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_DoubleFromObj(value, &area)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid type for area, must be numeric");
        return -1;
    }

    if (area <= 0) {
        PyErr_SetString(PyExc_ValueError, "Invalid area value, must be > 0");
        return -1;
    }

    self->circle.r = sqrt(area / M_PI);

    return 0;
}

static PyObject *
pg_circle_getcircumference(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(M_TWOPI * self->circle.r);
}

static int
pg_circle_setcircumference(pgCircleObject *self, PyObject *value,
                           void *closure)
{
    double circumference;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_DoubleFromObj(value, &circumference)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid type for circumference, must be numeric");
        return -1;
    }

    if (circumference <= 0) {
        PyErr_SetString(PyExc_ValueError,
                        "Invalid circumference value, must be > 0");
        return -1;
    }

    self->circle.r = circumference / M_TWOPI;

    return 0;
}

static PyObject *
pg_circle_getdiameter(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(2 * self->circle.r);
}

static int
pg_circle_setdiameter(pgCircleObject *self, PyObject *value, void *closure)
{
    double diameter;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_DoubleFromObj(value, &diameter)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid type for diameter, must be numeric");
        return -1;
    }

    if (diameter <= 0) {
        PyErr_SetString(PyExc_ValueError,
                        "Invalid diameter value, must be > 0");
        return -1;
    }

    self->circle.r = diameter / 2;

    return 0;
}

static PyGetSetDef pg_circle_getsets[] = {
    {"x", (getter)pg_circle_getx, (setter)pg_circle_setx, DOC_CIRCLE_X, NULL},
    {"y", (getter)pg_circle_gety, (setter)pg_circle_sety, DOC_CIRCLE_Y, NULL},
    {"r", (getter)pg_circle_getr, (setter)pg_circle_setr, DOC_CIRCLE_R, NULL},
    {"radius", (getter)pg_circle_getr, (setter)pg_circle_setr, DOC_CIRCLE_R,
     NULL},
    {"r_sqr", (getter)pg_circle_getr_sqr, (setter)pg_circle_setr_sqr,
     DOC_CIRCLE_RSQR, NULL},
    {"d", (getter)pg_circle_getdiameter, (setter)pg_circle_setdiameter,
     DOC_CIRCLE_DIAMETER, NULL},
    {"diameter", (getter)pg_circle_getdiameter, (setter)pg_circle_setdiameter,
     DOC_CIRCLE_DIAMETER, NULL},
    {"center", (getter)pg_circle_getcenter, (setter)pg_circle_setcenter,
     DOC_CIRCLE_CENTER, NULL},
    {"area", (getter)pg_circle_getarea, (setter)pg_circle_setarea,
     DOC_CIRCLE_AREA, NULL},
    {"circumference", (getter)pg_circle_getcircumference,
     (setter)pg_circle_setcircumference, DOC_CIRCLE_CIRCUMFERENCE, NULL},
    {NULL, 0, NULL, NULL, NULL}};

static PyTypeObject pgCircle_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame.geometry.Circle",
    .tp_basicsize = sizeof(pgCircleObject),
    .tp_dealloc = (destructor)pg_circle_dealloc,
    .tp_repr = (reprfunc)pg_circle_repr,
    .tp_str = (reprfunc)pg_circle_str,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = DOC_CIRCLE,
    .tp_weaklistoffset = offsetof(pgCircleObject, weakreflist),
    .tp_methods = pg_circle_methods,
    .tp_getset = pg_circle_getsets,
    .tp_init = (initproc)pg_circle_init,
    .tp_new = pg_circle_new,
};
