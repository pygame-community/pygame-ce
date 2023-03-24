/*
  pygame-ce - Python Game Library
  Copyright (C) 2000-2001  Pete Shinners

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Library General Public
  License as published by the Free Software Foundation; either
  version 2 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Library General Public License for more details.

  You should have received a copy of the GNU Library General Public
  License along with this library; if not, write to the Free
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

  Pete Shinners
  pete@shinners.org
*/

/*
 *  Python Rect Object -- useful 2d rectangle class
 */
#define PYGAMEAPI_RECT_INTERNAL
#include "pygame.h"

#include "doc/rect_doc.h"

#include "structmember.h"

#include "pgcompat.h"

#include "pgcompat_rect.h"

#include <limits.h>

static PyTypeObject pgRect_Type;
static PyTypeObject pgFRect_Type;
#define pgRect_Check(x) (PyObject_IsInstance(x, (PyObject *)&pgRect_Type))
#define pgRect_CheckExact(x) (Py_TYPE(x) == &pgRect_Type)
#define pgFRect_Check(x) (PyObject_IsInstance(x, (PyObject *)&pgFRect_Type))
#define pgFRect_CheckExact(x) (Py_TYPE(x) == &pgFRect_Type)

static int
four_ints_from_obj(PyObject *obj, int *val1, int *val2, int *val3, int *val4);
static int
four_floats_from_obj(PyObject *obj, float *val1, float *val2, float *val3,
                     float *val4);

#define RectExport_init pg_rect_init
#define RectExport_subtypeNew4 _pg_rect_subtype_new4
#define RectExport_new pg_rect_new
#define RectExport_dealloc pg_rect_dealloc
#define RectExport_normalize pg_rect_normalize
#define RectExport_move pg_rect_move
#define RectExport_moveIp pg_rect_move_ip
#define RectExport_inflate pg_rect_inflate
#define RectExport_inflateIp pg_rect_inflate_ip
#define RectExport_update pg_rect_update
#define RectExport_union pg_rect_union
#define RectExport_unionIp pg_rect_union_ip
#define RectExport_unionall pg_rect_unionall
#define RectExport_unionallIp pg_rect_unionall_ip
#define RectExport_collidepoint pg_rect_collidepoint
#define RectExport_colliderect pg_rect_colliderect
#define RectExport_collidelist pg_rect_collidelist
#define RectExport_collidelistall pg_rect_collidelistall
#define RectExport_RectFromObjectAndKeyFunc pgRect_FromObjectAndKeyFunc
#define RectExport_collideobjectsall pg_rect_collideobjectsall
#define RectExport_collideobjects pg_rect_collideobjects
#define RectExport_collidedict pg_rect_collidedict
#define RectExport_collidedictall pg_rect_collidedictall
#define RectExport_clip pg_rect_clip
#define RectExport_clipline pg_rect_clipline
#define RectExport_do_rects_intresect _pg_do_rects_intersect
#define RectExport_RectFromObject pgRect_FromObject
#define RectExport_RectNew pgRect_New
#define RectExport_RectNew4 pgRect_New4
#define RectExport_Normalize pgRect_Normalize
#define RectExport_contains_internal _pg_rect_contains
#define RectExport_contains pg_rect_contains
#define RectExport_containsSeq pg_rect_contains_seq
#define RectExport_clamp pg_rect_clamp
#define RectExport_fit pg_rect_fit
#define RectExport_clampIp pg_rect_clamp_ip
#define RectExport_reduce pg_rect_reduce
#define RectExport_copy pg_rect_copy
#define RectExport_item pg_rect_item
#define RectExport_assItem pg_rect_ass_item
#define RectExport_subscript pg_rect_subscript
#define RectExport_assSubscript pg_rect_ass_subscript
#define RectExport_bool pg_rect_bool
#define RectExport_richcompare pg_rect_richcompare
#define RectExport_iterator pg_rect_iterator
#define RectExport_getwidth pg_rect_getwidth
#define RectExport_setwidth pg_rect_setwidth
#define RectExport_getheight pg_rect_getheight
#define RectExport_setheight pg_rect_setheight
#define RectExport_gettop pg_rect_gettop
#define RectExport_settop pg_rect_settop
#define RectExport_getleft pg_rect_getleft
#define RectExport_setleft pg_rect_setleft
#define RectExport_getright pg_rect_getright
#define RectExport_setright pg_rect_setright
#define RectExport_getbottom pg_rect_getbottom
#define RectExport_setbottom pg_rect_setbottom
#define RectExport_getcenterx pg_rect_getcenterx
#define RectExport_setcenterx pg_rect_setcenterx
#define RectExport_getcentery pg_rect_getcentery
#define RectExport_setcentery pg_rect_setcentery
#define RectExport_gettopleft pg_rect_gettopleft
#define RectExport_settopleft pg_rect_settopleft
#define RectExport_gettopright pg_rect_gettopright
#define RectExport_settopright pg_rect_settopright
#define RectExport_getbottomleft pg_rect_getbottomleft
#define RectExport_setbottomleft pg_rect_setbottomleft
#define RectExport_getbottomright pg_rect_getbottomright
#define RectExport_setbottomright pg_rect_setbottomright
#define RectExport_getmidtop pg_rect_getmidtop
#define RectExport_setmidtop pg_rect_setmidtop
#define RectExport_getmidleft pg_rect_getmidleft
#define RectExport_setmidleft pg_rect_setmidleft
#define RectExport_getmidbottom pg_rect_getmidbottom
#define RectExport_setmidbottom pg_rect_setmidbottom
#define RectExport_getmidright pg_rect_getmidright
#define RectExport_setmidright pg_rect_setmidright
#define RectExport_getcenter pg_rect_getcenter
#define RectExport_setcenter pg_rect_setcenter
#define RectExport_getsize pg_rect_getsize
#define RectExport_setsize pg_rect_setsize
#define RectImport_primitiveType int
#define RectImport_RectCheck pgRect_Check
#define RectImport_RectCheckExact pgRect_CheckExact
#define RectImport_innerRectStruct SDL_Rect
#define RectImport_innerPointStruct SDL_Point
#define RectImport_fourPrimiviteFromObj four_ints_from_obj
#define RectImport_primitiveFromObjIndex pg_IntFromObjIndex
#define RectImport_twoPrimitivesFromObj pg_TwoIntsFromObj
#define RectImport_PrimitiveFromObj pg_IntFromObj
#define RectImport_RectObject pgRectObject
#define RectImport_TypeObject pgRect_Type
#define RectImport_IntersectRectAndLine SDL_IntersectRectAndLine
#define RectImport_PyBuildValueFormat "i"
#define RectImport_ObjectName "pygame.rect.Rect"
#define RectImport_PythonNumberCheck PyLong_Check
#define RectImport_PythonNumberAsPrimitiveType PyLong_AsLong
#define RectImport_PrimitiveTypeAsPythonNumber PyLong_FromLong
#ifdef PYPY_VERSION
#define RectOptional_FREELIST
#define RectOptional_FreelistlimitNumberName PG_RECT_FREELIST_MAX
#define RectOptional_FreelistlimitNumber 49152
#define RectOptional_FreelistFreelistName pg_rect_freelist
#define RectOptional_Freelist_Num pg_rect_freelist_num
#endif /* PYPY_VERSION */
#include "rect_impl.h"

#define RectExport_init pg_frect_init
#define RectExport_subtypeNew4 _pg_frect_subtype_new4
#define RectExport_new pg_frect_new
#define RectExport_dealloc pg_frect_dealloc
#define RectExport_normalize pg_frect_normalize
#define RectExport_move pg_frect_move
#define RectExport_moveIp pg_frect_move_ip
#define RectExport_inflate pg_frect_inflate
#define RectExport_inflateIp pg_frect_inflate_ip
#define RectExport_update pg_frect_update
#define RectExport_union pg_frect_union
#define RectExport_unionIp pg_frect_union_ip
#define RectExport_unionall pg_frect_unionall
#define RectExport_unionallIp pg_frect_unionall_ip
#define RectExport_collidepoint pg_frect_collidepoint
#define RectExport_colliderect pg_frect_colliderect
#define RectExport_collidelist pg_frect_collidelist
#define RectExport_collidelistall pg_frect_collidelistall
#define RectExport_RectFromObjectAndKeyFunc pgFRect_FromObjectAndKeyFunc
#define RectExport_collideobjectsall pg_frect_collideobjectsall
#define RectExport_collideobjects pg_frect_collideobjects
#define RectExport_collidedict pg_frect_collidedict
#define RectExport_collidedictall pg_frect_collidedictall
#define RectExport_clip pg_frect_clip
#define RectExport_clipline pg_frect_clipline
#define RectExport_do_rects_intresect _pg_do_frects_intersect
#define RectExport_RectFromObject pgFRect_FromObject
#define RectExport_RectNew pgFRect_New
#define RectExport_RectNew4 pgFRect_New4
#define RectExport_Normalize pgFRect_Normalize
#define RectExport_contains_internal _pg_frect_contains
#define RectExport_contains pg_frect_contains
#define RectExport_containsSeq pg_frect_contains_seq
#define RectExport_clamp pg_frect_clamp
#define RectExport_fit pg_frect_fit
#define RectExport_clampIp pg_frect_clamp_ip
#define RectExport_reduce pg_frect_reduce
#define RectExport_copy pg_frect_copy
#define RectExport_item pg_frect_item
#define RectExport_assItem pg_frect_ass_item
#define RectExport_subscript pg_frect_subscript
#define RectExport_assSubscript pg_frect_ass_subscript
#define RectExport_bool pg_frect_bool
#define RectExport_richcompare pg_frect_richcompare
#define RectExport_iterator pg_frect_iterator
#define RectExport_getwidth pg_frect_getwidth
#define RectExport_setwidth pg_frect_setwidth
#define RectExport_getheight pg_frect_getheight
#define RectExport_setheight pg_frect_setheight
#define RectExport_gettop pg_frect_gettop
#define RectExport_settop pg_frect_settop
#define RectExport_getleft pg_frect_getleft
#define RectExport_setleft pg_frect_setleft
#define RectExport_getright pg_frect_getright
#define RectExport_setright pg_frect_setright
#define RectExport_getbottom pg_frect_getbottom
#define RectExport_setbottom pg_frect_setbottom
#define RectExport_getcenterx pg_frect_getcenterx
#define RectExport_setcenterx pg_frect_setcenterx
#define RectExport_getcentery pg_frect_getcentery
#define RectExport_setcentery pg_frect_setcentery
#define RectExport_gettopleft pg_frect_gettopleft
#define RectExport_settopleft pg_frect_settopleft
#define RectExport_gettopright pg_frect_gettopright
#define RectExport_settopright pg_frect_settopright
#define RectExport_getbottomleft pg_frect_getbottomleft
#define RectExport_setbottomleft pg_frect_setbottomleft
#define RectExport_getbottomright pg_frect_getbottomright
#define RectExport_setbottomright pg_frect_setbottomright
#define RectExport_getmidtop pg_frect_getmidtop
#define RectExport_setmidtop pg_frect_setmidtop
#define RectExport_getmidleft pg_frect_getmidleft
#define RectExport_setmidleft pg_frect_setmidleft
#define RectExport_getmidbottom pg_frect_getmidbottom
#define RectExport_setmidbottom pg_frect_setmidbottom
#define RectExport_getmidright pg_frect_getmidright
#define RectExport_setmidright pg_frect_setmidright
#define RectExport_getcenter pg_frect_getcenter
#define RectExport_setcenter pg_frect_setcenter
#define RectExport_getsize pg_frect_getsize
#define RectExport_setsize pg_frect_setsize
#define RectImport_primitiveType float
#define RectImport_RectCheck pgFRect_Check
#define RectImport_RectCheckExact pgFRect_CheckExact
#define RectImport_innerRectStruct SDL_FRect
#define RectImport_innerPointStruct SDL_FPoint
#define RectImport_fourPrimiviteFromObj four_floats_from_obj
#define RectImport_primitiveFromObjIndex pg_FloatFromObjIndex
#define RectImport_twoPrimitivesFromObj pg_TwoFloatsFromObj
#define RectImport_PrimitiveFromObj pg_FloatFromObj
#define RectImport_RectObject pgFRectObject
#define RectImport_IntersectRectAndLine SDL_IntersectFRectAndLine
#define RectImport_TypeObject pgFRect_Type
#define RectImport_PyBuildValueFormat "f"
#define RectImport_ObjectName "pygame.rect.FRect"
#define RectImport_PythonNumberCheck PyFloat_Check
#define RectImport_PythonNumberAsPrimitiveType PyFloat_AsDouble
#define RectImport_PrimitiveTypeAsPythonNumber pg_PyFloat_FromFloat
#ifdef PYPY_VERSION
#define RectOptional_FREELIST
#define RectOptional_FreelistlimitNumberName PG_FRECT_FREELIST_MAX
#define RectOptional_FreelistlimitNumber 49152
#define RectOptional_FreelistFreelistName pg_frect_freelist
#define RectOptional_Freelist_Num pg_frect_freelist_num
#endif /* PYPY_VERSION */
#include "rect_impl.h"

/* Helper method to extract 4 ints from an object.
 *
 * This sequence extraction supports the following formats:
 *     - 4 ints
 *     - 2 tuples/lists of 2 ints each
 *
 * Params:
 *     obj: sequence object to extract the 4 ints from
 *     val1 .. val4: extracted int values
 *
 * Returns:
 *     int: 0 to indicate failure (exception set)
 *          1 to indicate success
 *
 * Assumptions:
 *     - obj argument is a sequence
 *     - all val arguments are valid pointers
 */
static int
four_ints_from_obj(PyObject *obj, int *val1, int *val2, int *val3, int *val4)
{
    Py_ssize_t length = PySequence_Length(obj);

    if (length < -1) {
        return 0; /* Exception already set. */
    }

    if (length == 2) {
        /* Get one end of the line. */
        PyObject *item = PySequence_GetItem(obj, 0);
        int result;

        if (item == NULL) {
            return 0; /* Exception already set. */
        }

        result = pg_TwoIntsFromObj(item, val1, val2);
        Py_DECREF(item);

        if (!result) {
            PyErr_SetString(PyExc_TypeError,
                            "number pair expected for first argument");
            return 0;
        }

        /* Get the other end of the line. */
        item = PySequence_GetItem(obj, 1);

        if (item == NULL) {
            return 0; /* Exception already set. */
        }

        result = pg_TwoIntsFromObj(item, val3, val4);
        Py_DECREF(item);

        if (!result) {
            PyErr_SetString(PyExc_TypeError,
                            "number pair expected for second argument");
            return 0;
        }
    }
    else if (length == 4) {
        if (!pg_IntFromObjIndex(obj, 0, val1)) {
            PyErr_SetString(PyExc_TypeError,
                            "number expected for first argument");
            return 0;
        }

        if (!pg_IntFromObjIndex(obj, 1, val2)) {
            PyErr_SetString(PyExc_TypeError,
                            "number expected for second argument");
            return 0;
        }

        if (!pg_IntFromObjIndex(obj, 2, val3)) {
            PyErr_SetString(PyExc_TypeError,
                            "number expected for third argument");
            return 0;
        }

        if (!pg_IntFromObjIndex(obj, 3, val4)) {
            PyErr_SetString(PyExc_TypeError,
                            "number expected for fourth argument");
            return 0;
        }
    }
    else {
        PyErr_Format(PyExc_TypeError,
                     "sequence argument takes 2 or 4 items (%ld given)",
                     length);
        return 0;
    }

    return 1;
}

static int
four_floats_from_obj(PyObject *obj, float *val1, float *val2, float *val3,
                     float *val4)
{
    Py_ssize_t length = PySequence_Length(obj);

    if (length < -1) {
        return 0; /* Exception already set. */
    }

    if (length == 2) {
        /* Get one end of the line. */
        PyObject *item = PySequence_GetItem(obj, 0);
        int result;

        if (item == NULL) {
            return 0; /* Exception already set. */
        }

        result = pg_TwoFloatsFromObj(item, val1, val2);
        Py_DECREF(item);

        if (!result) {
            PyErr_SetString(PyExc_TypeError,
                            "number pair expected for first argument");
            return 0;
        }

        /* Get the other end of the line. */
        item = PySequence_GetItem(obj, 1);

        if (item == NULL) {
            return 0; /* Exception already set. */
        }

        result = pg_TwoFloatsFromObj(item, val3, val4);
        Py_DECREF(item);

        if (!result) {
            PyErr_SetString(PyExc_TypeError,
                            "number pair expected for second argument");
            return 0;
        }
    }
    else if (length == 4) {
        if (!pg_FloatFromObjIndex(obj, 0, val1)) {
            PyErr_SetString(PyExc_TypeError,
                            "number expected for first argument");
            return 0;
        }

        if (!pg_FloatFromObjIndex(obj, 1, val2)) {
            PyErr_SetString(PyExc_TypeError,
                            "number expected for second argument");
            return 0;
        }

        if (!pg_FloatFromObjIndex(obj, 2, val3)) {
            PyErr_SetString(PyExc_TypeError,
                            "number expected for third argument");
            return 0;
        }

        if (!pg_FloatFromObjIndex(obj, 3, val4)) {
            PyErr_SetString(PyExc_TypeError,
                            "number expected for fourth argument");
            return 0;
        }
    }
    else {
        PyErr_Format(PyExc_TypeError,
                     "sequence argument takes 2 or 4 items (%ld given)",
                     length);
        return 0;
    }

    return 1;
}

static struct PyMethodDef pg_rect_methods[] = {
    {"normalize", (PyCFunction)pg_rect_normalize, METH_NOARGS,
     DOC_RECT_NORMALIZE},
    {"clip", (PyCFunction)pg_rect_clip, METH_VARARGS, DOC_RECT_CLIP},
    {"clipline", (PyCFunction)pg_rect_clipline, METH_VARARGS,
     DOC_RECT_CLIPLINE},
    {"clamp", (PyCFunction)pg_rect_clamp, METH_VARARGS, DOC_RECT_CLAMP},
    {"clamp_ip", (PyCFunction)pg_rect_clamp_ip, METH_VARARGS,
     DOC_RECT_CLAMPIP},
    {"copy", (PyCFunction)pg_rect_copy, METH_NOARGS, DOC_RECT_COPY},
    {"fit", (PyCFunction)pg_rect_fit, METH_VARARGS, DOC_RECT_FIT},
    {"move", (PyCFunction)pg_rect_move, METH_VARARGS, DOC_RECT_MOVE},
    {"update", (PyCFunction)pg_rect_update, METH_VARARGS, DOC_RECT_UPDATE},
    {"inflate", (PyCFunction)pg_rect_inflate, METH_VARARGS, DOC_RECT_INFLATE},
    {"union", (PyCFunction)pg_rect_union, METH_VARARGS, DOC_RECT_UNION},
    {"unionall", (PyCFunction)pg_rect_unionall, METH_VARARGS,
     DOC_RECT_UNIONALL},
    {"move_ip", (PyCFunction)pg_rect_move_ip, METH_VARARGS, DOC_RECT_MOVEIP},
    {"inflate_ip", (PyCFunction)pg_rect_inflate_ip, METH_VARARGS,
     DOC_RECT_INFLATEIP},
    {"union_ip", (PyCFunction)pg_rect_union_ip, METH_VARARGS,
     DOC_RECT_UNIONIP},
    {"unionall_ip", (PyCFunction)pg_rect_unionall_ip, METH_VARARGS,
     DOC_RECT_UNIONALLIP},
    {"collidepoint", (PyCFunction)pg_rect_collidepoint, METH_FASTCALL,
     DOC_RECT_COLLIDEPOINT},
    {"colliderect", (PyCFunction)pg_rect_colliderect, METH_FASTCALL,
     DOC_RECT_COLLIDERECT},
    {"collidelist", (PyCFunction)pg_rect_collidelist, METH_O,
     DOC_RECT_COLLIDELIST},
    {"collidelistall", (PyCFunction)pg_rect_collidelistall, METH_O,
     DOC_RECT_COLLIDELISTALL},
    {"collidedict", (PyCFunction)pg_rect_collidedict, METH_VARARGS,
     DOC_RECT_COLLIDEDICT},
    {"collidedictall", (PyCFunction)pg_rect_collidedictall, METH_VARARGS,
     DOC_RECT_COLLIDEDICTALL},
    {"collideobjectsall", (PyCFunction)pg_rect_collideobjectsall,
     METH_VARARGS | METH_KEYWORDS, DOC_RECT_COLLIDEOBJECTSALL},
    {"collideobjects", (PyCFunction)pg_rect_collideobjects,
     METH_VARARGS | METH_KEYWORDS, DOC_RECT_COLLIDEOBJECTS},
    {"contains", (PyCFunction)pg_rect_contains, METH_VARARGS,
     DOC_RECT_CONTAINS},
    {"__reduce__", (PyCFunction)pg_rect_reduce, METH_NOARGS, NULL},
    {"__copy__", (PyCFunction)pg_rect_copy, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}};

static struct PyMethodDef pg_frect_methods[] = {
    {"normalize", (PyCFunction)pg_frect_normalize, METH_NOARGS,
     DOC_RECT_NORMALIZE},
    {"clip", (PyCFunction)pg_frect_clip, METH_VARARGS, DOC_RECT_CLIP},
    {"clipline", (PyCFunction)pg_frect_clipline, METH_VARARGS,
     DOC_RECT_CLIPLINE},
    {"clamp", (PyCFunction)pg_frect_clamp, METH_VARARGS, DOC_RECT_CLAMP},
    {"clamp_ip", (PyCFunction)pg_frect_clamp_ip, METH_VARARGS,
     DOC_RECT_CLAMPIP},
    {"copy", (PyCFunction)pg_frect_copy, METH_NOARGS, DOC_RECT_COPY},
    {"fit", (PyCFunction)pg_frect_fit, METH_VARARGS, DOC_RECT_FIT},
    {"move", (PyCFunction)pg_frect_move, METH_VARARGS, DOC_RECT_MOVE},
    {"update", (PyCFunction)pg_frect_update, METH_VARARGS, DOC_RECT_UPDATE},
    {"inflate", (PyCFunction)pg_frect_inflate, METH_VARARGS, DOC_RECT_INFLATE},
    {"union", (PyCFunction)pg_frect_union, METH_VARARGS, DOC_RECT_UNION},
    {"unionall", (PyCFunction)pg_frect_unionall, METH_VARARGS,
     DOC_RECT_UNIONALL},
    {"move_ip", (PyCFunction)pg_frect_move_ip, METH_VARARGS, DOC_RECT_MOVEIP},
    {"inflate_ip", (PyCFunction)pg_frect_inflate_ip, METH_VARARGS,
     DOC_RECT_INFLATEIP},
    {"union_ip", (PyCFunction)pg_frect_union_ip, METH_VARARGS,
     DOC_RECT_UNIONIP},
    {"unionall_ip", (PyCFunction)pg_frect_unionall_ip, METH_VARARGS,
     DOC_RECT_UNIONALLIP},
    {"collidepoint", (PyCFunction)pg_frect_collidepoint, METH_FASTCALL,
     DOC_RECT_COLLIDEPOINT},
    {"colliderect", (PyCFunction)pg_frect_colliderect, METH_FASTCALL,
     DOC_RECT_COLLIDERECT},
    {"collidelist", (PyCFunction)pg_frect_collidelist, METH_O,
     DOC_RECT_COLLIDELIST},
    {"collidelistall", (PyCFunction)pg_frect_collidelistall, METH_O,
     DOC_RECT_COLLIDELISTALL},
    {"collidedict", (PyCFunction)pg_frect_collidedict, METH_VARARGS,
     DOC_RECT_COLLIDEDICT},
    {"collidedictall", (PyCFunction)pg_frect_collidedictall, METH_VARARGS,
     DOC_RECT_COLLIDEDICTALL},
    {"collideobjectsall", (PyCFunction)pg_frect_collideobjectsall,
     METH_VARARGS | METH_KEYWORDS, DOC_RECT_COLLIDEOBJECTSALL},
    {"collideobjects", (PyCFunction)pg_frect_collideobjects,
     METH_VARARGS | METH_KEYWORDS, DOC_RECT_COLLIDEOBJECTS},
    {"contains", (PyCFunction)pg_frect_contains, METH_VARARGS,
     DOC_RECT_CONTAINS},
    {"__reduce__", (PyCFunction)pg_frect_reduce, METH_NOARGS, NULL},
    {"__copy__", (PyCFunction)pg_frect_copy, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}};

/* sequence functions */

/* common method for both objects */
static Py_ssize_t
pg_rect_length(PyObject *_self)
{
    return 4;
}

static PySequenceMethods pg_rect_as_sequence = {
    .sq_length = pg_rect_length,
    .sq_item = (ssizeargfunc)pg_rect_item,
    .sq_ass_item = (ssizeobjargproc)pg_rect_ass_item,
    .sq_contains = (objobjproc)pg_rect_contains_seq,
};

static PySequenceMethods pg_frect_as_sequence = {
    .sq_length = pg_rect_length,
    .sq_item = (ssizeargfunc)pg_frect_item,
    .sq_ass_item = (ssizeobjargproc)pg_frect_ass_item,
    .sq_contains = (objobjproc)pg_frect_contains_seq,
};

static PyMappingMethods pg_rect_as_mapping = {
    .mp_length = (lenfunc)pg_rect_length,
    .mp_subscript = (binaryfunc)pg_rect_subscript,
    .mp_ass_subscript = (objobjargproc)pg_rect_ass_subscript,
};

static PyMappingMethods pg_frect_as_mapping = {
    .mp_length = (lenfunc)pg_rect_length,
    .mp_subscript = (binaryfunc)pg_frect_subscript,
    .mp_ass_subscript = (objobjargproc)pg_frect_ass_subscript,
};

static PyNumberMethods pg_rect_as_number = {
    .nb_bool = (inquiry)pg_rect_bool,
};

static PyNumberMethods pg_frect_as_number = {
    .nb_bool = (inquiry)pg_frect_bool,
};

/* the functions below are just not worth putting in teh template system (-_-)
 */
static PyObject *
pg_rect_repr(pgRectObject *self)
{
    return PyUnicode_FromFormat("Rect(%d, %d, %d, %d)", self->r.x, self->r.y,
                                self->r.w, self->r.h);
}

static PyObject *
pg_frect_repr(pgFRectObject *self)
{
    char str[64];

    int ret = PyOS_snprintf(str, 64, "FRect(%f, %f, %f, %f)", self->r.x,
                            self->r.y, self->r.w, self->r.h);
    if (ret < 0 || ret >= 64) {
        return RAISE(PyExc_RuntimeError,
                     "Internal PyOS_snprintf call failed!");
    }

    return PyUnicode_FromString(str);
}

static PyObject *
pg_rect_str(pgRectObject *self)
{
    return pg_rect_repr(self);
}

static PyObject *
pg_frect_str(pgFRectObject *self)
{
    return pg_frect_repr(self);
}

/* True for both types of rects */
static PyObject *
pg_rect_getsafepickle(pgRectObject *self, void *closure)
{
    Py_RETURN_TRUE;
}

static PyGetSetDef pg_frect_getsets[] = {
    {"x", (getter)pg_frect_getleft, (setter)pg_frect_setleft, NULL, NULL},
    {"y", (getter)pg_frect_gettop, (setter)pg_frect_settop, NULL, NULL},
    {"w", (getter)pg_frect_getwidth, (setter)pg_frect_setwidth, NULL, NULL},
    {"h", (getter)pg_frect_getheight, (setter)pg_frect_setheight, NULL, NULL},
    {"width", (getter)pg_frect_getwidth, (setter)pg_frect_setwidth, NULL,
     NULL},
    {"height", (getter)pg_frect_getheight, (setter)pg_frect_setheight, NULL,
     NULL},
    {"top", (getter)pg_frect_gettop, (setter)pg_frect_settop, NULL, NULL},
    {"left", (getter)pg_frect_getleft, (setter)pg_frect_setleft, NULL, NULL},
    {"bottom", (getter)pg_frect_getbottom, (setter)pg_frect_setbottom, NULL,
     NULL},
    {"right", (getter)pg_frect_getright, (setter)pg_frect_setright, NULL,
     NULL},
    {"centerx", (getter)pg_frect_getcenterx, (setter)pg_frect_setcenterx, NULL,
     NULL},
    {"centery", (getter)pg_frect_getcentery, (setter)pg_frect_setcentery, NULL,
     NULL},
    {"topleft", (getter)pg_frect_gettopleft, (setter)pg_frect_settopleft, NULL,
     NULL},
    {"topright", (getter)pg_frect_gettopright, (setter)pg_frect_settopright,
     NULL, NULL},
    {"bottomleft", (getter)pg_frect_getbottomleft,
     (setter)pg_frect_setbottomleft, NULL, NULL},
    {"bottomright", (getter)pg_frect_getbottomright,
     (setter)pg_frect_setbottomright, NULL, NULL},
    {"midtop", (getter)pg_frect_getmidtop, (setter)pg_frect_setmidtop, NULL,
     NULL},
    {"midleft", (getter)pg_frect_getmidleft, (setter)pg_frect_setmidleft, NULL,
     NULL},
    {"midbottom", (getter)pg_frect_getmidbottom, (setter)pg_frect_setmidbottom,
     NULL, NULL},
    {"midright", (getter)pg_frect_getmidright, (setter)pg_frect_setmidright,
     NULL, NULL},
    {"size", (getter)pg_frect_getsize, (setter)pg_frect_setsize, NULL, NULL},
    {"center", (getter)pg_frect_getcenter, (setter)pg_frect_setcenter, NULL,
     NULL},

    {"__safe_for_unpickling__", (getter)pg_rect_getsafepickle, NULL, NULL,
     NULL},
    {NULL, 0, NULL, NULL, NULL} /* Sentinel */
};

static PyGetSetDef pg_rect_getsets[] = {
    {"x", (getter)pg_rect_getleft, (setter)pg_rect_setleft, NULL, NULL},
    {"y", (getter)pg_rect_gettop, (setter)pg_rect_settop, NULL, NULL},
    {"w", (getter)pg_rect_getwidth, (setter)pg_rect_setwidth, NULL, NULL},
    {"h", (getter)pg_rect_getheight, (setter)pg_rect_setheight, NULL, NULL},
    {"width", (getter)pg_rect_getwidth, (setter)pg_rect_setwidth, NULL, NULL},
    {"height", (getter)pg_rect_getheight, (setter)pg_rect_setheight, NULL,
     NULL},
    {"top", (getter)pg_rect_gettop, (setter)pg_rect_settop, NULL, NULL},
    {"left", (getter)pg_rect_getleft, (setter)pg_rect_setleft, NULL, NULL},
    {"bottom", (getter)pg_rect_getbottom, (setter)pg_rect_setbottom, NULL,
     NULL},
    {"right", (getter)pg_rect_getright, (setter)pg_rect_setright, NULL, NULL},
    {"centerx", (getter)pg_rect_getcenterx, (setter)pg_rect_setcenterx, NULL,
     NULL},
    {"centery", (getter)pg_rect_getcentery, (setter)pg_rect_setcentery, NULL,
     NULL},
    {"topleft", (getter)pg_rect_gettopleft, (setter)pg_rect_settopleft, NULL,
     NULL},
    {"topright", (getter)pg_rect_gettopright, (setter)pg_rect_settopright,
     NULL, NULL},
    {"bottomleft", (getter)pg_rect_getbottomleft,
     (setter)pg_rect_setbottomleft, NULL, NULL},
    {"bottomright", (getter)pg_rect_getbottomright,
     (setter)pg_rect_setbottomright, NULL, NULL},
    {"midtop", (getter)pg_rect_getmidtop, (setter)pg_rect_setmidtop, NULL,
     NULL},
    {"midleft", (getter)pg_rect_getmidleft, (setter)pg_rect_setmidleft, NULL,
     NULL},
    {"midbottom", (getter)pg_rect_getmidbottom, (setter)pg_rect_setmidbottom,
     NULL, NULL},
    {"midright", (getter)pg_rect_getmidright, (setter)pg_rect_setmidright,
     NULL, NULL},
    {"size", (getter)pg_rect_getsize, (setter)pg_rect_setsize, NULL, NULL},
    {"center", (getter)pg_rect_getcenter, (setter)pg_rect_setcenter, NULL,
     NULL},

    {"__safe_for_unpickling__", (getter)pg_rect_getsafepickle, NULL, NULL,
     NULL},
    {NULL, 0, NULL, NULL, NULL} /* Sentinel */
};

static PyTypeObject pgRect_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame.rect.Rect",
    .tp_basicsize = sizeof(pgRectObject),
    .tp_dealloc = (destructor)pg_rect_dealloc,
    .tp_repr = (reprfunc)pg_rect_repr, .tp_as_number = &pg_rect_as_number,
    .tp_as_sequence = &pg_rect_as_sequence,
    .tp_as_mapping = &pg_rect_as_mapping, .tp_str = (reprfunc)pg_rect_str,
    /* Space for future expansion */
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, .tp_doc = DOC_RECT,
    .tp_richcompare = (richcmpfunc)pg_rect_richcompare,
    .tp_weaklistoffset = offsetof(pgRectObject, weakreflist),
    .tp_iter = (getiterfunc)pg_rect_iterator, .tp_methods = pg_rect_methods,
    .tp_getset = pg_rect_getsets, .tp_init = (initproc)pg_rect_init,
    .tp_new = pg_rect_new};

// FRECT_TYPE
static PyTypeObject pgFRect_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame.rect.FRect",
    .tp_basicsize = sizeof(pgFRectObject), .tp_itemsize = 0,
    /* methods */
    .tp_dealloc = (destructor)pg_frect_dealloc,
    .tp_repr = (reprfunc)pg_frect_repr, .tp_as_number = &pg_frect_as_number,
    .tp_as_sequence = &pg_frect_as_sequence,
    .tp_as_mapping = &pg_frect_as_mapping, .tp_str = (reprfunc)pg_frect_str,
    /* Space for future expansion */
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, .tp_doc = DOC_RECT,
    .tp_richcompare = (richcmpfunc)pg_frect_richcompare,
    .tp_weaklistoffset = offsetof(pgFRectObject, weakreflist),
    .tp_iter = (getiterfunc)pg_frect_iterator, .tp_methods = pg_frect_methods,
    .tp_getset = pg_frect_getsets, .tp_init = (initproc)pg_frect_init,
    .tp_new = pg_frect_new};

static PyMethodDef _pg_module_methods[] = {{NULL, NULL, 0, NULL}};

static char _pg_module_doc[] = "Module for the rectangle object\n";

MODINIT_DEFINE(rect)
{
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_RECT_NUMSLOTS];

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "rect",
                                         _pg_module_doc,
                                         -1,
                                         _pg_module_methods,
                                         NULL,
                                         NULL,
                                         NULL,
                                         NULL};

    /* import needed apis; Do this first so if there is an error
       the module is not loaded.
    */
    import_pygame_base();
    if (PyErr_Occurred()) {
        return NULL;
    }

    /* Create the module and add the functions */
    if (PyType_Ready(&pgRect_Type) < 0 || PyType_Ready(&pgFRect_Type) < 0) {
        return NULL;
    }

    module = PyModule_Create(&_module);
    if (module == NULL) {
        return NULL;
    }

    Py_INCREF(&pgRect_Type);
    if (PyModule_AddObject(module, "RectType", (PyObject *)&pgRect_Type)) {
        Py_DECREF(&pgRect_Type);
        Py_DECREF(module);
        return NULL;
    }
    Py_INCREF(&pgRect_Type);
    if (PyModule_AddObject(module, "Rect", (PyObject *)&pgRect_Type)) {
        Py_DECREF(&pgRect_Type);
        Py_DECREF(module);
        return NULL;
    }
    Py_INCREF(&pgFRect_Type);
    if (PyModule_AddObject(module, "FRectType", (PyObject *)&pgFRect_Type)) {
        Py_DECREF(&pgFRect_Type);
        Py_DECREF(module);
        return NULL;
    }
    Py_INCREF(&pgFRect_Type);
    if (PyModule_AddObject(module, "FRect", (PyObject *)&pgFRect_Type)) {
        Py_DECREF(&pgFRect_Type);
        Py_DECREF(module);
        return NULL;
    }

    /* export the c api */
    c_api[0] = &pgRect_Type;
    c_api[1] = pgRect_New;
    c_api[2] = pgRect_New4;
    c_api[3] = pgRect_FromObject;
    c_api[4] = pgRect_Normalize;
    c_api[5] = &pgFRect_Type;
    c_api[6] = pgFRect_New;
    c_api[7] = pgFRect_New4;
    c_api[8] = pgFRect_FromObject;
    c_api[9] = pgFRect_Normalize;
    apiobj = encapsulate_api(c_api, "rect");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }
    return module;
}
