#include <Python.h>

#include "base.h"
#include "test_common.h"

static PyObject *base_module;

/* setUp and tearDown must be nonstatic void(void) */
void setUp(void) {}

void tearDown(void) {}

/**
 * @brief Tests _pg_is_int_tuple when passed a tuple of ints
 */
static PyObject *test__pg_is_int_tuple_nominal(PyObject *self,
                                               PyObject *_null) {
  PyObject *arg1 = Py_BuildValue("(iii)", 1, 2, 3);
  PyObject *arg2 = Py_BuildValue("(iii)", -1, -2, -3);
  PyObject *arg3 = Py_BuildValue("(iii)", 1, -2, -3);

  TEST_ASSERT_EQUAL(1, _pg_is_int_tuple(arg1));
  TEST_ASSERT_EQUAL(1, _pg_is_int_tuple(arg2));
  TEST_ASSERT_EQUAL(1, _pg_is_int_tuple(arg3));

  Py_RETURN_NONE;
}

/**
 * @brief Tests _pg_is_int_tuple when passed a tuple of non-numeric values
 */
static PyObject *test__pg_is_int_tuple_failureModes(PyObject *self,
                                                    PyObject *_null) {
  PyObject *arg1 =
      Py_BuildValue("(sss)", (char *)"Larry", (char *)"Moe", (char *)"Curly");
  PyObject *arg2 = Py_BuildValue("(sss)", (char *)NULL, (char *)NULL,
                                 (char *)NULL); // tuple of None's
  PyObject *arg3 = Py_BuildValue("(OOO)", arg1, arg2, arg1);

  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg1));
  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg2));
  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg3));

  Py_RETURN_NONE;
}

/**
 * @brief Tests _pg_is_int_tuple when passed a tuple of floats
 */
static PyObject *test__pg_is_int_tuple_floats(PyObject *self, PyObject *_null) {
  PyObject *arg1 = Py_BuildValue("(ddd)", 1.0, 2.0, 3.0);
  PyObject *arg2 = Py_BuildValue("(ddd)", -1.1, -2.2, -3.3);
  PyObject *arg3 = Py_BuildValue("(ddd)", 1.0, -2.0, -3.1);

  TEST_ASSERT_EQUAL(1, _pg_is_int_tuple(arg1));
  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg2));
  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg3));

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
  RUN_TEST_PG_INTERNAL(test__pg_is_int_tuple_nominal, 15, self, _null);
  RUN_TEST_PG_INTERNAL(test__pg_is_int_tuple_failureModes, 29, self, _null);
  RUN_TEST_PG_INTERNAL(test__pg_is_int_tuple_floats, 46, self, _null);

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
     "Resets the test suite between tests, run_tests automatically calls this "
     "after each test case it calls"},
    {"run_tests", (PyCFunction)run_tests, METH_NOARGS,
     "Runs all the tests in this test wuite"},
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

// #undef main
// /*=======MAIN=====*/
// int main(void) {
//   Py_Initialize();
//   UnityBegin("test_base.c");
//   RUN_TEST(test__pg_is_int_tuple_nominal, 17);
//   RUN_TEST(test__pg_is_int_tuple_failureModes, 31);
//   RUN_TEST(test__pg_is_int_tuple_floats, 45);

//   return (UnityEnd());
// }
