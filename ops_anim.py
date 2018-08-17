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
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty


# Utils
# ---------------------------


class AdSetup:

    def invoke(self, context, event):
        self.ad_type = set(self.prop_pfx.upper().split("_"))

        return self.execute(context)


class AdCheck:

    def invoke(self, context, event):

        self.ad_type = set(self.prop_pfx.upper().split("_"))

        # Get animation data
        # ----------------------------

        if "SK" in self.ad_type:

            try:
                sk = context.active_object.data.shape_keys
                ad = sk.animation_data
            except:
                self.report({"ERROR"}, "Object has no Shape Keys")
                return {"CANCELLED"}

        else:

            ad = context.active_object.animation_data

        # Check
        # ----------------------------

        if "FCURVES" in self.ad_type and not (ad and ad.action):
            self.report({"ERROR"}, "Object has no animation")
            return {"CANCELLED"}

        elif "NLA" in self.ad_type and not (ad and ad.nla_tracks and ad.nla_tracks[0].strips):
            self.report({"ERROR"}, "Object NLA tracks are empty")
            return {"CANCELLED"}

        return self.execute(context)


# Operators
# ---------------------------


class ANIM_OT_commotion_animation_link(Operator, AdCheck):
    bl_label = "Link"
    bl_description = "Link animation from active to selected objects"
    bl_idname = "anim.commotion_animation_link"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    prop_pfx = StringProperty(options={"HIDDEN", "SKIP_SAVE"})

    def execute(self, context):

        def link_strips(ob_strip, obj_strip):
            obj_fstart = obj_strip.action_frame_start
            obj_fend = obj_strip.action_frame_end
            ob_strip.action = obj_strip.action
            ob_strip.action_frame_start = obj_fstart
            ob_strip.action_frame_end = obj_fend

        obj = context.active_object
        obs = context.selected_objects

        if "FCURVES" in self.ad_type:

            if "SK" in self.ad_type:
                action = obj.data.shape_keys.animation_data.action

                for ob in obs:
                    if ob.data and ob.data.shape_keys:
                        sk = ob.data.shape_keys
                        if sk.animation_data:
                            sk.animation_data.action = action
                        else:
                            sk.animation_data_create()
                            sk.animation_data.action = action

            elif "OB" in self.ad_type:
                action = obj.animation_data.action

                for ob in obs:
                    if ob.animation_data:
                        ob.animation_data.action = action
                    else:
                        ob.animation_data_create()
                        ob.animation_data.action = action

        elif "NLA" in self.ad_type:

            if "SK" in self.ad_type:
                obj_strip = obj.data.shape_keys.animation_data.nla_tracks[0].strips[0]

                for ob in obs:

                    try:
                        ob_strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]
                        link_strips(ob_strip, obj_strip)
                    except:
                        continue

            elif "OB" in self.ad_type:
                obj_strip = obj.animation_data.nla_tracks[0].strips[0]

                for ob in obs:

                    try:
                        ob_strip = ob.animation_data.nla_tracks[0].strips[0]
                        link_strips(ob_strip, obj_strip)
                    except:
                        continue

        return {"FINISHED"}


class ANIM_OT_commotion_animation_copy(Operator, AdCheck):
    bl_label = "Copy"
    bl_description = "Copy animation from active to selected objects (can also use this to unlink animation)"
    bl_idname = "anim.commotion_animation_copy"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    prop_pfx = StringProperty(options={"HIDDEN", "SKIP_SAVE"})

    def execute(self, context):
        obj = context.active_object
        obs = context.selected_objects

        if "SK" in self.ad_type:
            action = obj.data.shape_keys.animation_data.action

            for ob in obs:
                if ob.data and ob.data.shape_keys:
                    if ob.data.shape_keys.animation_data:
                        ob.data.shape_keys.animation_data.action = action.copy()
                    else:
                        ob.data.shape_keys.animation_data_create()
                        ob.data.shape_keys.animation_data.action = action.copy()

        elif "OB" in self.ad_type:
            action = obj.animation_data.action

            for ob in obs:
                if ob.animation_data:
                    ob.animation_data.action = action.copy()
                else:
                    ob.animation_data_create()
                    ob.animation_data.action = action.copy()

        return {"FINISHED"}


class ANIM_OT_commotion_fcurves_to_nla(Operator, AdSetup):
    bl_label = "F-Curves to Strips"
    bl_description = "Convert F-Curves to NLA strips"
    bl_idname = "nla.commotion_fcurves_to_nla"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    prop_pfx = StringProperty(options={"HIDDEN", "SKIP_SAVE"})

    def execute(self, context):

        def strips_create(ad):
            fstart = ad.action.frame_range[0]
            if not ad.nla_tracks:
                ad.nla_tracks.new()
            ad.nla_tracks[0].strips.new("name", fstart, ad.action)
            ad.action = None

        if "SK" in self.ad_type:
            for ob in context.selected_objects:

                try:
                    ad = ob.data.shape_keys.animation_data
                    strips_create(ad)
                except:
                    continue

        elif "OB" in self.ad_type:
            for ob in context.selected_objects:

                try:
                    ad = ob.animation_data
                    strips_create(ad)
                except:
                    continue

        return {"FINISHED"}


class ANIM_OT_commotion_nla_to_fcurves(Operator, AdSetup):
    bl_label = "Strips to F-Curves"
    bl_description = "Convert strips back to F-Curves"
    bl_idname = "anim.commotion_nla_to_fcurves"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    prop_pfx = StringProperty(options={"HIDDEN", "SKIP_SAVE"})

    def execute(self, context):

        def remove_nla_track(ad):
            trks = ad.nla_tracks
            ad.action = trks[0].strips[0].action
            trks.remove(trks[0])

        obs = context.selected_objects

        if "SK" in self.ad_type:
            for ob in obs:

                try:
                    ad = ob.data.shape_keys.animation_data
                    remove_nla_track(ad)
                except:
                    continue

        elif "OB" in self.ad_type:
            for ob in obs:

                try:
                    ad = ob.animation_data
                    remove_nla_track(ad)
                except:
                    continue

        return {"FINISHED"}


class NLA_OT_commotion_sync_length(Operator, AdSetup):
    bl_label = "Sync Length"
    bl_description = "Synchronize strip length for selected objects"
    bl_idname = "nla.commotion_sync_length"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    prop_pfx = StringProperty(options={"HIDDEN", "SKIP_SAVE"})

    def execute(self, context):
        obs = context.selected_objects

        if "SK" in self.ad_type:
            for ob in obs:

                try:
                    strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]
                    strip.action_frame_end = strip.action_frame_start + strip.action.frame_range[1] - 1
                except:
                    continue

        elif "OB" in self.ad_type:
            for ob in obs:

                try:
                    strip = ob.animation_data.nla_tracks[0].strips[0]
                    strip.action_frame_end = strip.action_frame_start + strip.action.frame_range[1] - 1
                except:
                    continue

        return {"FINISHED"}


class AnimationOffset:
    bl_label = "Offset Animation"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    prop_pfx = StringProperty(options={"HIDDEN", "SKIP_SAVE"})

    offset = FloatProperty(name="Frame Offset", description="Frame step for animation offset", default=1, min=0, step=10, precision=3)
    threshold = IntProperty(name="Threshold", description="Number of objects to animate per frame step", default=1, min=1)
    reverse = BoolProperty(name="Reverse", description="Reverse animation offset")

    def invoke(self, context, event):
        scene = context.scene
        props = scene.commotion

        self.ad_type = set(self.prop_pfx.upper().split("_"))
        self.frame = scene.frame_current
        self.cursor = scene.cursor_location
        self.offset = getattr(props, self.prop_pfx + "_offset")
        self.threshold = getattr(props, self.prop_pfx + "_threshold")
        self.reverse = getattr(props, self.prop_pfx + "_reverse")
        self.sort_options = getattr(props, self.prop_pfx + "_sort_options")
        self.group_objects = ""
        self.group_targets = ""

        if self.sort_options == "MULTITARGET":
            self.group_objects = getattr(props, self.prop_pfx + "_group_objects")
            self.group_targets = getattr(props, self.prop_pfx + "_group_targets")
            self.objects = bpy.data.groups[self.group_objects].objects
            self.targets = bpy.data.groups[self.group_targets].objects

        return self.execute(context)

    def preset_add(self, ob):
        ob["commotion_preset"] = {
            "offset": self.offset,
            "threshold": self.threshold,
            "reverse": self.reverse,
            "sort_options": self.sort_options,
            "group_objects": self.group_objects,
            "group_targets": self.group_targets,
        }

    def offset_simple(self, obs):
        obs = sorted(obs, key=obs.get, reverse=self.reverse)
        i = 0
        i2 = self.threshold

        for ob in obs:

            if self.ad_offset(ob, i) is False:
                continue

            self.preset_add(ob)

            if i2 > 1:
                if i2 <= (obs.index(ob) + 1):
                    i2 += self.threshold
                    i += self.offset
            else:
                i += self.offset

    def ad_offset(self, ob, i):
        try:

            if "FCURVES" in self.ad_type:

                if "SK" in self.ad_type:
                    fcus = ob.data.shape_keys.animation_data.action.fcurves

                elif "OB" in self.ad_type:
                    fcus = ob.animation_data.action.fcurves

                for fcu in fcus:
                    fcu_range = fcu.range()[0]
                    for kp in fcu.keyframe_points:
                        kp.co[0] = kp.co[0] + self.frame + i - fcu_range
                        kp.handle_left[0] = kp.handle_left[0] + self.frame + i - fcu_range
                        kp.handle_right[0] = kp.handle_right[0] + self.frame + i - fcu_range

            elif "NLA" in self.ad_type:

                if "SK" in self.ad_type:
                    strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]

                elif "OB" in self.ad_type:
                    strip = ob.animation_data.nla_tracks[0].strips[0]

                strip.frame_end = self.frame - 1 + i + strip.frame_end
                strip.frame_start = self.frame + i
                strip.scale = 1

        except:
            return False


class ANIM_OT_commotion_offset_cursor(Operator, AnimationOffset):
    bl_description = "Offset animation from 3D cursor for selected objects (won't work if F-Curves are linked)"
    bl_idname = "anim.commotion_offset_cursor"

    def execute(self, context):
        obs = {}

        for ob in context.selected_objects:
            obs[ob] = (self.cursor - ob.matrix_world.translation).length

        self.offset_simple(obs)

        return {"FINISHED"}


class ANIM_OT_commotion_offset_name(Operator, AnimationOffset):
    bl_description = "Offset animation by object name for selected objects (won't work if F-Curves are linked)"
    bl_idname = "anim.commotion_offset_name"

    def execute(self, context):
        obs = {}

        for ob in context.selected_objects:
            obs[ob] = ob.name

        self.offset_simple(obs)

        return {"FINISHED"}


class ANIM_OT_commotion_offset_multitarget(Operator, AnimationOffset):
    bl_description = "Offset animation from multiple targets for selected objects (won't work if F-Curves are linked)"
    bl_idname = "anim.commotion_offset_multitarget"

    def execute(self, context):
        obs = {}

        for ob in self.objects:
            targs = {}

            for t in self.targets:
                distance = (t.matrix_world.translation - ob.matrix_world.translation).length
                targs[distance] = t
                dist = sorted(targs)[0]

            obs[ob] = [dist, targs[dist]]

        for t in self.targets:
            obs_thold = []
            i = 0.0
            i2 = self.threshold

            obs_sorted = sorted(obs, key=obs.get, reverse=self.reverse)

            for ob in obs_sorted:

                if obs[ob][1] == t:

                    if self.ad_offset(ob, i) is False:
                        continue

                    self.preset_add(ob)

                    if i2 > 1:
                        obs_thold.append(ob)

                        if i2 <= (obs_thold.index(ob) + 1):
                            i += self.offset
                            i2 += self.threshold
                    else:
                        i += self.offset

        return {"FINISHED"}
