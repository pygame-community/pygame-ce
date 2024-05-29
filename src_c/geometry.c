#include "rect.c"
#include "circle.c"
#include "geometry_common.c"

static PyMethodDef geometry_methods[] = {{NULL, NULL, 0, NULL}};

MODINIT_DEFINE(geometry)
{
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_GEOMETRY_NUMSLOTS];

    static struct PyModuleDef _module = {
        .m_base = PyModuleDef_HEAD_INIT,
        .m_name = "geometry",
        .m_doc = "Module for the Line, Circle and Polygon objects\n",
        .m_size = -1,
        .m_methods = geometry_methods,
    };

    import_pygame_base();
    if (PyErr_Occurred()) {
        return NULL;
    }

    if (PyType_Ready(&pgCircle_Type) < 0) {
        return NULL;
    }

    if (PyType_Ready(&pgRect_Type) < 0 || PyType_Ready(&pgFRect_Type) < 0) {
        return NULL;
    }

    module = PyModule_Create(&_module);
    if (!module) {
        return NULL;
    }

    Py_INCREF(&pgRect_Type);
    if (PyModule_AddObject(module, "RectType", (PyObject *)&pgRect_Type)) {
        Py_DECREF(&pgRect_Type);
        Py_DECREF(module);
        return NULL;
    }
    Py_INCREF(&pgRect_Type);
    if (PyModule_AddObject(module, "Rect", (PyObject *)&pgRect_Type)) {
        Py_DECREF(&pgRect_Type);
        Py_DECREF(module);
        return NULL;
    }
    Py_INCREF(&pgFRect_Type);
    if (PyModule_AddObject(module, "FRectType", (PyObject *)&pgFRect_Type)) {
        Py_DECREF(&pgFRect_Type);
        Py_DECREF(module);
        return NULL;
    }
    Py_INCREF(&pgFRect_Type);
    if (PyModule_AddObject(module, "FRect", (PyObject *)&pgFRect_Type)) {
        Py_DECREF(&pgFRect_Type);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&pgCircle_Type);
    if (PyModule_AddObject(module, "Circle", (PyObject *)&pgCircle_Type)) {
        Py_DECREF(&pgCircle_Type);
        Py_DECREF(module);
        return NULL;
    }

    c_api[0] = &pgRect_Type;
    c_api[1] = pgRect_New;
    c_api[2] = pgRect_New4;
    c_api[3] = pgRect_FromObject;
    c_api[4] = pgRect_Normalize;
    c_api[5] = &pgFRect_Type;
    c_api[6] = pgFRect_New;
    c_api[7] = pgFRect_New4;
    c_api[8] = pgFRect_FromObject;
    c_api[9] = pgFRect_Normalize;
    c_api[10] = &pgCircle_Type;
    apiobj = encapsulate_api(c_api, "geometry");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}
