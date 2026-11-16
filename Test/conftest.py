from types import SimpleNamespace
import sys
import types
import pytest


# Some Python installations ship tkinter.py without the optional _tkinter
# extension. The game only needs Tk constructors at startup, so provide
# placeholders for unit tests that use FakeCanvas and FakeWindow instead.
try:
    import tkinter  # noqa: F401
except ModuleNotFoundError:
    tkinter_stub = types.ModuleType("tkinter")
    tkinter_stub.TclError = type("TclError", (Exception,), {})
    tkinter_stub.Tk = lambda: None
    tkinter_stub.Canvas = lambda parent, width, height, bg: None
    sys.modules["tkinter"] = tkinter_stub


class FakeCanvas:
    '''Small in-memory stand-in for the Tk canvas API used by the game.'''

    def __init__(self):
        self.items = {}
        self.next_id = 1
        self.bindings = {}
        self.after_calls = []

    def _create(self, kind, coords, options):
        item_id = self.next_id
        self.next_id += 1
        item = {"kind": kind, "coords": tuple(coords)}
        item.update(options)
        self.items[item_id] = item
        return item_id

    @staticmethod
    def _options(fill=None, outline=None, width=None, stipple=None, state=None,
                 text=None, font=None):
        options = {}
        if fill is not None:
            options["fill"] = fill
        if outline is not None:
            options["outline"] = outline
        if width is not None:
            options["width"] = width
        if stipple is not None:
            options["stipple"] = stipple
        if state is not None:
            options["state"] = state
        if text is not None:
            options["text"] = text
        if font is not None:
            options["font"] = font
        return options

    def create_rectangle(self, x1, y1, x2, y2, fill=None, outline=None,
                         width=None, stipple=None, state=None):
        options = self._options(fill, outline, width, stipple, state)
        return self._create("rectangle", (x1, y1, x2, y2), options)

    def create_oval(self, x1, y1, x2, y2, fill=None, outline=None,
                    width=None, stipple=None, state=None):
        options = self._options(fill, outline, width, stipple, state)
        return self._create("oval", (x1, y1, x2, y2), options)

    def create_text(self, x, y, text="", font=None, fill=None, state=None):
        options = self._options(text=text, font=font, fill=fill, state=state)
        return self._create("text", (x, y), options)

    def coords(self, item_id, x1=None, y1=None, x2=None, y2=None):
        if x1 is not None and y1 is not None:
            coordinates = (x1, y1)
            if x2 is not None and y2 is not None:
                coordinates += (x2, y2)
            self.items[item_id]["coords"] = coordinates
        return self.items[item_id]["coords"]

    def itemconfig(self, item_id, text=None, state=None, fill=None):
        options = self._options(text=text, state=state, fill=fill)
        self.items[item_id].update(options)

    itemconfigure = itemconfig

    def move(self, item_id, dx, dy):
        coords = self.items[item_id]["coords"]
        self.items[item_id]["coords"] = tuple(
            value + (dx if index % 2 == 0 else dy)
            for index, value in enumerate(coords)
        )

    def delete(self, item_id):
        self.items.pop(item_id, None)

    def find_all(self):
        return tuple(self.items)

    def tag_raise(self, item_id):
        return item_id

    def pack(self):
        self.packed = True

    def bind(self, sequence, callback, add=None):
        binding_id = f"binding-{len(self.bindings) + 1}"
        self.bindings[(sequence, binding_id)] = callback
        return binding_id

    def unbind(self, sequence, binding_id=None):
        self.bindings.pop((sequence, binding_id), None)


class FakeWidget:
    def __init__(self):
        self.bindings = {}
        self.after_calls = []
        self.cancelled = []
        self.destroyed = False

    def bind(self, sequence, callback, add=None):
        binding_id = f"binding-{len(self.bindings) + 1}"
        self.bindings[(sequence, binding_id)] = callback
        return binding_id

    def unbind(self, sequence, binding_id=None):
        self.bindings.pop((sequence, binding_id), None)

    def after(self, milliseconds, callback):
        self.after_calls.append((milliseconds, callback))
        return f"after-{len(self.after_calls)}"

    def after_cancel(self, after_id):
        self.cancelled.append(after_id)

    def destroy(self):
        self.destroyed = True

    def mainloop(self):
        return None

    def geometry(self, value):
        self.geometry_value = value


class FakeWindow:
    def __init__(self):
        self.window = FakeWidget()
        self.canva = FakeCanvas()
        self.window_width = 1000
        self.window_height = 700
        self.running = True

    def create_window(self):
        self.window.geometry(f"{self.window_width}x{self.window_height}")


@pytest.fixture
def canvas():
    return FakeCanvas()


@pytest.fixture
def window():
    return FakeWindow()


@pytest.fixture
def event():
    return lambda x=0, y=0: SimpleNamespace(x=x, y=y)
