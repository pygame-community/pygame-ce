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


_splits = version.split(".")

# handle optional dev tag
if len(_splits) == 3:
    _splits.append('""')
elif len(_splits) == 4:
    _splits[3] = f'".{_splits[3]}"'
else:
    raise ValueError("Invalid version!")

version_short = ".".join(_splits[:3])
version_macros = tuple(
    zip(
        ("PG_MAJOR_VERSION", "PG_MINOR_VERSION", "PG_PATCH_VERSION", "PG_VERSION_TAG"),
        _splits,
    )
)


if __name__ == "__main__":
    print(
        "\n".join(f"-D{key}={value}" for key, value in version_macros)
        if "--macros" in sys.argv
        else version
    )
