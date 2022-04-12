# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2014-2022 Mikhail Rachinskiy

bl_info = {
    "name": "Commotion",
    "author": "Mikhail Rachinskiy",
    "version": (2, 3, 0),
    "blender": (2, 93, 0),
    "location": "3D View > Sidebar",
    "description": "Animation offset tools for motion graphics.",
    "doc_url": "https://github.com/mrachinskiy/commotion#readme",
    "tracker_url": "https://github.com/mrachinskiy/commotion/issues",
    "category": "Animation",
}


if "bpy" in locals():
    _essential.reload_recursive(var.ADDON_DIR, locals())
else:
    import bpy
    from bpy.props import PointerProperty

    from . import _essential, var

    _essential.check(var.ADDON_DIR / "mod_update", bl_info["blender"])

    from . import (
        mod_update,
        op_offset,
        ops_anim,
        ops_proxy,
        ops_shapekey,
        preferences,
        ui,
    )


classes = (
    preferences.CommotionShapeKeyCollection,
    preferences.CommotionPreferences,
    preferences.SceneProperties,
    preferences.WmProperties,
    ui.VIEW3D_MT_commotion,
    ui.VIEW3D_PT_commotion_update,
    ui.VIEW3D_PT_commotion_animation_offset,
    ui.VIEW3D_PT_commotion_animation_utils,
    ui.VIEW3D_PT_commotion_shape_keys,
    ui.VIEW3D_PT_commotion_proxy_effector,
    ui.VIEW3D_PT_commotion_proxy_effector_loc,
    ui.VIEW3D_PT_commotion_proxy_effector_rot,
    ui.VIEW3D_PT_commotion_proxy_effector_sca,
    ui.VIEW3D_PT_commotion_proxy_effector_sk,
    ui.VIEW3D_PT_commotion_proxy_effector_bake,
    op_offset.ANIM_OT_animation_offset,
    op_offset.ANIM_OT_animation_offset_eyedropper,
    ops_shapekey.OBJECT_OT_sk_coll_refresh,
    ops_shapekey.OBJECT_OT_sk_interpolation_set,
    ops_shapekey.ANIM_OT_sk_generate_keyframes,
    ops_anim.ANIM_OT_animation_copy,
    ops_anim.ANIM_OT_animation_link,
    ops_anim.ANIM_OT_animation_convert,
    ops_proxy.ANIM_OT_bake,
    ops_proxy.ANIM_OT_bake_remove,
    *mod_update.ops,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.commotion = PointerProperty(type=preferences.SceneProperties)
    bpy.types.WindowManager.commotion = PointerProperty(type=preferences.WmProperties)

    # Menu
    # ---------------------------

    bpy.types.VIEW3D_MT_object.append(ui.draw_commotion_menu)

    # mod_update
    # ---------------------------

    mod_update.init(
        addon_version=bl_info["version"],
        repo_url="mrachinskiy/commotion",
    )


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
