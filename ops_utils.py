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


import bpy
from bpy.types import Operator
from bpy.props import StringProperty


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
            "group_animated": "",
            "group_effectors": "",
        }

        ob_preset = {k: v for k, v in ob["commotion_preset"].items() if k in settings.keys()}
        settings.update(ob_preset)

        props = context.scene.commotion

        for k, v in settings.items():
            setattr(props, "offset_" + k, v)

        return {"FINISHED"}


class AddToGroup:
    bl_label = "Add to group"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    prop_pfx = StringProperty(options={"HIDDEN", "SKIP_SAVE"})

    def execute(self, context):
        obs = context.selected_objects

        if not obs:
            self.report({"WARNING"}, "No objects selected")
            return {"CANCELLED"}

        group = bpy.data.groups.new(self.group_name)

        for ob in obs:
            group.objects.link(ob)

        setattr(context.scene.commotion, self.prop_pfx + self.prop_suf, group.name)

        return {"FINISHED"}


class OBJECT_OT_commotion_add_to_group_animated(Operator, AddToGroup):
    bl_description = "Add selected objects to Animated group"
    bl_idname = "object.commotion_add_to_group_animated"

    group_name = "Animated"
    prop_suf = "_group_animated"


class OBJECT_OT_commotion_add_to_group_effector(Operator, AddToGroup):
    bl_description = "Add selected objects to Effectors group"
    bl_idname = "object.commotion_add_to_group_objects_effector"

    group_name = "Effectors"
    prop_suf = "_group_effectors"
