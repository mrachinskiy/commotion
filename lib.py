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


from typing import List

from bpy.types import AnimData, Object


def ad_check(ad: AnimData) -> bool:
    return ad and (ad.action or ad.nla_tracks)


def ad_get(ob: Object, use_ob=True, use_data=True, use_sk=True, use_mat=True) -> List[AnimData]:
    ads = []

    if use_ob and ad_check(ob.animation_data):
        ads.append(ob.animation_data)

    if ob.data:

        if use_data and ad_check(ob.data.animation_data):
            ads.append(ob.data.animation_data)

        if use_sk:
            try:
                ad = ob.data.shape_keys.animation_data
                if ad_check(ad):
                    ads.append(ad)
            except AttributeError:
                pass

    if use_mat and ob.material_slots:
        for slot in ob.material_slots:
            if ad_check(slot.material.animation_data):
                ads.append(slot.material.animation_data)
            if slot.material.node_tree and ad_check(slot.material.node_tree.animation_data):
                ads.append(slot.material.node_tree.animation_data)

    return ads


def effector_radius(ob: Object) -> float:
    if ob.type == "EMPTY":
        return ob.empty_display_size * ob.matrix_world.to_scale().x

    return ob.dimensions.x / 2
