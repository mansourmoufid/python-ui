import ctypes

from . import encode
from . import libui
from . import window


# void uiMsgBox(uiWindow *parent, const char *title, const char *description);
_msg_box = libui.uiMsgBox
_msg_box.restype = None
_msg_box.argtypes = [
    ctypes.POINTER(window._Window),
    ctypes.c_char_p,
    ctypes.c_char_p,
]


# void uiMsgBoxError(
#     uiWindow *parent,
#     const char *title,
#     const char *description
# );
_msg_box_error = libui.uiMsgBoxError
_msg_box_error.restype = None
_msg_box_error.argtypes = [
    ctypes.POINTER(window._Window),
    ctypes.c_char_p,
    ctypes.c_char_p,
]


def message(win, title, description):
    assert isinstance(win, window.Window)
    assert isinstance(title, str)
    assert isinstance(description, str)
    _msg_box_error(win.window, encode(title), encode(description))


def error(win, title, description):
    assert isinstance(win, window.Window)
    assert isinstance(title, str)
    assert isinstance(description, str)
    _msg_box_error(win.window, encode(title), encode(description))
