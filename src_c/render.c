#define PYGAMEAPI_RENDER_INTERNAL

#include "pygame.h"

#include "pgcompat.h"

#include "doc/sdl2_video_doc.h"

static PyTypeObject pgRenderer_Type;

static PyTypeObject pgTexture_Type;

static PyTypeObject pgImage_Type;

static PyMethodDef renderer_methods[] = {{NULL, NULL, 0, NULL}};

static PyGetSetDef renderer_getset[] = {{NULL, 0, NULL, NULL, NULL}};

static PyMethodDef texture_methods[] = {{NULL, NULL, 0, NULL}};

static PyGetSetDef texture_getset[] = {{NULL, 0, NULL, NULL, NULL}};

static PyMethodDef image_methods[] = {{NULL, NULL, 0, NULL}};

static PyGetSetDef image_getset[] = {{NULL, 0, NULL, NULL, NULL}};

static PyTypeObject pgRenderer_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._render.Renderer",
    .tp_basicsize = sizeof(pgRendererObject),
    //.tp_dealloc = (destructor)renderer_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_RENDERER, .tp_methods = renderer_methods,
    //.tp_init = (initproc)renderer_init,
    .tp_new = PyType_GenericNew, .tp_getset = renderer_getset};

static PyTypeObject pgTexture_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._render.Texture",
    .tp_basicsize = sizeof(pgTextureObject),
    //.tp_dealloc = (destructor)texture_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_TEXTURE, .tp_methods = texture_methods,
    //.tp_init = (initproc)texture_init,
    .tp_new = PyType_GenericNew, .tp_getset = texture_getset};

static PyTypeObject pgImage_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._render.Image",
    .tp_basicsize = sizeof(pgImageObject),
    //.tp_dealloc = (destructor)image_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_IMAGE, .tp_methods = image_methods,
    //.tp_init = (initproc)image_init,
    .tp_new = PyType_GenericNew, .tp_getset = image_getset};

static PyMethodDef _render_methods[] = {{NULL, NULL, 0, NULL}};

MODINIT_DEFINE(_render)
{
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_RENDER_NUMSLOTS];

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "_render",
                                         "docs_needed",
                                         -1,
                                         _render_methods,
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

    if (PyType_Ready(&pgTexture_Type) < 0) {
        return NULL;
    }

    if (PyType_Ready(&pgImage_Type) < 0) {
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

    Py_INCREF(&pgTexture_Type);
    if (PyModule_AddObject(module, "Texture", (PyObject *)&pgTexture_Type)) {
        Py_DECREF(&pgTexture_Type);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&pgImage_Type);
    if (PyModule_AddObject(module, "Image", (PyObject *)&pgImage_Type)) {
        Py_DECREF(&pgImage_Type);
        Py_DECREF(module);
        return NULL;
    }

    c_api[0] = &pgRenderer_Type;
    c_api[1] = &pgTexture_Type;
    c_api[2] = &pgImage_Type;
    apiobj = encapsulate_api(c_api, "_render");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}
