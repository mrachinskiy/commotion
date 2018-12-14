# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Commotion motion graphics add-on for Blender.
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
    "version": (1, 7, 2),
    "blender": (2, 77, 0),
    "location": "3D View > Tool Shelf",
    "description": "Animation offset tools for motion graphics.",
    "wiki_url": "https://github.com/mrachinskiy/commotion#readme",
    "tracker_url": "https://github.com/mrachinskiy/commotion/issues",
    "category": "Animation",
}


if "bpy" in locals():
    import os
    import importlib

    for entry in os.scandir(os.path.dirname(__file__)):

        if entry.is_file() and entry.name.endswith(".py") and not entry.name.startswith("__"):
            module = os.path.splitext(entry.name)[0]
            importlib.reload(eval(module))

        elif entry.is_dir() and not entry.name.startswith((".", "__")) and not entry.name.endswith("updater"):

            for subentry in os.scandir(entry.path):

                if subentry.name.endswith(".py"):
                    module = "{}.{}".format(entry.name, os.path.splitext(subentry.name)[0])
                    importlib.reload(eval(module))
else:
    import bpy
    from bpy.props import PointerProperty, CollectionProperty
    from . import (
        proxy_effector,
        settings,
        ui,
        ops_anim,
        ops_proxy,
        ops_shapekey,
        ops_slow_parent,
        ops_utils,
        addon_updater_ops,
    )
    from .op_offset import offset_op


classes = (
    settings.CommotionShapeKeyCollection,
    settings.CommotionPreferences,
    settings.CommotionPropertiesScene,
    settings.CommotionPropertiesWm,
    ui.VIEW3D_PT_commotion_update,
    ui.VIEW3D_PT_commotion_shape_keys,
    ui.VIEW3D_PT_commotion_animation_offset,
    ui.VIEW3D_PT_commotion_slow_parent,
    ui.VIEW3D_PT_commotion_proxy_effector,
    offset_op.ANIM_OT_commotion_animation_offset,
    ops_shapekey.OBJECT_OT_commotion_sk_coll_refresh,
    ops_shapekey.OBJECT_OT_commotion_sk_interpolation_set,
    ops_shapekey.ANIM_OT_commotion_sk_auto_keyframes,
    ops_anim.ANIM_OT_commotion_animation_copy,
    ops_anim.ANIM_OT_commotion_animation_link,
    ops_anim.ANIM_OT_commotion_animation_convert,
    ops_proxy.ANIM_OT_commotion_bake,
    ops_proxy.ANIM_OT_commotion_bake_remove,
    ops_slow_parent.OBJECT_OT_commotion_slow_parent_offset,
    ops_slow_parent.OBJECT_OT_commotion_slow_parent_toggle,
    ops_utils.OBJECT_OT_commotion_preset_apply,
    ops_utils.OBJECT_OT_commotion_add_to_group_animated,
    ops_utils.OBJECT_OT_commotion_add_to_group_effector,
)


def register():
    addon_updater_ops.register(bl_info)

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.commotion = PointerProperty(type=settings.CommotionPropertiesScene)
    bpy.types.WindowManager.commotion = PointerProperty(type=settings.CommotionPropertiesWm)


def unregister():
    addon_updater_ops.unregister()

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.commotion
    del bpy.types.WindowManager.commotion
    proxy_effector.handler_del()


if __name__ == "__main__":
    register()
