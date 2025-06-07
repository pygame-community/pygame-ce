#include "unity.h"

#ifndef TEST_COMMON_H
#define TEST_COMMON_H

#define RUN_TEST_PG_INTERNAL(TestFunc, TestLineNum, self_arg, null_arg) \
    {                                                                   \
        Unity.CurrentTestName = #TestFunc;                              \
        Unity.CurrentTestLineNumber = TestLineNum;                      \
        Unity.NumberOfTests++;                                          \
        if (TEST_PROTECT())                                             \
        {                                                               \
            setUp();                                                    \
            TestFunc(self_arg, null_arg);                               \
        }                                                               \
        if (TEST_PROTECT())                                             \
        {                                                               \
            tearDown();                                                 \
        }                                                               \
        UnityConcludeTest();                                            \
    }

#endif // #ifndef TEST_COMMON_H
