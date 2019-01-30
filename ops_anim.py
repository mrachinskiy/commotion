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
from bpy.props import EnumProperty

from . import lib


def anim_get(ob):
    action_ob = None
    action_data = None
    action_sk = None
    action_mat = {}
    action_node = {}

    nla_tracks_ob = None
    nla_tracks_data = None
    nla_tracks_sk = None
    nla_tracks_mat = {}
    nla_tracks_node = {}

    ad = ob.animation_data
    if ad:
        action_ob = ob.animation_data.action
        nla_tracks_ob = ob.animation_data.nla_tracks

    if ob.data:
        ad = ob.data.animation_data
        if ad:
            action_data = ad.action
            nla_tracks_data = ad.nla_tracks

        try:
            ad = ob.data.shape_keys.animation_data
            if ad:
                action_sk = ad.action
                nla_tracks_sk = ad.nla_tracks
        except:
            pass

    if ob.material_slots:
        for i, slot in enumerate(ob.material_slots):

            ad = slot.material.animation_data
            if ad:
                action_mat[i] = ad.action
                nla_tracks_mat[i] = ad.nla_tracks

            if slot.material.node_tree:
                ad = slot.material.node_tree.animation_data
                if ad:
                    action_node[i] = ad.action
                    nla_tracks_node[i] = ad.nla_tracks

    return (
        action_ob,
        action_data,
        action_sk,
        action_mat,
        action_node,
        nla_tracks_ob,
        nla_tracks_data,
        nla_tracks_sk,
        nla_tracks_mat,
        nla_tracks_node,
    )


class AdCopy:

    def execute(self, context):
        ob_active = context.object
        obs = list(context.selected_objects)

        if ob_active.select_get():
            obs.remove(ob_active)

        (action_ob,
         action_data,
         action_sk,
         action_mat,
         action_node,
         nla_tracks_ob,
         nla_tracks_data,
         nla_tracks_sk,
         nla_tracks_mat,
         nla_tracks_node) = anim_get(ob_active)

        is_action_mat = bool(action_mat) or bool(action_node)
        is_nla_tracks_mat = bool(nla_tracks_mat) or bool(nla_tracks_node)

        for ob in obs:

            act_data = []
            nla_data = []

            if action_ob:
                act_data.append((action_ob, ob))

            if nla_tracks_ob:
                nla_data.append((nla_tracks_ob, ob))

            if ob.data:
                if action_data:
                    act_data.append((action_data, ob.data))
                if nla_tracks_data:
                    nla_data.append((nla_tracks_data, ob.data))

                try:
                    if action_sk:
                        act_data.append((action_sk, ob.data.shape_keys))
                    if nla_tracks_sk:
                        nla_data.append((nla_tracks_sk, ob.data.shape_keys))
                except:
                    pass

            if (is_action_mat or is_nla_tracks_mat) and ob.material_slots:
                for i, slot in enumerate(ob.material_slots):

                    if i in action_mat:
                        act_data.append((action_mat[i], slot.material))
                    if i in nla_tracks_mat:
                        nla_data.append((nla_tracks_mat[i], slot.material))

                    if i in action_node:
                        act_data.append((action_node[i], slot.material.node_tree))
                    if i in nla_tracks_node:
                        nla_data.append((nla_tracks_node[i], slot.material.node_tree))

            if act_data:
                for action, data in act_data:
                    if not data.animation_data:
                        data.animation_data_create()
                    data.animation_data.action = action if self.use_link else action.copy()

            if nla_data:
                for nla_tracks, data in nla_data:
                    if not data.animation_data:
                        data.animation_data_create()
                    self.nla_copy(data.animation_data.nla_tracks, nla_tracks)

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


class ANIM_OT_commotion_animation_copy(Operator, AdCopy):
    bl_label = "Commotion Copy"
    bl_description = "Copy animation from active to selected objects (can also use this to unlink animation)"
    bl_idname = "anim.commotion_animation_copy"
    bl_options = {"REGISTER", "UNDO"}

    use_link = False


class ANIM_OT_commotion_animation_link(Operator, AdCopy):
    bl_label = "Commotion Link"
    bl_description = "Link animation from active to selected objects"
    bl_idname = "anim.commotion_animation_link"
    bl_options = {"REGISTER", "UNDO"}

    use_link = True


class ANIM_OT_commotion_animation_convert(Operator):
    bl_label = "Commotion Convert To"
    bl_description = "Convert action to another type for selected objects"
    bl_idname = "anim.commotion_animation_convert"
    bl_options = {"REGISTER", "UNDO"}

    ad_type: EnumProperty(
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
            ads = lib.ad_get(ob)

            if ads:
                for ad in ads:

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

        return {"FINISHED"}
