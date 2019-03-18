# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Commotion motion graphics add-on for Blender.
#  Copyright (C) 2014-2019  Mikhail Rachinskiy
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
    "version": (2, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Sidebar",
    "description": "Animation offset tools for motion graphics.",
    "wiki_url": "https://github.com/mrachinskiy/commotion#readme",
    "tracker_url": "https://github.com/mrachinskiy/commotion/issues",
    "category": "Animation",
}


if "bpy" in locals():
    import os
    import importlib

    for entry in os.scandir(var.ADDON_DIR):

        if entry.is_file() and entry.name.endswith(".py") and not entry.name.startswith("__"):
            module = os.path.splitext(entry.name)[0]
            importlib.reload(eval(module))

        elif entry.is_dir() and not entry.name.startswith((".", "__")):

            for subentry in os.scandir(entry.path):
                if subentry.is_file() and subentry.name.endswith(".py"):
                    if subentry.name == "__init__.py":
                        module = os.path.splitext(entry.name)[0]
                    else:
                        module = entry.name + "." + os.path.splitext(subentry.name)[0]
                    importlib.reload(eval(module))
else:
    import bpy
    from bpy.props import PointerProperty, CollectionProperty

    from . import (
        var,
        preferences,
        lib,
        proxy_effector,
        op_offset,
        ops_anim,
        ops_proxy,
        ops_shapekey,
        ui,
        mod_update,
    )


var.UPDATE_CURRENT_VERSION = bl_info["version"]

classes = (
    preferences.CommotionShapeKeyCollection,
    preferences.CommotionPreferences,
    preferences.CommotionPropertiesScene,
    preferences.CommotionPropertiesWm,
    ui.VIEW3D_PT_commotion_update,
    ui.VIEW3D_PT_commotion_animation_offset,
    ui.VIEW3D_PT_commotion_animation_utils,
    ui.VIEW3D_PT_commotion_shape_keys,
    ui.VIEW3D_PT_commotion_proxy_effector,
    op_offset.ANIM_OT_commotion_animation_offset,
    ops_shapekey.OBJECT_OT_commotion_sk_coll_refresh,
    ops_shapekey.OBJECT_OT_commotion_sk_interpolation_set,
    ops_shapekey.ANIM_OT_commotion_sk_generate_keyframes,
    ops_anim.ANIM_OT_commotion_animation_copy,
    ops_anim.ANIM_OT_commotion_animation_link,
    ops_anim.ANIM_OT_commotion_animation_convert,
    ops_proxy.ANIM_OT_commotion_bake,
    ops_proxy.ANIM_OT_commotion_bake_remove,
    mod_update.WM_OT_commotion_update_check,
    mod_update.WM_OT_commotion_update_download,
    mod_update.WM_OT_commotion_update_whats_new,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.commotion = PointerProperty(type=preferences.CommotionPropertiesScene)
    bpy.types.WindowManager.commotion = PointerProperty(type=preferences.CommotionPropertiesWm)

    mod_update.update_init_check()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.commotion
    del bpy.types.WindowManager.commotion
    proxy_effector.handler_del()


if __name__ == "__main__":
    register()
