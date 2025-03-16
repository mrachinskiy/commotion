# SPDX-FileCopyrightText: 2014-2025 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later


if "bpy" in locals():
    from pathlib import Path
    essentials.reload_recursive(Path(__file__).parent, locals())
else:
    import bpy
    from bpy.props import PointerProperty

    from . import essentials, op_offset, ops_anim, ops_proxy, ops_shapekey, preferences, ui


classes = essentials.get_classes(
    (preferences, ui, op_offset, ops_shapekey, ops_anim, ops_proxy)
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.commotion = PointerProperty(type=preferences.SceneProperties)
    bpy.types.WindowManager.commotion = PointerProperty(type=preferences.WmProperties)

    # Menu
    # ---------------------------

    bpy.types.VIEW3D_MT_object.append(ui.draw_commotion_menu)


def unregister():
    from . import proxy_effector

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.commotion
    del bpy.types.WindowManager.commotion

    # Menu
    # ---------------------------

    bpy.types.VIEW3D_MT_object.remove(ui.draw_commotion_menu)

    # Handlers
    # ---------------------------

    proxy_effector.handler_del()


if __name__ == "__main__":
    register()
