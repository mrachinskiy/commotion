# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Commotion motion graphics add-on for Blender.
#  Copyright (C) 2014-2018  Mikhail Rachinskiy
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


import bpy
from bpy.app.handlers import persistent
from mathutils import Vector


def handler_add():
    if proxy_handler not in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.append(proxy_handler)


def handler_del():
    if proxy_handler in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(proxy_handler)


def handler_toggle(self, context):
    if self.use_proxy:
        handler_add()
    else:
        handler_del()


def lerp(a, b, factor):
    return a + factor * (b - a)


@persistent
def proxy_handler(scene):
    props = scene.commotion

    use_loc = props.proxy_use_loc
    use_rot = props.proxy_use_rot
    use_sca = props.proxy_use_sca
    use_sk = props.proxy_use_sk

    if not (use_loc or use_rot or use_sca or use_sk):
        return

    gr_obs = props.proxy_group_animated
    gr_eff = props.proxy_group_effectors

    if not (gr_obs and gr_eff):
        return

    objects = bpy.data.groups[gr_obs].objects
    radius = props.proxy_radius
    falloff = props.proxy_falloff
    fade_factor = props.proxy_trail_fade
    use_trail = props.proxy_use_trail and fade_factor < 1.0
    use_fade = fade_factor > 0.0

    start_loc = props.proxy_start_loc
    final_loc = props.proxy_final_loc
    start_rot = props.proxy_start_rot
    final_rot = props.proxy_final_rot
    start_sca = props.proxy_start_sca
    final_sca = props.proxy_final_sca
    start_sk = props.proxy_start_sk
    final_sk = props.proxy_final_sk

    is_neg_loc = start_loc > final_loc
    is_neg_rot = Vector(start_rot) > Vector(final_rot)
    is_neg_sca = start_sca > final_sca
    is_neg_sk = start_sk > final_sk

    use_reset = use_trail and scene.frame_current <= scene.frame_start
    fac = 1.0 / radius
    effector_loc = [x.matrix_world.translation for x in bpy.data.groups[gr_eff].objects]

    for ob in objects:
        ob_loc = ob.matrix_world.translation - ob.delta_location
        distance = radius + 1.0

        if use_sk:
            ob_sk = ob.data.shape_keys

        if use_reset:
            if use_loc: ob.delta_location = start_loc
            if use_rot: ob.delta_rotation_euler = start_rot
            if use_sca: ob.delta_scale = start_sca
            if use_sk: ob_sk.eval_time = start_sk

        for loc in effector_loc:
            distance = min((loc - ob_loc).length, distance)

        if distance > radius:
            if use_trail:
                if use_fade:
                    if use_loc: ob.delta_location = ob.delta_location.lerp(start_loc, fade_factor)
                    if use_rot: ob.delta_rotation_euler = ob.delta_rotation_euler.to_quaternion().slerp(start_rot.to_quaternion(), fade_factor).to_euler()
                    if use_sca: ob.delta_scale = ob.delta_scale.lerp(start_sca, fade_factor)
                    if use_sk: ob_sk.eval_time = lerp(ob_sk.eval_time, start_sk, fade_factor)
            else:
                if use_loc: ob.delta_location = start_loc
                if use_rot: ob.delta_rotation_euler = start_rot
                if use_sca: ob.delta_scale = start_sca
                if use_sk: ob_sk.eval_time = start_sk
            continue

        factor = fac * distance - (falloff / (distance / radius))
        factor = min(max(factor, 0.0), 1.0)
        if use_loc: vec_loc = final_loc.lerp(start_loc, factor)
        if use_rot: vec_rot = final_rot.to_quaternion().slerp(start_rot.to_quaternion(), factor).to_euler()
        if use_sca: vec_sca = final_sca.lerp(start_sca, factor)
        if use_sk: val_sk = lerp(final_sk, start_sk, factor)

        if use_trail:
            if use_loc:
                if use_fade:
                    ob.delta_location = ob.delta_location.lerp(start_loc, fade_factor)
                if is_neg_loc:
                    if vec_loc < ob.delta_location: ob.delta_location = vec_loc
                else:
                    if vec_loc > ob.delta_location: ob.delta_location = vec_loc
            if use_rot:
                if use_fade:
                    ob.delta_rotation_euler = ob.delta_rotation_euler.to_quaternion().slerp(start_rot.to_quaternion(), fade_factor).to_euler()
                if is_neg_rot:
                    if Vector(vec_rot) < Vector(ob.delta_rotation_euler): ob.delta_rotation_euler = vec_rot
                else:
                    if Vector(vec_rot) > Vector(ob.delta_rotation_euler): ob.delta_rotation_euler = vec_rot
            if use_sca:
                if use_fade:
                    ob.delta_scale = ob.delta_scale.lerp(start_sca, fade_factor)
                if is_neg_sca:
                    if vec_sca < ob.delta_scale: ob.delta_scale = vec_sca
                else:
                    if vec_sca > ob.delta_scale: ob.delta_scale = vec_sca
            if use_sk:
                if use_fade:
                    ob_sk.eval_time = lerp(ob_sk.eval_time, start_sk, fade_factor)
                if is_neg_sk:
                    if val_sk < ob_sk.eval_time: ob_sk.eval_time = val_sk
                else:
                    if val_sk > ob_sk.eval_time: ob_sk.eval_time = val_sk
        else:
            if use_loc: ob.delta_location = vec_loc
            if use_rot: ob.delta_rotation_euler = vec_rot
            if use_sca: ob.delta_scale = vec_sca
            if use_sk: ob_sk.eval_time = val_sk


def update_proxy_use_loc(self, context):
    if not self.proxy_group_animated:
        return

    if not self.proxy_use_loc:
        for ob in bpy.data.groups[self.proxy_group_animated].objects:
            ob.delta_location = (0.0, 0.0, 0.0)


def update_proxy_use_rot(self, context):
    if not self.proxy_group_animated:
        return

    if not self.proxy_use_rot:
        for ob in bpy.data.groups[self.proxy_group_animated].objects:
            ob.delta_rotation_euler = (0.0, 0.0, 0.0)


def update_proxy_use_sca(self, context):
    if not self.proxy_group_animated:
        return

    if not self.proxy_use_sca:
        for ob in bpy.data.groups[self.proxy_group_animated].objects:
            ob.delta_scale = (1.0, 1.0, 1.0)


def update_proxy_use_sk(self, context):
    if not self.proxy_group_animated:
        return

    if not self.proxy_use_sk:
        for ob in bpy.data.groups[self.proxy_group_animated].objects:
            try:
                ob.data.shape_keys.eval_time = 0.0
            except:
                continue
