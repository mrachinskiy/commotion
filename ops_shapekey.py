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


from bpy.types import Operator
from bpy.props import EnumProperty


class OBJECT_OT_commotion_sk_coll_refresh(Operator):
    bl_label = "Refresh List"
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
            sk = context.object.data.shape_keys
        except:
            sk = False

        if not sk:
            self.report({"ERROR"}, "Object has no Shape Keys")
            return {"CANCELLED"}

        return self.execute(context)


class OBJECT_OT_commotion_sk_interpolation_set(Operator):
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
                sk = ob.data.shape_keys
            except:
                continue

            for i, kb in enumerate(sk.key_blocks):
                if skcoll[i].selected:
                    kb.interpolation = self.interp

        return {"FINISHED"}


class ANIM_OT_commotion_sk_generate_keyframes(Operator):
    bl_label = "Commotion Shape Key Generate Keyframes"
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
            except:
                continue

            if not sk.use_relative:
                sk.eval_time = int(sk.key_blocks[1].frame)
                sk.keyframe_insert(data_path="eval_time", frame=frame_start)

                frame_end = int(sk.key_blocks[-1].frame)
                sk.eval_time = frame_end
                sk.keyframe_insert(data_path="eval_time", frame=frame_start + frame_end)

                for fcu in sk.animation_data.action.fcurves:
                    fcu.color_mode = "AUTO_RAINBOW"

        return {"FINISHED"}
