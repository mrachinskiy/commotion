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


import random


class OffsetMethods:

    def offset_from_cursor(self, context):
        obs = []
        app = obs.append

        for ob in context.selected_objects:
            distance = (self.cursor - ob.matrix_world.translation).length
            app((ob, distance))

        self.offset_simple(obs)

    def offset_from_name(self, context):
        obs = []
        app = obs.append

        for ob in context.selected_objects:
            app((ob, ob.name))

        self.offset_simple(obs)

    def offset_from_random(self, context):
        selected = list(context.selected_objects)
        obs = []
        app = obs.append

        random.Random(self.seed).shuffle(selected)

        for i, ob in enumerate(selected):
            app((ob, i))

        self.offset_simple(obs)

    def offset_from_multi(self, context):
        obs = [[] for x in self.coll_effectors.objects]
        effector_loc = [(i, x.matrix_world.translation) for i, x in enumerate(self.coll_effectors.objects)]

        for ob in self.coll_animated.objects:
            ob_loc = ob.matrix_world.translation
            eff_to_ob_dist = []

            for i, loc in effector_loc:
                distance = (loc - ob_loc).length
                eff_to_ob_dist.append((i, distance))

            _id, distance = sorted(eff_to_ob_dist, key=lambda x: x[1])[0]
            obs[_id].append((ob, distance))

        for ob_groups in obs:
            offset = 0
            i = 1

            for ob, dis in sorted(ob_groups, key=lambda x: x[1], reverse=self.use_reverse):

                if self.ad_offset(ob, offset) is False:
                    continue

                if i < self.threshold:
                    i += 1
                else:
                    offset += self.offset
                    i = 1

    def offset_from_multi_proxy(self, context):
        animated = self.coll_animated.objects
        effectors = self.coll_effectors.objects
        scene = context.scene
        self.frame = 0
        frame = scene.frame_start
        scene.frame_set(frame)
        obs = [[i, ob, False] for i, ob in enumerate(animated)]

        while frame <= scene.frame_end:

            effector_loc = [x.matrix_world.translation for x in effectors]

            for i, ob, flag in obs:
                if not flag:
                    ob_loc = ob.matrix_world.translation
                    distance = self.radius + 1.0

                    for loc in effector_loc:
                        distance = min((loc - ob_loc).length, distance)

                    if distance < self.radius:
                        obs[i][2] = True

                        if self.ad_offset(ob, frame) is False:
                            continue

            frame += 1
            scene.frame_set(frame)

        frame_end = scene.frame_end + 1

        for ob in (ob for i, ob, flag in obs if not flag):
            if self.ad_offset(ob, frame_end) is False:
                continue

        scene.frame_set(scene.frame_start)
