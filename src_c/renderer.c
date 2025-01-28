#define PYGAMEAPI_RENDERER_INTERNAL

#include "pygame.h"

#include "pgcompat.h"

#include "doc/sdl2_video_doc.h"

static PyTypeObject pgRenderer_Type;

static PyMethodDef renderer_methods[] = {{NULL, NULL, 0, NULL}};

static PyGetSetDef renderer_getset[] = {{NULL, 0, NULL, NULL, NULL}};

static PyTypeObject pgRenderer_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._renderer.Renderer",
    .tp_basicsize = sizeof(pgRendererObject),
    //.tp_dealloc = (destructor)renderer_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_RENDERER, .tp_methods = renderer_methods,
    //.tp_init = (initproc)renderer_init,
    .tp_new = PyType_GenericNew, .tp_getset = renderer_getset};

static PyMethodDef _renderer_methods[] = {{NULL, NULL, 0, NULL}};

MODINIT_DEFINE(_renderer)
{
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_RENDERER_NUMSLOTS];

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "_renderer",
                                         "docs_needed",
                                         -1,
                                         _renderer_methods,
                                         NULL,
                                         NULL,
                                         NULL,
                                         NULL};

    /* imported needed apis; Do this first so if there is an error
       the module is not loaded.
    */
    import_pygame_base();
    if (PyErr_Occurred()) {
        return NULL;
    }

    if (PyType_Ready(&pgRenderer_Type) < 0) {
        return NULL;
    }

    /* create the module */
    module = PyModule_Create(&_module);
    if (module == 0) {
        return NULL;
    }

    Py_INCREF(&pgRenderer_Type);
    if (PyModule_AddObject(module, "Renderer", (PyObject *)&pgRenderer_Type)) {
        Py_DECREF(&pgRenderer_Type);
        Py_DECREF(module);
        return NULL;
    }

    c_api[0] = &pgRenderer_Type;
    apiobj = encapsulate_api(c_api, "_renderer");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}
