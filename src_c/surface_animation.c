#define PYGAMEAPI_SURFACE_INTERNAL
#include "_surface.h"

enum AnimationLoopMode {
    ANIM_LOOP_SIMPLE,
    ANIM_LOOP_LOOP,
    ANIM_LOOP_PINGPONG,
};

static int
anim_init_internal(pgAnimatedSurfaceObject *self, int nframes);

pgAnimatedSurfaceObject *
pgAnimatedSurface_New(int nframes)
{
    pgAnimatedSurfaceObject *anim;
    anim = PyObject_New(pgAnimatedSurfaceObject, &pgAnimatedSurface_Type);
    if (anim_init_internal(anim, nframes) < 0) {
        return NULL;
    }
    return anim;
}

Py_ssize_t
pgAnimatedSurface_GetIndexByTime(pgAnimatedSurfaceObject *anim, Sint64 time)
{
    int i;
    Py_ssize_t size = PyList_Size(anim->frame_list);
    if (size == 0) {
        PyErr_SetString(PyExc_TypeError, "No frame in animation.");
        return -1;
    }
    Uint64 total_time = anim->delay_prefix_sum[size - 1];

    switch (anim->loop_mode) {
        case ANIM_LOOP_SIMPLE:
            if (time > total_time) {
                return size - 1;
            }
            break;
        case ANIM_LOOP_LOOP:
            time %= total_time;
            break;
        case ANIM_LOOP_PINGPONG:
            time %= total_time * 2;
            time = total_time - llabs(time - total_time);
            break;
        default:
            PyErr_SetString(PyExc_RuntimeError, "Unknown loop mode.");
            return -1;
            break;
    }

    for (i = 0; i < size; i++) {
        if (anim->delay_prefix_sum[i] >= time) {
            return i;
        }
    }

    return -1;
}

pgSurfaceObject *
pgAnimatedSurface_AsSurface(PyObject *obj)
{
    pgAnimatedSurfaceObject *anim = (pgAnimatedSurfaceObject *)obj;
    Uint64 time;
    if (anim->pause) {
        time = anim->pause_offset;
    }
    else {
        time = PG_GetTicks() - anim->play_start_time;
    }
    Py_ssize_t index = pgAnimatedSurface_GetIndexByTime(anim, time);
    if (index < 0) {
        return NULL;
    }
    PyObject *result = PyList_GetItem((anim)->frame_list, index);
    return (pgSurfaceObject *)result;
}

static PyObject *
anim_start_play(pgAnimatedSurfaceObject *self, PyObject *const *args,
                Py_ssize_t nargs, PyObject *kwnames)
{
    Sint64 time_offset = 0;
    if (nargs != 0) {
        return RAISE(PyExc_TypeError,
                     "'start_play' takes no positional arguments");
    }
    if (kwnames) {
        Py_ssize_t sequence_len = PySequence_Fast_GET_SIZE(kwnames);
        if (sequence_len != 1) {
            return RAISE(PyExc_TypeError,
                         "'start_play' takes only 1 keyword argument");
        }
        PyObject *name = PySequence_Fast_ITEMS(kwnames)[0];
        if (PyUnicode_CompareWithASCIIString(name, "time_offset")) {
            PyErr_Format(
                PyExc_TypeError,
                "'start_play' got an unexpected keyword argument '%s'",
                PyUnicode_AsUTF8(name));
            return NULL;
        }
        time_offset = PyLong_AsLongLong(args[0]);
        if (time_offset == -1 && PyErr_Occurred()) {
            return NULL;
        }
        if (time_offset < 0) {
            return RAISE(PyExc_ValueError, "'time_offset' must be positive");
        }
    }

    self->play_start_time = PG_GetTicks() - time_offset;
    self->pause = SDL_FALSE;
    Py_RETURN_NONE;
}

static PyObject *
anim_pause(pgAnimatedSurfaceObject *self)
{
    if (self->pause) {
        Py_RETURN_NONE;
    }
    self->pause = SDL_TRUE;
    self->pause_offset = PG_GetTicks() - self->play_start_time;
    Py_RETURN_NONE;
}

static PyObject *
anim_resume(pgAnimatedSurfaceObject *self)
{
    if (!self->pause) {
        Py_RETURN_NONE;
    }
    self->pause = SDL_FALSE;
    self->play_start_time = PG_GetTicks() - self->pause_offset;
    Py_RETURN_NONE;
}

static PyObject *
anim_toggle_pause(pgAnimatedSurfaceObject *self)
{
    if (self->pause) {
        return anim_resume(self);
    }
    else {
        return anim_pause(self);
    }
}

struct PyMethodDef animated_surface_methods[] = {
    {"start_play", (PyCFunction)anim_start_play, METH_FASTCALL | METH_KEYWORDS,
     "docs_needed"},
    {"pause", (PyCFunction)anim_pause, METH_NOARGS, "docs_needed"},
    {"resume", (PyCFunction)anim_resume, METH_NOARGS, "docs_needed"},
    {"toggle_pause", (PyCFunction)anim_toggle_pause, METH_NOARGS,
     "docs_needed"},
    {NULL, NULL, 0, NULL}};

int
anim_set_loop_mode(pgAnimatedSurfaceObject *self, PyObject *arg, void *v)
{
    const char *arg_str;
    if (!PyUnicode_Check(arg)) {
        PyErr_Format(PyExc_TypeError, "expected a str, got %s",
                     Py_TYPE(arg)->tp_name);
        return -1;
    }
    arg_str = PyUnicode_AsUTF8(arg);
    if (!arg_str)
        return -1;

    if (!strcmp(arg_str, "simple")) {
        self->loop_mode = ANIM_LOOP_SIMPLE;
    }
    else if (!strcmp(arg_str, "loop")) {
        self->loop_mode = ANIM_LOOP_LOOP;
    }
    else if (!strcmp(arg_str, "ping-pong")) {
        self->loop_mode = ANIM_LOOP_PINGPONG;
    }
    else {
        PyErr_SetString(
            PyExc_TypeError,
            "unknown loop mode, expected 'simple', 'loop' or 'ping-pong'");
        return -1;
    }
    return 0;
}

static PyObject *
anim_get_loop_mode(pgAnimatedSurfaceObject *self, void *v)
{
    PyObject *result;
    switch (self->loop_mode) {
        case ANIM_LOOP_SIMPLE:
            result = PyUnicode_FromString("simple");
            break;
        case ANIM_LOOP_LOOP:
            result = PyUnicode_FromString("loop");
            break;
        case ANIM_LOOP_PINGPONG:
            result = PyUnicode_FromString("ping-pong");
            break;
        default:
            PyErr_SetString(PyExc_RuntimeError, "Unknown loop mode.");
            result = NULL;
            break;
    }
    return result;
}

static PyGetSetDef animated_surface_getsets[] = {
    {"loop_mode", (getter)anim_get_loop_mode, (setter)anim_set_loop_mode,
     "docs_needed", NULL},
    {NULL, NULL, NULL, NULL, NULL}};

static void
anim_dealloc(pgAnimatedSurfaceObject *self)
{
    Py_XDECREF(self->frame_list);
    free(self->delays);
    free(self->delay_prefix_sum);
    Py_TYPE(self)->tp_free(self);
}

static int
anim_init_internal(pgAnimatedSurfaceObject *self, int nframes)
{
    self->frame_list = PyList_New(nframes);
    if (!self->frame_list) {
        Py_TYPE(self)->tp_free(self);
        return -1;
    }
    self->delays = malloc(nframes * sizeof(Uint64));
    if (!self->delays) {
        Py_TYPE(self)->tp_free(self);
        PyErr_NoMemory();
        return -1;
    }
    self->delay_prefix_sum = malloc(nframes * sizeof(Uint64));
    if (!self->delay_prefix_sum) {
        Py_TYPE(self)->tp_free(self);
        PyErr_NoMemory();
        return -1;
    }
    self->play_start_time = 0;
    self->pause = SDL_TRUE;
    self->pause_offset = 0;
    self->loop_mode = ANIM_LOOP_SIMPLE;
    return 0;
}

static int
anim_init(pgAnimatedSurfaceObject *self, PyObject *args, PyObject *kwargs)
{
    return anim_init_internal(self, 0);
}

PyTypeObject pgAnimatedSurface_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame.surface.AnimatedSurface",
    .tp_basicsize = sizeof(pgAnimatedSurfaceObject),
    .tp_dealloc = (destructor)anim_dealloc,
    .tp_doc = "docs_needed",
    .tp_methods = animated_surface_methods,
    .tp_getset = animated_surface_getsets,
    .tp_init = (initproc)anim_init,
    .tp_new = PyType_GenericNew,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
};
