import ctypes

from . import encode
from . import libui
from . import nop


class _MenuItem(ctypes.Structure):
    pass


# void uiMenuItemEnable(uiMenuItem *m);
_menu_item_enable = libui.uiMenuItemEnable
_menu_item_enable.restype = None
_menu_item_enable.argtypes = [
    ctypes.POINTER(_MenuItem),
]


# void uiMenuItemDisable(uiMenuItem *m);
_menu_item_disable = libui.uiMenuItemDisable
_menu_item_disable.restype = None
_menu_item_disable.argtypes = [
    ctypes.POINTER(_MenuItem),
]


# void uiMenuItemOnClicked(
#   uiMenuItem *m,
#   void (*f)(uiMenuItem *sender, uiWindow *window, void *data),
#   void *data
# );
_menu_item_on_clicked = libui.uiMenuItemOnClicked
_menu_item_on_clicked.restype = None
_menu_item_on_clicked.argtypes = [
    ctypes.POINTER(_MenuItem),
    ctypes.CFUNCTYPE(
        None,
        ctypes.POINTER(_MenuItem),
        ctypes.c_void_p,
        ctypes.c_void_p,
    ),
    ctypes.c_void_p,
]


# int uiMenuItemChecked(uiMenuItem *m);
_menu_item_checked = libui.uiMenuItemChecked
_menu_item_checked.restype = ctypes.c_int
_menu_item_checked.argtypes = [
    ctypes.POINTER(_MenuItem),
]


# void uiMenuItemSetChecked(uiMenuItem *m, int checked);
_menu_item_set_checked = libui.uiMenuItemSetChecked
_menu_item_set_checked.restype = None
_menu_item_set_checked.argtypes = [
    ctypes.POINTER(_MenuItem),
    ctypes.c_int,
]


class Item(object):

    def __init__(self, item, type=None, on_clicked=None):

        super().__init__()

        self.item = ctypes.cast(item, ctypes.POINTER(_MenuItem))
        self.type = type

        self.callbacks = []
        self.set_on_clicked(on_clicked or self.on_clicked)

    def on_clicked(self, item=None):
        pass

    def set_on_clicked(self, f=None):

        if f is None:
            return
        self.on_clicked = f

        def _on_clicked(item, window, data):
            return self.on_clicked()

        cb = _menu_item_on_clicked.argtypes[1](_on_clicked)
        if not self.type == 'Quit':
            _menu_item_on_clicked(self.item, cb, None)
        self.callbacks += [cb]

    def enable(self, x):
        assert isinstance(x, bool)
        if x:
            _menu_item_enable(self.item)
        else:
            _menu_item_disable(self.item)

    def checked(self, x=None):
        assert self.type == 'Check'
        assert x is None or isinstance(x, bool)
        if x is None:
            return not _menu_item_checked(self.item) == 0
        else:
            _menu_item_set_checked(self.item, 1 if x else 0)


class _Menu(ctypes.Structure):
    pass


# uiMenu *uiNewMenu(const char *name);
_new_menu = libui.uiNewMenu
_new_menu.restype = ctypes.c_void_p
_new_menu.argtypes = [
    ctypes.c_char_p,
]


# uiMenuItem *uiMenuAppendItem(uiMenu *m, const char *name);
_menu_append_item = libui.uiMenuAppendItem
_menu_append_item.restype = ctypes.c_void_p
_menu_append_item.argtypes = [
    ctypes.POINTER(_Menu),
    ctypes.c_char_p,
]


# uiMenuItem *uiMenuAppendCheckItem(uiMenu *m, const char *name);
_menu_append_check_item = libui.uiMenuAppendCheckItem
_menu_append_check_item.restype = ctypes.c_void_p
_menu_append_check_item.argtypes = [
    ctypes.POINTER(_Menu),
    ctypes.c_char_p,
]


# uiMenuItem *uiMenuAppendAboutItem(uiMenu *m);
_menu_append_about_item = libui.uiMenuAppendAboutItem
_menu_append_about_item.restype = ctypes.c_void_p
_menu_append_about_item.argtypes = [
    ctypes.POINTER(_Menu),
]


# uiMenuItem *uiMenuAppendQuitItem(uiMenu *m);
_menu_append_quit_item = libui.uiMenuAppendQuitItem
_menu_append_quit_item.restype = ctypes.c_void_p
_menu_append_quit_item.argtypes = [
    ctypes.POINTER(_Menu),
]


# void uiMenuAppendSeparator(uiMenu *m);
_menu_append_separator = libui.uiMenuAppendSeparator
_menu_append_separator.restype = None
_menu_append_separator.argtypes = [
    ctypes.POINTER(_Menu),
]


# void uiMenuDeleteItem(uiMenu *m, uiMenuItem *item);
_menu_delete_item = libui.uiMenuDeleteItem
_menu_delete_item.restype = None
_menu_delete_item.argtypes = [
    ctypes.POINTER(_Menu),
    ctypes.POINTER(_MenuItem),
]


class Menu(object):

    def __init__(self, name):
        super().__init__()
        assert isinstance(name, str)
        self.name = name
        self.menu = ctypes.cast(
            _new_menu(encode(self.name)),
            ctypes.POINTER(_Menu),
        )
        self.items = {}

    def append(self, name=None, type=None, **kwargs):

        assert name is None or isinstance(name, str)
        assert type in [None, 'Check', 'About', 'Quit', 'Separator']

        if type == 'About':
            item = _menu_append_about_item(self.menu)
        elif type == 'Quit':
            item = _menu_append_quit_item(self.menu)
        elif type == 'Check':
            item = _menu_append_check_item(self.menu, encode(name))
        elif type == 'Separator':
            _menu_append_separator(self.menu)
            return
        else:
            item = _menu_append_item(self.menu, encode(name))

        assert name not in self.items
        if name is None:
            name = type
        on_clicked = kwargs.get('on_clicked', None)
        self.items[name] = Item(
            item,
            type=type,
            on_clicked=on_clicked,
        )

        enabled = kwargs.get('enabled', True)
        assert isinstance(enabled, bool)
        self.items[name].enable(enabled)

        if type == 'Check':
            checked = kwargs.get('checked', True)
            assert isinstance(checked, bool)
            self.items[name].checked(checked)

    def delete(self, item):
        self.items[item].set_on_clicked(nop)
        _menu_delete_item(self.menu, self.items[item].item)
        del self.items[item]

    def __del__(self):
        # for item in tuple(self.items):
        #     self.delete(item)
        pass
