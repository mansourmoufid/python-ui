import ctypes
import typing

from . import control
from . import decode, encode
from . import libui


class _Button(ctypes.Structure):
    pass


# char *uiButtonText(uiButton *b);
_button_text = libui.uiButtonText
_button_text.restype = ctypes.c_char_p
_button_text.argtypes = [
    ctypes.POINTER(_Button),
]


# void uiButtonSetText(uiButton *b, const char *text);
_button_set_text = libui.uiButtonSetText
_button_set_text.restype = None
_button_set_text.argtypes = [
    ctypes.POINTER(_Button),
    ctypes.c_char_p,
]


# void uiButtonOnClicked(
#   uiButton *b,
#   void (*f)(uiButton *b, void *data),
#   void *data
# );
_button_on_clicked = libui.uiButtonOnClicked
_button_on_clicked.restype = None
_button_on_clicked.argtypes = [
    ctypes.POINTER(_Button),
    ctypes.CFUNCTYPE(
        None,
        ctypes.POINTER(_Button),
        ctypes.c_void_p,
    ),
    ctypes.c_void_p,
]


# uiButton *uiNewButton(const char *text);
_new_button = libui.uiNewButton
_new_button.restype = ctypes.POINTER(_Button)
_new_button.argtypes = [
    ctypes.c_char_p,
]


class Button(control.Control):

    def __init__(
        self,
        text: str,
        on_clicked: typing.Optional[typing.Callable] = None,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.button = _new_button(encode(text))
        self.ctrl = self.button

        self.callbacks: typing.List[typing.Callable] = []
        self.set_on_clicked(on_clicked or self.on_clicked)

    def text(self, x=None):
        assert x is None or isinstance(x, str)
        if x is None:
            return decode(_button_text(self.button))
        else:
            _button_set_text(self.button, encode(x))

    def on_clicked(self):
        pass

    def set_on_clicked(self, f=None):

        if f is None:
            return
        self.on_clicked = f

        def _on_clicked(button, data):
            return self.on_clicked()

        cb = _button_on_clicked.argtypes[1](_on_clicked)
        _button_on_clicked(self.button, cb, None)
        self.callbacks += [cb]
