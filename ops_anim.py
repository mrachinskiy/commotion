# SPDX-FileCopyrightText: 2014-2024 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Sequence
from typing import Optional

from bpy.props import EnumProperty
from bpy.types import Action, NlaTrack, Object, Operator


NlaTracks = Sequence[NlaTrack]


class _Animation:
    __slots__ = (
        "action_ob",
        "action_data",
        "action_sk",
        "action_mat",
        "action_node",
        "nla_tracks_ob",
        "nla_tracks_data",
        "nla_tracks_sk",
        "nla_tracks_mat",
        "nla_tracks_node",
    )

    def __init__(self) -> None:
        self.action_ob: Optional[Action] = None
        self.action_data: Optional[Action] = None
        self.action_sk: Optional[Action] = None
        self.action_mat: dict[int, Action] = {}
        self.action_node: dict[int, Action] = {}
        self.nla_tracks_ob: Optional[NlaTracks] = None
        self.nla_tracks_data: Optional[NlaTracks] = None
        self.nla_tracks_sk: Optional[NlaTracks] = None
        self.nla_tracks_mat: dict[int, NlaTracks] = {}
        self.nla_tracks_node: dict[int, NlaTracks] = {}


def _anim_get(ob: Object) -> _Animation:
    Anim = _Animation()

    ad = ob.animation_data
    if ad:
        Anim.action_ob = ob.animation_data.action
        Anim.nla_tracks_ob = ob.animation_data.nla_tracks

    if ob.data:
        ad = ob.data.animation_data
        if ad:
            Anim.action_data = ad.action
            Anim.nla_tracks_data = ad.nla_tracks

        try:
            ad = ob.data.shape_keys.animation_data
            if ad:
                Anim.action_sk = ad.action
                Anim.nla_tracks_sk = ad.nla_tracks
        except AttributeError:
            pass

    if ob.material_slots:
        for i, slot in enumerate(ob.material_slots):

            if not (mat := slot.material):
                continue

            if (ad := mat.animation_data):
                Anim.action_mat[i] = ad.action
                Anim.nla_tracks_mat[i] = ad.nla_tracks

            if mat.node_tree and (ad := mat.node_tree.animation_data):
                Anim.action_node[i] = ad.action
                Anim.nla_tracks_node[i] = ad.nla_tracks

    return Anim


class _AdCopy:

    def execute(self, context):
        ob_active = context.object
        obs = list(context.selected_objects)

        if ob_active.select_get():
            obs.remove(ob_active)

        Anim = _anim_get(ob_active)
        is_anim_mat = bool(Anim.action_mat or Anim.action_node or Anim.nla_tracks_mat or Anim.nla_tracks_node)

        for ob in obs:

            if Anim.action_ob:
                self.action_copy(ob, Anim.action_ob)
            if Anim.nla_tracks_ob:
                self.nla_copy(ob, Anim.nla_tracks_ob)

            if ob.data:
                if Anim.action_data:
                    self.action_copy(ob.data, Anim.action_data)
                if Anim.nla_tracks_data:
                    self.nla_copy(ob.data, Anim.nla_tracks_data)

                try:
                    if Anim.action_sk:
                        self.action_copy(ob.data.shape_keys, Anim.action_sk)
                    if Anim.nla_tracks_sk:
                        self.nla_copy(ob.data.shape_keys, Anim.nla_tracks_sk)
                except AttributeError:
                    pass

            if is_anim_mat and ob.material_slots:
                for i, slot in enumerate(ob.material_slots):

                    if i in Anim.action_mat:
                        self.action_copy(slot.material, Anim.action_mat[i])
                    if i in Anim.nla_tracks_mat:
                        self.nla_copy(slot.material, Anim.nla_tracks_mat[i])

                    if i in Anim.action_node:
                        self.action_copy(slot.material.node_tree, Anim.action_node[i])
                    if i in Anim.nla_tracks_node:
                        self.nla_copy(slot.material.node_tree, Anim.nla_tracks_node[i])

        return {"FINISHED"}

    def action_copy(self, data, action: Action) -> None:
        if not data.animation_data:
            data.animation_data_create()

        data.animation_data.action = action if self.use_link else action.copy()

    def nla_copy(self, data, nla_tracks: NlaTracks) -> None:
        if not data.animation_data:
            data.animation_data_create()

        ob_nla_tracks = data.animation_data.nla_tracks

        if ob_nla_tracks:
            for track in ob_nla_tracks:
                ob_nla_tracks.remove(track)

        for track in nla_tracks:
            track_new = ob_nla_tracks.new()
            track_new.name = track.name
            track_new.select = False

            for strip in track.strips:
                if self.use_link:
                    strip_new = track_new.strips.new(strip.name, int(strip.frame_start), strip.action)
                else:
                    strip_new = track_new.strips.new(strip.name, int(strip.frame_start), strip.action.copy())

                strip_new.name = strip.name
                strip_new.select = strip.select

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


class ANIM_OT_animation_copy(_AdCopy, Operator):
    bl_label = "Copy Animation"
    bl_description = "Copy animation from active to selected objects (can also use this to unlink animation)"
    bl_idname = "anim.commotion_animation_copy"
    bl_options = {"REGISTER", "UNDO"}

    use_link = False


class ANIM_OT_animation_link(_AdCopy, Operator):
    bl_label = "Link Animation"
    bl_description = "Link animation from active to selected objects"
    bl_idname = "anim.commotion_animation_link"
    bl_options = {"REGISTER", "UNDO"}

    use_link = True


class ANIM_OT_animation_convert(Operator):
    bl_label = "Convert to"
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
        from . import lib

        use_to_strips = self.ad_type == "STRIPS"

        for ob in context.selected_objects:
            ads = lib.ad_get(ob)

            if not ads:
                continue

            for ad in ads:

                if use_to_strips:

                    if not (ad and ad.action):
                        continue

                    nla_tracks = ad.nla_tracks

                    if not nla_tracks:
                        nla_tracks.new()

                    frame_start, frame_end = ad.action.frame_range
                    strip_new = nla_tracks.active.strips.new("name", int(frame_start), ad.action)
                    strip_new.frame_start = frame_start
                    strip_new.frame_end = frame_end
                    ad.action = None

                else:

                    nla_tracks = ad.nla_tracks

                    if not nla_tracks:
                        continue

                    ad.action = nla_tracks.active.strips[0].action

                    for track in nla_tracks:
                        nla_tracks.remove(track)

        return {"FINISHED"}
