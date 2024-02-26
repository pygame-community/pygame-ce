#include "geometry_utils.h"

int
_pg_circle_set_radius(PyObject *value, pgCircleBase *circle)
{
    double radius = 0;
    if (!pg_DoubleFromObj(value, &radius) || radius <= 0) {
        return 0;
    }
    circle->r = radius;

    return 1;
}

int
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

int
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

/* === Collision Functions === */

inline int
pgCollision_CirclePoint(pgCircleBase *circle, double Cx, double Cy)
{
    double dx = circle->x - Cx;
    double dy = circle->y - Cy;
    return dx * dx + dy * dy <= circle->r * circle->r;
}

inline int
pgCollision_CircleCircle(pgCircleBase *A, pgCircleBase *B)
{
    double dx, dy;
    double sum_radi;

    dx = A->x - B->x;
    dy = A->y - B->y;
    sum_radi = A->r + B->r;

    return dx * dx + dy * dy <= sum_radi * sum_radi;
}

inline int
pgCollision_RectCircle(double rx, double ry, double rw, double rh,
                       pgCircleBase *circle)
{
    const double cx = circle->x, cy = circle->y;
    const double r_bottom = ry + rh, r_right = rx + rw;

    const double test_x = (cx < rx) ? rx : ((cx > r_right) ? r_right : cx);
    const double test_y = (cy < ry) ? ry : ((cy > r_bottom) ? r_bottom : cy);

    return pgCollision_CirclePoint(circle, test_x, test_y);
}
