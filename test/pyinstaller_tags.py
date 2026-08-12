__tags__ = []

exclude = False
try:
    import PyInstaller
except ImportError:
    exclude = True

if exclude:
    __tags__.extend(("ignore", "subprocess_ignore"))