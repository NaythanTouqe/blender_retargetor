_need_reload = "ui" in locals()

import bpy
from . import common # static or constant stuff. so... no register & unregister.
from . import properties
from . import operation
from . import ui


if _need_reload:
    import importlib

    common = importlib.reload(common)
    properties = importlib.reload(properties)
    operation = importlib.reload(operation)
    ui = importlib.reload(ui)

    print(f"Needing reload = {_need_reload}\n", "simple retargeting extention : reloaded")


def register():
    properties.register()
    operation.register()
    ui.register()


def unregister():
    properties.unregister()
    operation.unregister()
    ui.unregister()


if __name__ == "__main__":
    print("this is an Extension. Run it like one. Please~")
    register()


