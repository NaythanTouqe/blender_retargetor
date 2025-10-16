_need_reload = "main_sre" in locals()

import bpy
from . import main_sre

if _need_reload:
    import importlib
    main_sre = importlib.reload(main_sre)
    print("simple retargeting extention : reloading")



def register():
    main_sre.register()


def unregister():
    main_sre.unregister()


if __name__ == "__main__":
    register()
