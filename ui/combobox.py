import ctypes

from . import control
from . import encode
from . import libui


class _Combobox(ctypes.Structure):
    pass


# void uiComboboxAppend(uiCombobox *c, const char *text);
_combobox_append = libui.uiComboboxAppend
_combobox_append.restype = None
_combobox_append.argtypes = [
    ctypes.POINTER(_Combobox),
    ctypes.c_char_p,
]


# int uiComboboxSelected(uiCombobox *c);
_combobox_selected = libui.uiComboboxSelected
_combobox_selected.restype = ctypes.c_int
_combobox_selected.argtypes = [
    ctypes.POINTER(_Combobox),
]


# void uiComboboxSetSelected(uiCombobox *c, int n);
_combobox_set_selected = libui.uiComboboxSetSelected
_combobox_set_selected.restype = None
_combobox_set_selected.argtypes = [
    ctypes.POINTER(_Combobox),
    ctypes.c_int,
]


# void uiComboboxOnSelected(
#   uiCombobox *c,
#   void (*f)(uiCombobox *c, void *data),
#   void *data
# );
_combobox_on_selected = libui.uiComboboxOnSelected
_combobox_on_selected.restype = None
_combobox_on_selected.argtypes = [
    ctypes.POINTER(_Combobox),
    ctypes.CFUNCTYPE(
        None,
        ctypes.POINTER(_Combobox),
        ctypes.c_void_p,
    ),
    ctypes.c_void_p,
]


# uiCombobox *uiNewCombobox(void);
_new_combobox = libui.uiNewCombobox
_new_combobox.restype = ctypes.c_void_p
_new_combobox.argtypes = []


class Combobox(control.Control):

    def __init__(self, items=None, on_selected=None):

        super(Combobox, self).__init__()

        assert items is None or isinstance(items, (list, tuple))
        self.items = items or []

        self.combobox = ctypes.cast(
            _new_combobox(),
            ctypes.POINTER(_Combobox)
        )
        self.ctrl = self.control(self.combobox)
        self.callbacks = []

        for item in self.items:
            self.append(item)
        self.set_on_selected(on_selected)

    def on_selected(self):
        pass

    def set_on_selected(self, f=None):

        if f is None:
            return
        self.on_selected = f

        def _on_selected(combobox, data):
            return self.on_selected()

        cb = _combobox_on_selected.argtypes[1](_on_selected)
        _combobox_on_selected(self.combobox, cb, None)
        self.callbacks += [cb]

    def append(self, x):
        assert isinstance(x, str)
        _combobox_append(self.combobox, encode(x))

    def selected(self, x=None):
        assert x is None or isinstance(x, str)
        if x is None:
            i = _combobox_selected(self.combobox)
            if i in range(len(self.items)):
                return self.items[i]
            else:
                return None
        else:
            i = self.items.index(x)
            _combobox_set_selected(self.combobox, int(i))
