"""
A helper file invoked by the meson buildconfig to write DLL paths to a json file
"""

import json
import sys

from pathlib import Path

dll_parents = {str(Path(i).parent) for i in sys.argv[1:]}
win_dll_dirs_file = Path(__file__).parent / "win_dll_dirs.json"

if __name__ == "__main__":
    win_dll_dirs_file.write_text(json.dumps(list(dll_parents)), encoding="utf-8")
