import ctypes


def _proc_from_address(addr):
    return ctypes.CFUNCTYPE(None)(addr)
