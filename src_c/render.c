#define PYGAMEAPI_RENDER_INTERNAL

#include "pygame.h"

#include "pgcompat.h"

typedef struct {
    PyObject_HEAD int chan;
} pgRendererObject;

static PyMethodDef _methods[] = {{NULL, NULL, 0, NULL}};

static void
renderer_dealloc(PyObject *self)
{
    PyObject_Free(self);
}

static int
renderer_init(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
    PyErr_SetString(PyExc_NotImplementedError,
                    "__init__() is not implemented. Use "
                    "Renderer.from_window_id() instead");
    return -1;
}

static PyTypeObject pgRenderer_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame.render.Renderer",
    .tp_basicsize = sizeof(pgRendererObject),
    .tp_dealloc = renderer_dealloc,
    .tp_doc = "docs",
    .tp_methods = _methods,
    .tp_init = (initproc)renderer_init,
    .tp_new = PyType_GenericNew,
};

static PyMethodDef _render_methods[] = {{NULL, NULL, 0, NULL}};

MODINIT_DEFINE(render)
{
    PyObject *module = NULL;

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "render",
                                         "docs",
                                         -1,
                                         _render_methods,
                                         NULL,
                                         NULL,
                                         NULL,
                                         NULL};

    /* imported needed apis; Do this first so if there is an error
       the module is not loaded.
    */

    /*imported needed apis*/
    import_pygame_base();
    if (PyErr_Occurred()) {
        return NULL;
    }

    /* type preparation */
    if (PyType_Ready(&pgRenderer_Type) < 0) {
        return NULL;
    }

    /* create the module */
    module = PyModule_Create(&_module);
    if (module == NULL) {
        return NULL;
    }
    Py_INCREF(&pgRenderer_Type);
    if (PyModule_AddObject(module, "RendererType",
                           (PyObject *)&pgRenderer_Type)) {
        Py_DECREF(&pgRenderer_Type);
        Py_DECREF(module);
        return NULL;
    }
    Py_INCREF(&pgRenderer_Type);
    if (PyModule_AddObject(module, "Renderer", (PyObject *)&pgRenderer_Type)) {
        Py_DECREF(&pgRenderer_Type);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}