"""
A simple script that reads the pyproject.toml at the root of the project, and
prints the project version specified in it.
"""

import sys
import pathlib

base_dir = pathlib.Path(__file__).parents[1]
config_file = base_dir / "pyproject.toml"
config_text = config_file.read_text()

if sys.version_info >= (3, 11):
    # more elegant and robust solution
    import tomllib

    conf = tomllib.loads(config_text)
    version = conf["project"]["version"]

else:
    # hacky solution, because we don't have tomllib in stdlib on older python
    # versions
    import re
    import ast

    finds = re.findall(r"^version\s*=(.*)", config_text, flags=re.MULTILINE)
    if len(finds) != 1:
        raise RuntimeError(f"Could not find precise version from {config_file}")

    version = ast.literal_eval(finds[0].strip())

print(version)
