import ctypes

from . import libui


class _Control(ctypes.Structure):
    pass


# int uiControlVisible(uiControl *);
_control_visible = libui.uiControlVisible
_control_visible.restype = ctypes.c_int
_control_visible.argtypes = [
    ctypes.POINTER(_Control),
]


# void uiControlShow(uiControl *);
_control_show = libui.uiControlShow
_control_show.restype = None
_control_show.argtypes = [
    ctypes.POINTER(_Control),
]


# void uiControlHide(uiControl *);
_control_hide = libui.uiControlHide
_control_hide.restype = None
_control_hide.argtypes = [
    ctypes.POINTER(_Control),
]


# int uiControlEnabled(uiControl *);
_control_enabled = libui.uiControlEnabled
_control_enabled.restype = ctypes.c_int
_control_enabled.argtypes = [
    ctypes.POINTER(_Control),
]


# void uiControlEnable(uiControl *);
_control_enable = libui.uiControlEnable
_control_enable.restype = None
_control_enable.argtypes = [
    ctypes.POINTER(_Control),
]


# void uiControlDisable(uiControl *);
_control_disable = libui.uiControlDisable
_control_disable.restype = None
_control_disable.argtypes = [
    ctypes.POINTER(_Control),
]


# void uiFreeControl(uiControl *);
_free_control = libui.uiFreeControl
_free_control.restype = None
_free_control.argtypes = [
    ctypes.POINTER(_Control),
]


# void uiControlDestroy(uiControl *);
_control_destroy = libui.uiControlDestroy
_control_destroy.restype = None
_control_destroy.argtypes = [
    ctypes.POINTER(_Control),
]


class Control(object):

    def __init__(self):
        super(Control, self).__init__()
        self.ctrl = None

    def control(self, this=None):
        x = this or self.ctrl
        assert isinstance(x, ctypes._Pointer)
        return ctypes.cast(x, ctypes.POINTER(_Control))

    def enabled(self, x=None):
        if self.ctrl is None:
            return False
        if x is None:
            return not _control_enabled(self.ctrl) == 0
        else:
            assert isinstance(x, bool)
            if x:
                _control_enable(self.ctrl)
            else:
                _control_disable(self.ctrl)

    def visible(self, x=None):
        if self.ctrl is None:
            return False
        if x is None:
            return not _control_visible(self.ctrl) == 0
        else:
            assert isinstance(x, bool)
            if x:
                _control_show(self.ctrl)
            else:
                _control_hide(self.ctrl)

    def destroy(self):
        if self.ctrl is None:
            return
        _control_destroy(self.control())
        self.ctrl = None

    def __del__(self):
        pass
