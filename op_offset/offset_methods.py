# SPDX-FileCopyrightText: 2014-2024 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

import operator
import random
from typing import Any, Iterator

import bpy
from bpy.types import Collection, Object

from ..lib import effector_radius
from . import offset_ad


def _flatten(obs: list[tuple[Object, Any]]) -> Iterator[Object]:
    for ob, _ in obs:
        yield ob


def offset_from_cursor(self) -> None:
    obs = [(ob, (self.cursor - ob.matrix_world.translation).length) for ob in bpy.context.selected_objects]
    obs.sort(key=operator.itemgetter(1), reverse=self.use_reverse)
    offset_ad.offset_simple(self, _flatten(obs))


def offset_from_name(self) -> None:
    obs = [(ob, ob.name) for ob in bpy.context.selected_objects]
    obs.sort(key=operator.itemgetter(1), reverse=self.use_reverse)
    offset_ad.offset_simple(self, _flatten(obs))


def offset_from_random(self) -> None:
    obs = list(bpy.context.selected_objects)
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


def offset_from_multi_proxy(self, coll_animated: Collection, coll_effectors: Collection) -> None:
    scene = bpy.context.scene
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
