#include <Python.h>

#include "unity.h"

#ifndef TEST_COMMON_H
#define TEST_COMMON_H

struct TestCase {
  char *test_name;
  int line_num;
};

/*
    This will take some explanation... the PG_CTEST macro defines two things
    for an individual test case. The test case itself, and a struct instance
    called meta_TEST_CASE_NAME. The struct has two pieces of important
    information that unity needs: the name in string format and the line
    number of the test. This would be an absolute nightmare to maintain by
    hand, so I defined a macro to do it automagically for us.

    The RUN_TEST_PG_INTERNAL macro then references that struct for each test
    case that we tell it about and automatically populates the unity fields
    with the requisite data.

    Note that the arguments to the test function must be *exactly*
    (PyObject * self, PyObject * _null), but due to gcc throwing a fit, I
    cannot just use token pasting to have the macro generate that part for me

    Also note that tests are expected to end with PY_RETURN_NONE when
   successful, or return NULL with an exception set when failed.
*/
#define PG_CTEST(TestFunc)                                                     \
  static struct TestCase meta_##TestFunc = {#TestFunc, __LINE__};              \
  static PyObject *TestFunc

#define RUN_TEST_PG_INTERNAL(TestFunc)                                         \
  {                                                                            \
    Unity.CurrentTestName = meta_##TestFunc.test_name;                         \
    Unity.CurrentTestLineNumber = meta_##TestFunc.line_num;                    \
    Unity.NumberOfTests++;                                                     \
    PyObject *result = NULL;                                                   \
    if (TEST_PROTECT()) {                                                      \
      setUp();                                                                 \
      result = TestFunc(self, _null);                                          \
      TEST_ASSERT_NOT_EQUAL(NULL, result);                                     \
    }                                                                          \
    if (TEST_PROTECT()) {                                                      \
      tearDown();                                                              \
    }                                                                          \
    if (PyErr_Occurred()) {                                                    \
      PyErr_Print();                                                           \
      PyErr_Clear();                                                           \
    }                                                                          \
                                                                               \
    UnityConcludeTest();                                                       \
  }

#endif // #ifndef TEST_COMMON_H
