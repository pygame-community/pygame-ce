/*
  pygame-ce - Python Game Library
  Copyright (C) 2000-2001  Pete Shinners

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Library General Public
  License as published by the Free Software Foundation; either
  version 2 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Library General Public License for more details.

  You should have received a copy of the GNU Library General Public
  License along with this library; if not, write to the Free
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

  Pete Shinners
  pete@shinners.org
*/

/*
 *  SDL_RWops support for python objects
 */
#define NO_PYGAME_C_API
#define PYGAMEAPI_RWOBJECT_INTERNAL
#include "pygame.h"

#include "pgcompat.h"

#include "doc/pygame_doc.h"

typedef struct {
    PyObject *read;
    PyObject *write;
    PyObject *seek;
    PyObject *tell;
    PyObject *close;
} pgRWHelper;

/*static const char pg_default_encoding[] = "unicode_escape";*/
/*static const char pg_default_errors[] = "backslashreplace";*/
static const char pg_default_encoding[] = "unicode_escape";
static const char pg_default_errors[] = "backslashreplace";

static PyObject *os_module = NULL;
static PyObject *difflib_module = NULL;

static Sint64
_pg_rw_size(SDL_RWops *);
static Sint64
_pg_rw_seek(SDL_RWops *, Sint64, int);
static size_t
_pg_rw_read(SDL_RWops *, void *, size_t, size_t);
static size_t
_pg_rw_write(SDL_RWops *, const void *, size_t, size_t);
static int
_pg_rw_close(SDL_RWops *);

/* Converter function used by PyArg_ParseTupleAndKeywords with the "O&" format.
 *
 * Returns: 1 on success
 *          0 on fail (with exception set)
 */
static int
_pg_is_exception_class(PyObject *obj, void **optr)
{
    PyObject **rval = (PyObject **)optr;
    PyObject *oname;
    PyObject *tmp;

    if (!PyType_Check(obj) || /* conditional or */
        !PyObject_IsSubclass(obj, PyExc_BaseException)) {
        oname = PyObject_Str(obj);
        if (oname == NULL) {
            PyErr_SetString(PyExc_TypeError,
                            "invalid exception class argument");
            return 0;
        }
        tmp = PyUnicode_AsEncodedString(oname, "ascii", "replace");
        Py_DECREF(oname);

        if (tmp == NULL) {
            PyErr_SetString(PyExc_TypeError,
                            "invalid exception class argument");
            return 0;
        }

        oname = tmp;
        PyErr_Format(PyExc_TypeError,
                     "Expected an exception class: got %.1024s",
                     PyBytes_AS_STRING(oname));
        Py_DECREF(oname);
        return 0;
    }
    *rval = obj;
    return 1;
}

static int
fetch_object_methods(pgRWHelper *helper, PyObject *obj)
{
    helper->read = helper->write = helper->seek = helper->tell =
        helper->close = NULL;

    if (PyObject_HasAttrString(obj, "read")) {
        helper->read = PyObject_GetAttrString(obj, "read");
        if (helper->read && !PyCallable_Check(helper->read)) {
            Py_DECREF(helper->read);
            helper->read = NULL;
        }
    }
    if (PyObject_HasAttrString(obj, "write")) {
        helper->write = PyObject_GetAttrString(obj, "write");
        if (helper->write && !PyCallable_Check(helper->write)) {
            Py_DECREF(helper->write);
            helper->write = NULL;
        }
    }
    if (!helper->read && !helper->write) {
        PyErr_SetString(PyExc_TypeError, "not a file object");
        return -1;
    }
    if (PyObject_HasAttrString(obj, "seek")) {
        helper->seek = PyObject_GetAttrString(obj, "seek");
        if (helper->seek && !PyCallable_Check(helper->seek)) {
            Py_DECREF(helper->seek);
            helper->seek = NULL;
        }
    }
    if (PyObject_HasAttrString(obj, "tell")) {
        helper->tell = PyObject_GetAttrString(obj, "tell");
        if (helper->tell && !PyCallable_Check(helper->tell)) {
            Py_DECREF(helper->tell);
            helper->tell = NULL;
        }
    }
    if (PyObject_HasAttrString(obj, "close")) {
        helper->close = PyObject_GetAttrString(obj, "close");
        if (helper->close && !PyCallable_Check(helper->close)) {
            Py_DECREF(helper->close);
            helper->close = NULL;
        }
    }
    return 0;
}

/* This function is meant to decode a pathlib object into its str/bytes
 * representation. */
static PyObject *
_trydecode_pathlibobj(PyObject *obj)
{
    PyObject *ret = PyOS_FSPath(obj);
    if (!ret) {
        /* A valid object was not passed. But we do not consider it an error */
        PyErr_Clear();
        Py_INCREF(obj);
        return obj;
    }
    return ret;
}

static PyObject *
pg_EncodeString(PyObject *obj, const char *encoding, const char *errors,
                PyObject *eclass)
{
    PyObject *oencoded, *exc_type, *exc_value, *exc_trace, *str, *ret;

    if (obj == NULL) {
        /* Assume an error was raise; forward it */
        return NULL;
    }
    if (encoding == NULL) {
        encoding = pg_default_encoding;
    }
    if (errors == NULL) {
        errors = pg_default_errors;
    }

    ret = _trydecode_pathlibobj(obj);
    if (!ret)
        return NULL;

    if (PyUnicode_Check(ret)) {
        oencoded = PyUnicode_AsEncodedString(ret, encoding, errors);
        Py_DECREF(ret);

        if (oencoded != NULL) {
            return oencoded;
        }
        else if (PyErr_ExceptionMatches(PyExc_MemoryError)) {
            /* Forward memory errors */
            return NULL;
        }
        else if (eclass != NULL) {
            /* Forward as eclass error */
            PyErr_Fetch(&exc_type, &exc_value, &exc_trace);
            Py_DECREF(exc_type);
            Py_XDECREF(exc_trace);
            if (exc_value == NULL) {
                PyErr_SetString(eclass, "Unicode encoding error");
            }
            else {
                str = PyObject_Str(exc_value);
                Py_DECREF(exc_value);
                if (str != NULL) {
                    PyErr_SetObject(eclass, str);
                    Py_DECREF(str);
                }
            }
            return NULL;
        }
        else if (encoding == pg_default_encoding &&
                 errors == pg_default_errors) {
            /* The default encoding and error handling should not fail */
            return RAISE(PyExc_SystemError,
                         "Pygame bug (in pg_EncodeString):"
                         " unexpected encoding error");
        }
        PyErr_Clear();
        Py_RETURN_NONE;
    }

    if (PyBytes_Check(ret)) {
        return ret;
    }

    Py_DECREF(ret);
    Py_RETURN_NONE;
}

static PyObject *
pg_EncodeFilePath(PyObject *obj, PyObject *eclass)
{
    /* All of this code is a replacement for Py_FileSystemDefaultEncoding,
     * which is deprecated in Python 3.12
     *
     * But I'm not sure of the use of this function, so maybe it should be
     * deprecated. */

    PyObject *sys_module = PyImport_ImportModule("sys");
    if (sys_module == NULL) {
        return NULL;
    }
    PyObject *system_encoding_obj =
        PyObject_CallMethod(sys_module, "getfilesystemencoding", NULL);
    if (system_encoding_obj == NULL) {
        Py_DECREF(sys_module);
        return NULL;
    }
    Py_DECREF(sys_module);
    const char *encoding = PyUnicode_AsUTF8(system_encoding_obj);
    if (encoding == NULL) {
        Py_DECREF(system_encoding_obj);
        return NULL;
    }

    /* End code replacement section */

    if (obj == NULL) {
        PyErr_SetString(PyExc_SyntaxError, "Forwarded exception");
    }

    PyObject *result =
        pg_EncodeString(obj, encoding, UNICODE_DEF_FS_ERROR, eclass);
    Py_DECREF(system_encoding_obj);

    if (result == NULL || result == Py_None) {
        return result;
    }
    if ((size_t)PyBytes_GET_SIZE(result) !=
        strlen(PyBytes_AS_STRING(result))) {
        if (eclass != NULL) {
            Py_DECREF(result);
            result = pg_EncodeString(obj, NULL, NULL, NULL);
            if (result == NULL) {
                return NULL;
            }
            PyErr_Format(eclass,
                         "File path '%.1024s' contains null characters",
                         PyBytes_AS_STRING(result));
            Py_DECREF(result);
            return NULL;
        }
        Py_DECREF(result);
        Py_RETURN_NONE;
    }
    return result;
}

static int
pgRWops_IsFileObject(SDL_RWops *rw)
{
    return rw->close == _pg_rw_close;
}

static Sint64
_pg_rw_size(SDL_RWops *context)
{
    pgRWHelper *helper = (pgRWHelper *)context->hidden.unknown.data1;
    PyObject *pos = NULL;
    PyObject *tmp = NULL;
    Sint64 size;
    Sint64 retval = -1;

    if (!helper->seek || !helper->tell)
        return retval;

    PyGILState_STATE state = PyGILState_Ensure();

    /* Current file position; need to restore it later.
     */
    pos = PyObject_CallFunction(helper->tell, NULL);
    if (!pos) {
        PyErr_Print();
        goto end;
    }

    /* Relocate to end of file.
     */
    tmp = PyObject_CallFunction(helper->seek, "ii", 0, SEEK_END);
    if (!tmp) {
        PyErr_Print();
        goto end;
    }
    Py_DECREF(tmp);

    /* Record file size.
     */
    tmp = PyObject_CallFunction(helper->tell, NULL);
    if (!tmp) {
        PyErr_Print();
        goto end;
    }

    size = PyLong_AsLongLong(tmp);
    if (size == -1 && PyErr_Occurred() != NULL) {
        PyErr_Print();
        goto end;
    }
    Py_DECREF(tmp);

    /* Return to original position.
     */
    tmp = PyObject_CallFunctionObjArgs(helper->seek, pos, NULL);
    if (!tmp) {
        PyErr_Print();
        goto end;
    }

    /* Success.
     */
    retval = size;

end:
    /* Cleanup.
     */
    Py_XDECREF(pos);
    Py_XDECREF(tmp);
    PyGILState_Release(state);
    return retval;
}

static size_t
_pg_rw_write(SDL_RWops *context, const void *ptr, size_t size, size_t num)
{
    pgRWHelper *helper = (pgRWHelper *)context->hidden.unknown.data1;
    PyObject *result;
    size_t retval;

    if (!helper->write)
        return -1;

    PyGILState_STATE state = PyGILState_Ensure();

    result = PyObject_CallFunction(helper->write, "y#", (const char *)ptr,
                                   (Py_ssize_t)size * num);
    if (!result) {
        PyErr_Print();
        retval = -1;
        goto end;
    }

    Py_DECREF(result);
    retval = num;

end:
    PyGILState_Release(state);
    return retval;
}

static int
_pg_rw_close(SDL_RWops *context)
{
    pgRWHelper *helper = (pgRWHelper *)context->hidden.unknown.data1;
    PyObject *result;
    int retval = 0;
    PyGILState_STATE state = PyGILState_Ensure();

    if (helper->close) {
        result = PyObject_CallFunction(helper->close, NULL);
        if (!result) {
            PyErr_Print();
            retval = -1;
        }
        Py_XDECREF(result);
    }

    Py_XDECREF(helper->seek);
    Py_XDECREF(helper->tell);
    Py_XDECREF(helper->write);
    Py_XDECREF(helper->read);
    Py_XDECREF(helper->close);

    PyMem_Free(helper);
    PyGILState_Release(state);
    SDL_FreeRW(context);
    return retval;
}

static SDL_RWops *
pgRWops_FromFileObject(PyObject *obj)
{
    SDL_RWops *rw;
    pgRWHelper *helper;

    if (obj == NULL) {
        return (SDL_RWops *)RAISE(PyExc_TypeError, "Invalid filetype object");
    }

    helper = PyMem_New(pgRWHelper, 1);
    if (helper == NULL) {
        return (SDL_RWops *)PyErr_NoMemory();
    }
    if (fetch_object_methods(helper, obj)) {
        PyMem_Free(helper);
        return NULL;
    }

    rw = SDL_AllocRW();
    if (rw == NULL) {
        PyMem_Free(helper);
        return (SDL_RWops *)PyErr_NoMemory();
    }

    /* Adding a helper to the hidden data to support file-like object RWops */
    rw->hidden.unknown.data1 = (void *)helper;
    rw->size = _pg_rw_size;
    rw->seek = _pg_rw_seek;
    rw->read = _pg_rw_read;
    rw->write = _pg_rw_write;
    rw->close = _pg_rw_close;

    return rw;
}

static Sint64
_pg_rw_seek(SDL_RWops *context, Sint64 offset, int whence)
{
    pgRWHelper *helper = (pgRWHelper *)context->hidden.unknown.data1;
    PyObject *result;
    Sint64 retval;

    if (!helper->seek || !helper->tell)
        return -1;

    PyGILState_STATE state = PyGILState_Ensure();

    if (!(offset == 0 &&
          whence == SEEK_CUR)) /* being seek'd, not just tell'd */
    {
        result = PyObject_CallFunction(helper->seek, "Li", (long long)offset,
                                       whence);
        if (!result) {
            PyErr_Print();
            retval = -1;
            goto end;
        }
        Py_DECREF(result);
    }

    result = PyObject_CallFunction(helper->tell, NULL);
    if (!result) {
        PyErr_Print();
        retval = -1;
        goto end;
    }

    retval = PyLong_AsLongLong(result);
    if (retval == -1 && PyErr_Occurred())
        PyErr_Clear();

    Py_DECREF(result);

end:
    PyGILState_Release(state);

    return retval;
}

static size_t
_pg_rw_read(SDL_RWops *context, void *ptr, size_t size, size_t maxnum)
{
    pgRWHelper *helper = (pgRWHelper *)context->hidden.unknown.data1;
    PyObject *result;
    Py_ssize_t retval;

    if (!helper->read)
        return -1;

    PyGILState_STATE state = PyGILState_Ensure();
    result = PyObject_CallFunction(helper->read, "K",
                                   (unsigned long long)size * maxnum);
    if (!result) {
        PyErr_Print();
        retval = -1;
        goto end;
    }

    if (!PyBytes_Check(result)) {
        Py_DECREF(result);
        PyErr_Print();
        retval = -1;
        goto end;
    }

    retval = PyBytes_GET_SIZE(result);
    if (retval) {
        memcpy(ptr, PyBytes_AsString(result), retval);
        retval /= size;
    }

    Py_DECREF(result);

end:
    PyGILState_Release(state);

    return retval;
}

PyObject *
add_to_path(PyObject *path, PyObject *existing_path, PyObject *new_part)
{
    // handles joining paths chunks which may include windows drive letters,
    // windows drive letters require special handling to work correctly.
    PyObject *temp_path = NULL;
    int path_length = (int)PySequence_Length(existing_path);
    if (path_length > 0) {
        PyObject *last_char =
            PySequence_GetItem(existing_path, path_length - 1);
        if (PyUnicode_Compare(last_char, PyUnicode_FromString(":")) == 0) {
            // handle Windows drive letters
            temp_path =
                PyObject_CallMethod(path, "join", "OOO", existing_path,
                                    PyUnicode_FromString("\\"), new_part);
        }
        Py_XDECREF(last_char);
    }
    else {
        // adding first item to a path, need to force adding a slash if it is
        // not windows drive letter
        int new_part_length = (int)PySequence_Length(new_part);
        if (new_part_length > 0) {
            PyObject *last_char =
                PySequence_GetItem(new_part, new_part_length - 1);
            if (PyUnicode_Compare(last_char, PyUnicode_FromString(":")) != 0) {
                // not a windows drive letter, so add a slash at the start
                PyObject *sep_obj = PyObject_GetAttrString(os_module, "sep");
                temp_path = PyObject_CallMethod(
                    path, "join", "OOO", existing_path, sep_obj, new_part);
                Py_XDECREF(sep_obj);
            }
            Py_XDECREF(last_char);
        }
    }

    if (!temp_path) {
        temp_path =
            PyObject_CallMethod(path, "join", "OO", existing_path, new_part);
    }
    return temp_path;
}

PyObject *
get_contents_at_path(PyObject *os_module, PyObject *path_submodule,
                     PyObject *path_to_check)
{
    // handles obtaining the contents of a directory.
    // windows drive letters require special handling to work correctly.
    PyObject *directories_found = NULL;
    int path_length = (int)PySequence_Length(path_to_check);
    if (path_length > 0) {
        PyObject *last_char =
            PySequence_GetItem(path_to_check, path_length - 1);
        if (PyUnicode_Compare(last_char, PyUnicode_FromString(":")) == 0) {
            // handle Windows drive letters
            PyObject *drive_letter_path =
                PyObject_CallMethod(path_submodule, "join", "OO",
                                    path_to_check, PyUnicode_FromString("\\"));
            Py_XDECREF(path_to_check);
            path_to_check = drive_letter_path;
        }
        Py_XDECREF(last_char);
        directories_found =
            PyObject_CallMethod(os_module, "listdir", "O", path_to_check);
    }
    return directories_found;
}

PyObject *
suggest_valid_path(PyObject *path_submodule, PyObject *original_path,
                   PyObject *starting_path)
{
    // To suggest a valid path from an invalid one we first normalise & split
    // the provided path into components (directory/drive letter/file chunks).
    PyObject *norm_orig_path =
        PyObject_CallMethod(path_submodule, "normpath", "O", original_path);
    PyObject *sep_obj = PyObject_GetAttrString(os_module, "sep");
    PyObject *path_components =
        PyObject_CallMethod(norm_orig_path, "split", "O", sep_obj);
    Py_XDECREF(sep_obj);
    Py_XDECREF(norm_orig_path);

    int all_path_comp_len = (int)PySequence_Length(path_components);
    if (all_path_comp_len > 0) {
        // We have a path with at least some content, the file will be the last
        // chunk so grab that seperately
        PyObject *file_comp =
            PySequence_GetItem(path_components, all_path_comp_len - 1);
        PyObject *longest_valid_path = NULL;
        PyObject *temp_path = NULL;
        // loop through all the non-file path components rebuilding the path
        // component-by-component and checking at each addition if the formed
        // path is valid.
        // If the path is not valid at any step, we search for the closest
        // match and add that instead.
        for (int i = 0; i < all_path_comp_len - 1; i++) {
            PyObject *path_comp = PySequence_GetItem(path_components, i);
            int path_comp_len = (int)PySequence_Length(path_comp);
            // Skip empty path components
            if (path_comp_len > 0) {
                if (temp_path) {
                    Py_XDECREF(temp_path);
                }
                if (longest_valid_path) {
                    temp_path = add_to_path(path_submodule, longest_valid_path,
                                            path_comp);
                }
                else {
                    temp_path =
                        add_to_path(path_submodule, starting_path, path_comp);
                }
                PyObject *is_dir = PyObject_CallMethod(path_submodule, "isdir",
                                                       "O", temp_path);
                if (is_dir == Py_True) {
                    // path step is valid, continue the loop
                    if (longest_valid_path) {
                        Py_XDECREF(longest_valid_path);
                    }
                    longest_valid_path = PyObject_CallMethod(
                        path_submodule, "normpath", "O", temp_path);
                }
                else {
                    // path step is invalid, look for potential alternatives
                    PyObject *potential_dirs = get_contents_at_path(
                        os_module, path_submodule, longest_valid_path);
                    if (!potential_dirs) {
                        PyErr_Format(PyExc_FileNotFoundError,
                                     "No Potential dirs at path: '%S'?",
                                     longest_valid_path);
                        Py_XDECREF(path_components);
                        Py_XDECREF(longest_valid_path);
                        Py_XDECREF(path_comp);
                        Py_XDECREF(file_comp);
                        Py_XDECREF(temp_path);
                        Py_XDECREF(is_dir);
                        return NULL;  // Suggested path not found
                    }

                    PyObject *actual_dirs = PyList_New(0);
                    int num_files_and_folders =
                        (int)PySequence_Length(potential_dirs);
                    for (int j = 0; j < num_files_and_folders; j++) {
                        PyObject *potential_dir =
                            PySequence_GetItem(potential_dirs, j);
                        PyObject *temp_potential_path = add_to_path(
                            path_submodule, longest_valid_path, potential_dir);
                        PyObject *potential_is_dir = PyObject_CallMethod(
                            path_submodule, "isdir", "O", temp_potential_path);
                        if (potential_is_dir == Py_True) {
                            PyList_Append(actual_dirs, potential_dir);
                        }
                        Py_XDECREF(potential_is_dir);
                        Py_XDECREF(temp_potential_path);
                        Py_XDECREF(potential_dir);
                    }
                    Py_XDECREF(potential_dirs);
                    // we've found some actual directories that could be our
                    // path step pick the one closest to what we were given
                    // using difflib
                    if ((int)PySequence_Length(actual_dirs) > 0) {
                        PyObject *closest_matches = PyObject_CallMethod(
                            difflib_module, "get_close_matches", "OO",
                            path_comp, actual_dirs);
                        if ((int)PySequence_Length(closest_matches) > 0) {
                            PyObject *closest_match =
                                PySequence_GetItem(closest_matches, 0);
                            PyObject *new_longest_valid_path =
                                add_to_path(path_submodule, longest_valid_path,
                                            closest_match);
                            Py_XDECREF(closest_match);
                            Py_XDECREF(longest_valid_path);
                            longest_valid_path = new_longest_valid_path;
                        }
                        Py_XDECREF(closest_matches);
                    }
                    else {
                        // no directories to match against,
                        // default to simple error
                        PyErr_Format(PyExc_FileNotFoundError,
                                     "No actual dirs at path: '%S'?",
                                     longest_valid_path);
                        Py_XDECREF(actual_dirs);
                        Py_XDECREF(path_components);
                        Py_XDECREF(longest_valid_path);
                        Py_XDECREF(path_comp);
                        Py_XDECREF(file_comp);
                        Py_XDECREF(temp_path);
                        Py_XDECREF(is_dir);
                        return NULL;  // Suggested path not found
                    }
                    Py_XDECREF(actual_dirs);
                }
                Py_XDECREF(is_dir);
            }
            Py_XDECREF(path_comp);
        }
        Py_XDECREF(temp_path);
        Py_XDECREF(path_components);
        // We have the longest valid directory path that is the most similar
        // to the given path. Now we look for the most similar file on that
        // path.
        PyObject *potential_files = get_contents_at_path(
            os_module, path_submodule, longest_valid_path);
        if (!potential_files) {
            Py_XDECREF(longest_valid_path);
            Py_XDECREF(file_comp);
            return NULL;  // Suggested path not found
        }
        PyObject *actual_files = PyList_New(0);
        int num_files_and_folders = (int)PySequence_Length(potential_files);
        for (int j = 0; j < num_files_and_folders; j++) {
            PyObject *potential_file = PySequence_GetItem(potential_files, j);
            PyObject *temp_potential_path = add_to_path(
                path_submodule, longest_valid_path, potential_file);
            PyObject *potential_is_file = PyObject_CallMethod(
                path_submodule, "isfile", "O", temp_potential_path);
            if (potential_is_file == Py_True) {
                PyList_Append(actual_files, potential_file);
            }
            Py_XDECREF(potential_is_file);
            Py_XDECREF(temp_potential_path);
            Py_XDECREF(potential_file);
        }
        Py_XDECREF(potential_files);
        if ((int)PySequence_Length(actual_files) > 0) {
            PyObject *closest_matches =
                PyObject_CallMethod(difflib_module, "get_close_matches", "OO",
                                    file_comp, actual_files);
            if ((int)PySequence_Length(closest_matches) > 0) {
                PyObject *closest_match =
                    PySequence_GetItem(closest_matches, 0);
                PyObject *new_longest_valid_path = NULL;
                new_longest_valid_path = add_to_path(
                    path_submodule, longest_valid_path, closest_match);
                Py_DECREF(closest_match);
                Py_XDECREF(longest_valid_path);
                longest_valid_path = new_longest_valid_path;
            }
            Py_XDECREF(closest_matches);
        }
        else {
            // no files to match against,
            // default to simple error
            PyErr_Format(PyExc_FileNotFoundError,
                         "No Actual files at path: '%S'?", longest_valid_path);
            Py_XDECREF(actual_files);
            Py_XDECREF(longest_valid_path);
            Py_XDECREF(file_comp);
            return NULL;  // Suggested path not found
        }
        Py_XDECREF(actual_files);
        Py_XDECREF(file_comp);
        PyObject *new_longest_valid_path = PyObject_CallMethod(
            path_submodule, "normpath", "O", longest_valid_path);
        Py_XDECREF(longest_valid_path);
        return new_longest_valid_path;
    }
    else {
        PyErr_Format(PyExc_FileNotFoundError, "unable to split path: '%S'?",
                     original_path);
        Py_XDECREF(path_components);
        return NULL;  // Suggested path not found
    }
}

static SDL_RWops *
_rwops_from_pystr(PyObject *obj, char **extptr)
{
    SDL_RWops *rw = NULL;
    PyObject *oencoded;
    char *encoded = NULL;

    /* If a valid extptr has been passed, we want it to default to NULL
     * to show that an extension hasn't been procured (if it has it will
     * get set to that later) */
    if (extptr) {
        *extptr = NULL;
    }

    if (!obj) {
        // forward any errors
        return NULL;
    }

    oencoded = pg_EncodeString(obj, "UTF-8", NULL, NULL);
    if (!oencoded || oencoded == Py_None) {
        /* if oencoded is NULL, we are forwarding an error. If it is None, the
         * object passed was not a bytes/string/pathlib object so handling of
         * that is done after this function, exit early here */
        Py_XDECREF(oencoded);
        return NULL;
    }

    encoded = PyBytes_AS_STRING(oencoded);
    rw = SDL_RWFromFile(encoded, "rb");

    if (rw) {
        /* If a valid extptr has been passed, populate it with a dynamically
         * allocated field for the file extension. */
        if (extptr) {
            char *ext = strrchr(encoded, '.');
            if (ext && strlen(ext) > 1) {
                ext++;
                *extptr = malloc(strlen(ext) + 1);
                if (!(*extptr)) {
                    /* If out of memory, decref oencoded to be safe, and try
                     * to close out `rw` as well. */
                    Py_DECREF(oencoded);
                    if (SDL_RWclose(rw) < 0) {
                        PyErr_SetString(PyExc_IOError, SDL_GetError());
                    }
                    return (SDL_RWops *)PyErr_NoMemory();
                }
                strcpy(*extptr, ext);
            }
        }

        Py_DECREF(oencoded);
        return rw;
    }

    Py_DECREF(oencoded);
    /* Clear SDL error and set our own error message for filenotfound errors
     * TODO: Check SDL error here and forward any non filenotfound related
     * errors correctly here */
    SDL_ClearError();

    PyObject *cwd = NULL, *path_submodule = NULL, *isabs = NULL;
    PyObject *new_cwd = NULL;
    if (!os_module)
        goto simple_case_no_path;

    cwd = PyObject_CallMethod(os_module, "getcwd", NULL);
    if (!cwd)
        goto simple_case_no_path;

    path_submodule = PyObject_GetAttrString(os_module, "path");
    if (!path_submodule)
        goto simple_case;

    int length_provided_path = (int)PySequence_Length(obj);

    if (length_provided_path > 0) {
        isabs = PyObject_CallMethod(path_submodule, "isabs", "O", obj);

        // At this point we should know that we can't find a file to load at
        // the provided path. The error strategy is to check if the provided
        // path is absolute or relative and then, if possible, suggest a path
        // in that format that might have been intended. We cannot anticipate
        // and correct all malformed paths - so we instead focus on provided
        // paths where the correct number of sub-directories has been indicated
        // and then select the most likely directory and file at each level.
        if (!isabs || isabs == Py_True) {
            PyObject *abs_path = PyObject_Str(
                PyObject_CallMethod(path_submodule, "normpath", "O", obj));

            PyObject *empty_string = PyUnicode_FromString("");
            PyObject *suggested_valid_path =
                suggest_valid_path(path_submodule, abs_path, empty_string);
            Py_XDECREF(abs_path);
            Py_XDECREF(empty_string);

            if (!suggested_valid_path)
                goto simple_case;

            // we will elect to always provide suggested paths with forward
            // slashes as these will work in python/pygame-ce on all platforms
            // and are less fiddly than back slash paths with escaped back
            // slashes.
            PyObject *new_suggested_valid_path = PyObject_CallMethod(
                suggested_valid_path, "replace", "ss", "\\", "/");
            Py_XDECREF(suggested_valid_path);
            PyErr_Format(PyExc_FileNotFoundError,
                         "File not found at path: '%S', did you mean: '%S'?",
                         obj, new_suggested_valid_path);

            Py_XDECREF(new_suggested_valid_path);
        }
        else {
            PyObject *rel_path_obj =
                PyObject_CallMethod(path_submodule, "relpath", "OO", obj, cwd);
            PyObject *rel_path = PyObject_Str(rel_path_obj);
            Py_XDECREF(rel_path_obj);

            PyObject *suggested_valid_path =
                suggest_valid_path(path_submodule, rel_path, cwd);
            Py_XDECREF(rel_path);

            if (!suggested_valid_path)
                goto simple_relative_case_w_path;

            PyObject *suggested_rel_path_obj = PyObject_CallMethod(
                path_submodule, "relpath", "OO", suggested_valid_path, cwd);
            PyObject *suggested_rel_path =
                PyObject_Str(suggested_rel_path_obj);
            Py_XDECREF(suggested_valid_path);
            Py_XDECREF(suggested_rel_path_obj);

            // we will elect to always provide suggested paths with forward
            // slashes as these will work in python/pygame-ce on all platforms
            // and are less fiddly than back slash paths with escaped back
            // slashes.
            PyObject *new_suggested_rel_path = PyObject_CallMethod(
                suggested_rel_path, "replace", "ss", "\\", "/");
            Py_XDECREF(suggested_rel_path);
            new_cwd = PyObject_CallMethod(cwd, "replace", "ss", "\\", "/");
            Py_XDECREF(cwd);
            cwd = new_cwd;
            PyErr_Format(PyExc_FileNotFoundError,
                         "No file '%S' found in working directory '%S', did "
                         "you mean: '%S'?",
                         obj, cwd, new_suggested_rel_path);

            Py_XDECREF(new_suggested_rel_path);
        }

        Py_XDECREF(path_submodule);
        Py_XDECREF(cwd);
        Py_XDECREF(isabs);
        return NULL;
    }

simple_case:
    Py_XDECREF(path_submodule);
    goto simple_case_no_path;
simple_relative_case_w_path:
    new_cwd = PyObject_CallMethod(cwd, "replace", "ss", "\\", "/");
    Py_XDECREF(cwd);
    PyErr_Format(PyExc_FileNotFoundError,
                 "No file '%S' found in working directory '%S'.", obj,
                 new_cwd);
    Py_XDECREF(path_submodule);
    Py_XDECREF(new_cwd);
    Py_XDECREF(isabs);
    return NULL;
simple_case_no_path:
    Py_XDECREF(cwd);
    Py_XDECREF(isabs);
    PyErr_Format(PyExc_FileNotFoundError, "No such file or directory: '%S'.",
                 obj);
    return NULL;
}

static SDL_RWops *
pgRWops_FromObject(PyObject *obj, char **extptr)
{
#if __EMSCRIPTEN__
    SDL_RWops *rw;
    int retry = 0;
again:
    rw = _rwops_from_pystr(obj, extptr);
    if (retry)
        Py_XDECREF(obj);
    if (!rw) {
        if (PyErr_Occurred())
            return NULL;
    }
    else {
        return rw;
    }

fail:
    if (retry)
        return RAISE(PyExc_RuntimeError, "can't access resource on platform");

    retry = 1;
    PyObject *name = PyObject_GetAttrString(obj, "name");
    if (name) {
        obj = name;
        goto again;
    }
    goto fail;
    // unreachable.
#else
    SDL_RWops *rw = _rwops_from_pystr(obj, extptr);
    if (!rw) {
        if (PyErr_Occurred())
            return NULL;
    }
    else {
        return rw;
    }
    return pgRWops_FromFileObject(obj);
#endif
}

static PyObject *
pg_encode_string(PyObject *self, PyObject *args, PyObject *keywds)
{
    PyObject *obj = NULL;
    PyObject *eclass = NULL;
    const char *encoding = NULL;
    const char *errors = NULL;
    static char *kwids[] = {"obj", "encoding", "errors", "etype", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "|OssO&", kwids, &obj,
                                     &encoding, &errors,
                                     &_pg_is_exception_class, &eclass)) {
        return NULL;
    }

    if (obj == NULL) {
        PyErr_SetString(PyExc_SyntaxError, "Forwarded exception");
    }
    return pg_EncodeString(obj, encoding, errors, eclass);
}

static PyObject *
pg_encode_file_path(PyObject *self, PyObject *args, PyObject *keywds)
{
    PyObject *obj = NULL;
    PyObject *eclass = NULL;
    static char *kwids[] = {"obj", "etype", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "|OO&", kwids, &obj,
                                     &_pg_is_exception_class, &eclass)) {
        return NULL;
    }

    return pg_EncodeFilePath(obj, eclass);
}

static PyMethodDef _pg_rwobject_methods[] = {
    {"encode_string", (PyCFunction)pg_encode_string,
     METH_VARARGS | METH_KEYWORDS, DOC_ENCODESTRING},
    {"encode_file_path", (PyCFunction)pg_encode_file_path,
     METH_VARARGS | METH_KEYWORDS, DOC_ENCODEFILEPATH},
    {NULL, NULL, 0, NULL}};

/*DOC*/ static char _pg_rwobject_doc[] =
    /*DOC*/ "SDL_RWops support";

MODINIT_DEFINE(rwobject)
{
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_RWOBJECT_NUMSLOTS];

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "rwobject",
                                         _pg_rwobject_doc,
                                         -1,
                                         _pg_rwobject_methods,
                                         NULL,
                                         NULL,
                                         NULL,
                                         NULL};

    /* Create the module and add the functions */
    module = PyModule_Create(&_module);
    if (module == NULL) {
        return NULL;
    }

    /* export the c api */
    c_api[0] = pgRWops_FromObject;
    c_api[1] = pgRWops_IsFileObject;
    c_api[2] = pg_EncodeFilePath;
    c_api[3] = pg_EncodeString;
    c_api[4] = pgRWops_FromFileObject;
    apiobj = encapsulate_api(c_api, "rwobject");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }

    /* import os, don't sweat if it errors, it will be checked before use */
    os_module = PyImport_ImportModule("os");
    if (os_module == NULL)
        PyErr_Clear();

    difflib_module = PyImport_ImportModule("difflib");
    if (difflib_module == NULL)
        PyErr_Clear();

    return module;
}
