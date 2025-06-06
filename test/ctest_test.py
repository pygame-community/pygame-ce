import io
import os
import re
import subprocess
import unittest


class Ctest(unittest.TestCase):
    def test_run_ctests(self):
        filename_regex = re.compile(".*run_ctests.*")

        test_dir = os.path.dirname(os.path.abspath(__file__))
        pg_dir = os.path.join(test_dir, "..")

        test_executable_exists = False
        test_filename = ""
        for filename in os.listdir(pg_dir):
            if re.match(filename_regex, filename):
                test_filename = filename
                test_executable_exists = True
                break

        if test_executable_exists:
            cwd = os.getcwd()
            os.chdir(pg_dir)

            with open(f"{cwd}/ctest.log", 'w') as ctest_log:
                test_result = subprocess.run(
                    [test_filename], stdout=ctest_log, stderr=subprocess.STDOUT
                )

            os.chdir(cwd)

            self.assertEqual(test_result.returncode, 0)

        else:
            unittest.skip("Test Executable Not Available")


if __name__ == "__main__":
    unittest.main()
