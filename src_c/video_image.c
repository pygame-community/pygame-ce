#define PYGAMEAPI_IMAGE_INTERNAL

#include "pygame.h"

#include "pgcompat.h"

#include "doc/sdl2_video_doc.h"

static PyTypeObject pgImage_Type;

#define pgImage_Check(x) \
    (PyObject_IsInstance((x), (PyObject *)&pgImage_Type))

static int
image_init(pgImageObject *self, PyObject *args, PyObject *kwargs) {
    printf("Image: %d %d %d %d" self->angle, self->origin.x, self->origin.y, self->flip);
    PyObject *texture_or_imageobj;
    PyObject *srcrectobj;
    char *keywords[] = {"texture_or_image", "srcrect", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", keywords, &texture_or_imageobj, &srcrectobj)) {
        return -1;
    }

}

static void
image_dealloc(pgImageObject *self, PyObject *_null) {
    Py_TYPE(self)->tp_free(self);
}

static PyMethodDef image_methods[] = {
//    {"draw", (PyCFunction)image_draw, METH_VARARGS | METH_KEYWORDS,
//     DOC_SDL2_VIDEO_IMAGE_DRAW},
    {NULL, NULL, 0, NULL}
};

static PyGetSetDef image_getset[] = {
//    {"color", (getter)image_get_color, (setter)image_set_color,
//     DOC_SDL2_VIDEO_IMAGE_COLOR, NULL},
    {NULL, 0, NULL, NULL, NULL}
};


static PyMethodDef _image_methods[] = {
    {NULL, NULL, 0, NULL}};

static PyTypeObject pgImage_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._image.Image",
    .tp_basicsize = sizeof(pgImageObject),
    .tp_dealloc = (destructor)image_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_IMAGE,
    .tp_methods = image_methods,
    .tp_init = (initproc)image_init,
    .tp_new = PyType_GenericNew,
    .tp_getset = image_getset};

MODINIT_DEFINE(_image)
{
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_IMAGE_NUMSLOTS];

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "_image",
                                         "docs_needed",
                                         -1,
                                         _image_methods,
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

    if (PyType_Ready(&pgImage_Type) < 0) {
        return NULL;
    }

    /* create the module */
    module = PyModule_Create(&_module);
    if (module == 0) {
        return NULL;
    }

    Py_INCREF(&pgImage_Type);
    if (PyModule_AddObject(module, "Image", (PyObject *)&pgImage_Type)) {
        Py_DECREF(&pgImage_Type);
        Py_DECREF(module);
        return NULL;
    }

    c_api[0] = &pgImage_Type;
    apiobj = encapsulate_api(c_api, "_image");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}