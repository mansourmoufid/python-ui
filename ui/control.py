import ctypes
import typing

from . import libui


class _Control(ctypes.Structure):
    pass


# uintptr_t uiControlHandle(uiControl *);
_control_handle = libui.uiControlHandle
_control_handle.restype = ctypes.c_ulonglong
_control_handle.argtypes = [
    ctypes.POINTER(_Control),
]


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

    def __init__(
        self,
        enabled: typing.Optional[bool] = None,
        visible: typing.Optional[bool] = None,
    ):
        super(Control, self).__init__()
        self.ctrl: typing.Optional[ctypes._Pointer] = None
        if enabled is not None:
            self.enabled(enabled)
        if visible is not None:
            self.visible(visible)

    def control(self) -> typing.Optional[ctypes._Pointer]:
        if self.ctrl is None:
            return None
        return ctypes.cast(self.ctrl, ctypes.POINTER(_Control))

    def handle(self) -> ctypes.c_void_p:
        return ctypes.c_void_p(_control_handle(self.ctrl))

    def enabled(
        self,
        x: typing.Optional[bool] = None,
    ) -> typing.Optional[bool]:
        if self.control() is None:
            return False
        if x is None:
            return not _control_enabled(self.control()) == 0
        else:
            if x and not self.enabled():
                _control_enable(self.control())
            if not x and self.enabled():
                _control_disable(self.control())
        return None

    def visible(
        self,
        x: typing.Optional[bool] = None,
    ) -> typing.Optional[bool]:
        if self.control() is None:
            return False
        if x is None:
            return not _control_visible(self.control()) == 0
        else:
            if x:
                _control_show(self.control())
            else:
                _control_hide(self.control())
        return None

    def destroy(self) -> None:
        if self.control() is None:
            return
        _control_destroy(self.control())
        self.ctrl = None

    def __del__(self):
        pass
