# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Commotion motion graphics add-on for Blender.
#  Copyright (C) 2014-2021  Mikhail Rachinskiy
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


import random
import operator
from typing import Iterable, Any, Tuple, Iterator

from bpy.types import Collection, Object

from ..lib import effector_radius
from . import offset_ad


def _flatten(obs: Iterable[Tuple[Object, Any]]) -> Iterator[Object]:
    for ob, _ in obs:
        yield ob


def offset_from_cursor(self, context) -> None:
    obs = [(ob, (self.cursor - ob.matrix_world.translation).length) for ob in context.selected_objects]
    obs.sort(key=operator.itemgetter(1), reverse=self.use_reverse)
    offset_ad.offset_simple(self, _flatten(obs))


def offset_from_name(self, context) -> None:
    obs = [(ob, ob.name) for ob in context.selected_objects]
    obs.sort(key=operator.itemgetter(1), reverse=self.use_reverse)
    offset_ad.offset_simple(self, _flatten(obs))


def offset_from_random(self, context) -> None:
    obs = list(context.selected_objects)
    random.Random(self.seed).shuffle(obs)

    if self.use_reverse:
        obs.reverse()

    offset_ad.offset_simple(self, obs)


def offset_from_multi(self, coll_animated: Collection, coll_effectors: Collection) -> None:
    obs = [[] for _ in coll_effectors.objects]
    effector_loc = [(i, ob.matrix_world.translation) for i, ob in enumerate(coll_effectors.objects)]

    for ob in coll_animated.objects:
        ob_loc = ob.matrix_world.translation
        eff_to_ob_dist = [(i, (loc - ob_loc).length) for i, loc in effector_loc]
        eff_to_ob_dist.sort(key=operator.itemgetter(1))

        i, distance = eff_to_ob_dist[0]
        obs[i].append((ob, distance))

    for ob_groups in obs:
        ob_groups.sort(key=operator.itemgetter(1), reverse=self.use_reverse)
        offset_ad.offset_simple(self, _flatten(ob_groups))


def offset_from_multi_proxy(self, context, coll_animated: Collection, coll_effectors: Collection) -> None:
    scene = context.scene
    frame = scene.frame_start
    scene.frame_set(frame)
    self.frame = 0

    obs = [[i, ob, False] for i, ob in enumerate(coll_animated.objects)]
    effectors = coll_effectors.objects

    while frame <= scene.frame_end:

        effector_data = [(x.matrix_world.translation, effector_radius(x)) for x in effectors]

        for i, ob, is_animated in obs:
            if not is_animated:
                ob_loc = ob.matrix_world.translation

                for loc, rad in effector_data:
                    if (loc - ob_loc).length < rad:
                        offset_ad.ad_offset(self, ob, frame)
                        obs[i][2] = True
                        break

        frame += 1
        scene.frame_set(frame)

    frame_end = scene.frame_end + 1

    for i, ob, is_animated in obs:
        if not is_animated:
            offset_ad.ad_offset(self, ob, frame_end)

    scene.frame_set(scene.frame_start)
