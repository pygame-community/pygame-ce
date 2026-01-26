/*
  pygame-ce - Python Game Library
  Copyright (C) 2019 David Lönnhager

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

#include "../pygame.h"
#include "../pgcompat.h"

#include "../doc/touch_doc.h"

static PyObject *
pg_touch_num_devices(PyObject *self, PyObject *_null)
{
    int count;
#if SDL_VERSION_ATLEAST(3, 0, 0)

    SDL_TouchID *devices = SDL_GetTouchDevices(&count);
    if (devices == NULL) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    SDL_free(devices);
#else
    count = SDL_GetNumTouchDevices();
#endif
    return PyLong_FromLong(count);
}

static PyObject *
pg_touch_get_device(PyObject *self, PyObject *index_obj)
{
    SDL_TouchID touchid;
    if (!PyLong_Check(index_obj)) {
        return RAISE(PyExc_TypeError,
                     "index must be an integer "
                     "specifying a device to get the ID for");
    }
    int index = PyLong_AsLong(index_obj);
    if (PyErr_Occurred()) {
        return NULL;  // exception already set
    }
#if SDL_VERSION_ATLEAST(3, 0, 0)
    int count;
    SDL_TouchID *devices = SDL_GetTouchDevices(&count);
    if (devices == NULL) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    if (index < 0 || index >= count) {
        SDL_free(devices);
        return RAISE(PyExc_IndexError, "index is out of bounds");
    }
    touchid = devices[index];
    SDL_free(devices);
#else
    touchid = SDL_GetTouchDevice(index);
#endif
    if (touchid == 0) {
        /* invalid index */
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    return PyLong_FromLongLong(touchid);
}

static PyObject *
pg_touch_num_fingers(PyObject *self, PyObject *device_id_obj)
{
    int fingercount;
    if (!PyLong_Check(device_id_obj)) {
        return RAISE(PyExc_TypeError,
                     "device_id must be an integer "
                     "specifying a touch device");
    }
    int device_id = PyLong_AsLongLong(device_id_obj);
    if (PyErr_Occurred()) {
        return NULL;  // exception already set
    }

    VIDEO_INIT_CHECK();
#if SDL_VERSION_ATLEAST(3, 0, 0)
    SDL_Finger **fingers = SDL_GetTouchFingers(device_id, &fingercount);
    if (fingers == NULL) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    SDL_free(fingers);
#else
    fingercount = SDL_GetNumTouchFingers(device_id);
    if (fingercount == 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
#endif
    return PyLong_FromLong(fingercount);
}
#if !defined(BUILD_STATIC)
/* Helper for adding objects to dictionaries. Check for errors with
   PyErr_Occurred() */
static void
_pg_insobj(PyObject *dict, char *name, PyObject *v)
{
    if (v) {
        PyDict_SetItemString(dict, name, v);
        Py_DECREF(v);
    }
}
#else
extern void
_pg_insobj(PyObject *dict, char *name, PyObject *v);
#endif

static PyObject *
pg_touch_get_finger(PyObject *self, PyObject *args, PyObject *kwargs)
{
    char *keywords[] = {"touchid", "index", NULL};
    SDL_TouchID touchid;
    int index;
    SDL_Finger *finger;
    PyObject *fingerobj;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "Li", keywords, &touchid,
                                     &index)) {
        return NULL;
    }

    VIDEO_INIT_CHECK();
#if SDL_VERSION_ATLEAST(3, 0, 0)
    int fingercount;
    SDL_Finger **fingers = SDL_GetTouchFingers(touchid, &fingercount);
    if (fingers == NULL) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    if (index < 0 || index >= fingercount) {
        SDL_free(fingers);
        return RAISE(PyExc_IndexError, "index is out of bounds");
    }
    finger = fingers[index];
#else
    if (!(finger = SDL_GetTouchFinger(touchid, index))) {
        Py_RETURN_NONE;
    }
#endif

    fingerobj = PyDict_New();
    if (!fingerobj) {
        return NULL;
    }

    _pg_insobj(fingerobj, "id", PyLong_FromLongLong(finger->id));
    _pg_insobj(fingerobj, "x", PyFloat_FromDouble(finger->x));
    _pg_insobj(fingerobj, "y", PyFloat_FromDouble(finger->y));
    _pg_insobj(fingerobj, "pressure", PyFloat_FromDouble(finger->pressure));

    if (PyErr_Occurred()) {
        Py_DECREF(fingerobj);
        return NULL;
    }
#if SDL_VERSION_ATLEAST(3, 0, 0)
    SDL_free(fingers);
#endif
    return fingerobj;
}

static PyMethodDef _touch_methods[] = {
    {"get_num_devices", pg_touch_num_devices, METH_NOARGS,
     DOC_SDL2_TOUCH_GETNUMDEVICES},
    {"get_device", pg_touch_get_device, METH_O, DOC_SDL2_TOUCH_GETDEVICE},

    {"get_num_fingers", pg_touch_num_fingers, METH_O,
     DOC_SDL2_TOUCH_GETNUMFINGERS},
    {"get_finger", (PyCFunction)pg_touch_get_finger,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_TOUCH_GETFINGER},

    {NULL, NULL, 0, NULL}};

MODINIT_DEFINE(touch)
{
    PyObject *module;
    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "touch",
                                         DOC_SDL2_TOUCH,
                                         -1,
                                         _touch_methods,
                                         NULL,
                                         NULL,
                                         NULL,
                                         NULL};
    import_pygame_base();
    if (PyErr_Occurred()) {
        return NULL;
    }

    /* create the module */
    module = PyModule_Create(&_module);
    if (module == NULL) {
        return NULL;
    }
    return module;
}
