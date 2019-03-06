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


from .. import lib


class AdOffset:

    def offset_simple(self, obs):
        offset = 0
        i = 1

        for ob, _ in sorted(obs, key=lambda x: x[1], reverse=self.use_reverse):

            if self.ad_offset(ob, offset) is False:
                continue

            if i < self.threshold:
                i += 1
            else:
                offset += self.offset
                i = 1

    def ad_offset(self, ob, offset):
        ads = lib.ad_get(ob, self.use_ob, self.use_data, self.use_sk, self.use_mat)

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
                        if use_rev:
                            strip.frame_end += strip_offset
                            strip.frame_start += strip_offset
                            strip.frame_end = strip.frame_end  # Trigger update for strip scale value
                        else:
                            strip.frame_start += strip_offset
                            strip.frame_end += strip_offset

        return bool(fcus_frame_start) or bool(strips_frame_start)
