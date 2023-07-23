#include "pygame.h"

#include "pgcompat.h"

#include "doc/system_doc.h"

static PyObject *
pg_system_get_cpu_instruction_sets(PyObject *self, PyObject *_null)
{
    PyObject *tmp_bool = NULL;
    PyObject *instruction_sets = NULL;

    instruction_sets = PyDict_New();
    if (!instruction_sets) {
        goto error;
    }

#define INSERT_INSTRUCTIONSET_INFO(name, SDL_fn_name)               \
    tmp_bool = PyBool_FromLong((SDL_fn_name)());                    \
    if (PyDict_SetItemString(instruction_sets, (name), tmp_bool)) { \
        Py_DECREF(tmp_bool);                                        \
        goto error;                                                 \
    }                                                               \
    Py_DECREF(tmp_bool);

    INSERT_INSTRUCTIONSET_INFO("RDTSC", SDL_HasRDTSC);
    INSERT_INSTRUCTIONSET_INFO("ALTIVEC", SDL_HasAltiVec);
    INSERT_INSTRUCTIONSET_INFO("MMX", SDL_HasMMX);
    INSERT_INSTRUCTIONSET_INFO("SSE", SDL_HasSSE);
    INSERT_INSTRUCTIONSET_INFO("SSE2", SDL_HasSSE2);
    INSERT_INSTRUCTIONSET_INFO("SSE3", SDL_HasSSE3);
    INSERT_INSTRUCTIONSET_INFO("SSE41", SDL_HasSSE41);
    INSERT_INSTRUCTIONSET_INFO("SSE42", SDL_HasSSE42);
    INSERT_INSTRUCTIONSET_INFO("AVX", SDL_HasAVX);
    INSERT_INSTRUCTIONSET_INFO("AVX2", SDL_HasAVX2);
    INSERT_INSTRUCTIONSET_INFO("AVX512F", SDL_HasAVX512F);
    INSERT_INSTRUCTIONSET_INFO("NEON", SDL_HasNEON);
#if SDL_VERSION_ATLEAST(2, 0, 12)
    INSERT_INSTRUCTIONSET_INFO("ARMSIMD", SDL_HasARMSIMD);
#else
    if (PyDict_SetItemString(instruction_sets, "ARMSIMD", Py_False))
        goto error;
#endif
#if SDL_VERSION_ATLEAST(2, 24, 0)
    INSERT_INSTRUCTIONSET_INFO("LSX", SDL_HasLSX);
    INSERT_INSTRUCTIONSET_INFO("LASX", SDL_HasLASX);
#else
    if (PyDict_SetItemString(instruction_sets, "LSX", Py_False))
        goto error;
    if (PyDict_SetItemString(instruction_sets, "LASX", Py_False))
        goto error;
#endif

#undef INSERT_INSTRUCTIONSET_INFO

    return instruction_sets;

error:
    Py_XDECREF(instruction_sets);
    return NULL;
}

static PyObject *
pg_system_get_total_ram(PyObject *self, PyObject *_null)
{
    return PyLong_FromLong(SDL_GetSystemRAM());
}

static PyObject *
pg_system_get_pref_path(PyObject *self, PyObject *args, PyObject *kwargs)
{
    char *org, *project;
    static char *kwids[] = {"org", "app", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "ss", kwids, &org,
                                     &project)) {
        return NULL;
    }

    char *path = SDL_GetPrefPath(org, project);
    if (path == NULL) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    PyObject *ret = PyUnicode_FromString(path);
    SDL_free(path);

    return ret;
}

static PyObject *
pg_system_get_pref_locales(PyObject *self, PyObject *_null)
{
    PyObject *ret_list = PyList_New(0);
    if (!ret_list) {
        return NULL;
    }

#if SDL_VERSION_ATLEAST(2, 0, 14)
    PyObject *dict, *val = NULL;
    SDL_Locale *locales = SDL_GetPreferredLocales();
    if (!locales) {
        /* Return an empty list if SDL function does not return any useful
         * information */
        return ret_list;
    }

    SDL_Locale *current_locale = locales;

    /* The array is terminated when the language attribute of the last struct
     * in the array is NULL */
    while (current_locale->language) {
        dict = PyDict_New();
        if (!dict) {
            goto error;
        }

        val = PyUnicode_FromString(current_locale->language);
        if (!val) {
            goto error;
        }
        if (PyDict_SetItemString(dict, "language", val)) {
            goto error;
        }
        Py_DECREF(val);

        if (current_locale->country) {
            val = PyUnicode_FromString(current_locale->country);
            if (!val) {
                goto error;
            }
        }
        else {
            Py_INCREF(Py_None);
            val = Py_None;
        }
        if (PyDict_SetItemString(dict, "country", val)) {
            goto error;
        }
        Py_DECREF(val);

        /* reset val to NULL because goto XDECREF's this */
        val = NULL;
        if (PyList_Append(ret_list, dict)) {
            goto error;
        }
        Py_DECREF(dict);
        current_locale++;
    }

    SDL_free(locales);
    return ret_list;
error:
    Py_XDECREF(val);
    Py_XDECREF(dict);
    SDL_free(locales);
    Py_DECREF(ret_list);
    return NULL;
#else
    return ret_list;
#endif
}

static PyMethodDef _system_methods[] = {
    {"get_cpu_instruction_sets", pg_system_get_cpu_instruction_sets,
     METH_NOARGS, DOC_SYSTEM_GETCPUINSTRUCTIONSETS},
    {"get_total_ram", pg_system_get_total_ram, METH_NOARGS,
     DOC_SYSTEM_GETTOTALRAM},
    {"get_pref_path", (PyCFunction)pg_system_get_pref_path,
     METH_VARARGS | METH_KEYWORDS, DOC_SYSTEM_GETPREFPATH},
    {"get_pref_locales", pg_system_get_pref_locales, METH_NOARGS,
     DOC_SYSTEM_GETPREFLOCALES},
    {NULL, NULL, 0, NULL}};

MODINIT_DEFINE(system)
{
    PyObject *module;
    static struct PyModuleDef _module = {
        .m_base = PyModuleDef_HEAD_INIT,
        .m_name = "system",
        .m_doc = DOC_SYSTEM,
        .m_size = -1,
        .m_methods = _system_methods,
    };

    /* need to import base module, just so SDL is happy. Do this first so if
       the module is there is an error the module is not loaded.
    */
    import_pygame_base();
    if (PyErr_Occurred()) {
        return NULL;
    }

    /* create the module */
    module = PyModule_Create(&_module);
    if (!module) {
        return NULL;
    }

    return module;
}
