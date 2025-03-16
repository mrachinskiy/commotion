# SPDX-FileCopyrightText: 2014-2025 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterable

from bpy.types import FCurve, Object

from .. import lib


def offset_simple(self, obs: Iterable[Object]) -> None:
    offset = 0
    i = 1

    for ob in obs:

        if ad_offset(self, ob, offset) is False:
            continue

        if i < self.threshold:
            i += 1
        else:
            offset += self.offset
            i = 1


def ad_offset(self, ob: Object, offset: float) -> bool:
    ads = lib.ad_get(ob, self.use_ob, self.use_data, self.use_sk, self.use_mat)

    if not ads:
        return False

    # F-Curves

    # Get F-Curves
    unique_fcurves: set[FCurve] = set()
    for ad in ads:
        if ad.action:
            for fcu in ad.action.layers[0].strips[0].channelbag(ad.action_slot).fcurves:
                unique_fcurves.add(fcu)

    # Get start keyframe
    fcus_frame_start = set()
    for fcu in unique_fcurves:
        if self.use_select:
            for kp in fcu.keyframe_points:
                if kp.select_control_point:
                    fcus_frame_start.add(kp.co.x)
                    break
        else:
            fcus_frame_start.add(fcu.range()[0])

    if fcus_frame_start:
        fcu_offset = self.frame - min(fcus_frame_start) + offset
        for fcu in unique_fcurves:
            for kp in fcu.keyframe_points:
                if self.use_select and not kp.select_control_point:
                    continue
                kp.co.x += fcu_offset
                kp.handle_left.x += fcu_offset
                kp.handle_right.x += fcu_offset

    # NLA

    strips_frame_start = set()

    for ad in ads:
        tracks = ad.nla_tracks
        for track in tracks:
            for strip in track.strips:
                if self.use_select:
                    if strip.select:
                        strips_frame_start.add(strip.frame_start)
                else:
                    strips_frame_start.add(strip.frame_start)

    if strips_frame_start:
        min_frame_start = min(strips_frame_start)
        strip_offset = self.frame - min_frame_start + offset
        use_rev = min_frame_start < self.frame + strip_offset

        for ad in ads:
            tracks = ad.nla_tracks
            for track in tracks:
                strips = reversed(track.strips) if use_rev else track.strips
                for strip in strips:
                    if self.use_select and not strip.select:
                        continue
                    if use_rev:
                        strip.frame_end += strip_offset
                        strip.frame_start += strip_offset
                        strip.frame_end = strip.frame_end  # Trigger update for strip scale value
                    else:
                        strip.frame_start += strip_offset
                        strip.frame_end += strip_offset

    return bool(fcus_frame_start) or bool(strips_frame_start)
