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


from bpy.types import Operator
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
)

from .offset_methods import OffsetMethods
from .offset_ad import AdOffset


class ANIM_OT_animation_offset(AdOffset, OffsetMethods, Operator):
    bl_label = "Commotion Offset Animation"
    bl_description = "Offset animation"
    bl_idname = "anim.commotion_animation_offset"
    bl_options = {"REGISTER", "UNDO"}

    offset: FloatProperty(name="Frame Offset", description="Frame step for animation offset", default=1, min=0, step=10, precision=3)
    threshold: IntProperty(name="Threshold", description="Number of objects to animate per frame step", default=1, min=1)
    use_reverse: BoolProperty(name="Reverse", description="Reverse animation offset")
    seed: IntProperty(name="Seed", description="Seed value for randomizer to get different offset patterns", min=0)

    def draw(self, context):
        if self.sort_method == "MULTI" and self.use_proxy:
            return

        layout = self.layout
        layout.use_property_split = True

        col = layout.column()
        col.prop(self, "offset")
        col.prop(self, "threshold")
        col.prop(self, "use_reverse")

        if self.sort_method == "RANDOM":
            col.prop(self, "seed")

    def invoke(self, context, event):
        scene = context.scene
        props = scene.commotion

        self.use_ob = props.offset_id_type in {"OBJECT", "ALL"}
        self.use_data = props.offset_id_type in {"OBJECT_DATA", "ALL"}
        self.use_sk = props.offset_id_type in {"SHAPE_KEYS", "ALL"}
        self.use_mat = props.offset_id_type in {"MATERIAL", "ALL"}
        self.frame = scene.frame_current
        self.cursor = scene.cursor.location
        self.offset = props.offset_offset
        self.threshold = props.offset_threshold
        self.seed = props.offset_seed
        self.use_reverse = props.offset_use_reverse
        self.sort_method = props.offset_sort_method
        self.use_proxy = props.offset_use_proxy
        self.coll_animated_name = ""
        self.coll_effectors_name = ""

        if self.sort_method == "MULTI":
            self.coll_animated = props.offset_coll_animated
            self.coll_effectors = props.offset_coll_effectors
            self.coll_animated_name = self.coll_animated.name
            self.coll_effectors_name = self.coll_effectors.name

            if not (self.coll_animated and self.coll_effectors):
                self.report({"ERROR"}, "Animated or Effector collections are not specified")
                return {"CANCELLED"}

        return self.execute(context)

    def execute(self, context):
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
