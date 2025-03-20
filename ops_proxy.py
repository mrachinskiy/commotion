# SPDX-FileCopyrightText: 2014-2025 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

from bpy.types import Operator


class ANIM_OT_bake(Operator):
    bl_label = "Bake Animation"
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
                        except AttributeError:
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

        self.use_sk = props.proxy_use_sk

        return self.execute(context)


class ANIM_OT_bake_remove(Operator):
    bl_label = "Free Bake"
    bl_description = "Remove baked keyframes"
    bl_idname = "anim.commotion_bake_remove"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.commotion

        if not props.proxy_coll_animated:
            return {"CANCELLED"}

        reset_loc = props.proxy_start_loc if props.proxy_use_loc else (0.0, 0.0, 0.0)
        reset_rot = props.proxy_start_rot if props.proxy_use_rot else (0.0, 0.0, 0.0)
        reset_sca = props.proxy_start_sca if props.proxy_use_sca else (1.0, 1.0, 1.0)
        reset_sk = props.proxy_start_sk if props.proxy_use_sk else 0.0
        handled_data = set()

        dpaths = {
            "delta_location",
            "delta_rotation_euler",
            "delta_scale",
        }

        for ob in props.proxy_coll_animated.objects:

            if ob.animation_data and ob.animation_data.action:
                bag = ob.animation_data.action.layers[0].strips[0].channelbag(ob.animation_data.action_slot)
                for fcu in bag.fcurves:
                    if fcu.data_path in dpaths:
                        bag.fcurves.remove(fcu)

            ob.delta_location = reset_loc
            ob.delta_rotation_euler = reset_rot
            ob.delta_scale = reset_sca

            if ob.data and ob.data not in handled_data:
                try:
                    sk = ob.data.shape_keys

                    if sk.animation_data and sk.animation_data.action:
                        bag = sk.animation_data.action.layers[0].strips[0].channelbag(sk.animation_data.action_slot)
                        for fcu in bag.fcurves:
                            bag.fcurves.remove(fcu)

                    sk.eval_time = reset_sk
                except AttributeError:
                    pass

                handled_data.add(ob.data)

        return {"FINISHED"}
