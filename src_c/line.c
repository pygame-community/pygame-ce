#include "doc/geometry_doc.h"
#include "geometry_common.h"

static PyObject *
_pg_line_subtype_new4(PyTypeObject *type, double xa, double ya, double xb,
                      double yb)
{
    pgLineObject *line = (pgLineObject *)pgLine_Type.tp_new(type, NULL, NULL);

    if (line) {
        line->line.xa = xa;
        line->line.ya = ya;
        line->line.xb = xb;
        line->line.yb = yb;
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
pgLine_FromObject(PyObject *obj, pgLineBase *out)
{
    Py_ssize_t length;

    if (pgLine_Check(obj)) {
        *out = ((pgLineObject *)obj)->line;
        return 1;
    }
    if (pgSequenceFast_Check(obj)) {
        length = PySequence_Fast_GET_SIZE(obj);
        PyObject **farray = PySequence_Fast_ITEMS(obj);

        if (length == 4) {
            if (!pg_DoubleFromObj(farray[0], &out->xa) ||
                !pg_DoubleFromObj(farray[1], &out->ya) ||
                !pg_DoubleFromObj(farray[2], &out->xb) ||
                !pg_DoubleFromObj(farray[3], &out->yb)) {
                return 0;
            }
            return 1;
        }
        else if (length == 2) {
            if (!pg_TwoDoublesFromObj(farray[0], &out->xa, &out->ya) ||
                !pg_TwoDoublesFromObj(farray[1], &out->xb, &out->yb)) {
                PyErr_Clear();
                return 0;
            }
            return 1;
        }
        else if (length == 1) /*looks like an arg?*/ {
            if (PyUnicode_Check(farray[0]) ||
                !pgLine_FromObject(farray[0], out)) {
                return 0;
            }
            return 1;
        }
    }
    if (PySequence_Check(obj)) {
        length = PySequence_Length(obj);
        if (length == 4) {
            PyObject *tmp;
            tmp = PySequence_GetItem(obj, 0);
            if (!pg_DoubleFromObj(tmp, &out->xa)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            tmp = PySequence_GetItem(obj, 1);
            if (!pg_DoubleFromObj(tmp, &out->ya)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            tmp = PySequence_GetItem(obj, 2);
            if (!pg_DoubleFromObj(tmp, &out->xb)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            tmp = PySequence_GetItem(obj, 3);
            if (!pg_DoubleFromObj(tmp, &out->yb)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            return 1;
        }
        else if (length == 2) {
            PyObject *tmp;
            tmp = PySequence_GetItem(obj, 0);
            if (!pg_TwoDoublesFromObj(tmp, &out->xa, &out->ya)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            tmp = PySequence_GetItem(obj, 1);
            if (!pg_TwoDoublesFromObj(tmp, &out->xb, &out->yb)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            return 1;
        }
        else if (PyTuple_Check(obj) && length == 1) /*looks like an arg?*/ {
            PyObject *sub = PySequence_GetItem(obj, 0);
            if (PyUnicode_Check(sub) || !pgLine_FromObject(sub, out)) {
                Py_DECREF(sub);
                return 0;
            }
            Py_DECREF(sub);
            return 1;
        }
        else {
            return 0;
        }
    }
    if (PyObject_HasAttrString(obj, "line")) {
        PyObject *lineattr;
        lineattr = PyObject_GetAttrString(obj, "line");
        if (!lineattr) {
            PyErr_Clear();
            return 0;
        }
        if (PyCallable_Check(lineattr)) /*call if it's a method*/
        {
            PyObject *lineresult = PyObject_CallObject(lineattr, NULL);
            Py_DECREF(lineattr);
            if (!lineresult) {
                PyErr_Clear();
                return 0;
            }
            lineattr = lineresult;
        }
        Py_DECREF(lineattr);
        return pgLine_FromObject(lineattr, out);
    }
    return 0;
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
    return _pg_line_subtype_new4(Py_TYPE(self), self->line.xa, self->line.ya,
                                 self->line.xb, self->line.yb);
}

static struct PyMethodDef pg_line_methods[] = {
    {"__copy__", (PyCFunction)pg_line_copy, METH_NOARGS, DOC_LINE_COPY},
    {"copy", (PyCFunction)pg_line_copy, METH_NOARGS, DOC_LINE_COPY},
    {NULL, NULL, 0, NULL}};

static PyObject *
pg_line_repr(pgLineObject *self)
{
    PyObject *result, *xa, *ya, *xb, *yb;

    xa = PyFloat_FromDouble(self->line.xa);
    if (!xa) {
        return NULL;
    }
    ya = PyFloat_FromDouble(self->line.ya);
    if (!ya) {
        Py_DECREF(xa);
        return NULL;
    }
    xb = PyFloat_FromDouble(self->line.xb);
    if (!xb) {
        Py_DECREF(xa);
        Py_DECREF(ya);
        return NULL;
    }
    yb = PyFloat_FromDouble(self->line.yb);
    if (!yb) {
        Py_DECREF(xa);
        Py_DECREF(ya);
        Py_DECREF(xb);
        return NULL;
    }

    result =
        PyUnicode_FromFormat("<Line((%R, %R), (%R, %R))>", xa, ya, xb, yb);

    Py_DECREF(xa);
    Py_DECREF(ya);
    Py_DECREF(xb);
    Py_DECREF(yb);

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

__LINE_GETSET_NAME(xa)
__LINE_GETSET_NAME(ya)
__LINE_GETSET_NAME(xb)
__LINE_GETSET_NAME(yb)
#undef __LINE_GETSET_NAME

static PyObject *
pg_line_geta(pgLineObject *self, void *closure)
{
    return pg_tuple_couple_from_values_double(self->line.xa, self->line.ya);
}

static int
pg_line_seta(pgLineObject *self, PyObject *value, void *closure)
{
    double x, y;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (pg_TwoDoublesFromObj(value, &x, &y)) {
        self->line.xa = x;
        self->line.ya = y;
        return 0;
    }
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
    return -1;
}

static PyObject *
pg_line_getb(pgLineObject *self, void *closure)
{
    return pg_tuple_couple_from_values_double(self->line.xb, self->line.yb);
}

static int
pg_line_setb(pgLineObject *self, PyObject *value, void *closure)
{
    double x, y;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (pg_TwoDoublesFromObj(value, &x, &y)) {
        self->line.xb = x;
        self->line.yb = y;
        return 0;
    }
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
    return -1;
}

static PyGetSetDef pg_line_getsets[] = {
    {"xa", (getter)pg_line_getxa, (setter)pg_line_setxa, DOC_LINE_XA, NULL},
    {"ya", (getter)pg_line_getya, (setter)pg_line_setya, DOC_LINE_YA, NULL},
    {"xb", (getter)pg_line_getxb, (setter)pg_line_setxb, DOC_LINE_XB, NULL},
    {"yb", (getter)pg_line_getyb, (setter)pg_line_setyb, DOC_LINE_YB, NULL},
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
