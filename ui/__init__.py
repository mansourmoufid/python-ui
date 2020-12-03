'''ctypes wrapper for libui'''


import ctypes


__author__ = 'Mansour Moufid'
__copyright__ = 'Copyright 2020, Mansour Moufid'
__license__ = 'ISC'
__version__ = '0.1'
__email__ = 'mansourmoufid@gmail.com'
__status__ = 'Development'

__all__ = [
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
