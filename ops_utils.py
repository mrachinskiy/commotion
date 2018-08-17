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


import bpy
from bpy.types import Operator
from bpy.props import StringProperty


class VIEW3D_OT_commotion_preset_apply(Operator):
    bl_label = "Apply Preset"
    bl_description = "Apply preset from active object"
    bl_idname = "view3d.commotion_preset_apply"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    prop_pfx = StringProperty(options={"HIDDEN", "SKIP_SAVE"})

    def execute(self, context):
        ob = context.active_object

        if "commotion_preset" not in ob:
            self.report({"WARNING"}, "No presets on active object")
            return {"CANCELLED"}

        settings = {
            "offset": 1.0,
            "threshold": 1,
            "reverse": False,
            "sort_options": "CURSOR",
            "group_objects": "",
            "group_targets": "",
        }
        settings.update(ob["commotion_preset"])

        props = context.scene.commotion
        setattr(props, self.prop_pfx + "_offset", settings["offset"])
        setattr(props, self.prop_pfx + "_threshold", settings["threshold"])
        setattr(props, self.prop_pfx + "_reverse", settings["reverse"])
        setattr(props, self.prop_pfx + "_sort_options", settings["sort_options"])
        setattr(props, self.prop_pfx + "_group_objects", settings["group_objects"])
        setattr(props, self.prop_pfx + "_group_targets", settings["group_targets"])

        return {"FINISHED"}


class AddToGroup:
    bl_label = "Add to group"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    prop_pfx = StringProperty(options={"HIDDEN", "SKIP_SAVE"})

    def execute(self, context):
        group_name = bpy.data.groups.new(self.group).name
        bpy.ops.object.group_link(group=group_name)
        bpy.ops.group.objects_add_active()

        setattr(context.scene.commotion, self.prop_pfx + self.prop_suf, group_name)

        return {"FINISHED"}


class OBJECT_OT_commotion_add_to_group_objects(Operator, AddToGroup):
    bl_description = "Add selected objects to Objects group for multi-offset"
    bl_idname = "object.commotion_add_to_group_objects"
    group = "Objects"
    prop_suf = "_group_objects"


class OBJECT_OT_commotion_add_to_group_targets(Operator, AddToGroup):
    bl_description = "Add selected objects to Targets group for multi-offset"
    bl_idname = "object.commotion_add_to_group_objects_targets"
    group = "Targets"
    prop_suf = "_group_targets"
