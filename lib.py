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


def ad_get(ob, use_ob=True, use_data=True, use_sk=True, use_mat=True):
    ads = []

    if use_ob and ob.animation_data:
        ads.append(ob.animation_data)

    if ob.data:

        if use_data and ob.data.animation_data:
            ads.append(ob.data.animation_data)

        if use_sk:
            try:
                ad = ob.data.shape_keys.animation_data
                if ad:
                    ads.append(ad)
            except:
                pass

    if use_mat and ob.material_slots:
        for slot in ob.material_slots:
            if slot.material.animation_data:
                ads.append(slot.material.animation_data)
            if slot.material.node_tree and slot.material.node_tree.animation_data:
                ads.append(slot.material.node_tree.animation_data)

    return ads
