#include "pygame.h"

#include "pgcompat.h"

#include "doc/sdl2_video_doc.h"

static PyTypeObject pgImage_Type;

static PyMethodDef image_methods[] = {{NULL, NULL, 0, NULL}};

static PyGetSetDef image_getset[] = {{NULL, 0, NULL, NULL, NULL}};

static PyTypeObject pgImage_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._renderer.Image",
    .tp_basicsize = sizeof(pgImageObject),
    //.tp_dealloc = (destructor)image_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_IMAGE, .tp_methods = image_methods,
    //.tp_init = (initproc)image_init,
    .tp_new = PyType_GenericNew, .tp_getset = image_getset};
