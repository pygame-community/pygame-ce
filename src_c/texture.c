#include "pygame.h"

#include "pgcompat.h"

#include "doc/sdl2_video_doc.h"

static PyTypeObject pgTexture_Type;

static PyMethodDef texture_methods[] = {{NULL, NULL, 0, NULL}};

static PyGetSetDef texture_getset[] = {{NULL, 0, NULL, NULL, NULL}};

static PyTypeObject pgTexture_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._renderer.Texture",
    .tp_basicsize = sizeof(pgTextureObject),
    //.tp_dealloc = (destructor)texture_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_TEXTURE, .tp_methods = texture_methods,
    //.tp_init = (initproc)texture_init,
    .tp_new = PyType_GenericNew, .tp_getset = texture_getset};
