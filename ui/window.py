import ctypes

from . import control
from . import decode, encode
from . import libui


class _Window(ctypes.Structure):
    pass


# char *uiWindowTitle(uiWindow *w);
_window_title = libui.uiWindowTitle
_window_title.restype = ctypes.c_char_p
_window_title.argtypes = [
    ctypes.POINTER(_Window),
]


# void uiWindowSetTitle(uiWindow *w, const char *title);
_window_set_title = libui.uiWindowSetTitle
_window_set_title.restype = None
_window_set_title.argtypes = [
    ctypes.POINTER(_Window),
    ctypes.c_char_p,
]


# void uiWindowContentSize(uiWindow *w, int *width, int *height);
_window_content_size = libui.uiWindowContentSize
_window_content_size.restype = None
_window_content_size.argtypes = [
    ctypes.POINTER(_Window),
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
]


# void uiWindowSetContentSize(uiWindow *w, int width, int height);
_window_set_content_size = libui.uiWindowSetContentSize
_window_set_content_size.restype = None
_window_set_content_size.argtypes = [
    ctypes.POINTER(_Window),
    ctypes.c_int,
    ctypes.c_int,
]


# void uiWindowOnContentSizeChanged(
#   uiWindow *w,
#   void (*f)(uiWindow *, void *),
#   void *data
# );
_window_on_content_size_changed = libui.uiWindowOnContentSizeChanged
_window_on_content_size_changed.restype = None
_window_on_content_size_changed.argtypes = [
    ctypes.POINTER(_Window),
    ctypes.CFUNCTYPE(
        None,
        ctypes.POINTER(_Window),
        ctypes.c_void_p,
    ),
    ctypes.c_void_p,
]


# void uiWindowOnClosing(
#   uiWindow *w,
#   int (*f)(uiWindow *w, void *data),
#   void *data
# );
_window_on_closing = libui.uiWindowOnClosing
_window_on_closing.restype = None
_window_on_closing.argtypes = [
    ctypes.POINTER(_Window),
    ctypes.CFUNCTYPE(
        ctypes.c_int,
        ctypes.POINTER(_Window),
        ctypes.c_void_p,
    ),
    ctypes.c_void_p,
]


# int uiWindowBorderless(uiWindow *w);
_window_borderless = libui.uiWindowBorderless
_window_borderless.restype = ctypes.c_int
_window_borderless.argtypes = [
    ctypes.POINTER(_Window),
]


# void uiWindowSetBorderless(uiWindow *w, int borderless);
_window_set_borderless = libui.uiWindowSetBorderless
_window_set_borderless.restype = None
_window_set_borderless.argtypes = [
    ctypes.POINTER(_Window),
    ctypes.c_int,
]


# void uiWindowSetChild(uiWindow *w, uiControl *child);
_window_set_child = libui.uiWindowSetChild
_window_set_child.restype = None
_window_set_child.argtypes = [
    ctypes.POINTER(_Window),
    ctypes.POINTER(control._Control),
]


# int uiWindowMargined(uiWindow *w);
_window_margined = libui.uiWindowMargined
_window_margined.restype = ctypes.c_int
_window_margined.argtypes = [
    ctypes.POINTER(_Window),
]


# void uiWindowSetMargined(uiWindow *w, int margined);
_window_set_margined = libui.uiWindowSetMargined
_window_set_margined.restype = None
_window_set_margined.argtypes = [
    ctypes.POINTER(_Window),
    ctypes.c_int,
]


# uiWindow *uiNewWindow(
#   const char *title,
#   int width,
#   int height,
#   int hasMenubar
# );
_new_window = libui.uiNewWindow
_new_window.restype = ctypes.POINTER(_Window)
_new_window.argtypes = [
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]


class Window(control.Control):

    def __init__(self, name=None, size=None, menubar=False, **kwargs):

        border = kwargs.pop('border', True)
        margined = kwargs.pop('margined', True)

        super(Window, self).__init__(**kwargs)

        assert name is None or isinstance(name, str)

        assert size is None or isinstance(size, (list, tuple))
        self.width, self.height = size or (100, 100)

        assert isinstance(menubar, bool)
        assert isinstance(border, bool)
        assert isinstance(margined, bool)

        self.window = _new_window(
            encode(name),
            int(self.width),
            int(self.height),
            1 if menubar else 0
        )
        self.ctrl = self.window
        self.callbacks = []

        def _on_closing(window, data):
            return self.on_closing()

        def _on_resize(window, data):
            return self.on_resize()

        cb = _window_on_closing.argtypes[1](_on_closing)
        _window_on_closing(self.window, cb, None)
        self.callbacks += [cb]
        cb = _window_on_content_size_changed.argtypes[1](_on_resize)
        _window_on_content_size_changed(self.window, cb, None)
        self.callbacks += [cb]

        self.border(border)
        self.margined(margined)

    def title(self, x=None):
        assert x is None or isinstance(x, str)
        if x is None:
            return decode(_window_title(self.window))
        else:
            _window_set_title(self.window, encode(x))

    def size(self, x=None):
        assert x is None or isinstance(x, (list, tuple))
        if x is None:
            w = ctypes.c_int()
            h = ctypes.c_int()
            _window_content_size(
                self.window,
                ctypes.byref(w),
                ctypes.byref(h),
            )
            return (w.value, h.value)
        else:
            w, h = x
            assert isinstance(w, (float, int))
            assert isinstance(h, (float, int))
            _window_set_content_size(self.window, int(w), int(h))

    def border(self, x=None):
        assert x is None or isinstance(x, bool)
        if x is None:
            return _window_borderless(self.window) == 0
        else:
            _window_set_borderless(self.window, 0 if x else 1)

    def on_closing(self):
        self.destroy()
        return 0

    def on_resize(self):
        pass

    def set_child(self, child):
        assert isinstance(child, control.Control)
        _window_set_child(self.window, child.control())
        child.parent = self

    def margined(self, x=None):
        assert x is None or isinstance(x, bool)
        if x is None:
            return not _window_margined(self.window) == 0
        else:
            _window_set_margined(self.window, 1 if x else 0)

    def __add__(self, x):
        self.set_child(x)
        return self
