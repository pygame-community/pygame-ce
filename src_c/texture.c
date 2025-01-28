#define PYGAMEAPI_TEXTURE_INTERNAL

#include "pygame.h"

#include "pgcompat.h"

#include "doc/sdl2_video_doc.h"

static PyTypeObject pgTexture_Type;

static PyMethodDef texture_methods[] = {
    {NULL, NULL, 0, NULL}
};

static PyGetSetDef texture_getset[] = {
    {NULL, 0, NULL, NULL, NULL}
};

static PyTypeObject pgTexture_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._texture.Texture",
    .tp_basicsize = sizeof(pgTextureObject),
    //.tp_dealloc = (destructor)texture_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_TEXTURE,
    .tp_methods = texture_methods,
    //.tp_init = (initproc)texture_init,
    .tp_new = PyType_GenericNew,
    .tp_getset = texture_getset
};

static PyMethodDef _texture_methods[] = {
    {NULL, NULL, 0, NULL}
};

MODINIT_DEFINE(_texture)
{
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_TEXTURE_NUMSLOTS];

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "_texture",
                                         "docs_needed",
                                         -1,
                                         _texture_methods,
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

    if (PyType_Ready(&pgTexture_Type) < 0) {
        return NULL;
    }

    /* create the module */
    module = PyModule_Create(&_module);
    if (module == 0) {
        return NULL;
    }

    Py_INCREF(&pgTexture_Type);
    if (PyModule_AddObject(module, "Texture", (PyObject *)&pgTexture_Type)) {
        Py_DECREF(&pgTexture_Type);
        Py_DECREF(module);
        return NULL;
    }

    c_api[0] = &pgTexture_Type;
    apiobj = encapsulate_api(c_api, "_texture");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}
