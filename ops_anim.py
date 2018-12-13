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


from bpy.types import Operator
from bpy.props import EnumProperty


class AdSetup:

    def invoke(self, context, event):
        props = context.scene.commotion
        self.is_ob = props.offset_id_type == "OBJECT"
        self.is_fcurves = props.offset_ad_type == "FCURVES"

        return self.execute(context)


class AdCheck:

    def invoke(self, context, event):
        props = context.scene.commotion
        self.is_ob = props.offset_id_type == "OBJECT"
        self.is_fcurves = props.offset_ad_type == "FCURVES"

        # Get animation data
        # ----------------------------

        if self.is_ob:
            ad = context.active_object.animation_data
        else:
            try:
                sk = context.active_object.data.shape_keys
                ad = sk.animation_data
            except:
                self.report({"ERROR"}, "Object has no Shape Keys")
                return {"CANCELLED"}

        # Check
        # ----------------------------

        if self.is_fcurves and not (ad and ad.action):
            self.report({"ERROR"}, "Object has no animation")
            return {"CANCELLED"}

        elif not self.is_fcurves and not (ad and ad.nla_tracks and ad.nla_tracks[0].strips):
            self.report({"ERROR"}, "Object NLA tracks are empty")
            return {"CANCELLED"}

        return self.execute(context)


class AdCopy:

    def execute(self, context):
        ob_active = context.active_object
        obs = list(context.selected_objects)

        if ob_active.select:
            obs.remove(ob_active)

        if self.is_fcurves:

            if self.is_ob:
                action = ob_active.animation_data.action
                for ob in obs:
                    if not ob.animation_data:
                        ob.animation_data_create()
                    ob.animation_data.action = action if self.use_link else action.copy()
            else:
                action = ob_active.data.shape_keys.animation_data.action
                for ob in obs:
                    if ob.data and ob.data.shape_keys:
                        sk = ob.data.shape_keys
                        if not sk.animation_data:
                            sk.animation_data_create()
                        sk.animation_data.action = action if self.use_link else action.copy()

        else:

            if self.is_ob:
                nla_tracks = ob_active.animation_data.nla_tracks
                for ob in obs:
                    if not ob.animation_data:
                        ob.animation_data_create()
                    self.nla_copy(ob.animation_data.nla_tracks, nla_tracks)
            else:
                nla_tracks = ob_active.data.shape_keys.animation_data.nla_tracks
                for ob in obs:
                    if ob.data and ob.data.shape_keys:
                        sk = ob.data.shape_keys
                        if not sk.animation_data:
                            sk.animation_data_create()
                        self.nla_copy(sk.animation_data.nla_tracks, nla_tracks)

        return {"FINISHED"}

    def nla_copy(self, ob_nla_tracks, nla_tracks):
        if ob_nla_tracks:
            for track in ob_nla_tracks:
                ob_nla_tracks.remove(track)

        for track in nla_tracks:
            track_new = ob_nla_tracks.new()
            track_new.name = track.name
            track_new.select = False

            for strip in track.strips:
                if self.use_link:
                    strip_new = track_new.strips.new(strip.name, strip.frame_start, strip.action)
                else:
                    strip_new = track_new.strips.new(strip.name, strip.frame_start, strip.action.copy())

                strip_new.name = strip.name
                strip_new.select = False

                strip_new.frame_start = strip.frame_start
                strip_new.frame_end = strip.frame_end
                strip_new.extrapolation = strip.extrapolation
                strip_new.blend_type = strip.blend_type
                strip_new.use_auto_blend = strip.use_auto_blend
                strip_new.blend_in = strip.blend_in
                strip_new.blend_out = strip.blend_out
                strip_new.mute = strip.mute
                strip_new.use_reverse = strip.use_reverse

                strip_new.action_frame_start = strip.action_frame_start
                strip_new.action_frame_end = strip.action_frame_end
                strip_new.use_sync_length = strip.use_sync_length
                strip_new.repeat = strip.repeat

                strip_new.use_animated_influence = strip.use_animated_influence
                strip_new.influence = strip.influence
                strip_new.use_animated_time_cyclic = strip.use_animated_time_cyclic
                strip_new.strip_time = strip.strip_time


class ANIM_OT_commotion_animation_copy(Operator, AdCheck, AdCopy):
    bl_label = "Commotion Copy"
    bl_description = "Copy animation from active to selected objects (can also use this to unlink animation)"
    bl_idname = "anim.commotion_animation_copy"
    bl_options = {"REGISTER", "UNDO"}

    use_link = False


class ANIM_OT_commotion_animation_link(Operator, AdCheck, AdCopy):
    bl_label = "Commotion Link"
    bl_description = "Link animation from active to selected objects"
    bl_idname = "anim.commotion_animation_link"
    bl_options = {"REGISTER", "UNDO"}

    use_link = True


class ANIM_OT_commotion_animation_convert(Operator, AdSetup):
    bl_label = "Commotion Convert To"
    bl_description = "Convert action to another type for selected objects"
    bl_idname = "anim.commotion_animation_convert"
    bl_options = {"REGISTER", "UNDO"}

    ad_type = EnumProperty(
        name="Animation Data",
        description="Animation data type",
        items=(
            ("FCURVES", "F-Curves", "", "IPO_BEZIER", 0),
            ("STRIPS", "Strips", "", "NLA", 1),
        ),
    )

    def execute(self, context):
        use_to_strips = self.ad_type == "STRIPS"

        for ob in context.selected_objects:
            try:

                if self.is_ob:
                    ad = ob.animation_data
                else:
                    ad = ob.data.shape_keys.animation_data

                if use_to_strips:
                    nla_tracks = ad.nla_tracks

                    if not nla_tracks:
                        nla_tracks.new()

                    frame_start = ad.action.frame_range[0]
                    nla_tracks[0].strips.new("name", frame_start, ad.action)
                    ad.action = None
                else:
                    nla_tracks = ad.nla_tracks
                    ad.action = nla_tracks[0].strips[0].action

                    for track in nla_tracks:
                        nla_tracks.remove(track)

            except:
                continue

        return {"FINISHED"}
