import ctypes
import sys


def _gl_proc_from_address(addr):
    if sys.platform == "win32":
        # use __stdcall on win32
        return ctypes.WINFUNCTYPE(None)(addr)
    return ctypes.CFUNCTYPE(None)(addr)
