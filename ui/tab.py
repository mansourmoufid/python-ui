import collections
import ctypes

from . import control
from . import encode
from . import libui


class _Tab(ctypes.Structure):
    pass


# void uiTabAppend(uiTab *t, const char *name, uiControl *c);
_tab_append = libui.uiTabAppend
_tab_append.restype = None
_tab_append.argtypes = [
    ctypes.POINTER(_Tab),
    ctypes.c_char_p,
    ctypes.POINTER(control._Control),
]


# int uiTabMargined(uiTab *t, int page);
_tab_margined = libui.uiTabMargined
_tab_margined.restype = ctypes.c_int
_tab_margined.argtypes = [
    ctypes.POINTER(_Tab),
    ctypes.c_int,
]


# void uiTabSetMargined(uiTab *t, int page, int margined);
_tab_set_margined = libui.uiTabSetMargined
_tab_set_margined.restype = None
_tab_set_margined.argtypes = [
    ctypes.POINTER(_Tab),
    ctypes.c_int,
    ctypes.c_int,
]


# uiTab *uiNewTab(void);
_new_tab = libui.uiNewTab
_new_tab.restype = ctypes.POINTER(_Tab)
_new_tab.argtypes = []


class Tab(control.Control):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tab = _new_tab()
        self.ctrl = self.tab
        self.pages = collections.OrderedDict()

    def append(self, name, x, margined=False):
        assert isinstance(name, str)
        assert isinstance(x, control.Control)
        _tab_append(self.tab, encode(name), x.control())
        self.pages[name] = x
        self.margined(name, margined)

    def margined(self, page, x=None):
        assert isinstance(page, str)
        assert page in self.pages
        i = list(self.pages).index(page)
        if x is None:
            return not _tab_margined(self.tab, i) == 0
        else:
            assert isinstance(x, bool)
            _tab_set_margined(self.tab, i, 1 if x else 0)

    def __len__(self):
        return len(self.pages)

    def __getitem__(self, x):
        assert isinstance(x, (int, str))
        if isinstance(x, int):
            return list(self.pages)[x]
        else:
            return self.pages[x]

    def __del__(self):
        for page in list(self.pages):
            del self.pages[page]
