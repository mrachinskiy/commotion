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


from re import sub

import bpy
from bpy.types import Operator


class ANIM_OT_commotion_sk_driver_distance_set(Operator):
    bl_label = "Set Distance Driver"
    bl_description = (
        "Set distance driver for absolute shape keys on selected objects, "
        "if active object is not an Empty, then a new Empty object will be created "
        "as a target for driver distance variable"
    )
    bl_idname = "anim.commotion_sk_driver_distance_set"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        ob = context.active_object

        if ob.type != "EMPTY":
            scene = context.scene
            empty = bpy.data.objects.new("Distance Target", None)
            scene.objects.link(empty)
            empty.location = scene.cursor_location
            empty.select = True
            empty.empty_draw_type = "SPHERE"
        else:
            empty = ob

        for ob in context.selected_objects:
            if ob.data and ob.data.shape_keys:

                sk = ob.data.shape_keys

                sk.driver_remove("eval_time")

                kb = int(sk.key_blocks[1].frame)
                kb_last = str(int(sk.key_blocks[-1].frame) + 5)

                sk.driver_add("eval_time")

                fcu = ob.data.shape_keys.animation_data.drivers.find("eval_time")

                drv = fcu.driver
                drv.type = "SCRIPTED"
                drv.expression = kb_last + " - (dis * 3 / sc)"
                drv.show_debug_info = True

                var = drv.variables.new()
                var.name = "dis"
                var.type = "LOC_DIFF"
                var.targets[0].id = ob
                var.targets[1].id = empty

                var = drv.variables.new()
                var.name = "sc"
                var.type = "SINGLE_PROP"
                var.targets[0].id = empty
                var.targets[0].data_path = "scale[0]"

                if fcu.modifiers:
                    fcu.modifiers.remove(fcu.modifiers[0])

                fcu.keyframe_points.insert(0, kb)
                fcu.keyframe_points.insert(kb, kb)
                fcu.keyframe_points.insert(kb + 10, kb + 10)

                fcu.extrapolation = "LINEAR"

                for kp in fcu.keyframe_points:
                    kp.interpolation = "LINEAR"

        return {"FINISHED"}


class ANIM_OT_commotion_sk_driver_expression_copy(Operator):
    bl_label = "Copy"
    bl_description = "Copy driver expression from active to selected objects"
    bl_idname = "anim.commotion_sk_driver_expression_copy"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        active_fcu = context.active_object.data.shape_keys.animation_data.drivers.find("eval_time")

        for ob in context.selected_objects:

            try:
                fcu = ob.data.shape_keys.animation_data.drivers.find("eval_time")
                fcu.driver.expression = active_fcu.driver.expression
            except:
                pass

        return {"FINISHED"}


class ANIM_OT_commotion_sk_driver_target_remap(Operator):
    bl_label = "Remap Target"
    bl_description = (
        "Remap driver distance variable target property from original to current object, "
        "useful after Make Single User on linked objects, "
        "when distance variable on all objects points only to one object"
    )
    bl_idname = "anim.commotion_sk_driver_target_remap"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        for ob in context.selected_objects:

            try:
                fcu = ob.data.shape_keys.animation_data.drivers.find("eval_time")
                var = fcu.driver.variables["dis"]
                var.targets[0].id = ob
            except:
                continue

        return {"FINISHED"}


def dis_trig(var, name):
    scene = bpy.context.scene
    etm = scene.objects[name].data.shape_keys.eval_time

    if scene.frame_current <= scene.frame_start:
        etm = 0

    elif var > etm:
        etm = var

    return etm


class ANIM_OT_commotion_sk_driver_function_register(Operator):
    bl_label = "Register"
    bl_description = (
        "Register Distance Trigger driver function, "
        "use it every time after opening blend file, otherwise Distance Trigger drivers will not work"
    )
    bl_idname = "anim.commotion_sk_driver_function_register"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        bpy.app.driver_namespace["dis_trig"] = dis_trig

        for sk in bpy.data.shape_keys:
            if sk.animation_data and sk.animation_data.drivers:
                fcu = sk.animation_data.drivers.find("eval_time")
                fcu.driver.expression = fcu.driver.expression

        return {"FINISHED"}


class OBJECT_OT_commotion_sk_reset_eval_time(Operator):
    bl_label = "Reset Eval Time"
    bl_description = "Reset Evaluation Time property for selected objects to 0"
    bl_idname = "object.commotion_sk_reset_eval_time"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        for ob in context.selected_objects:

            try:
                ob.data.shape_keys.eval_time = 0
            except:
                pass

        return {"FINISHED"}


class ANIM_OT_commotion_sk_driver_func_expression_get(Operator):
    bl_label = "Get Expression"
    bl_description = "Get expression from active object"
    bl_idname = "anim.commotion_sk_driver_func_expression_get"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        fcu = context.active_object.data.shape_keys.animation_data.drivers.find("eval_time")
        expression = fcu.driver.expression
        sanitized = sub(r"dis_trig\((.+),.+\)", r"\1", expression)
        context.scene.commotion.sk_drivers_expression_func = sanitized

        return {"FINISHED"}


class ANIM_OT_commotion_sk_driver_func_expression_set(Operator):
    bl_label = "Set Expression"
    bl_description = "Set distance trigger expression for selected objects"
    bl_idname = "anim.commotion_sk_driver_func_expression_set"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        props = context.scene.commotion
        expr = props.sk_drivers_expression_func

        for ob in context.selected_objects:

            try:
                fcu = ob.data.shape_keys.animation_data.drivers.find("eval_time")
                fcu.driver.expression = 'dis_trig({}, "{}")'.format(expr, ob.name)
            except:
                pass

        return {"FINISHED"}
