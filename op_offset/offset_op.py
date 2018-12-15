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

from .. import settings
from .offset_methods import OffsetMethods
from .offset_ad import AdOffset


class ANIM_OT_commotion_animation_offset(Operator, AdOffset, OffsetMethods):
    bl_label = "Commotion Offset Animation"
    bl_description = "Offset animation"
    bl_idname = "anim.commotion_animation_offset"
    bl_options = {"REGISTER", "UNDO"}

    offset = settings.CommotionPropertiesScene.offset_offset
    threshold = settings.CommotionPropertiesScene.offset_threshold
    use_reverse = settings.CommotionPropertiesScene.offset_use_reverse
    seed = settings.CommotionPropertiesScene.offset_seed

    def draw(self, context):
        if self.sort_method == "MULTI" and self.use_proxy:
            return

        layout = self.layout

        split = layout.split()
        split.label("Frame Offset")
        split.prop(self, "offset", text="")

        split = layout.split()
        split.label("Threshold")
        split.prop(self, "threshold", text="")

        split = layout.split()
        split.row()
        split.prop(self, "use_reverse")

        if self.sort_method == "RANDOM":
            split = layout.split()
            split.label("Seed")
            split.prop(self, "seed", text="")

    def invoke(self, context, event):
        scene = context.scene
        props = scene.commotion

        self.is_ob = props.offset_id_type == "OBJECT"
        self.is_fcurves = props.offset_ad_type == "FCURVES"
        self.frame = scene.frame_current
        self.cursor = scene.cursor_location
        self.offset = props.offset_offset
        self.threshold = props.offset_threshold
        self.seed = props.offset_seed
        self.use_reverse = props.offset_use_reverse
        self.sort_method = props.offset_sort_method
        self.group_animated = ""
        self.group_effectors = ""
        self.radius = props.offset_proxy_radius
        self.use_proxy = props.offset_use_proxy

        if self.sort_method == "MULTI":
            self.group_animated = props.offset_group_animated
            self.group_effectors = props.offset_group_effectors

            if not (self.group_animated and self.group_effectors):
                self.report({"ERROR"}, "Object or Effector object groups are not specified")
                return {"CANCELLED"}

        return self.execute(context)

    def preset_add(self, ob):
        ob["commotion_preset"] = self.preset

    def execute(self, context):
        self.preset = {
            "offset": self.offset,
            "proxy_radius": self.radius,
            "threshold": self.threshold,
            "seed": self.seed,
            "use_reverse": self.use_reverse,
            "use_proxy": self.use_proxy,
            "sort_option": self.sort_method,
            "group_animated": self.group_animated,
            "group_effectors": self.group_effectors,
        }

        if self.sort_method == "CURSOR":
            self.offset_from_cursor(context)
        elif self.sort_method == "NAME":
            self.offset_from_name(context)
        elif self.sort_method == "RANDOM":
            self.offset_from_random(context)
        else:
            if self.use_proxy:
                self.offset_from_multi_proxy(context)
            else:
                self.offset_from_multi(context)

        return {"FINISHED"}
