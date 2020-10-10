# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Commotion motion graphics add-on for Blender.
#  Copyright (C) 2014-2020  Mikhail Rachinskiy
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
    EnumProperty,
)


class ANIM_OT_animation_offset(Operator):
    bl_label = "Offset Animation"
    bl_description = "Offset animation"
    bl_idname = "anim.commotion_animation_offset"
    bl_options = {"REGISTER", "UNDO"}

    use_ob: BoolProperty(name="Object", description="Affect object animation data")
    use_data: BoolProperty(name="Object Data", description="Affect object data animation data")
    use_sk: BoolProperty(name="Shape Keys", description="Affect shape keys animation data")
    use_mat: BoolProperty(name="Material", description="Affect material animation data")
    use_reverse: BoolProperty(name="Reverse", description="Reverse animation offset")
    use_proxy: BoolProperty(
        name="Proxymity",
        description="Enable offset by proximity from effector (effector range controlled by object size)",
    )
    offset: FloatProperty(
        name="Frame Offset",
        description="Frame step for animation offset",
        default=1.0,
        min=0,
        step=10,
        precision=3,
    )
    threshold: IntProperty(
        name="Threshold",
        description="Number of objects to animate per frame step",
        default=1,
        min=1,
    )
    seed: IntProperty(
        name="Seed",
        description="Seed value for randomizer to get different offset patterns",
        min=0,
    )
    sort_method: EnumProperty(
        name="Sort By",
        description="Sort objects method",
        items=(
            ("CURSOR", "Cursor", ""),
            ("NAME", "Name", ""),
            ("MULTI", "Multi-Offset", ""),
            ("RANDOM", "Random", ""),
        ),
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column(heading="Data")
        sub = col.column(align=True)
        sub.prop(self, "use_ob")
        sub.prop(self, "use_data")
        sub.prop(self, "use_sk")
        sub.prop(self, "use_mat")

        sub = col.column()
        sub.enabled = not (self.sort_method == "MULTI" and self.use_proxy)
        sub.prop(self, "offset")
        sub.prop(self, "threshold")
        sub.prop(self, "use_reverse")

        col.prop(self, "sort_method")

        if self.sort_method == "MULTI":
            col.prop(self, "use_proxy")
        elif self.sort_method == "RANDOM":
            col.prop(self, "seed")

    def execute(self, context):
        from . import offset_methods

        if self.sort_method == "CURSOR":
            offset_methods.offset_from_cursor(self, context)
        elif self.sort_method == "NAME":
            offset_methods.offset_from_name(self, context)
        elif self.sort_method == "RANDOM":
            offset_methods.offset_from_random(self, context)
        else:
            props = context.scene.commotion

            if not props.offset_coll_animated or not props.offset_coll_effectors:
                self.report({"ERROR"}, "Animated or Effectors collections are not specified")
                return {"CANCELLED"}

            if self.use_proxy:
                offset_methods.offset_from_multi_proxy(
                    self,
                    context,
                    props.offset_coll_animated,
                    props.offset_coll_effectors,
                )
            else:
                offset_methods.offset_from_multi(
                    self,
                    props.offset_coll_animated,
                    props.offset_coll_effectors,
                )

        return {"FINISHED"}

    def invoke(self, context, event):
        scene = context.scene
        props = scene.commotion

        self.use_ob = props.offset_use_ob
        self.use_data = props.offset_use_data
        self.use_sk = props.offset_use_sk
        self.use_mat = props.offset_use_mat
        self.frame = scene.frame_current
        self.cursor = scene.cursor.location
        self.offset = props.offset_offset
        self.threshold = props.offset_threshold
        self.seed = props.offset_seed
        self.use_reverse = props.offset_use_reverse
        self.sort_method = props.offset_sort_method
        self.use_proxy = props.offset_use_proxy

        if self.sort_method == "MULTI" and not (props.offset_coll_animated and props.offset_coll_effectors):
            self.report({"ERROR"}, "Animated or Effectors collections are not specified")
            return {"CANCELLED"}

        return self.execute(context)


class ANIM_OT_animation_offset_eyedropper(Operator):
    bl_label = "Animation Offset Eyedropper"
    bl_description = "Set offset and threshold properties from selected animated objects"
    bl_idname = "anim.commotion_animation_offset_eyedropper"
    bl_options = {"REGISTER", "UNDO"}

    use_ob: BoolProperty(name="Object")
    use_data: BoolProperty(name="Object Data")
    use_sk: BoolProperty(name="Shape Keys")
    use_mat: BoolProperty(name="Material")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column(heading="Data")
        col.prop(self, "use_ob")
        col.prop(self, "use_data")
        col.prop(self, "use_sk")
        col.prop(self, "use_mat")

    def execute(self, context):
        from collections import Counter
        from .. import lib

        obs_frames = []

        for ob in context.selected_objects:
            ads = lib.ad_get(ob, self.use_ob, self.use_data, self.use_sk, self.use_mat)

            if not ads:
                continue

            ob_frames = []

            for ad in ads:

                if ad.action:
                    ob_frames.append(ad.action.frame_range[0])

                for track in ad.nla_tracks:
                    for strip in track.strips:
                        ob_frames.append(strip.frame_start)

            obs_frames.append(min(ob_frames))

        if not (obs_frames and len(obs_frames) >= 2):
            self.report({"ERROR"}, "At least two animated objects must be selected")
            return {"CANCELLED"}

        frame_steps = sorted(set(obs_frames))

        props = context.scene.commotion
        props.offset_offset = frame_steps[1] - frame_steps[0] if len(frame_steps) >= 2 else 0.0
        props.offset_threshold = Counter(obs_frames).most_common(1)[0][1]

        context.area.tag_redraw()

        return {"FINISHED"}

    def invoke(self, context, event):
        props = context.scene.commotion
        self.use_ob = props.offset_use_ob
        self.use_data = props.offset_use_data
        self.use_sk = props.offset_use_sk
        self.use_mat = props.offset_use_mat

        if event.ctrl:
            return context.window_manager.invoke_props_dialog(self)

        return self.execute(context)
