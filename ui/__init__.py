'''ctypes wrapper for libui'''


import ctypes


__author__ = 'Mansour Moufid'
__copyright__ = 'Copyright 2020, Mansour Moufid'
__license__ = 'ISC'
__version__ = '0.1'
__email__ = 'mansourmoufid@gmail.com'
__status__ = 'Development'

__all__ = [
    'control',
]


try:
    import ctypes.util
    lib = ctypes.util.find_library('ui')
    assert lib is not None
    libui = ctypes.CDLL(lib)
except (AssertionError, OSError):
    import distutils.sysconfig
    import itertools
    import os
    dirs = ['.', distutils.sysconfig.get_config_var('LIBDIR')]
    names = ['libui.dll', 'libui.dylib', 'libui.so']
    libs = [os.path.join(x, y) for x, y in itertools.product(dirs, names)]
    for lib in libs:
        try:
            libui = ctypes.CDLL(lib)
        except OSError:
            continue
        break


class _InitOptions(ctypes.Structure):
    _fields_ = [
        ('size', ctypes.c_size_t),
    ]


# const char *uiInit(uiInitOptions *options);
_init = libui.uiInit
_init.restype = ctypes.c_char_p
_init.argtypes = [
    ctypes.POINTER(_InitOptions),
]


# void uiUninit(void);
_uninit = libui.uiUninit
_uninit.restype = None
_uninit.argtypes = []


# void uiMain(void);
_main = libui.uiMain
_main.restype = None
_main.argtype = []


# void uiQuit(void);
_quit = libui.uiQuit
_quit.restype = None
_quit.argtypes = []


# void uiOnShouldQuit(int (*f)(void *data), void *data);
_on_should_quit = libui.uiOnShouldQuit
_on_should_quit.restype = None
_on_should_quit.argtypes = [
    ctypes.CFUNCTYPE(
        ctypes.c_int,
        ctypes.c_void_p,
    ),
    ctypes.c_void_p,
]


class UI(object):

    def __init__(self):

        options = _InitOptions()
        ctypes.memset(ctypes.pointer(options), 0, ctypes.sizeof(options))
        assert _init(ctypes.pointer(options)) is None

        def __on_should_quit(data):
            return self.on_should_quit()

        cb = _on_should_quit.argtypes[0](__on_should_quit)
        _on_should_quit(cb, None)
        self.callbacks = [cb]

    def main(self):
        _main()

    def on_should_quit(self):
        return 1

    def quit(self):
        _quit()
        return 0

    def __del__(self):
        _uninit()
