#include "pygame.h"

#include <sdl3webgpu.h>

static void *
pg_pointer_from_object(PyObject *object)
{
    if (PyCapsule_CheckExact(object)) {
        return PyCapsule_GetPointer(object, NULL);
    }
    return PyLong_AsVoidPtr(object);
}

static PyObject *
pg_sdl3webgpu_get_surface(PyObject *self, PyObject *args)
{
    PyObject *instance_object;
    PyObject *window_object;
    PyObject *window_pointer_object;
    WGPUInstance instance;
    SDL_Window *window;
    WGPUSurface surface;

    (void)self;
    if (!PyArg_ParseTuple(args, "OO:get_surface", &instance_object,
                          &window_object)) {
        return NULL;
    }

    instance = (WGPUInstance)pg_pointer_from_object(instance_object);
    if (PyErr_Occurred()) {
        return NULL;
    }
    window_pointer_object = PyObject_CallMethod(
        window_object, "_get_sdl_window_pointer", NULL);
    if (!window_pointer_object) {
        return NULL;
    }
    window = (SDL_Window *)pg_pointer_from_object(window_pointer_object);
    Py_DECREF(window_pointer_object);
    if (PyErr_Occurred()) {
        return NULL;
    }
    if (!instance || !window) {
        PyErr_SetString(PyExc_ValueError,
                        "instance and window must be valid handles");
        return NULL;
    }

    surface = SDL_GetWGPUSurface(instance, window);
    if (!surface) {
        PyErr_SetString(PyExc_RuntimeError, SDL_GetError());
        return NULL;
    }
    return PyCapsule_New((void *)surface, "WGPUSurface", NULL);
}

static PyMethodDef pg_sdl3webgpu_methods[] = {
    {"get_surface", pg_sdl3webgpu_get_surface, METH_VARARGS,
     "Return a WebGPU surface for a pygame Window."},
    {NULL, NULL, 0, NULL},
};

MODINIT_DEFINE(_sdl3webgpu)
{
    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT,
        "_sdl3webgpu",
        "Optional SDL3 WebGPU surface integration.",
        -1,
        pg_sdl3webgpu_methods,
    };
    return PyModule_Create(&module);
}