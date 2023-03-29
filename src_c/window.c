#include "pygame.h"

#include "pgcompat.h"

// #include "doc/window_doc.h"

PyObject *_window_list = NULL;

typedef struct {
    PyObject_HEAD SDL_Window *win;
    SDL_bool is_from_display;
} pgWindowObject;

static PyObject *
get_windows(PyObject *self)
{
    PyObject *t = PyTuple_New(PySequence_Size(_window_list));
    for (int i = 0; i < PySequence_Size(_window_list); i++) {
        PyTuple_SetItem(t, i, PySequence_GetItem(_window_list, i));
    }
    return t;
}

static PyObject *
get_grabbed_window(PyObject *self)
{
    SDL_Window *grabbed = SDL_GetGrabbedWindow();
    PyObject *win_obj = NULL;
    if (grabbed) {
        win_obj = SDL_GetWindowData(grabbed, "pg_window");
        if (!win_obj) {
            Py_RETURN_NONE;
        }
        Py_INCREF(win_obj);
        return win_obj;
    }
    Py_RETURN_NONE;
}

static PyObject *
window_destroy(pgWindowObject *self)
{
    int i;

    if (!self->win) {
        Py_RETURN_NONE;
    }

    SDL_DestroyWindow(self->win);
    self->win = NULL;

    for (i = 0; i < PySequence_Size(_window_list); i++) {
        if ((PyObject *)self == PySequence_GetItem(_window_list, i)) {
            PySequence_DelItem(_window_list, i);
            Py_DECREF(self);
            Py_RETURN_NONE;
        }
    }
    Py_RETURN_NONE;
}

static PyObject *
window_set_windowed(pgWindowObject *self)
{
    if (SDL_SetWindowFullscreen(self->win, 0)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
window_set_fullscreen(pgWindowObject *self, PyObject *args, PyObject *kwargs)
{
    SDL_bool desktop = SDL_FALSE;
    int flags = SDL_WINDOW_FULLSCREEN;
    char *kwids[] = {"desktop", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|p", kwids, &desktop)) {
        return NULL;
    }
    if (desktop) {
        flags = SDL_WINDOW_FULLSCREEN_DESKTOP;
    }
    if (SDL_SetWindowFullscreen(self->win, flags)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
window_set_icon(pgWindowObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    if (nargs != 1) {
        return RAISE(PyExc_TypeError,
                     "set_icon() takes 1 positional argument.");
    }
    if (!pgSurface_Check(args[0])) {
        return RAISE(PyExc_TypeError,
                     "Argument to set_icon must be a Surface");
    }
    SDL_SetWindowIcon(self->win, pgSurface_AsSurface(args[0]));
    Py_RETURN_NONE;
}

static PyObject *
window_set_grab(pgWindowObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    if (nargs != 1) {
        return RAISE(PyExc_TypeError,
                     "set_grab() takes 1 positional argument.");
    }

    if (PyObject_IsTrue(args[0])) {
        SDL_SetWindowGrab(self->win, SDL_TRUE);
    }
    else {
        SDL_SetWindowGrab(self->win, SDL_FALSE);
    }

    Py_RETURN_NONE;
}

static PyObject *
window_get_grab(pgWindowObject *self)
{
    return PyBool_FromLong(SDL_GetWindowGrab(self->win));
}

static void
window_dealloc(pgWindowObject *self)
{
    if (self->is_from_display) {
        return;
    }
    PyObject_Free(self);
}

static int
window_init(pgWindowObject *self, PyObject *args, PyObject *kwargs)
{
    char *title = "pygame";
    PyObject *size = NULL;
    int size_w = 640, size_h = 480;
    PyObject *position = NULL;
    int pos_x = SDL_WINDOWPOS_UNDEFINED;
    int pos_y = SDL_WINDOWPOS_UNDEFINED;
    SDL_bool fullscreen = SDL_FALSE;
    SDL_bool fullscreen_desktop = SDL_FALSE;
    Uint32 flags = 0;
    SDL_Window *_win = NULL;

    char *kwids[] = {
        "title", "size", "position", "fullscreen", "fullscreen_desktop", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|sOOpp", kwids, &title,
                                     &size, &position, &fullscreen,
                                     &fullscreen_desktop)) {
        return -1;
    }

    if (fullscreen && fullscreen_desktop) {
        PyErr_SetString(
            PyExc_ValueError,
            "fullscreen and fullscreen_desktop cannot be used at the same "
            "time.");
        return -1;
    }
    if (fullscreen)
        flags |= SDL_WINDOW_FULLSCREEN;
    else if (fullscreen_desktop)
        flags |= SDL_WINDOW_FULLSCREEN_DESKTOP;

    if (size) {
        if (!pg_TwoIntsFromObj(size, &size_w, &size_h)) {
            PyErr_SetString(PyExc_TypeError, "invalid size argument");
            return -1;
        }
    }

    if (position) {
        if (Py_TYPE(position) == &PyLong_Type) {
            pos_x = pos_y = PyLong_AsLong(position);
        }
        else if (!pg_TwoIntsFromObj(position, &pos_x, &pos_y)) {
            PyErr_SetString(PyExc_TypeError, "invalid positon argument");
            return -1;
        }
    }

    _win = SDL_CreateWindow(title, pos_x, pos_y, size_w, size_h, flags);
    if (!_win) {
        PyErr_SetString(pgExc_SDLError, SDL_GetError());
        return -1;
    }
    self->win = _win;
    self->is_from_display = SDL_FALSE;

    SDL_SetWindowData(_win, "pg_window", self);

    PyList_Append(_window_list, (PyObject *)self);

    return 0;
}

static PyMethodDef window_methods[] = {
    {"set_windowed", (PyCFunction)window_set_windowed, METH_NOARGS,
     "docs_needed"},
    {"set_fullscreen", (PyCFunction)window_set_fullscreen,
     METH_VARARGS | METH_KEYWORDS, "docs_needed"},
    {"set_icon", (PyCFunction)window_set_icon, METH_FASTCALL, "docs_needed"},
    {"set_grab", (PyCFunction)window_set_grab, METH_FASTCALL, "docs_needed"},
    {"get_grab", (PyCFunction)window_get_grab, METH_NOARGS, "docs_needed"},
    {"destroy", (PyCFunction)window_destroy, METH_NOARGS, "docs_needed"},
    {NULL, NULL, 0, NULL}};

static PyTypeObject pgWindow_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame.window.Window",
    .tp_basicsize = sizeof(pgWindowObject),
    .tp_dealloc = (destructor)window_dealloc,
    .tp_doc = "docs_needed",
    .tp_methods = window_methods,
    .tp_init = (initproc)window_init,
    .tp_new = PyType_GenericNew,
};

static PyMethodDef _window_methods[] = {
    {"get_grabbed_window", (PyCFunction)get_grabbed_window, METH_NOARGS,
     "docs_needed"},
    {"get_windows", (PyCFunction)get_windows, METH_NOARGS, "docs_needed"},
    {NULL, NULL, 0, NULL}};

MODINIT_DEFINE(window)
{
    PyObject *module;

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "window",
                                         "docs_needed",
                                         -1,
                                         _window_methods,
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

    import_pygame_surface();
    if (PyErr_Occurred()) {
        return NULL;
    }

    if (PyType_Ready(&pgWindow_Type) < 0) {
        return NULL;
    }

    /* create the module */
    module = PyModule_Create(&_module);
    if (module == 0) {
        return NULL;
    }

    Py_INCREF(&pgWindow_Type);
    if (PyModule_AddObject(module, "Window", (PyObject *)&pgWindow_Type)) {
        Py_DECREF(&pgWindow_Type);
        Py_DECREF(module);
        return NULL;
    }
    Py_INCREF(&pgWindow_Type);
    if (PyModule_AddObject(module, "WindowType", (PyObject *)&pgWindow_Type)) {
        Py_DECREF(&pgWindow_Type);
        Py_DECREF(module);
        return NULL;
    }

    _window_list = PyList_New(0);
    Py_XINCREF(_window_list);

    PyObject *WINDOWPOS_UNDEFINED = PyLong_FromLong(SDL_WINDOWPOS_UNDEFINED);
    if (PyModule_AddObject(module, "WINDOWPOS_UNDEFINED",
                           WINDOWPOS_UNDEFINED)) {
        Py_DECREF(WINDOWPOS_UNDEFINED);
        Py_DECREF(module);
        return NULL;
    }
    PyObject *WINDOWPOS_CENTERED = PyLong_FromLong(SDL_WINDOWPOS_CENTERED);
    if (PyModule_AddObject(module, "WINDOWPOS_CENTERED", WINDOWPOS_CENTERED)) {
        Py_DECREF(WINDOWPOS_CENTERED);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}