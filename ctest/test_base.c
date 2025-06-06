#include "base.h"
#include "unity.h"

PyObject *base_module;

void setUp(void) {}

void tearDown(void) {}

/**
 * @brief Tests _pg_is_int_tuple when passed a tuple of ints
 */
void test__pg_is_int_tuple_nominal(void) {
  PyObject *arg1 = Py_BuildValue("(iii)", 1, 2, 3);
  PyObject *arg2 = Py_BuildValue("(iii)", -1, -2, -3);
  PyObject *arg3 = Py_BuildValue("(iii)", 1, -2, -3);

  TEST_ASSERT_EQUAL(1, _pg_is_int_tuple(arg1));
  TEST_ASSERT_EQUAL(1, _pg_is_int_tuple(arg2));
  TEST_ASSERT_EQUAL(1, _pg_is_int_tuple(arg3));
}

/**
 * @brief Tests _pg_is_int_tuple when passed a tuple of non-numeric values
 */
void test__pg_is_int_tuple_failureModes(void) {
  PyObject *arg1 =
      Py_BuildValue("(sss)", (char *)"Larry", (char *)"Moe", (char *)"Curly");
  PyObject *arg2 = Py_BuildValue("(sss)", (char *)NULL, (char *)NULL,
                                 (char *)NULL); // tuple of None's
  PyObject *arg3 = Py_BuildValue("(OOO)", arg1, arg2, arg1);

  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg1));
  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg2));
  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg3));
}

/**
 * @brief Tests _pg_is_int_tuple when passed a tuple of floats
 */
void test__pg_is_int_tuple_floats(void) {
  PyObject *arg1 = Py_BuildValue("(ddd)", 1.0, 2.0, 3.0);
  PyObject *arg2 = Py_BuildValue("(ddd)", -1.1, -2.2, -3.3);
  PyObject *arg3 = Py_BuildValue("(ddd)", 1.0, -2.0, -3.1);

  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg1));
  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg2));
  TEST_ASSERT_EQUAL(0, _pg_is_int_tuple(arg3));
}

#define RUN_TEST(TestFunc, TestLineNum)                                        \
  {                                                                            \
    Unity.CurrentTestName = #TestFunc;                                         \
    Unity.CurrentTestLineNumber = TestLineNum;                                 \
    Unity.NumberOfTests++;                                                     \
    if (TEST_PROTECT()) {                                                      \
      setUp();                                                                 \
      TestFunc();                                                              \
    }                                                                          \
    if (TEST_PROTECT()) {                                                      \
      tearDown();                                                              \
    }                                                                          \
    UnityConcludeTest();                                                       \
  }

/*=======Test Reset Option=====*/
void resetTest(void) {
  tearDown();
  setUp();
}

#undef main
/*=======MAIN=====*/
int main(void) {
  Py_Initialize();
  UnityBegin("test_base.c");
  RUN_TEST(test__pg_is_int_tuple_nominal, 17);
  RUN_TEST(test__pg_is_int_tuple_failureModes, 31);
  RUN_TEST(test__pg_is_int_tuple_floats, 45);

  return (UnityEnd());
}
