#include <Python.h>

#include "base.h"
#include "test_common.h"

/* setUp and tearDown must be nonstatic void(void) */
void setUp(void) {}

void tearDown(void) {}

/**
 * @brief Tests _pg_is_int_tuple when passed a tuple of ints
 */
PG_CTEST(test__pg_is_int_tuple_nominal)(PyObject *self, PyObject *_null) {
  PyObject *arg1 = Py_BuildValue("(iii)", 1, 2, 3);
  if (!arg1) {
    // exception already set by Py_BuildValue
    return NULL;
  }

  PyObject *arg2 = Py_BuildValue("(iii)", -1, -2, -3);
  if (!arg2) {
    // exception already set by Py_BuildValue
    return NULL;
  }

  PyObject *arg3 = Py_BuildValue("(iii)", 1, -2, -3);
  if (!arg3) {
    // exception already set by Py_BuildValue
    return NULL;
  }

  TEST_ASSERT_EQUAL(1, _pg_is_int_tuple(arg1));
  TEST_ASSERT_EQUAL(1, _pg_is_int_tuple(arg2));
  TEST_ASSERT_EQUAL(1, _pg_is_int_tuple(arg3));

  Py_DECREF(arg1);
  Py_DECREF(arg2);
  Py_DECREF(arg3);

  Py_RETURN_NONE;
}

/**
 * @brief Tests _pg_is_int_tuple when passed a tuple of non-numeric values
 */
PG_CTEST(test__pg_is_int_tuple_failureModes)(PyObject *self, PyObject *_null) {
  PyObject *arg1 =
      Py_BuildValue("(sss)", (char *)"Larry", (char *)"Moe", (char *)"Curly");
  if (!arg1) {
    // exception already set by Py_BuildValue
    return NULL;
  }

  PyObject *arg2 = Py_BuildValue("(zzz)", NULL, NULL, NULL); // tuple of None's
  if (!arg2) {
    // exception already set by Py_BuildValue
    return NULL;
  }

  PyObject *arg3 = Py_BuildValue("(OOO)", arg1, arg2, arg1);
  if (!arg3) {
    // exception already set by Py_BuildValue
    return NULL;
  }

  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg1));
  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg2));
  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg3));

  Py_DECREF(arg1);
  Py_DECREF(arg2);
  Py_DECREF(arg3);

  Py_RETURN_NONE;
}

/**
 * @brief Tests _pg_is_int_tuple when passed a tuple of floats
 */
PG_CTEST(test__pg_is_int_tuple_floats)(PyObject *self, PyObject *_null) {
  PyObject *arg1 = Py_BuildValue("(ddd)", 1.0, 2.0, 3.0);
  if (!arg1) {
    // exception already set by Py_BuildValue
    return NULL;
  }

  PyObject *arg2 = Py_BuildValue("(ddd)", -1.1, -2.2, -3.3);
  if (!arg2) {
    // exception already set by Py_BuildValue
    return NULL;
  }

  PyObject *arg3 = Py_BuildValue("(ddd)", 1.0, -2.0, -3.1);
  if (!arg3) {
    // exception already set by Py_BuildValue
    return NULL;
  }

  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg1));
  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg2));
  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg3));

  Py_DECREF(arg1);
  Py_DECREF(arg2);
  Py_DECREF(arg3);

  Py_RETURN_NONE;
}

/*=======Test Reset Option=====*/
/* This must be void(void) */
void resetTest(void) {
  tearDown();
  setUp();
}

/*=======Exposed Test Reset Option=====*/
static PyObject *reset_test(PyObject *self, PyObject *_null) {
  resetTest();

  Py_RETURN_NONE;
}

/*=======Run The Tests=======*/
static PyObject *run_tests(PyObject *self, PyObject *_null) {
  UnityBegin("base_ctest.c");
  // This macro has calls to setUp and tearDown already baked into it
  // so there's no need to explicitly call resetTest between test cases
  RUN_TEST_PG_INTERNAL(test__pg_is_int_tuple_nominal);
  RUN_TEST_PG_INTERNAL(test__pg_is_int_tuple_failureModes);
  RUN_TEST_PG_INTERNAL(test__pg_is_int_tuple_floats);

  return PyLong_FromLong(UnityEnd());
}

static PyMethodDef base_test_methods[] = {
    {"test__pg_is_int_tuple_nominal",
     (PyCFunction)test__pg_is_int_tuple_nominal, METH_NOARGS,
     "Tests _pg_is_int_tuple when passed a tuple of ints"},
    {"test__pg_is_int_tuple_failureModes",
     (PyCFunction)test__pg_is_int_tuple_failureModes, METH_NOARGS,
     "Tests _pg_is_int_tuple when passed a tuple of non-numeric values"},
    {"test__pg_is_int_tuple_floats", (PyCFunction)test__pg_is_int_tuple_floats,
     METH_NOARGS, "Tests _pg_is_int_tuple when passed a tuple of floats"},
    {"reset_test", (PyCFunction)reset_test, METH_NOARGS,
     "Explicitly runs tearDown(); setUp(). Note: RUN_TEST_PG_INTERNAL calls "
     "setUp/tearDown around each test; run_tests does not call reset_test "
     "explicitly."},
    {"run_tests", (PyCFunction)run_tests, METH_NOARGS,
     "Runs all the tests in this test suite"},
    {NULL, NULL, 0, NULL}};

MODINIT_DEFINE(base_ctest) {
  PyObject *module;

  static struct PyModuleDef _module = {
      PyModuleDef_HEAD_INIT,
      "base_ctest",
      "C unit tests for the pygame.base internal implementation",
      -1,
      base_test_methods,
      NULL,
      NULL,
      NULL,
      NULL};

  /* create the module */
  module = PyModule_Create(&_module);
  if (!module) {
    return NULL;
  }

  return module;
}
