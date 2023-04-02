#define PYGAMEAPI_WINDOW_INTERNAL

#include "pygame.h"

#include "pgcompat.h"

#include <SDL_syswm.h>

#include "doc/window_doc.h"

static PyTypeObject pgWindow_Type;
PyObject *_window_list = NULL;
SDL_Surface *_dummy_surface = NULL;
PyObject *_pg_display_quit = NULL;

#define pgWindow_Check(x) \
    (PyObject_IsInstance((x), (PyObject *)&pgWindow_Type))

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
    PyObject *item;

    if (!self->win) {
        return RAISE(pgExc_SDLError, "Invalid window");
    }

    SDL_DestroyWindow(self->win);
    Py_XDECREF(self->surf);

    // set the surface to dummy
    // to prevent segfaut when writing the surface after
    // the window is destroyed
    if (self->surf)
        self->surf->surf = _dummy_surface;

    self->surf = NULL;
    self->win = NULL;

    for (i = 0; i < PySequence_Size(_window_list); i++) {
        item = PySequence_GetItem(_window_list, i);
        if ((PyObject *)self == item) {
            PySequence_DelItem(_window_list, i);
            Py_DECREF(self);
            break;
        }
        Py_DECREF(item);
    }

    // if the window is from display module
    // quit the display module
    if (self->is_from_display) {
        if (!PyObject_CallObject(_pg_display_quit, NULL)) {
            return NULL;
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
window_focus(pgWindowObject *self, PyObject *args, PyObject *kwargs)
{
    SDL_bool input_only = SDL_FALSE;
    char *kwids[] = {"input_only", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|p", kwids, &input_only)) {
        return NULL;
    }
    if (input_only) {
        if (SDL_SetWindowInputFocus(self->win)) {
            return RAISE(pgExc_SDLError, SDL_GetError());
        }
    }
    else {
        SDL_RaiseWindow(self->win);
    }
    Py_RETURN_NONE;
}

static PyObject *
window_hide(pgWindowObject *self)
{
    SDL_HideWindow(self->win);
    Py_RETURN_NONE;
}

static PyObject *
window_show(pgWindowObject *self)
{
    SDL_ShowWindow(self->win);
    Py_RETURN_NONE;
}

static PyObject *
window_restore(pgWindowObject *self)
{
    SDL_RestoreWindow(self->win);
    Py_RETURN_NONE;
}

static PyObject *
window_maximize(pgWindowObject *self)
{
    SDL_MaximizeWindow(self->win);
    Py_RETURN_NONE;
}

static PyObject *
window_minimize(pgWindowObject *self)
{
    SDL_MinimizeWindow(self->win);
    Py_RETURN_NONE;
}

static PyObject *
window_set_modal_for(pgWindowObject *self, PyObject *arg)
{
    if (!pgWindow_Check(arg)) {
        return RAISE(PyExc_TypeError,
                     "Argument to set_modal_for must be a Window.");
    }
    if (!SDL_SetWindowModalFor(self->win, ((pgWindowObject *)arg)->win)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
window_update_from_surface(pgWindowObject *self, PyObject *const *args,
                           Py_ssize_t nargs)
{
    int i;
    SDL_Rect *rects = NULL, tmp, *r;
    if (nargs == 0) {
        if (SDL_UpdateWindowSurface(self->win)) {
            return RAISE(pgExc_SDLError, SDL_GetError());
        }
    }
    else {
        rects = malloc(nargs * sizeof(SDL_Rect));
        for (i = 0; i < nargs; i++) {
            r = pgRect_FromObject(args[i], &tmp);
            if (!r) {
                return RAISE(PyExc_TypeError,
                             "Arguments must be rect or rect-like objects.");
            }
            rects[i] = *r;
            if (SDL_UpdateWindowSurfaceRects(self->win, rects, (int)nargs)) {
                return RAISE(pgExc_SDLError, SDL_GetError());
            }
        }
        free(rects);
    }
    Py_RETURN_NONE;
}

static PyObject *
window_set_icon(pgWindowObject *self, PyObject *arg)
{
    if (!pgSurface_Check(arg)) {
        return RAISE(PyExc_TypeError,
                     "Argument to set_icon must be a Surface.");
    }
    SDL_SetWindowIcon(self->win, pgSurface_AsSurface(arg));
    Py_RETURN_NONE;
}

static PyObject *
window_set_grab(pgWindowObject *self, PyObject *arg)
{
    int enable = PyObject_IsTrue(arg);
    if (enable == -1)
        return NULL;

    SDL_SetWindowGrab(self->win, enable);

    Py_RETURN_NONE;
}

static PyObject *
window_get_grab(pgWindowObject *self)
{
    return PyBool_FromLong(SDL_GetWindowGrab(self->win));
}

static PyObject *
window_set_title(pgWindowObject *self, PyObject *arg)
{
    const char *title;
    if (!PyUnicode_Check(arg)) {
        return RAISE(PyExc_TypeError, "Argument to set_title must be a str.");
    }
    title = PyUnicode_AsUTF8(arg);
    SDL_SetWindowTitle(self->win, title);
    Py_RETURN_NONE;
}

static PyObject *
window_get_title(pgWindowObject *self)
{
    const char *title = SDL_GetWindowTitle(self->win);
    return PyUnicode_FromString(title);
}

static PyObject *
window_set_resizable(pgWindowObject *self, PyObject *arg)
{
    int enable = PyObject_IsTrue(arg);
    if (enable == -1)
        return NULL;

    SDL_SetWindowResizable(self->win, enable);

    Py_RETURN_NONE;
}

static PyObject *
window_get_resizable(pgWindowObject *self)
{
    return PyBool_FromLong(SDL_GetWindowFlags(self->win) &
                           SDL_WINDOW_RESIZABLE);
}

static PyObject *
window_set_borderless(pgWindowObject *self, PyObject *arg)
{
    int enable = PyObject_IsTrue(arg);
    if (enable == -1)
        return NULL;

    SDL_SetWindowBordered(self->win, !enable);

    Py_RETURN_NONE;
}

static PyObject *
window_get_borderless(pgWindowObject *self)
{
    return PyBool_FromLong(SDL_GetWindowFlags(self->win) &
                           SDL_WINDOW_BORDERLESS);
}

static PyObject *
window_get_window_id(pgWindowObject *self)
{
    Uint32 window_id = SDL_GetWindowID(self->win);
    if (!window_id) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    return PyLong_FromLong(window_id);
}

static PyObject *
window_set_size(pgWindowObject *self, PyObject *arg)
{
    int w, h;

    if (!pg_TwoIntsFromObj(arg, &w, &h)) {
        return RAISE(PyExc_TypeError, "invalid size argument");
    }

    if (w <= 0 || h <= 0) {
        return RAISE(
            PyExc_ValueError,
            "width or height should not be less than or equal to zero.");
    }

    SDL_SetWindowSize(self->win, w, h);

    Py_RETURN_NONE;
}

static PyObject *
window_get_size(pgWindowObject *self)
{
    int w, h;
    PyObject *out = PyTuple_New(2);

    SDL_GetWindowSize(self->win, &w, &h);
    PyTuple_SetItem(out, 0, PyLong_FromLong(w));
    PyTuple_SetItem(out, 1, PyLong_FromLong(h));

    return out;
}

static PyObject *
window_set_position(pgWindowObject *self, PyObject *arg)
{
    int x, y;

    if (Py_TYPE(arg) == &PyLong_Type) {
        x = y = PyLong_AsLong(arg);
        if (x != SDL_WINDOWPOS_CENTERED && x != SDL_WINDOWPOS_UNDEFINED) {
            return RAISE(PyExc_TypeError, "invalid position argument");
        }
    }
    else if (!pg_TwoIntsFromObj(arg, &x, &y)) {
        return RAISE(PyExc_TypeError, "invalid position argument");
    }

    SDL_SetWindowPosition(self->win, x, y);

    Py_RETURN_NONE;
}

static PyObject *
window_get_position(pgWindowObject *self)
{
    int x, h;
    PyObject *out = PyTuple_New(2);

    SDL_GetWindowPosition(self->win, &x, &h);
    PyTuple_SetItem(out, 0, PyLong_FromLong(x));
    PyTuple_SetItem(out, 1, PyLong_FromLong(h));

    return out;
}

static PyObject *
window_set_opacity(pgWindowObject *self, PyObject *arg)
{
    float opacity;
    opacity = (float)PyFloat_AsDouble(arg);
    if (PyErr_Occurred()) {
        return NULL;
    }
    if (SDL_SetWindowOpacity(self->win, opacity)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
window_get_opacity(pgWindowObject *self)
{
    float opacity;
    if (SDL_GetWindowOpacity(self->win, &opacity)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    return PyFloat_FromDouble(opacity);
}

static PyObject *
window_get_display_index(pgWindowObject *self)
{
    int index = SDL_GetWindowDisplayIndex(self->win);
    if (index < 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    return PyLong_FromLong(index);
}

static PyObject *
window_get_surface(pgWindowObject *self)
{
    PyObject *surf = NULL;
    SDL_Surface *_surf = SDL_GetWindowSurface(self->win);
    if (!_surf) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    surf = (PyObject *)pgSurface_New(_surf);
    if (!surf) {
        return NULL;
    }
    self->surf = (pgSurfaceObject *)surf;
    Py_INCREF(surf);
    return surf;
}

static int SDLCALL
_resize_event_watch(void *userdata, SDL_Event *event)
{
    pgWindowObject *item;
    SDL_Window *event_window;
    int i;
    if ((event->type != SDL_WINDOWEVENT))
        return 0;
    if (event->window.event != SDL_WINDOWEVENT_SIZE_CHANGED)
        return 0;
    event_window = SDL_GetWindowFromID(event->window.windowID);

    for (i = 0; i < PySequence_Size(_window_list); i++) {
        item = (pgWindowObject *)PySequence_GetItem(_window_list, i);
        Py_DECREF(item);
        if (item->win == event_window) {
            if (item->surf) {
                item->surf->surf = SDL_GetWindowSurface(item->win);
            }
            return 0;
        }
    }
    return 0;
}

#if SDL_VERSION_ATLEAST(2, 0, 16)
static PyObject *
window_set_always_on_top(pgWindowObject *self, PyObject *arg)
{
    int enable = PyObject_IsTrue(arg);
    if (enable == -1)
        return NULL;

    SDL_SetWindowAlwaysOnTop(self->win, enable);

    Py_RETURN_NONE;
}

static PyObject *
window_get_always_on_top(pgWindowObject *self)
{
    return PyBool_FromLong(SDL_GetWindowFlags(self->win) &
                           SDL_WINDOW_ALWAYS_ON_TOP);
}
#else
static PyObject *
window_set_always_on_top(pgWindowObject *self, PyObject *arg)
{
    if (PyErr_WarnEx(PyExc_Warning, "set_always_on_top() requires SDL 2.0.16+",
                     1) != 0) {
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject *
window_get_always_on_top(pgWindowObject *self)
{
    if (PyErr_WarnEx(PyExc_Warning, "get_always_on_top() requires SDL 2.0.16+",
                     1) != 0) {
        return NULL;
    }
    Py_RETURN_FALSE;
}
#endif  // SDL_VERSION_ATLEAST(2,0,16)

static PyObject *
window_get_wm_info(pgWindowObject *self)
{
    PyObject *dict;
    PyObject *tmp;
    SDL_SysWMinfo info;
    SDL_Window *win;

    VIDEO_INIT_CHECK();

    SDL_VERSION(&(info.version))
    dict = PyDict_New();
    if (!dict)
        return NULL;

    win = self->win;
    if (!SDL_GetWindowWMInfo(win, &info))
        return dict;

    (void)tmp;
#if defined(SDL_VIDEO_DRIVER_WINDOWS)
    tmp = PyLong_FromLongLong((long long)info.info.win.window);
    PyDict_SetItemString(dict, "window", tmp);
    Py_DECREF(tmp);

    tmp = PyLong_FromLongLong((long long)info.info.win.hdc);
    PyDict_SetItemString(dict, "hdc", tmp);
    Py_DECREF(tmp);
    tmp = PyLong_FromLongLong((long long)info.info.win.hinstance);
    PyDict_SetItemString(dict, "hinstance", tmp);
    Py_DECREF(tmp);
#endif
#if defined(SDL_VIDEO_DRIVER_WINRT)
    tmp = PyCapsule_New(info.info.winrt.window, "window", NULL);
    PyDict_SetItemString(dict, "window", tmp);
    Py_DECREF(tmp);
#endif
#if defined(SDL_VIDEO_DRIVER_X11)
    tmp = PyLong_FromLong(info.info.x11.window);
    PyDict_SetItemString(dict, "window", tmp);
    Py_DECREF(tmp);

    tmp = PyCapsule_New(info.info.x11.display, "display", NULL);
    PyDict_SetItemString(dict, "display", tmp);
    Py_DECREF(tmp);
#endif
#if defined(SDL_VIDEO_DRIVER_DIRECTFB)
    tmp = PyCapsule_New(info.info.dfb.dfb, "dfb", NULL);
    PyDict_SetItemString(dict, "dfb", tmp);
    Py_DECREF(tmp);

    tmp = PyCapsule_New(info.info.dfb.window, "window", NULL);
    PyDict_SetItemString(dict, "window", tmp);
    Py_DECREF(tmp);

    tmp = PyCapsule_New(info.info.dfb.surface, "surface", NULL);
    PyDict_SetItemString(dict, "surface", tmp);
    Py_DECREF(tmp);
#endif
#if defined(SDL_VIDEO_DRIVER_COCOA)
    tmp = PyCapsule_New(info.info.cocoa.window, "window", NULL);
    PyDict_SetItemString(dict, "window", tmp);
    Py_DECREF(tmp);
#endif
#if defined(SDL_VIDEO_DRIVER_UIKIT)
    tmp = PyCapsule_New(info.info.uikit.window, "window", NULL);
    PyDict_SetItemString(dict, "window", tmp);
    Py_DECREF(tmp);

    tmp = PyLong_FromLong(info.info.uikit.framebuffer);
    PyDict_SetItemString(dict, "framebuffer", tmp);
    Py_DECREF(tmp);

    tmp = PyLong_FromLong(info.info.uikit.colorbuffer);
    PyDict_SetItemString(dict, "colorbuffer", tmp);
    Py_DECREF(tmp);

    tmp = PyLong_FromLong(info.info.uikit.resolveFramebuffer);
    PyDict_SetItemString(dict, "resolveFramebuffer", tmp);
    Py_DECREF(tmp);
#endif
#if defined(SDL_VIDEO_DRIVER_WAYLAND)
    tmp = PyCapsule_New(info.info.wl.display, "display", NULL);
    PyDict_SetItemString(dict, "display", tmp);
    Py_DECREF(tmp);

    tmp = PyCapsule_New(info.info.wl.surface, "surface", NULL);
    PyDict_SetItemString(dict, "surface", tmp);
    Py_DECREF(tmp);

    tmp = PyCapsule_New(info.info.wl.shell_surface, "shell_surface", NULL);
    PyDict_SetItemString(dict, "shell_surface", tmp);
    Py_DECREF(tmp);
#endif
#if defined(SDL_VIDEO_DRIVER_ANDROID)
    tmp = PyCapsule_New(info.info.android.window, "window", NULL);
    PyDict_SetItemString(dict, "window", tmp);
    Py_DECREF(tmp);

    tmp = PyLong_FromLong((long)info.info.android.surface);
    PyDict_SetItemString(dict, "surface", tmp);
    Py_DECREF(tmp);
#endif
#if defined(SDL_VIDEO_DRIVER_VIVANTE)
    tmp = PyLong_FromLong((long)info.info.vivante.display);
    PyDict_SetItemString(dict, "display", tmp);
    Py_DECREF(tmp);

    tmp = PyLong_FromLong((long)info.info.vivante.window);
    PyDict_SetItemString(dict, "window", tmp);
    Py_DECREF(tmp);
#endif

    return dict;
}

#if SDL_VERSION_ATLEAST(2, 0, 16)
static PyObject *
window_flash(pgWindowObject *self, PyObject *args, PyObject *kwargs)
{
    SDL_bool briefly = SDL_FALSE;
    int op = SDL_FLASH_UNTIL_FOCUSED;
    char *kwids[] = {"briefly", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|p", kwids, &briefly)) {
        return NULL;
    }

    if (briefly)
        op = SDL_FLASH_BRIEFLY;

    if (SDL_FlashWindow(self->win, op)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
window_flash_cancel(pgWindowObject *self)
{
    if (SDL_FlashWindow(self->win, SDL_FLASH_CANCEL)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}
#else
static PyObject *
window_flash(pgWindowObject *self, PyObject *args, PyObject *kwargs)
{
    if (PyErr_WarnEx(PyExc_Warning, "flash() requires SDL 2.0.16+", 1) != 0) {
        return NULL;
    }
    Py_RETURN_NONE;
}
static PyObject *
window_flash_cancel(pgWindowObject *self)
{
    if (PyErr_WarnEx(PyExc_Warning, "flash_cancel() requires SDL 2.0.16+",
                     1) != 0) {
        return NULL;
    }
    Py_RETURN_NONE;
}

#endif  // SDL_VERSION_ATLEAST(2,0,16)

static void
window_dealloc(pgWindowObject *self)
{
    PyObject_Free(self);
}

static int
window_init(pgWindowObject *self, PyObject *args, PyObject *kwargs)
{
    char *title = "pygame window";
    PyObject *size = NULL;
    int size_w = 640, size_h = 480;
    PyObject *position = NULL;
    int pos_x = SDL_WINDOWPOS_UNDEFINED;
    int pos_y = SDL_WINDOWPOS_UNDEFINED;
    Uint32 flags = 0;
    SDL_Window *_win = NULL;

    Py_ssize_t dict_pos = 0;
    PyObject *_key, *_value, *_kw;
    const char *_key_str;
    char _exc_str[64];
    int _value_bool;

    _kw = PyDict_New();
    if (!_kw)
        return -1;

    if (kwargs) {
        while (PyDict_Next(kwargs, &dict_pos, &_key, &_value)) {
            if (!PyUnicode_Check(_key)) {
                PyErr_SetString(PyExc_TypeError, "keywords must be strings");
                return -1;
            }

            _key_str = PyUnicode_AsUTF8(_key);
            if (!_key_str)
                return -1;

            if (!strcmp(_key_str, "title") || !strcmp(_key_str, "size") ||
                !strcmp(_key_str, "position")) {
                PyDict_SetItem(_kw, _key, _value);
            }

            // handle **flags
            else {
                _value_bool = PyObject_IsTrue(_value);
                if (_value_bool == -1)
                    return -1;

                if (!strcmp(_key_str, "opengl")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_OPENGL;
                }
                else if (!strcmp(_key_str, "fullscreen")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_FULLSCREEN;
                }
                else if (!strcmp(_key_str, "fullscreen_desktop")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_FULLSCREEN_DESKTOP;
                }
                else if (!strcmp(_key_str, "hidden")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_HIDDEN;
                }
                else if (!strcmp(_key_str, "borderless")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_BORDERLESS;
                }
                else if (!strcmp(_key_str, "resizable")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_RESIZABLE;
                }
                else if (!strcmp(_key_str, "minimized")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_MINIMIZED;
                }
                else if (!strcmp(_key_str, "maximized")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_MAXIMIZED;
                }
                else if (!strcmp(_key_str, "mouse_grabbed")) {
                    if (_value_bool)
#if SDL_VERSION_ATLEAST(2, 0, 16)
                        flags |= SDL_WINDOW_MOUSE_GRABBED;
#else
                        flags |= SDL_WINDOW_INPUT_GRABBED;
#endif
                }
                else if (!strcmp(_key_str, "allow_high_dpi")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_ALLOW_HIGHDPI;
                }
                else if (!strcmp(_key_str, "mouse_capture")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_MOUSE_CAPTURE;
                }
                else if (!strcmp(_key_str, "always_on_top")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_ALWAYS_ON_TOP;
                }
                else if (!strcmp(_key_str, "skip_taskbar")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_SKIP_TASKBAR;
                }
                else if (!strcmp(_key_str, "utility")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_UTILITY;
                }
                else if (!strcmp(_key_str, "tooltip")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_TOOLTIP;
                }
                else if (!strcmp(_key_str, "popup_menu")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_POPUP_MENU;
                }
                else if (!strcmp(_key_str, "keyboard_grabbed")) {
                    if (_value_bool) {
#if SDL_VERSION_ATLEAST(2, 0, 16)
                        flags |= SDL_WINDOW_KEYBOARD_GRABBED;
#endif
                    }
                }
                else if (!strcmp(_key_str, "vulkan")) {
                    if (_value_bool)
                        flags |= SDL_WINDOW_VULKAN;
                }
                else if (!strcmp(_key_str, "metal")) {
                    if (_value_bool) {
#if SDL_VERSION_ATLEAST(2, 0, 14)
                        flags |= SDL_WINDOW_METAL;
#endif
                    }
                }
                else {
                    sprintf(_exc_str, "__init__ got an unexpected flag \'%s\'",
                            _key_str);
                    PyErr_SetString(PyExc_TypeError, _exc_str);
                    return -1;
                }
            }
        }
    }

    char *kwids[] = {"title", "size", "position", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, _kw, "|sOO", kwids, &title, &size,
                                     &position)) {
        return -1;
    }

    if (size) {
        if (!pg_TwoIntsFromObj(size, &size_w, &size_h)) {
            PyErr_SetString(PyExc_TypeError, "invalid size argument");
            return -1;
        }
    }

    if (size_w <= 0 || size_h <= 0) {
        PyErr_SetString(
            PyExc_ValueError,
            "width or height should not be less than or equal to zero.");
        return -1;
    }

    if (position) {
        if (Py_TYPE(position) == &PyLong_Type) {
            pos_x = pos_y = PyLong_AsLong(position);
            if (pos_x != SDL_WINDOWPOS_CENTERED &&
                pos_x != SDL_WINDOWPOS_UNDEFINED) {
                PyErr_SetString(PyExc_TypeError, "invalid positon argument");
                return -1;
            }
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
    self->surf = NULL;

    SDL_SetWindowData(_win, "pg_window", self);

    PyList_Append(_window_list, (PyObject *)self);

    return 0;
}

static PyObject *
window_from_display_module(PyTypeObject *cls)
{
    SDL_Window *window;
    int i;
    pgWindowObject *self, *tmp_window;
    window = pg_GetDefaultWindow();
    if (!window) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    for (i = 0; i < PySequence_Size(_window_list); i++) {
        tmp_window = (pgWindowObject *)PySequence_GetItem(_window_list, i);
        if (window == tmp_window->win) {
            return (PyObject *)tmp_window;
        }
        Py_DECREF(tmp_window);
    }
    self = (pgWindowObject *)(cls->tp_new(cls, NULL, NULL));
    self->win = window;
    self->is_from_display = SDL_TRUE;
    SDL_SetWindowData(window, "pg_window", self);
    PyList_Append(_window_list, (PyObject *)self);
    return (PyObject *)self;
}

static PyObject *
window_from_existing_window(PyTypeObject *cls, PyObject *arg)
{
    SDL_Window *window;
    pgWindowObject *self;
    long long hwnd;

    hwnd = PyLong_AsLongLong(arg);
    if (PyErr_Occurred()) {
        return NULL;
    }

    window = SDL_CreateWindowFrom((void *)hwnd);
    if (!window) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    self = (pgWindowObject *)(cls->tp_new(cls, NULL, NULL));
    self->win = window;
    self->is_from_display = SDL_FALSE;
    SDL_SetWindowData(window, "pg_window", self);
    PyList_Append(_window_list, (PyObject *)self);
    return (PyObject *)self;
}

static PyMethodDef window_methods[] = {
    {"destroy", (PyCFunction)window_destroy, METH_NOARGS,
     DOC_WINDOW_WINDOW_DESTROY},
    {"set_windowed", (PyCFunction)window_set_windowed, METH_NOARGS,
     DOC_WINDOW_WINDOW_SETWINDOWED},
    {"set_fullscreen", (PyCFunction)window_set_fullscreen,
     METH_VARARGS | METH_KEYWORDS, DOC_WINDOW_WINDOW_SETFULLSCREEN},
    {"focus", (PyCFunction)window_focus, METH_VARARGS | METH_KEYWORDS,
     DOC_WINDOW_WINDOW_FOCUS},
    {"hide", (PyCFunction)window_hide, METH_NOARGS, DOC_WINDOW_WINDOW_HIDE},
    {"show", (PyCFunction)window_show, METH_NOARGS, DOC_WINDOW_WINDOW_SHOW},
    {"restore", (PyCFunction)window_restore, METH_NOARGS,
     DOC_WINDOW_WINDOW_RESTORE},
    {"maximize", (PyCFunction)window_maximize, METH_NOARGS,
     DOC_WINDOW_WINDOW_MAXIMIZE},
    {"minimize", (PyCFunction)window_minimize, METH_NOARGS,
     DOC_WINDOW_WINDOW_MINIMIZE},
    {"flash", (PyCFunction)window_flash, METH_VARARGS | METH_KEYWORDS,
     DOC_WINDOW_WINDOW_FLASH},
    {"flash_cancel", (PyCFunction)window_flash_cancel, METH_NOARGS,
     DOC_WINDOW_WINDOW_FLASHCANCEL},
    {"set_modal_for", (PyCFunction)window_set_modal_for, METH_O,
     DOC_WINDOW_WINDOW_SETMODALFOR},
    {"update_from_surface", (PyCFunction)window_update_from_surface,
     METH_FASTCALL, DOC_WINDOW_WINDOW_UPDATEFROMSURFACE},
    {"set_icon", (PyCFunction)window_set_icon, METH_O, "docs_needed"},
    {"set_grab", (PyCFunction)window_set_grab, METH_O, "docs_needed"},
    {"get_grab", (PyCFunction)window_get_grab, METH_NOARGS, "docs_needed"},
    {"set_title", (PyCFunction)window_set_title, METH_O, "docs_needed"},
    {"get_title", (PyCFunction)window_get_title, METH_NOARGS, "docs_needed"},
    {"set_resizable", (PyCFunction)window_set_resizable, METH_O,
     "docs_needed"},
    {"get_resizable", (PyCFunction)window_get_resizable, METH_NOARGS,
     "docs_needed"},
    {"set_borderless", (PyCFunction)window_set_borderless, METH_O,
     "docs_needed"},
    {"get_borderless", (PyCFunction)window_get_borderless, METH_NOARGS,
     "docs_needed"},
    {"get_window_id", (PyCFunction)window_get_window_id, METH_NOARGS,
     "docs_needed"},
    {"set_size", (PyCFunction)window_set_size, METH_O, "docs_needed"},
    {"get_size", (PyCFunction)window_get_size, METH_NOARGS, "docs_needed"},
    {"set_position", (PyCFunction)window_set_position, METH_O, "docs_needed"},
    {"get_position", (PyCFunction)window_get_position, METH_NOARGS,
     "docs_needed"},
    {"set_opacity", (PyCFunction)window_set_opacity, METH_O, "docs_needed"},
    {"get_opacity", (PyCFunction)window_get_opacity, METH_NOARGS,
     "docs_needed"},
    {"get_display_index", (PyCFunction)window_get_display_index, METH_NOARGS,
     "docs_needed"},
    {"get_surface", (PyCFunction)window_get_surface, METH_NOARGS,
     "docs_needed"},
    {"set_always_on_top", (PyCFunction)window_set_always_on_top, METH_O,
     "docs_needed"},
    {"get_always_on_top", (PyCFunction)window_get_always_on_top, METH_NOARGS,
     "docs_needed"},
    {"get_wm_info", (PyCFunction)window_get_wm_info, METH_NOARGS,
     "docs_needed"},
    {"from_display_module", (PyCFunction)window_from_display_module,
     METH_CLASS | METH_NOARGS, "docs_needed"},
    {"from_existing_window", (PyCFunction)window_from_existing_window,
     METH_CLASS | METH_O, "docs_needed"},
    {NULL, NULL, 0, NULL}};

static PyTypeObject pgWindow_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame.window.Window",
    .tp_basicsize = sizeof(pgWindowObject),
    .tp_dealloc = (destructor)window_dealloc,
    .tp_doc = DOC_WINDOW_WINDOW,
    .tp_methods = window_methods,
    .tp_init = (initproc)window_init,
    .tp_new = PyType_GenericNew,
};

static PyMethodDef _window_methods[] = {
    {"get_grabbed_window", (PyCFunction)get_grabbed_window, METH_NOARGS,
     DOC_WINDOW_GETGRABBEDWINDOW},
    {"get_windows", (PyCFunction)get_windows, METH_NOARGS,
     DOC_WINDOW_GETWINDOWS},
    {NULL, NULL, 0, NULL}};

MODINIT_DEFINE(window)
{
    PyObject *module, *apiobj, *display_module;
    static void *c_api[PYGAMEAPI_WINDOW_NUMSLOTS];

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "window",
                                         DOC_WINDOW,
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

    import_pygame_rect();
    if (PyErr_Occurred()) {
        return NULL;
    }

    display_module = PyImport_ImportModule("pygame.display");
    if (!display_module) {
        return NULL;
    }
    _pg_display_quit = PyObject_GetAttrString(display_module, "quit");
    Py_DECREF(display_module);
    if (!_pg_display_quit) {
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

    SDL_AddEventWatch(_resize_event_watch, NULL);

    _dummy_surface =
        SDL_CreateRGBSurface(0, 1, 1, 24, 0xff0000, 0xff00, 0xff, 0);

    c_api[0] = &pgWindow_Type;
    apiobj = encapsulate_api(c_api, "window");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_XDECREF(_window_list);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}