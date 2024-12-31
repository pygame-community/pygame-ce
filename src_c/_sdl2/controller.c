
#include "../pgcompat.h"
#include "../pygame.h"
#include "structmember.h"

#include "../doc/sdl2_controller_doc.h"
#define CONTROLLER_INIT_CHECK()                \
    if (!SDL_WasInit(SDL_INIT_GAMECONTROLLER)) \
        return RAISE(pgExc_SDLError, "Controller system not initialized");

typedef struct pgControllerObject {
    PyObject_HEAD int id;
    char *name;
    SDL_GameController *controller;

    struct pgControllerObject *next;
} pgControllerObject;

static pgControllerObject *_first_controller = NULL;

#if defined(_MSC_VER)
#define strtok_r strtok_s
#endif

static PyObject *
controller_module_init(PyObject *module, PyObject *_null)
{
    if (!SDL_WasInit(SDL_INIT_GAMECONTROLLER)) {
        if (SDL_InitSubSystem(SDL_INIT_GAMECONTROLLER)) {
            return RAISE(pgExc_SDLError, SDL_GetError());
        }
    }
    SDL_GameControllerEventState(SDL_ENABLE);

    Py_RETURN_NONE;
}

static PyObject *
controller_module_quit(PyObject *module, PyObject *_null)
{
    pgControllerObject *cur = _first_controller;

    while (cur) {
        if (cur->controller) {
            SDL_GameControllerClose(cur->controller);
            cur->controller = NULL;
        }
        cur = cur->next;
    }

    if (SDL_WasInit(SDL_INIT_GAMECONTROLLER)) {
        SDL_QuitSubSystem(SDL_INIT_GAMECONTROLLER);
    }
    Py_RETURN_NONE;
}

static void
_controller_module_auto_quit(void)
{
    controller_module_quit(NULL, NULL);
}

static PyObject *
controller_module_get_init(PyObject *module, PyObject *_null)
{
    return PyBool_FromLong(SDL_WasInit(SDL_INIT_GAMECONTROLLER) != 0);
}

static PyObject *
controller_module_is_controller(PyObject *module, PyObject *args,
                                PyObject *kwargs)
{
    int device_index;
    static char *keywords[] = {"device_index", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "i", keywords,
                                     &device_index)) {
        return NULL;
    }

    CONTROLLER_INIT_CHECK();

    return PyBool_FromLong(SDL_IsGameController(device_index));
}

static PyObject *
controller_module_get_count(PyObject *module, PyObject *_null)
{
    CONTROLLER_INIT_CHECK();

    int count = SDL_NumJoysticks();
    if (count < 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return PyLong_FromLong(count);
}

static PyMethodDef _controller_module_methods[] = {
    {"init", (PyCFunction)controller_module_init, METH_NOARGS,
     DOC_SDL2_CONTROLLER_INIT},
    {"quit", (PyCFunction)controller_module_quit, METH_NOARGS,
     DOC_SDL2_CONTROLLER_QUIT},
    {"get_init", (PyCFunction)controller_module_get_init, METH_NOARGS,
     DOC_SDL2_CONTROLLER_GETINIT},
    {"is_controller", (PyCFunction)controller_module_is_controller,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_CONTROLLER_ISCONTROLLER},
    {"get_count", (PyCFunction)controller_module_get_count, METH_NOARGS,
     DOC_SDL2_CONTROLLER_GETCOUNT},
    {NULL, NULL, 0, NULL}};

static PyObject *
controller_from_joystick(PyTypeObject *subtype, PyObject *args,
                         PyObject *kwargs)
{
    pgJoystickObject *joy;
    static char *keywords[] = {"joystick", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", keywords,
                                     &pgJoystick_Type, &joy)) {
        return NULL;
    }

    CONTROLLER_INIT_CHECK();
    return PyObject_CallFunction((PyObject *)subtype, "i", joy->id);
}

static int
controller_init(pgControllerObject *, PyObject *, PyObject *);

static PyObject *
controller_init_func(pgControllerObject *self)
{
    if (controller_init(self, NULL, NULL) == -1) {
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject *
controller_get_init(pgControllerObject *self, PyObject *_null)
{
    CONTROLLER_INIT_CHECK();
    return PyBool_FromLong(self->controller != NULL);
}

static PyObject *
controller_quit(pgControllerObject *self, PyObject *_null)
{
    CONTROLLER_INIT_CHECK();
    if (self->controller) {
        SDL_GameControllerClose(self->controller);
        self->controller = NULL;
    }
    Py_RETURN_NONE;
}

static PyObject *
controller_attached(pgControllerObject *self, PyObject *_null)
{
    CONTROLLER_INIT_CHECK();
    if (!self->controller) {
        return RAISE(pgExc_SDLError, "Controller is not initialized");
    }

    return PyBool_FromLong(SDL_GameControllerGetAttached(self->controller));
}

static PyObject *
controller_as_joystick(pgControllerObject *self, PyObject *_null)
{
    CONTROLLER_INIT_CHECK();
    JOYSTICK_INIT_CHECK();
    if (!self->controller) {
        return RAISE(pgExc_SDLError, "Controller is not initialized");
    }

    return pgJoystick_New(self->id);
}

static PyObject *
controller_get_axis(pgControllerObject *self, PyObject *args, PyObject *kwargs)
{
    int axis;
    static char *keywords[] = {"axis", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "i", keywords, &axis)) {
        return NULL;
    }
    CONTROLLER_INIT_CHECK();
    if (!self->controller) {
        return RAISE(pgExc_SDLError, "Controller is not initialized");
    }

    if (axis < 0 || axis > SDL_CONTROLLER_AXIS_MAX - 1) {
        return RAISE(pgExc_SDLError, "Invalid axis");
    }

    return PyLong_FromLong(SDL_GameControllerGetAxis(self->controller, axis));
}

static PyObject *
controller_get_button(pgControllerObject *self, PyObject *args,
                      PyObject *kwargs)
{
    int button;
    static char *keywords[] = {"button", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "i", keywords, &button)) {
        return NULL;
    }
    CONTROLLER_INIT_CHECK();
    if (!self->controller) {
        return RAISE(pgExc_SDLError, "Controller is not initialized");
    }

    if (button < 0 || button > SDL_CONTROLLER_BUTTON_MAX) {
        return RAISE(pgExc_SDLError, "Invalid button");
    }

    return PyBool_FromLong(
        SDL_GameControllerGetButton(self->controller, button));
}

static PyObject *
controller_get_mapping(pgControllerObject *self, PyObject *_null)
{
    char *mapping, *key, *value;
    char *token, *saveptr = NULL;
    PyObject *dict, *value_obj = NULL;

    CONTROLLER_INIT_CHECK();
    if (!self->controller) {
        return RAISE(pgExc_SDLError, "Controller is not initialized");
    }

    mapping = SDL_GameControllerMapping(self->controller);
    if (!mapping) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    dict = PyDict_New();
    if (!dict) {
        goto err;
    }

    token = strtok_r(mapping, ",", &saveptr);
    while (token != NULL) {
        key = strtok_r(token, ":", &value);

        if (value != NULL && value[0] != '\0') {
            value_obj = PyUnicode_FromString(value);
            if (!value_obj) {
                goto err;
            }
            if (PyDict_SetItemString(dict, key, value_obj)) {
                goto err;
            }
            Py_DECREF(value_obj);
        }
        token = strtok_r(NULL, ",", &saveptr);
    }

    SDL_free(saveptr);
    SDL_free(mapping);
    return dict;

err:
    Py_XDECREF(value_obj);
    Py_XDECREF(dict);
    SDL_free(mapping);
    SDL_free(saveptr);
    return NULL;
}

static PyObject *
controller_set_mapping(pgControllerObject *self, PyObject *args,
                       PyObject *kwargs)
{
    PyObject *dict;
    static char *keywords[] = {"mapping", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", keywords,
                                     &PyDict_Type, &dict)) {
        return NULL;
    }

    CONTROLLER_INIT_CHECK();
    if (!self->controller) {
        return RAISE(pgExc_SDLError, "Controller is not initialized");
    }

    char guid_str[64];
    SDL_Joystick *joy = SDL_GameControllerGetJoystick(self->controller);
    SDL_JoystickGetGUIDString(SDL_JoystickGetGUID(joy), guid_str, 63);

    PyObject *key, *value;
    const char *key_str, *value_str;
    Py_ssize_t dict_index = 0;
    int offset = 0, size = 512;
    char *mapping = malloc(size * sizeof(char));
    if (mapping == NULL) {
        return PyErr_NoMemory();
    }

    while (PyDict_Next(dict, &dict_index, &key, &value)) {
        if (!PyUnicode_Check(key) || !PyUnicode_Check(value)) {
            free(mapping);
            return RAISE(PyExc_TypeError, "Dict items must be strings");
        }

        key_str = PyUnicode_AsUTF8(key);
        value_str = PyUnicode_AsUTF8(value);
        if (key_str == NULL || value_str == NULL) {
            free(mapping);
            return NULL;
        }

        int res = SDL_snprintf(mapping + offset, size - offset, ",%s:%s",
                               key_str, value_str);
        if (res < 0) {
            free(mapping);
            return RAISE(PyExc_RuntimeError, "Internal snprintf call failed");
        }
        else if (res >= size - offset) {
            // Retry the same key value pair with more memory allocated
            dict_index -= 1;
            size *= 2;
            mapping = realloc(mapping, size);
            if (mapping == NULL) {
                return PyErr_NoMemory();
            }
            continue;
        }
        offset += res;
    }

    int res_size = offset + 64 + (int)SDL_strlen(self->name);
    char *mapping_string = malloc(res_size * sizeof(char));
    SDL_snprintf(mapping_string, res_size, "%s,%s%s", guid_str, self->name,
                 mapping);

    int res = SDL_GameControllerAddMapping(mapping_string);
    free(mapping);
    free(mapping_string);

    if (res < 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return PyLong_FromLong(res);
}

static PyObject *
controller_rumble(pgControllerObject *self, PyObject *args, PyObject *kwargs)
{
    double low_freq, high_freq;
    Uint32 duration;
    static char *keywords[] = {"low_frequency", "high_frequency", "duration",
                               NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "ddI", keywords, &low_freq,
                                     &high_freq, &duration)) {
        return NULL;
    }

    CONTROLLER_INIT_CHECK();
    if (!self->controller) {
        return RAISE(pgExc_SDLError, "Controller is not initialized");
    }

    // rumble takes values in range 0 to 0xFFFF (65535)
    low_freq = MAX(MIN(low_freq, 1.0f), 0.0f) * 65535;
    high_freq = MAX(MIN(high_freq, 1.0f), 0.0f) * 65535;

    int success = SDL_GameControllerRumble(self->controller, (Uint16)low_freq,
                                           (Uint16)high_freq, duration);

    return PyBool_FromLong(success == 0);
}

static PyObject *
controller_stop_rumble(pgControllerObject *self, PyObject *_null)
{
    CONTROLLER_INIT_CHECK();
    if (!self->controller) {
        return RAISE(pgExc_SDLError, "Controller is not initialized");
    }
    SDL_GameControllerRumble(self->controller, 0, 0, 1);
    Py_RETURN_NONE;
}

static PyMethodDef controller_methods[] = {
    {"from_joystick", (PyCFunction)controller_from_joystick,
     METH_CLASS | METH_VARARGS | METH_KEYWORDS,
     DOC_SDL2_CONTROLLER_CONTROLLER_FROMJOYSTICK},
    {"get_init", (PyCFunction)controller_get_init, METH_NOARGS,
     DOC_SDL2_CONTROLLER_CONTROLLER_GETINIT},
    {"init", (PyCFunction)controller_init_func, METH_NOARGS,
     DOC_SDL2_CONTROLLER_CONTROLLER_INIT},
    {"quit", (PyCFunction)controller_quit, METH_NOARGS,
     DOC_SDL2_CONTROLLER_CONTROLLER_QUIT},
    {"attached", (PyCFunction)controller_attached, METH_NOARGS,
     DOC_SDL2_CONTROLLER_CONTROLLER_ATTACHED},
    {"as_joystick", (PyCFunction)controller_as_joystick, METH_NOARGS,
     DOC_SDL2_CONTROLLER_CONTROLLER_ASJOYSTICK},
    {"get_axis", (PyCFunction)controller_get_axis,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_CONTROLLER_CONTROLLER_ASJOYSTICK},
    {"get_button", (PyCFunction)controller_get_button,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_CONTROLLER_CONTROLLER_GETBUTTON},
    {"get_mapping", (PyCFunction)controller_get_mapping, METH_NOARGS,
     DOC_SDL2_CONTROLLER_CONTROLLER_GETMAPPING},
    {"set_mapping", (PyCFunction)controller_set_mapping,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_CONTROLLER_CONTROLLER_SETMAPPING},
    {"rumble", (PyCFunction)controller_rumble, METH_VARARGS | METH_KEYWORDS,
     DOC_SDL2_CONTROLLER_CONTROLLER_RUMBLE},
    {"stop_rumble", (PyCFunction)controller_stop_rumble, METH_NOARGS,
     DOC_SDL2_CONTROLLER_CONTROLLER_STOPRUMBLE},
    {NULL, NULL, 0, NULL}};

static PyMemberDef controller_members[] = {
    {"id", T_INT, offsetof(pgControllerObject, id), READONLY,
     "Gets the id of the controller"},
    {"name", T_STRING, offsetof(pgControllerObject, name), READONLY,
     "Gets the name of the controller"},
    {NULL},
};

static PyObject *
controller_new(PyTypeObject *subtype, PyObject *args, PyObject *kwargs)
{
    int id;
    pgControllerObject *self, *cur;
    static char *keywords[] = {"device_index", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "i", keywords, &id)) {
        return NULL;
    }

    CONTROLLER_INIT_CHECK();

    if (id >= SDL_NumJoysticks() || !SDL_IsGameController(id)) {
        return RAISE(pgExc_SDLError, "Invalid index");
    }

    SDL_GameController *controller = SDL_GameControllerOpen(id);
    if (!controller) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    cur = _first_controller;
    while (cur) {
        if (cur->controller == controller) {
            Py_INCREF(cur);
            return (PyObject *)cur;
        }

        if (!cur->next) {
            break;
        }

        cur = cur->next;
    }
    self = PyObject_New(pgControllerObject, subtype);
    if (!self) {
        return NULL;
    }

    if (!_first_controller) {
        _first_controller = self;
    }
    else {
        cur->next = self;
    }
    self->next = NULL;
    self->controller = controller;
    self->id = id;
    self->name = NULL;
    return (PyObject *)self;
}

static int
controller_init(pgControllerObject *self, PyObject *args, PyObject *kwargs)
{
    SDL_GameController *controller;

    if (self->controller == NULL) {
        controller = SDL_GameControllerOpen(self->id);
        if (controller == NULL) {
            PyErr_SetString(pgExc_SDLError, SDL_GetError());
            return -1;
        }
        self->controller = controller;
    }

    if (self->name) {
        free(self->name);
    }
    self->name = strdup(SDL_GameControllerName(self->controller));

    return 0;
}

void
controller_dealloc(pgControllerObject *self)
{
    pgControllerObject *cur, *prev;
    if (self->controller && SDL_GameControllerGetAttached(self->controller)) {
        SDL_GameControllerClose(self->controller);
    }
    self->controller = NULL;
    free(self->name);

    cur = _first_controller;
    prev = NULL;
    while (cur) {
        if (cur == self) {
            if (!prev) {
                _first_controller = self->next;
                break;
            }
            prev->next = self->next;
            break;
        }

        prev = cur;
        cur = cur->next;
    }
    PyObject_DEL(self);
}

static PyTypeObject pgController_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "Controller",
    .tp_basicsize = sizeof(pgControllerObject),
    .tp_doc = DOC_SDL2_CONTROLLER_CONTROLLER,
    .tp_new = controller_new,
    .tp_init = (initproc)controller_init,
    .tp_dealloc = (destructor)controller_dealloc,
    .tp_methods = controller_methods,
    .tp_members = controller_members,
};

/* TODO: multiphase init
#if PY_VERSION_HEX >= 0x030D0000
static struct PyModuleDef_Slot mod_controller_slots[] = {
    {Py_mod_gil, Py_MOD_GIL_NOT_USED},
    {0, NULL}
};
#endif
*/

MODINIT_DEFINE(controller)
{
    PyObject *module;

    static struct PyModuleDef _module = {
        .m_base = PyModuleDef_HEAD_INIT,
        .m_name = "controller",
        .m_doc = DOC_SDL2_CONTROLLER,
        .m_size = -1,
        .m_methods = _controller_module_methods,
/*
#if PY_VERSION_HEX >= 0x030D0000
        .m_slots = mod_controller_slots,
#endif
*/
    };

    import_pygame_base();
    if (PyErr_Occurred()) {
        return NULL;
    }

    import_pygame_joystick();
    if (PyErr_Occurred()) {
        return NULL;
    }

    module = PyModule_Create(&_module);
#if Py_GIL_DISABLED
#if (defined(__EMSCRIPTEN__) || defined(__wasi__))
    PyUnstable_Module_SetGIL(module, Py_MOD_GIL_NOT_USED);
#endif
#endif
    if (!module) {
        return NULL;
    }

    if (PyType_Ready(&pgController_Type) < 0) {
        return NULL;
    }

    Py_INCREF(&pgController_Type);
    if (PyModule_AddObject(module, "Controller",
                           (PyObject *)&pgController_Type)) {
        Py_DECREF(&pgController_Type);
        Py_DECREF(module);
        return NULL;
    }

    /* note: whenever this module gets released from _sdl2, base.c _pg_quit
     * should should quit the controller module automatically, instead of
     * doing this */
    pg_RegisterQuit(_controller_module_auto_quit);

    return module;
}
