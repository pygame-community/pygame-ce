/*
  pygame-ce - Python Game Library
  Copyright (C) 2008 Marcus von Appen

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

*/
/*
  This is a proposed SDL_gfx draw module for Pygame. It is backported
  from Pygame 2.

  TODO:
  - do a filled pie version using filledPieColor
  - Determine if SDL video must be initiated for all routines to work.
    Add check if required, else remove ASSERT_VIDEO_INIT.
  - Example (Maybe).
*/
#define PYGAME_SDLGFXPRIM_INTERNAL

#include "pygame.h"

#include "doc/gfxdraw_doc.h"

#include "surface.h"

#include "pgcompat.h"

#include "SDL_gfx/SDL_gfxPrimitives.h"

static PyObject *
_gfx_aaellipsecolor(PyObject *self, PyObject *args);
static PyObject *
_gfx_piecolor(PyObject *self, PyObject *args);
static PyObject *
_gfx_aatrigoncolor(PyObject *self, PyObject *args);
static PyObject *
_gfx_aapolygoncolor(PyObject *self, PyObject *args);
static PyObject *
_gfx_texturedpolygon(PyObject *self, PyObject *args);
static PyObject *
_gfx_beziercolor(PyObject *self, PyObject *args);

static PyMethodDef _gfxdraw_methods[] = {
    {"aaellipse", _gfx_aaellipsecolor, METH_VARARGS, DOC_GFXDRAW_AAELLIPSE},
    {"pie", _gfx_piecolor, METH_VARARGS, DOC_GFXDRAW_PIE},
    {"aatrigon", _gfx_aatrigoncolor, METH_VARARGS, DOC_GFXDRAW_AATRIGON},
    {"aapolygon", _gfx_aapolygoncolor, METH_VARARGS, DOC_GFXDRAW_AAPOLYGON},
    {"textured_polygon", _gfx_texturedpolygon, METH_VARARGS,
     DOC_GFXDRAW_TEXTUREDPOLYGON},
    {"bezier", _gfx_beziercolor, METH_VARARGS, DOC_GFXDRAW_BEZIER},
    {NULL, NULL, 0, NULL},
};

#define ASSERT_VIDEO_INIT(unused) /* Is video really needed for gfxdraw? */

static int
Sint16FromObj(PyObject *item, Sint16 *val)
{
    if (PyNumber_Check(item)) {
        PyObject *intobj;
        long tmp;

        if (!(intobj = PyNumber_Long(item)))
            return 0;
        tmp = PyLong_AsLong(intobj);
        Py_DECREF(intobj);
        if (tmp == -1 && PyErr_Occurred())
            return 0;
        *val = (Sint16)tmp;
        return 1;
    }
    return 0;
}

static int
Sint16FromSeqIndex(PyObject *obj, Py_ssize_t _index, Sint16 *val)
{
    int result = 0;
    PyObject *item;
    item = PySequence_GetItem(obj, _index);
    if (item) {
        result = Sint16FromObj(item, val);
        Py_DECREF(item);
    }
    return result;
}

static PyObject *
_gfx_aaellipsecolor(PyObject *self, PyObject *args)
{
    PyObject *surface, *color;
    Sint16 x, y, rx, ry;
    Uint8 rgba[4];

    ASSERT_VIDEO_INIT(NULL);

    if (!PyArg_ParseTuple(args, "OhhhhO:aaellipse", &surface, &x, &y, &rx, &ry,
                          &color))
        return NULL;

    if (!pgSurface_Check(surface)) {
        return RAISE(PyExc_TypeError, "surface must be a Surface");
    }
    if (!pg_RGBAFromObjEx(color, rgba, PG_COLOR_HANDLE_SIMPLE)) {
        return NULL;
    }

    if (aaellipseRGBA(pgSurface_AsSurface(surface), x, y, rx, ry, rgba[0],
                      rgba[1], rgba[2], rgba[3]) == -1) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
_gfx_piecolor(PyObject *self, PyObject *args)
{
    PyObject *surface, *color;
    Sint16 x, y, r, start, end;
    Uint8 rgba[4];

    ASSERT_VIDEO_INIT(NULL);

    if (!PyArg_ParseTuple(args, "OhhhhhO:pie", &surface, &x, &y, &r, &start,
                          &end, &color))
        return NULL;

    if (!pgSurface_Check(surface)) {
        return RAISE(PyExc_TypeError, "surface must be a Surface");
    }
    if (!pg_RGBAFromObjEx(color, rgba, PG_COLOR_HANDLE_SIMPLE)) {
        return NULL;
    }

    if (pieRGBA(pgSurface_AsSurface(surface), x, y, r, start, end, rgba[0],
                rgba[1], rgba[2], rgba[3]) == -1) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
_gfx_aatrigoncolor(PyObject *self, PyObject *args)
{
    PyObject *surface, *color;
    Sint16 x1, x2, x3, _y1, y2, y3;
    Uint8 rgba[4];

    ASSERT_VIDEO_INIT(NULL);

    if (!PyArg_ParseTuple(args, "OhhhhhhO:aatrigon", &surface, &x1, &_y1, &x2,
                          &y2, &x3, &y3, &color))
        return NULL;

    if (!pgSurface_Check(surface)) {
        return RAISE(PyExc_TypeError, "surface must be a Surface");
    }
    if (!pg_RGBAFromObjEx(color, rgba, PG_COLOR_HANDLE_SIMPLE)) {
        return NULL;
    }

    if (aatrigonRGBA(pgSurface_AsSurface(surface), x1, _y1, x2, y2, x3, y3,
                     rgba[0], rgba[1], rgba[2], rgba[3]) == -1) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
_gfx_aapolygoncolor(PyObject *self, PyObject *args)
{
    PyObject *surface, *color, *points, *item;
    Sint16 *vx, *vy, x, y;
    Py_ssize_t count, i;
    int ret;
    Uint8 rgba[4];

    ASSERT_VIDEO_INIT(NULL);

    if (!PyArg_ParseTuple(args, "OOO:aapolygon", &surface, &points, &color))
        return NULL;

    if (!pgSurface_Check(surface)) {
        return RAISE(PyExc_TypeError, "surface must be a Surface");
    }
    if (!pg_RGBAFromObjEx(color, rgba, PG_COLOR_HANDLE_SIMPLE)) {
        return NULL;
    }
    if (!PySequence_Check(points)) {
        return RAISE(PyExc_TypeError, "points must be a sequence");
    }

    count = PySequence_Size(points);
    if (count < 3) {
        return RAISE(PyExc_ValueError,
                     "points must contain more than 2 points");
    }

    vx = PyMem_New(Sint16, (size_t)count);
    vy = PyMem_New(Sint16, (size_t)count);
    if (!vx || !vy) {
        if (vx)
            PyMem_Free(vx);
        if (vy)
            PyMem_Free(vy);
        return NULL;
    }

    for (i = 0; i < count; i++) {
        item = PySequence_ITEM(points, i);
        if (!Sint16FromSeqIndex(item, 0, &x)) {
            PyMem_Free(vx);
            PyMem_Free(vy);
            Py_XDECREF(item);
            return NULL;
        }
        if (!Sint16FromSeqIndex(item, 1, &y)) {
            PyMem_Free(vx);
            PyMem_Free(vy);
            Py_XDECREF(item);
            return NULL;
        }
        Py_DECREF(item);
        vx[i] = x;
        vy[i] = y;
    }

    Py_BEGIN_ALLOW_THREADS;
    ret = aapolygonRGBA(pgSurface_AsSurface(surface), vx, vy, (int)count,
                        rgba[0], rgba[1], rgba[2], rgba[3]);
    Py_END_ALLOW_THREADS;

    PyMem_Free(vx);
    PyMem_Free(vy);

    if (ret == -1) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
_gfx_texturedpolygon(PyObject *self, PyObject *args)
{
    PyObject *surface, *texture, *points, *item;
    SDL_Surface *s_surface, *s_texture;
    Sint16 *vx, *vy, x, y, tdx, tdy;
    Py_ssize_t count, i;
    int ret;

    ASSERT_VIDEO_INIT(NULL);

    if (!PyArg_ParseTuple(args, "OOOhh:textured_polygon", &surface, &points,
                          &texture, &tdx, &tdy))
        return NULL;

    if (!pgSurface_Check(surface)) {
        return RAISE(PyExc_TypeError, "surface must be a Surface");
    }
    s_surface = pgSurface_AsSurface(surface);
    if (!pgSurface_Check(texture)) {
        return RAISE(PyExc_TypeError, "texture must be a Surface");
    }
    s_texture = pgSurface_AsSurface(texture);
    if (!PySequence_Check(points)) {
        return RAISE(PyExc_TypeError, "points must be a sequence");
    }
    if (PG_SURF_BytesPerPixel(s_surface) == 1 &&
        (s_texture->format->Amask || s_texture->flags & SDL_SRCALPHA)) {
        return RAISE(PyExc_ValueError,
                     "Per-byte alpha texture unsupported "
                     "for 8 bit surfaces");
    }

    count = PySequence_Size(points);
    if (count < 3) {
        return RAISE(PyExc_ValueError,
                     "points must contain more than 2 points");
    }

    vx = PyMem_New(Sint16, (size_t)count);
    vy = PyMem_New(Sint16, (size_t)count);
    if (!vx || !vy) {
        if (vx)
            PyMem_Free(vx);
        if (vy)
            PyMem_Free(vy);
        return NULL;
    }

    for (i = 0; i < count; i++) {
        item = PySequence_ITEM(points, i);
        if (!Sint16FromSeqIndex(item, 0, &x)) {
            PyMem_Free(vx);
            PyMem_Free(vy);
            Py_XDECREF(item);
            return NULL;
        }
        if (!Sint16FromSeqIndex(item, 1, &y)) {
            PyMem_Free(vx);
            PyMem_Free(vy);
            Py_XDECREF(item);
            return NULL;
        }
        Py_DECREF(item);
        vx[i] = x;
        vy[i] = y;
    }

    Py_BEGIN_ALLOW_THREADS;
    ret = texturedPolygon(s_surface, vx, vy, (int)count, s_texture, tdx, tdy);
    Py_END_ALLOW_THREADS;

    PyMem_Free(vx);
    PyMem_Free(vy);

    if (ret == -1) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
_gfx_beziercolor(PyObject *self, PyObject *args)
{
    PyObject *surface, *color, *points, *item;
    Sint16 *vx, *vy, x, y;
    Py_ssize_t count, i;
    int ret, steps;
    Uint8 rgba[4];

    ASSERT_VIDEO_INIT(NULL);

    if (!PyArg_ParseTuple(args, "OOiO:bezier", &surface, &points, &steps,
                          &color))
        return NULL;

    if (!pgSurface_Check(surface)) {
        return RAISE(PyExc_TypeError, "surface must be a Surface");
    }
    if (!pg_RGBAFromObjEx(color, rgba, PG_COLOR_HANDLE_SIMPLE)) {
        return NULL;
    }
    if (!PySequence_Check(points)) {
        return RAISE(PyExc_TypeError, "points must be a sequence");
    }

    count = PySequence_Size(points);
    if (count < 3) {
        return RAISE(PyExc_ValueError,
                     "points must contain more than 2 points");
    }

    if (steps < 2) {
        return RAISE(PyExc_ValueError,
                     "steps parameter must be greater than 1");
    }

    vx = PyMem_New(Sint16, (size_t)count);
    vy = PyMem_New(Sint16, (size_t)count);
    if (!vx || !vy) {
        if (vx)
            PyMem_Free(vx);
        if (vy)
            PyMem_Free(vy);
        return RAISE(PyExc_MemoryError, "memory allocation failed");
    }

    for (i = 0; i < count; i++) {
        item = PySequence_ITEM(points, i);
        if (!Sint16FromSeqIndex(item, 0, &x)) {
            PyMem_Free(vx);
            PyMem_Free(vy);
            Py_XDECREF(item);
            return NULL;
        }
        if (!Sint16FromSeqIndex(item, 1, &y)) {
            PyMem_Free(vx);
            PyMem_Free(vy);
            Py_XDECREF(item);
            return NULL;
        }
        Py_DECREF(item);
        vx[i] = x;
        vy[i] = y;
    }

    Py_BEGIN_ALLOW_THREADS;
    ret = bezierRGBA(pgSurface_AsSurface(surface), vx, vy, (int)count, steps,
                     rgba[0], rgba[1], rgba[2], rgba[3]);
    Py_END_ALLOW_THREADS;

    PyMem_Free(vx);
    PyMem_Free(vy);

    if (ret == -1) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

MODINIT_DEFINE(_gfxdraw)
{
    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "_gfxdraw",
                                         DOC_GFXDRAW,
                                         -1,
                                         _gfxdraw_methods,
                                         NULL,
                                         NULL,
                                         NULL,
                                         NULL};

    /* import needed APIs; Do this first so if there is an error
       the module is not loaded.
    */
    import_pygame_base();
    if (PyErr_Occurred()) {
        return NULL;
    }
    import_pygame_color();
    if (PyErr_Occurred()) {
        return NULL;
    }
    import_pygame_rect();
    if (PyErr_Occurred()) {
        return NULL;
    }
    import_pygame_surface();
    if (PyErr_Occurred()) {
        return NULL;
    }

    return PyModule_Create(&_module);
}
