/*
  pygame-ce - Python Game Library
  Copyright (C) 2000-2001  Pete Shinners
  Copyright (C) 2006 Rene Dudfield

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
 *  extended image module for pygame, note this only has
 *  the extended load and save functions, which are automatically used
 *  by the normal pygame.image module if it is available.
 */
#include "pygame.h"

/* Keep a stray macro from conflicting with python.h */
#if defined(HAVE_PROTOTYPES)
#undef HAVE_PROTOTYPES
#endif
/* Remove GCC macro redefine warnings. */
#if defined(HAVE_STDDEF_H) /* also defined in pygame.h (python.h) */
#undef HAVE_STDDEF_H
#endif
#if defined(HAVE_STDLIB_H) /* also defined in pygame.h (SDL.h) */
#undef HAVE_STDLIB_H
#endif

#include "pgcompat.h"

#include "doc/image_doc.h"

#include "pgopengl.h"

#include <SDL_image.h>
#ifdef WIN32
#define strcasecmp _stricmp
#else
#include <strings.h>
#endif
#include <string.h>

#define JPEG_QUALITY 85

/*
#ifdef WITH_THREAD
static SDL_mutex *_pg_img_mutex = 0;
#endif
*/

static char *
iext_find_extension(char *fullname)
{
    char *dot;

    if (fullname == NULL) {
        return NULL;
    }

    dot = strrchr(fullname, '.');
    if (dot == NULL) {
        return fullname;
    }
    return dot + 1;
}

static PyObject *
image_load_ext(PyObject *self, PyObject *arg, PyObject *kwarg)
{
    PyObject *obj;
    PyObject *final;
    char *name = NULL, *ext = NULL, *type = NULL;
    SDL_Surface *surf;
    SDL_RWops *rw = NULL;
    static char *kwds[] = {"file", "namehint", NULL};

    if (!PyArg_ParseTupleAndKeywords(arg, kwarg, "O|s", kwds, &obj, &name)) {
        return NULL;
    }

    rw = pgRWops_FromObject(obj, &ext);
    if (rw == NULL) /* stop on NULL, error already set */
        return NULL;

    if (name) { /* override extension with namehint if given */
        type = iext_find_extension(name);
    }
    else { /* Otherwise type should be whatever ext is, even if ext is NULL */
        type = ext;
    }

#ifdef WITH_THREAD
    /*
    if (ext)
        lock_mutex = !strcasecmp(ext, "gif");
    */
    Py_BEGIN_ALLOW_THREADS;

    /* using multiple threads does not work for (at least) SDL_image
     * <= 2.0.4
    SDL_LockMutex(_pg_img_mutex);
    surf = IMG_LoadTyped_RW(rw, 1, ext);
    SDL_UnlockMutex(_pg_img_mutex);
    */

    surf = IMG_LoadTyped_RW(rw, 1, type);
    Py_END_ALLOW_THREADS;
#else  /* ~WITH_THREAD */
    surf = IMG_LoadTyped_RW(rw, 1, type);
#endif /* ~WITH_THREAD */

    if (ext) {
        free(ext);
    }

    if (surf == NULL)
        return RAISE(pgExc_SDLError, IMG_GetError());

    final = (PyObject *)pgSurface_New(surf);
    if (final == NULL) {
        SDL_FreeSurface(surf);
    }
    return final;
}

static PyObject *
imageext_load_sized_svg(PyObject *self, PyObject *arg, PyObject *kwargs)
{
#if SDL_IMAGE_VERSION_ATLEAST(2, 6, 0)
    PyObject *obj, *size, *final;
    SDL_Surface *surf;
    SDL_RWops *rw = NULL;
    int width, height;
    static char *kwds[] = {"file", "size", NULL};

    if (!PyArg_ParseTupleAndKeywords(arg, kwargs, "OO", kwds, &obj, &size)) {
        return NULL;
    }

    if (!pg_TwoIntsFromObj(size, &width, &height)) {
        return RAISE(PyExc_TypeError, "size must be two numbers");
    }

    if (width <= 0 || height <= 0) {
        return RAISE(PyExc_ValueError,
                     "both components of size must be be positive");
    }

    rw = pgRWops_FromObject(obj, NULL);
    if (rw == NULL) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS;
    surf = IMG_LoadSizedSVG_RW(rw, width, height);
    SDL_RWclose(rw);
    Py_END_ALLOW_THREADS;
    if (surf == NULL) {
        return RAISE(pgExc_SDLError, IMG_GetError());
    }
    final = (PyObject *)pgSurface_New(surf);
    if (final == NULL) {
        SDL_FreeSurface(surf);
    }
    return final;
#else  /* ~SDL_IMAGE_VERSION_ATLEAST(2, 6, 0) */
    return RAISE(
        pgExc_SDLError,
        "pygame must be compiled with SDL_image 2.6.0+ to use this function");
#endif /* ~SDL_IMAGE_VERSION_ATLEAST(2, 6, 0) */
}

static PyObject *
image_save_ext(PyObject *self, PyObject *arg, PyObject *kwarg)
{
    pgSurfaceObject *surfobj;
    PyObject *obj;
    char *namehint = NULL;
    PyObject *oencoded = NULL;
    SDL_Surface *surf;
    int result = 1;
    char *name = NULL;
    SDL_RWops *rw = NULL;
    static char *kwds[] = {"surface", "file", "namehint", NULL};

    if (!PyArg_ParseTupleAndKeywords(arg, kwarg, "O!O|s", kwds,
                                     &pgSurface_Type, &surfobj, &obj,
                                     &namehint)) {
        return NULL;
    }

    surf = pgSurface_AsSurface(surfobj);
    pgSurface_Prep(surfobj);

    oencoded = pg_EncodeString(obj, "UTF-8", NULL, pgExc_SDLError);
    if (oencoded == NULL) {
        result = -2;
    }
    else if (oencoded == Py_None) {
        rw = pgRWops_FromFileObject(obj);
        if (rw == NULL) {
            PyErr_Format(PyExc_TypeError,
                         "Expected a string or file object for the file "
                         "argument: got %.1024s",
                         Py_TYPE(obj)->tp_name);
            result = -2;
        }
        else {
            name = namehint;
        }
    }
    else {
        name = PyBytes_AS_STRING(oencoded);
    }

    if (result > 0) {
        char *ext = iext_find_extension(name);
        if (!strcasecmp(ext, "jpeg") || !strcasecmp(ext, "jpg")) {
            if (rw != NULL) {
                result = IMG_SaveJPG_RW(surf, rw, 0, JPEG_QUALITY);
            }
            else {
                result = IMG_SaveJPG(surf, name, JPEG_QUALITY);
            }
        }
        else if (!strcasecmp(ext, "png")) {
            /*Py_BEGIN_ALLOW_THREADS; */
            if (rw != NULL) {
                result = IMG_SavePNG_RW(surf, rw, 0);
            }
            else {
                result = IMG_SavePNG(surf, name);
            }
            /*Py_END_ALLOW_THREADS; */
        }
    }

    pgSurface_Unprep(surfobj);

    Py_XDECREF(oencoded);
    if (result == -2) {
        /* Python error raised elsewhere */
        return NULL;
    }
    if (result == -1) {
        /* SDL error: translate to Python error */
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    if (result == 1) {
        return RAISE(pgExc_SDLError, "Unrecognized image type");
    }

    Py_RETURN_NONE;
}

static PyObject *
imageext_get_sdl_image_version(PyObject *self, PyObject *args,
                               PyObject *kwargs)
{
    int linked = 1;

    static char *keywords[] = {"linked", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|p", keywords, &linked)) {
        return NULL;
    }

    if (linked) {
        const SDL_version *v = IMG_Linked_Version();
        return Py_BuildValue("iii", v->major, v->minor, v->patch);
    }
    else {
        SDL_version v;
        SDL_IMAGE_VERSION(&v);
        return Py_BuildValue("iii", v.major, v.minor, v.patch);
    }
}

/*
static void
_imageext_free(void *ptr)
{
#ifdef WITH_THREAD
    if (_pg_img_mutex) {
        SDL_DestroyMutex(_pg_img_mutex);
        _pg_img_mutex = 0;
    }
#endif
}
*/

static PyMethodDef _imageext_methods[] = {
    {"load_extended", (PyCFunction)image_load_ext,
     METH_VARARGS | METH_KEYWORDS, DOC_IMAGE_LOADEXTENDED},
    {"save_extended", (PyCFunction)image_save_ext,
     METH_VARARGS | METH_KEYWORDS, DOC_IMAGE_SAVEEXTENDED},
    {"_get_sdl_image_version", (PyCFunction)imageext_get_sdl_image_version,
     METH_VARARGS | METH_KEYWORDS,
     "_get_sdl_image_version() -> (major, minor, patch)\n"
     "Note: Should not be used directly."},
    {"_load_sized_svg", (PyCFunction)imageext_load_sized_svg,
     METH_VARARGS | METH_KEYWORDS, "Note: Should not be used directly."},
    {NULL, NULL, 0, NULL}};

/*DOC*/ static char _imageext_doc[] =
    /*DOC*/ "additional image loaders";

MODINIT_DEFINE(imageext)
{
    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "imageext",
                                         _imageext_doc,
                                         -1,
                                         _imageext_methods,
                                         NULL,
                                         NULL,
                                         NULL,
                                         NULL}; /* _imageext_free commented */

    /* imported needed apis; Do this first so if there is an error
       the module is not loaded.
    */
    import_pygame_base();
    if (PyErr_Occurred()) {
        return NULL;
    }
    import_pygame_surface();
    if (PyErr_Occurred()) {
        return NULL;
    }
    import_pygame_rwobject();

    if (PyErr_Occurred()) {
        return NULL;
    }

    /*
    #ifdef WITH_THREAD
        _pg_img_mutex = SDL_CreateMutex();
        if (!_pg_img_mutex) {
            PyErr_SetString(pgExc_SDLError, SDL_GetError());
            return NULL;
        }
    #endif
    */

    /* create the module */
    return PyModule_Create(&_module);
}
