import ctypes

from . import control
from . import decode, encode
from . import libui


class _Entry(ctypes.Structure):
    pass


# char *uiEntryText(uiEntry *e);
_entry_text = libui.uiEntryText
_entry_text.restype = ctypes.c_char_p
_entry_text.argtypes = [
    ctypes.POINTER(_Entry),
]


# void uiEntrySetText(uiEntry *e, const char *text);
_entry_set_text = libui.uiEntrySetText
_entry_set_text.restype = None
_entry_set_text.argtypes = [
    ctypes.POINTER(_Entry),
    ctypes.c_char_p,
]


# void uiEntryOnChanged(
#   uiEntry *e,
#   void (*f)(uiEntry *e, void *data),
#   void *data
# );
_entry_on_changed = libui.uiEntryOnChanged
_entry_on_changed.restype = None
_entry_on_changed.argtypes = [
    ctypes.POINTER(_Entry),
    ctypes.CFUNCTYPE(
        None,
        ctypes.POINTER(_Entry),
        ctypes.c_void_p,
    ),
    ctypes.c_void_p,
]


# int uiEntryReadOnly(uiEntry *e);
_entry_read_only = libui.uiEntryReadOnly
_entry_read_only.restype = ctypes.c_int
_entry_read_only.argtypes = [
    ctypes.POINTER(_Entry),
]


# void uiEntrySetReadOnly(uiEntry *e, int readonly);
_entry_set_read_only = libui.uiEntrySetReadOnly
_entry_set_read_only.restype = None
_entry_set_read_only.argtypes = [
    ctypes.POINTER(_Entry),
    ctypes.c_int,
]


class Entry(control.Control):

    def __init__(self):
        super(Entry, self).__init__()
        self.ctrl = self.control(self.entry)
        self.callbacks = []
        cb = _entry_on_changed.argtypes[1](self.on_changed)
        _entry_on_changed(self.entry, cb, None)
        self.callbacks += [cb]

    def text(self, x=None):
        assert x is None or isinstance(x, str)
        if x is None:
            return decode(_entry_text(self.entry))
        else:
            _entry_set_text(self.entry, encode(x))

    def readonly(self, x=None):
        assert x is None or isinstance(x, bool)
        if x is None:
            return not _entry_read_only(self.entry) == 0
        else:
            _entry_set_read_only(self.entry, 1 if x else 0)

    def on_changed(self, entry, data):
        pass


# uiEntry *uiNewSearchEntry(void);
_new_search_entry = libui.uiNewSearchEntry
_new_search_entry.restype = ctypes.POINTER(_Entry)
_new_search_entry.argtypes = []


class SearchEntry(Entry):

    def __new__(cls, *args, **kwargs):
        x = super(SearchEntry, cls).__new__(cls)
        x.entry = _new_search_entry()
        return x
