# ##### BEGIN GPL LICENSE BLOCK #####
#
#  JewelCraft jewelry design toolkit for Blender.
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


from bpy.types import Operator
from bpy.props import StringProperty


class OBJECT_OT_commotion_sk_coll_refresh(Operator):
    bl_label = "Refresh List"
    bl_description = "Refresh shape key list for active object"
    bl_idname = "object.commotion_sk_coll_refresh"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        skcoll = context.window_manager.commotion_skcoll
        skcoll.clear()
        i = 0

        for kb in context.active_object.data.shape_keys.key_blocks:
            skcoll.add()
            skcoll[i].name = kb.name
            skcoll[i].index = i
            i += 1

        return {"FINISHED"}

    def invoke(self, context, event):

        try:
            sk = context.active_object.data.shape_keys
        except:
            sk = False

        if not sk:
            self.report({"ERROR"}, "Object has no Shape Keys")
            return {"CANCELLED"}

        return self.execute(context)


class OBJECT_OT_commotion_sk_interpolation_set(Operator):
    bl_label = "Set Interpolation"
    bl_description = "Set interpolation type for selected shape keys (Linear, Cardinal, Catmull-Rom, BSpline)"
    bl_idname = "object.commotion_sk_interpolation_set"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    intr = StringProperty(options={"HIDDEN", "SKIP_SAVE"})

    def execute(self, context):
        skcoll = context.window_manager.commotion_skcoll

        for ob in context.selected_objects:

            try:
                sk = ob.data.shape_keys
            except:
                continue

            for kb in skcoll:
                if kb.selected:
                    sk.key_blocks[kb.index].interpolation = self.intr

        return {"FINISHED"}


class ANIM_OT_commotion_sk_auto_keyframes(Operator):
    bl_label = "Auto Keyframes"
    bl_description = (
        "Create keyframes for absolute shape keys on selected objects, "
        "based on the current frame and shape keys timings"
    )
    bl_idname = "anim.commotion_sk_auto_keyframes"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        frame = context.scene.frame_current

        for ob in context.selected_objects:

            try:
                sk = ob.data.shape_keys
            except:
                continue

            if not sk.use_relative:
                sk.eval_time = int(sk.key_blocks[1].frame)
                sk.keyframe_insert(data_path="eval_time", frame=frame)
                sk.eval_time = int(sk.key_blocks[-1].frame)
                sk.keyframe_insert(data_path="eval_time", frame=frame + 20)

                for fcu in sk.animation_data.action.fcurves:
                    fcu.color_mode = "AUTO_RAINBOW"

        return {"FINISHED"}
