# SPDX-FileCopyrightText: 2014-2024 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

from bpy.props import EnumProperty
from bpy.types import ID, Action, AnimData, Context, Operator


def _ensure_ad(data: ID) -> AnimData:
    if not data.animation_data:
        data.animation_data_create()
    return data.animation_data


def _get_frame_range(ad: AnimData) -> tuple[float, float]:
    fcus = ad.action.layers[0].strips[0].channelbag(ad.action_slot).fcurves
    frame_range = set()

    for fcu in fcus:
        start, end = fcu.range()
        frame_range.add(start)
        frame_range.add(end)

    return min(frame_range), max(frame_range)


class _AdCopy:

    def execute(self, context: Context):
        ob1 = context.object
        obs = list(context.selected_objects)

        if ob1.select_get():
            obs.remove(ob1)

        # Get shape key animation data
        try:
            ad1_sk = ob1.data.shape_keys.animation_data
        except AttributeError:
            ad1_sk = None

        # Get material animation data
        ad1_mat: dict[int, AnimData] = {}
        ad1_node: dict[int, AnimData] = {}

        if ob1.material_slots:
            for i, slot in enumerate(ob1.material_slots):

                if not (mat := slot.material):
                    continue

                if (ad := mat.animation_data):
                    ad1_mat[i] = ad

                if mat.node_tree and (ad := mat.node_tree.animation_data):
                    ad1_node[i] = ad

        is_ad_mat = bool(ad1_mat or ad1_node)

        for ob2 in obs:

            actions = {}
            actions_nla = {}

            if (ad := ob1.animation_data):
                ad2 = _ensure_ad(ob2)
                if ad.action:
                    self.action_copy(ad, ad2, actions)
                if ad.nla_tracks:
                    self.nla_copy(ad, ad2, actions_nla)

            if ob2.data:
                if (ad := ob1.data.animation_data):
                    ad2 = _ensure_ad(ob2.data)
                    if ad.action:
                        self.action_copy(ad, ad2, actions)
                    if ad.nla_tracks:
                        self.nla_copy(ad, ad2, actions_nla)

                if ad1_sk:
                    try:
                        ad2 = _ensure_ad(ob2.data.shape_keys)
                        if ad1_sk.action:
                            self.action_copy(ad1_sk, ad2, actions)
                        if ad1_sk.nla_tracks:
                            self.nla_copy(ad1_sk, ad2, actions_nla)
                    except AttributeError:
                        pass

            if is_ad_mat and ob2.material_slots:
                for i, slot in enumerate(ob2.material_slots):

                    if not (mat := slot.material):
                        continue

                    if (ad := ad1_mat.get(i)):
                        ad2 = _ensure_ad(mat)
                        if ad.action:
                            self.action_copy(ad, ad2, actions)
                        if ad.nla_tracks:
                            self.nla_copy(ad, ad2, actions_nla)

                    if (ad := ad1_node.get(i)):
                        ad2 = _ensure_ad(mat.node_tree)
                        if ad.action:
                            self.action_copy(ad, ad2, actions)
                        if ad.nla_tracks:
                            self.nla_copy(ad, ad2, actions_nla)

        return {"FINISHED"}

    def action_copy(self, ad_from: AnimData, ad_to: AnimData, actions: dict[Action, Action]) -> None:
        if self.use_link:
            ad_to.action = ad_from.action
        else:
            if (action := actions.get(ad_from.action)):
                ad_to.action = action
            else:
                action = ad_from.action.copy()
                actions[ad_from.action] = action
                ad_to.action = action

        ad_to.action_slot = ad_to.action.slots[ad_from.action_slot.identifier]

    def nla_copy(self, ad_from: AnimData, ad_to: AnimData, actions: dict[Action, Action]) -> None:
        if ad_to.nla_tracks:
            for track in ad_to.nla_tracks:
                ad_to.nla_tracks.remove(track)

        for track in ad_from.nla_tracks:
            track_new = ad_to.nla_tracks.new()
            track_new.name = track.name
            track_new.select = False

            for strip in track.strips:
                if self.use_link:
                    strip_new = track_new.strips.new(strip.name, int(strip.frame_start), strip.action)
                else:
                    if (action := actions.get(strip.action)):
                        strip_new = track_new.strips.new(strip.name, int(strip.frame_start), action)
                    else:
                        action_copy = strip.action.copy()
                        strip_new = track_new.strips.new(strip.name, int(strip.frame_start), action_copy)
                        actions[strip.action] = action_copy

                strip_new.action_slot = strip_new.action.slots[strip.action_slot.identifier]

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

                    frame_start, frame_end = _get_frame_range(ad)
                    strip_new = nla_tracks.active.strips.new("name", int(frame_start), ad.action)
                    strip_new.action_slot = strip_new.action.slots[ad.action_slot.identifier]
                    strip_new.frame_start = strip_new.action_frame_start = frame_start
                    strip_new.frame_end = strip_new.action_frame_end = frame_end
                    ad.action = None

                else:

                    nla_tracks = ad.nla_tracks

                    if not nla_tracks:
                        continue

                    ad.action = nla_tracks.active.strips[0].action
                    ad.action_slot = ad.action.slots[nla_tracks.active.strips[0].action_slot.identifier]

                    for track in nla_tracks:
                        nla_tracks.remove(track)

        return {"FINISHED"}
