# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2014-2022 Mikhail Rachinskiy

from bpy.types import Operator
from bpy.props import EnumProperty


class OBJECT_OT_sk_coll_refresh(Operator):
    bl_label = "Refresh"
    bl_description = "Refresh shape key list for active object"
    bl_idname = "object.commotion_sk_coll_refresh"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        skcoll = context.window_manager.commotion.skcoll
        skcoll.clear()

        for kb in context.object.data.shape_keys.key_blocks:
            skcoll.add()

        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            context.object.data.shape_keys.key_blocks
        except AttributeError:
            self.report({"ERROR"}, "Object has no Shape Keys")
            return {"CANCELLED"}

        return self.execute(context)


class OBJECT_OT_sk_interpolation_set(Operator):
    bl_label = "Set Interpolation"
    bl_description = "Set interpolation type for selected shape keys"
    bl_idname = "object.commotion_sk_interpolation_set"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    interp: EnumProperty(
        name="Interpolation",
        description="Interpolation type for absolute shape keys",
        items=(
            ("KEY_LINEAR", "Linear", ""),
            ("KEY_CARDINAL", "Cardinal", ""),
            ("KEY_CATMULL_ROM", "Catmull-Rom", ""),
            ("KEY_BSPLINE", "BSpline", ""),
        ),
    )

    def execute(self, context):
        skcoll = context.window_manager.commotion.skcoll

        for ob in context.selected_objects:

            try:
                kbs = ob.data.shape_keys.key_blocks
            except AttributeError:
                continue

            for i, kb in enumerate(kbs):
                if skcoll[i].selected:
                    kb.interpolation = self.interp

        return {"FINISHED"}


class ANIM_OT_sk_generate_keyframes(Operator):
    bl_label = "Shape Key Generate Keyframes"
    bl_description = (
        "Create keyframes for absolute shape keys on selected objects, "
        "based on the current frame and shape keys timings"
    )
    bl_idname = "anim.commotion_sk_generate_keyframes"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        frame_start = context.scene.frame_current

        for ob in context.selected_objects:

            try:
                sk = ob.data.shape_keys
                kbs = sk.key_blocks
            except AttributeError:
                continue

            if not sk.use_relative:
                sk.eval_time = int(kbs[1].frame)
                sk.keyframe_insert(data_path="eval_time", frame=frame_start)

                frame_end = int(kbs[-1].frame)
                sk.eval_time = frame_end
                sk.keyframe_insert(data_path="eval_time", frame=frame_start + frame_end)

                for fcu in sk.animation_data.action.fcurves:
                    fcu.color_mode = "AUTO_RAINBOW"

        return {"FINISHED"}
