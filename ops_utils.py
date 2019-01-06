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


import bpy
from bpy.types import Operator


class OBJECT_OT_commotion_preset_apply(Operator):
    bl_label = "Apply Preset"
    bl_description = "Apply preset from active object"
    bl_idname = "object.commotion_preset_apply"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        ob = context.active_object

        if "commotion_preset" not in ob:
            self.report({"WARNING"}, "No presets on active object")
            return {"CANCELLED"}

        settings = {
            "offset": 1.0,
            "proxy_radius": 5.0,
            "threshold": 1,
            "seed": 0,
            "use_reverse": False,
            "use_proxy": False,
            "sort_option": "CURSOR",
            "coll_animated": "",
            "coll_effectors": "",
        }

        ob_preset = {k: v for k, v in ob["commotion_preset"].items() if k in settings.keys()}
        settings.update(ob_preset)

        if settings["coll_animated"]:
            settings["coll_animated"] = bpy.data.collections.get(settings["coll_animated"], None)
        if settings["coll_effectors"]:
            settings["coll_effectors"] = bpy.data.collections.get(settings["coll_effectors"], None)

        props = context.scene.commotion

        for k, v in settings.items():
            setattr(props, "offset_" + k, v)

        return {"FINISHED"}
