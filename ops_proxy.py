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


import bpy
from bpy.types import Operator


class ANIM_OT_bake(Operator):
    bl_label = "Commotion Bake Animation"
    bl_description = "Bake procedural animation into keyframes"
    bl_idname = "anim.commotion_bake"
    bl_options = {"REGISTER", "UNDO"}

    def modal(self, context, event):
        if event.type in {"ESC", "RIGHTMOUSE"}:
            self.cancel(context)
            return {"FINISHED"}

        elif event.type == "TIMER":
            scene = context.scene
            props = scene.commotion

            if self.frame <= scene.frame_end:
                for ob in props.proxy_coll_animated.objects:

                    for dp in self.dpaths:
                        ob.keyframe_insert(data_path=dp)

                    if self.use_sk:
                        try:
                            ob_sk = ob.data.shape_keys
                            ob_sk.keyframe_insert(data_path="eval_time")
                        except:
                            pass

                self.frame += 1
                scene.frame_set(self.frame)
            else:
                self.cancel(context)
                return {"FINISHED"}

        return {"RUNNING_MODAL"}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(1 / 60, window=context.window)
        wm.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def invoke(self, context, event):
        scene = context.scene
        props = scene.commotion

        if (
            not (props.proxy_coll_animated and props.proxy_coll_effectors) or
            not (props.proxy_use_loc or props.proxy_use_rot or props.proxy_use_sca or props.proxy_use_sk)
        ):
            return {"CANCELLED"}

        self.frame = scene.frame_start
        scene.frame_set(self.frame)

        self.dpaths = []

        if props.proxy_use_loc:
            self.dpaths.append("delta_location")
        if props.proxy_use_rot:
            self.dpaths.append("delta_rotation_euler")
        if props.proxy_use_sca:
            self.dpaths.append("delta_scale")

        self.use_sk = props.proxy_use_sca

        return self.execute(context)


class ANIM_OT_bake_remove(Operator):
    bl_label = "Commotion Free Bake"
    bl_description = "Remove baked keyframes"
    bl_idname = "anim.commotion_bake_remove"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        props = scene.commotion

        if not props.proxy_coll_animated:
            return {"CANCELLED"}

        reset_loc = props.proxy_start_loc if props.proxy_use_loc else (0.0, 0.0, 0.0)
        reset_rot = props.proxy_start_rot if props.proxy_use_rot else (0.0, 0.0, 0.0)
        reset_sca = props.proxy_start_sca if props.proxy_use_sca else (1.0, 1.0, 1.0)
        reset_sk = props.proxy_start_sk if props.proxy_use_sk else 0.0
        ob_data_prev = None

        for ob in props.proxy_coll_animated.objects:
            try:
                action = ob.animation_data.action
                bpy.data.actions.remove(action)
            except:
                pass

            ob.delta_location = reset_loc
            ob.delta_rotation_euler = reset_rot
            ob.delta_scale = reset_sca

            if ob.data is not ob_data_prev:
                try:
                    sk = ob.data.shape_keys
                    action = sk.animation_data.action
                    bpy.data.actions.remove(action)
                    sk.eval_time = reset_sk
                except:
                    pass

                ob_data_prev = ob.data

        return {"FINISHED"}
