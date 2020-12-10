import ctypes

from . import control
from . import decode, encode
from . import libui


class _Group(ctypes.Structure):
    pass


# char *uiGroupTitle(uiGroup *g);
_group_title = libui.uiGroupTitle
_group_title.restype = ctypes.c_char_p
_group_title.argtypes = [
    ctypes.POINTER(_Group),
]


# void uiGroupSetTitle(uiGroup *g, const char *title);
_group_set_title = libui.uiGroupSetTitle
_group_set_title.restype = None
_group_set_title.argtypes = [
    ctypes.POINTER(_Group),
    ctypes.c_char_p,
]


# void uiGroupSetChild(uiGroup *g, uiControl *c);
_group_set_child = libui.uiGroupSetChild
_group_set_child.restype = None
_group_set_child.argtypes = [
    ctypes.POINTER(_Group),
    ctypes.POINTER(control._Control),
]


# int uiGroupMargined(uiGroup *g);
_group_margined = libui.uiGroupMargined
_group_margined.restype = ctypes.c_int
_group_margined.argtypes = [
    ctypes.POINTER(_Group),
]


# void uiGroupSetMargined(uiGroup *g, int margined);
_group_set_margined = libui.uiGroupSetMargined
_group_set_margined.restype = None
_group_set_margined.argtypes = [
    ctypes.POINTER(_Group),
    ctypes.c_int,
]


# uiGroup *uiNewGroup(const char *title);
_new_group = libui.uiNewGroup
_new_group.restype = ctypes.POINTER(_Group)
_new_group.argtypes = [
    ctypes.c_char_p,
]


class Group(control.Control):

    def __init__(self, title, margined=False):
        super(Group, self).__init__()
        assert isinstance(title, str)
        self.group = _new_group(encode(title))
        self.ctrl = self.control(self.group)
        self.margined(margined)

    def title(self, x=None):
        assert x is None or isinstance(x, str)
        if x is None:
            return decode(_group_title(self.group))
        else:
            _group_set_title(self.group, encode(x))

    def set_child(self, x):
        assert isinstance(x, control.Control)
        _group_set_child(self.group, x.control())

    def margined(self, x=None):
        assert x is None or isinstance(x, bool)
        if x is None:
            return not _group_margined(self.group) == 0
        else:
            _group_set_margined(self.group, 1 if x else 0)

    def __add__(self, x):
        assert isinstance(x, control.Control)
        self.set_child(x)
        return self
