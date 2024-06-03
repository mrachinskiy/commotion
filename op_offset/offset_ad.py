# SPDX-FileCopyrightText: 2014-2024 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterable

from bpy.types import Object

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

    fcus_frame_start = []

    for ad in ads:
        if ad.action:
            fcus = ad.action.fcurves
            for fcu in fcus:
                fcus_frame_start.append(fcu.range()[0])

    if fcus_frame_start:
        fcu_offset = self.frame - min(fcus_frame_start) + offset

        for ad in ads:
            fcus = ad.action.fcurves
            for fcu in fcus:
                for kp in fcu.keyframe_points:
                    if self.use_select and not kp.select_control_point:
                        continue
                    kp.co[0] += fcu_offset
                    kp.handle_left[0] += fcu_offset
                    kp.handle_right[0] += fcu_offset

    # NLA

    strips_frame_start = []

    for ad in ads:
        tracks = ad.nla_tracks
        for track in tracks:
            for strip in track.strips:
                strips_frame_start.append(strip.frame_start)

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
