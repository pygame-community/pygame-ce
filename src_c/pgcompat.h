/* Python 2.x/3.x compatibility tools (internal)
 */
#ifndef PGCOMPAT_INTERNAL_H
#define PGCOMPAT_INTERNAL_H

#include "include/pgcompat.h"

#include <string.h>

/* Return the unqualified runtime type name used by pygame repr strings. */
static inline const char *
pgObject_TypeName(PyObject *obj)
{
    const char *type_name = Py_TYPE(obj)->tp_name;
    const char *short_name = strrchr(type_name, '.');

    return short_name ? short_name + 1 : type_name;
}

/* Module init function returns new module instance. */
#define MODINIT_DEFINE(mod_name) PyMODINIT_FUNC PyInit_##mod_name(void)

/* Defaults for unicode file path encoding */
#if defined(MS_WIN32)
#define UNICODE_DEF_FS_ERROR "replace"
#else
#define UNICODE_DEF_FS_ERROR "surrogateescape"
#endif

#define RELATIVE_MODULE(m) ("." m)

#endif /* ~PGCOMPAT_INTERNAL_H */
