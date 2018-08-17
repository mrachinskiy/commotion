# ##### BEGIN GPL LICENSE BLOCK #####
#
#  JewelCraft jewelry design toolkit for Blender.
#  Copyright (C) 2014-2018  Mikhail Rachinskiy
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Commotion",
    "author": "Mikhail Rachinskiy",
    "version": (1, 6, 0),
    "blender": (2, 77, 0),
    "location": "3D View > Tool Shelf",
    "description": "Animation offset tools for motion graphics.",
    "wiki_url": "https://github.com/mrachinskiy/commotion#readme",
    "tracker_url": "https://github.com/mrachinskiy/commotion/issues",
    "category": "Animation",
}


if "bpy" in locals():
    import importlib

    importlib.reload(preferences)
    importlib.reload(ui)
    importlib.reload(ops_anim)
    importlib.reload(ops_driver)
    importlib.reload(ops_shapekey)
    importlib.reload(ops_slow_parent)
    importlib.reload(ops_utils)
else:
    import bpy
    from bpy.props import PointerProperty, CollectionProperty
    from . import (
        preferences,
        ui,
        ops_anim,
        ops_driver,
        ops_shapekey,
        ops_slow_parent,
        ops_utils,
        addon_updater_ops,
    )


classes = (
    preferences.CommotionShapeKeyCollection,
    preferences.CommotionPreferences,
    preferences.CommotionPropertiesScene,
    ui.VIEW3D_PT_commotion_update,
    ui.VIEW3D_PT_commotion_shape_keys,
    ui.VIEW3D_PT_commotion_sk_fcurves,
    ui.VIEW3D_PT_commotion_sk_nla,
    ui.VIEW3D_PT_commotion_sk_drivers,
    ui.VIEW3D_PT_commotion_ob_fcurves,
    ui.VIEW3D_PT_commotion_ob_nla,
    ui.VIEW3D_PT_commotion_slow_parent,
    ops_shapekey.OBJECT_OT_commotion_sk_coll_refresh,
    ops_shapekey.OBJECT_OT_commotion_sk_interpolation_set,
    ops_shapekey.ANIM_OT_commotion_sk_auto_keyframes,
    ops_anim.ANIM_OT_commotion_animation_link,
    ops_anim.ANIM_OT_commotion_animation_copy,
    ops_anim.ANIM_OT_commotion_fcurves_to_nla,
    ops_anim.ANIM_OT_commotion_nla_to_fcurves,
    ops_anim.NLA_OT_commotion_sync_length,
    ops_anim.ANIM_OT_commotion_offset_cursor,
    ops_anim.ANIM_OT_commotion_offset_multitarget,
    ops_anim.ANIM_OT_commotion_offset_name,
    ops_driver.ANIM_OT_commotion_sk_driver_distance_set,
    ops_driver.ANIM_OT_commotion_sk_driver_expression_copy,
    ops_driver.ANIM_OT_commotion_sk_driver_target_remap,
    ops_driver.ANIM_OT_commotion_sk_driver_function_register,
    ops_driver.OBJECT_OT_commotion_sk_reset_eval_time,
    ops_driver.ANIM_OT_commotion_sk_driver_func_expression_get,
    ops_driver.ANIM_OT_commotion_sk_driver_func_expression_set,
    ops_slow_parent.OBJECT_OT_commotion_slow_parent_offset,
    ops_slow_parent.OBJECT_OT_commotion_slow_parent_toggle,
    ops_utils.VIEW3D_OT_commotion_preset_apply,
    ops_utils.OBJECT_OT_commotion_add_to_group_objects,
    ops_utils.OBJECT_OT_commotion_add_to_group_targets,
)


def register():
    addon_updater_ops.register(bl_info)

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.commotion = PointerProperty(type=preferences.CommotionPropertiesScene)
    bpy.types.WindowManager.commotion_skcoll = CollectionProperty(type=preferences.CommotionShapeKeyCollection)


def unregister():
    addon_updater_ops.unregister()

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.commotion
    del bpy.types.WindowManager.commotion_skcoll


if __name__ == "__main__":
    register()
