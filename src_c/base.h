#define NO_PYGAME_C_API
#define PYGAMEAPI_BASE_INTERNAL

#include "pygame.h"

#include <signal.h>
#include "doc/pygame_doc.h"
#include "pgarrinter.h"
#include "pgcompat.h"

/* This file controls all the initialization of
 * the module and the various SDL subsystems
 */

/*platform specific init stuff*/

#ifdef MS_WIN32 /*python gives us MS_WIN32*/
#define WIN32_LEAN_AND_MEAN
#define VC_EXTRALEAN
#include <windows.h>
extern int
SDL_RegisterApp(const char *, Uint32, void *);
#endif

#if defined(macintosh)
#if (!defined(__MWERKS__) && !TARGET_API_MAC_CARBON)
QDGlobals pg_qd;
#endif
#endif

#if SDL_BYTEORDER == SDL_LIL_ENDIAN
#define PAI_MY_ENDIAN '<'
#define PAI_OTHER_ENDIAN '>'
#define BUF_OTHER_ENDIAN '>'
#else
#define PAI_MY_ENDIAN '>'
#define PAI_OTHER_ENDIAN '<'
#define BUF_OTHER_ENDIAN '<'
#endif
#define BUF_MY_ENDIAN '='

/* Extended array struct */
typedef struct pg_capsule_interface_s {
    PyArrayInterface inter;
    Py_intptr_t imem[1];
} pgCapsuleInterface;

/* Py_buffer internal data for an array interface/struct */
typedef struct pg_view_internals_s {
    char format[4]; /* make 4 byte word sized */
    Py_ssize_t imem[1];
} pgViewInternals;

static void
pg_install_parachute(void);
static void
pg_uninstall_parachute(void);
static void
pg_atexit_quit(void);
static int
pgGetArrayStruct(PyObject *, PyObject **, PyArrayInterface **);
static PyObject *
pgArrayStruct_AsDict(PyArrayInterface *);
static PyObject *
pgBuffer_AsArrayInterface(Py_buffer *);
static PyObject *
pgBuffer_AsArrayStruct(Py_buffer *);
static int
_pg_buffer_is_byteswapped(Py_buffer *);
static void
pgBuffer_Release(pg_buffer *);
static int
pgObject_GetBuffer(PyObject *, pg_buffer *, int);
static inline PyObject *
pgObject_getRectHelper(PyObject *, PyObject *const *, Py_ssize_t, PyObject *,
                       char *);
static int
pgGetArrayInterface(PyObject **, PyObject *);
static int
pgArrayStruct_AsBuffer(pg_buffer *, PyObject *, PyArrayInterface *, int);
static int
_pg_arraystruct_as_buffer(Py_buffer *, PyObject *, PyArrayInterface *, int);
static int
_pg_arraystruct_to_format(char *, PyArrayInterface *, int);
static int
pgDict_AsBuffer(pg_buffer *, PyObject *, int);
static int
_pg_shape_check(PyObject *);
static int
_pg_typestr_check(PyObject *);
static int
_pg_strides_check(PyObject *);
static int
_pg_data_check(PyObject *);
int
_pg_is_int_tuple(PyObject *);
static int
_pg_values_as_buffer(Py_buffer *, int, PyObject *, PyObject *, PyObject *,
                     PyObject *);
static int
_pg_int_tuple_as_ssize_arr(PyObject *, Py_ssize_t *);
static int
_pg_typestr_as_format(PyObject *, char *, Py_ssize_t *);
static PyObject *
pg_view_get_typestr_obj(Py_buffer *);
static PyObject *
pg_view_get_shape_obj(Py_buffer *);
static PyObject *
pg_view_get_strides_obj(Py_buffer *);
static PyObject *
pg_view_get_data_obj(Py_buffer *);
static char
_pg_as_arrayinter_typekind(Py_buffer *);
static char
_pg_as_arrayinter_byteorder(Py_buffer *);
static int
_pg_as_arrayinter_flags(Py_buffer *);
static pgCapsuleInterface *
_pg_new_capsuleinterface(Py_buffer *);
static void
_pg_capsule_PyMem_Free(PyObject *);
static PyObject *
_pg_shape_as_tuple(PyArrayInterface *);
static PyObject *
_pg_typekind_as_str(PyArrayInterface *);
static PyObject *
_pg_strides_as_tuple(PyArrayInterface *);
static PyObject *
_pg_data_as_tuple(PyArrayInterface *);
static PyObject *
pg_get_array_interface(PyObject *, PyObject *);
static void
_pg_release_buffer_array(Py_buffer *);
static void
_pg_release_buffer_generic(Py_buffer *);
static SDL_Window *
pg_GetDefaultWindow(void);
static void
pg_SetDefaultWindow(SDL_Window *);
static pgSurfaceObject *
pg_GetDefaultWindowSurface(void);
static void
pg_SetDefaultWindowSurface(pgSurfaceObject *);
static int
pg_EnvShouldBlendAlphaSDL2(void);
static int
pg_CheckSDLVersions(void);
void
pg_RegisterQuit(void (*func)(void));
static PyObject *
pg_register_quit(PyObject *self, PyObject *value);
static int
pg_mod_autoinit(const char *modname);
static void
pg_mod_autoquit(const char *modname);
static PyObject *
pg_init(PyObject *self, PyObject *_null);
static PyObject *
pg_get_sdl_version(PyObject *self, PyObject *args, PyObject *kwargs);
static PyObject *
pg_get_sdl_byteorder(PyObject *self, PyObject *_null);
static void
_pg_quit(void);
static PyObject *
pg_quit(PyObject *self, PyObject *_null);
static PyObject *
pg_base_get_init(PyObject *self, PyObject *_null);
/* internal C API utility functions */
static int
pg_IntFromObj(PyObject *obj, int *val);
static int
pg_IntFromObjIndex(PyObject *obj, int _index, int *val);
static int
pg_TwoIntsFromObj(PyObject *obj, int *val1, int *val2);
static int
pg_FloatFromObj(PyObject *obj, float *val);
static int
pg_FloatFromObjIndex(PyObject *obj, int _index, float *val);
static int
pg_TwoFloatsFromObj(PyObject *obj, float *val1, float *val2);
static inline int
pg_DoubleFromObj(PyObject *obj, double *val);
/*Assumes obj is a Sequence, internal or conscious use only*/
static inline int
_pg_DoubleFromObjIndex(PyObject *obj, int index, double *val);
static inline int
pg_TwoDoublesFromObj(PyObject *obj, double *val1, double *val2);
static inline int
pg_TwoDoublesFromFastcallArgs(PyObject *const *args, Py_ssize_t nargs,
                              double *val1, double *val2);
static int
pg_UintFromObj(PyObject *obj, Uint32 *val);
static int
pg_UintFromObjIndex(PyObject *obj, int _index, Uint32 *val);
/* You probably want to use the pg_RGBAFromObjEx function instead of this. */
static int
pg_RGBAFromObj(PyObject *obj, Uint8 *RGBA);
static PyObject *
pg_get_error(PyObject *self, PyObject *_null);
static PyObject *
pg_set_error(PyObject *s, PyObject *args);
/*error signal handlers(replacing SDL parachute)*/
static void
pygame_parachute(int sig);
static void
pg_SetDefaultConvertFormat(PG_PixelFormatEnum format);
static PG_PixelFormatEnum
pg_GetDefaultConvertFormat(void);

MODINIT_DEFINE(base);
