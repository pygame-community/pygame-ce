#include "doc/geometry_doc.h"
#include "geometry_common.h"

static PyObject *
_pg_line_subtype_new4(PyTypeObject *type, double ax, double ay, double bx,
                      double by)
{
    pgLineObject *line = (pgLineObject *)pgLine_Type.tp_new(type, NULL, NULL);

    if (line) {
        line->line.ax = ax;
        line->line.ay = ay;
        line->line.bx = bx;
        line->line.by = by;
    }
    return (PyObject *)line;
}

static PyObject *
pg_line_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    pgLineObject *self = (pgLineObject *)type->tp_alloc(type, 0);

    if (self != NULL)
        memset(&self->line, 0, sizeof(pgLineBase));

    return (PyObject *)self;
}

static void
pg_line_dealloc(pgLineObject *self)
{
    if (self->weakreflist != NULL) {
        PyObject_ClearWeakRefs((PyObject *)self);
    }

    Py_TYPE(self)->tp_free((PyObject *)self);
}

static int
pg_line_init(pgLineObject *self, PyObject *args, PyObject *kwds)
{
    if (!pgLine_FromObject(args, &(self->line))) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid line end points, expected 4 "
                        "numbers or 2 sequences of 2 numbers");
        return -1;
    }
    return 0;
}

static PyObject *
pg_line_copy(pgLineObject *self, PyObject *_null)
{
    return _pg_line_subtype_new4(Py_TYPE(self), self->line.ax, self->line.ay,
                                 self->line.bx, self->line.by);
}

static struct PyMethodDef pg_line_methods[] = {
    {"__copy__", (PyCFunction)pg_line_copy, METH_NOARGS, DOC_LINE_COPY},
    {"copy", (PyCFunction)pg_line_copy, METH_NOARGS, DOC_LINE_COPY},
    {NULL, NULL, 0, NULL}};

static PyObject *
pg_line_repr(pgLineObject *self)
{
    PyObject *result, *ax, *ay, *bx, *by;

    ax = PyFloat_FromDouble(self->line.ax);
    if (!ax) {
        return NULL;
    }
    ay = PyFloat_FromDouble(self->line.ay);
    if (!ay) {
        Py_DECREF(ax);
        return NULL;
    }
    bx = PyFloat_FromDouble(self->line.bx);
    if (!bx) {
        Py_DECREF(ax);
        Py_DECREF(ay);
        return NULL;
    }
    by = PyFloat_FromDouble(self->line.by);
    if (!by) {
        Py_DECREF(ax);
        Py_DECREF(ay);
        Py_DECREF(bx);
        return NULL;
    }

    result =
        PyUnicode_FromFormat("<Line((%R, %R), (%R, %R))>", ax, ay, bx, by);

    Py_DECREF(ax);
    Py_DECREF(ay);
    Py_DECREF(bx);
    Py_DECREF(by);

    return result;
}

static PyObject *
pg_line_str(pgLineObject *self)
{
    return pg_line_repr(self);
}

#define __LINE_GETSET_NAME(name)                                          \
    static PyObject *pg_line_get##name(pgLineObject *self, void *closure) \
    {                                                                     \
        return PyFloat_FromDouble(self->line.name);                       \
    }                                                                     \
    static int pg_line_set##name(pgLineObject *self, PyObject *value,     \
                                 void *closure)                           \
    {                                                                     \
        double val;                                                       \
        DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);                      \
        if (pg_DoubleFromObj(value, &val)) {                              \
            self->line.name = val;                                        \
            return 0;                                                     \
        }                                                                 \
        PyErr_SetString(PyExc_TypeError, "Expected a number");            \
        return -1;                                                        \
    }

__LINE_GETSET_NAME(ax)
__LINE_GETSET_NAME(ay)
__LINE_GETSET_NAME(bx)
__LINE_GETSET_NAME(by)
#undef __LINE_GETSET_NAME

static PyObject *
pg_line_geta(pgLineObject *self, void *closure)
{
    return pg_tuple_couple_from_values_double(self->line.ax, self->line.ay);
}

static int
pg_line_seta(pgLineObject *self, PyObject *value, void *closure)
{
    double x, y;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (pg_TwoDoublesFromObj(value, &x, &y)) {
        self->line.ax = x;
        self->line.ay = y;
        return 0;
    }
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
    return -1;
}

static PyObject *
pg_line_getb(pgLineObject *self, void *closure)
{
    return pg_tuple_couple_from_values_double(self->line.bx, self->line.by);
}

static int
pg_line_setb(pgLineObject *self, PyObject *value, void *closure)
{
    double x, y;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (pg_TwoDoublesFromObj(value, &x, &y)) {
        self->line.bx = x;
        self->line.by = y;
        return 0;
    }
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
    return -1;
}

static PyGetSetDef pg_line_getsets[] = {
    {"ax", (getter)pg_line_getax, (setter)pg_line_setax, DOC_LINE_AX, NULL},
    {"ay", (getter)pg_line_getay, (setter)pg_line_setay, DOC_LINE_AY, NULL},
    {"bx", (getter)pg_line_getbx, (setter)pg_line_setbx, DOC_LINE_BX, NULL},
    {"by", (getter)pg_line_getby, (setter)pg_line_setby, DOC_LINE_BY, NULL},
    {"a", (getter)pg_line_geta, (setter)pg_line_seta, DOC_LINE_A, NULL},
    {"b", (getter)pg_line_getb, (setter)pg_line_setb, DOC_LINE_B, NULL},
    {NULL, 0, NULL, NULL, NULL}};

static PyTypeObject pgLine_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame.geometry.Line",
    .tp_basicsize = sizeof(pgLineObject),
    .tp_dealloc = (destructor)pg_line_dealloc,
    .tp_repr = (reprfunc)pg_line_repr,
    .tp_str = (reprfunc)pg_line_str,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = DOC_LINE,
    .tp_weaklistoffset = offsetof(pgLineObject, weakreflist),
    .tp_methods = pg_line_methods,
    .tp_getset = pg_line_getsets,
    .tp_init = (initproc)pg_line_init,
    .tp_new = pg_line_new,
};
