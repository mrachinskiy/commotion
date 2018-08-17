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


import bpy
from bpy.types import Panel

from . import addon_updater_ops


# Utils
# ---------------------------


class Setup:
    bl_category = "Commotion"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None


class SetupFcuNla(Setup):

    def draw(self, context):
        layout = self.layout
        props = context.scene.commotion

        layout.operator("view3d.commotion_preset_apply", icon="SOLO_OFF").prop_pfx = self.prop_pfx

        # F-Curves/NLA operators
        # ------------------------------

        if self.ad_fcurves:

            row = layout.row(align=True)
            row.operator("anim.commotion_animation_link", icon="LINKED").prop_pfx = self.prop_pfx
            row.operator("anim.commotion_animation_copy", icon="COPYDOWN").prop_pfx = self.prop_pfx

        else:

            col = layout.column(align=True)
            col.operator("nla.commotion_fcurves_to_nla", icon="NLA_PUSHDOWN").prop_pfx = self.prop_pfx
            col.operator("anim.commotion_nla_to_fcurves", icon="IPO_BEZIER").prop_pfx = self.prop_pfx

            col = layout.column(align=True)
            col.operator("anim.commotion_animation_link", icon="LINKED").prop_pfx = self.prop_pfx
            col.operator("nla.commotion_sync_length", icon="TIME").prop_pfx = self.prop_pfx

        # Offset properties
        # ------------------------------

        sort_by = getattr(props, self.prop_pfx + "_sort_options")
        multi = sort_by == "MULTITARGET"

        row = layout.row(align=True)
        col_l = row.column(align=True)
        col_l.alignment = "RIGHT"
        col_l.scale_x = 0.9
        col_l.label("Offset")
        col_l.label("Threshold")
        col_l.label("Sort")
        col_l.label("Reverse")

        if multi:
            col_l.label("Objects")
            col_l.label("Targets")

        col_r = row.column(align=True)
        col_r.prop(props, self.prop_pfx + "_offset", text="")
        col_r.prop(props, self.prop_pfx + "_threshold", text="")
        col_r.prop(props, self.prop_pfx + "_sort_options", text="")
        col_r.prop(props, self.prop_pfx + "_reverse", text="")

        if multi:
            row = col_r.row(align=True)
            row.prop_search(props, self.prop_pfx + "_group_objects", bpy.data, "groups", text="")
            row.operator("object.commotion_add_to_group_objects", text="", icon="ZOOMIN").prop_pfx = self.prop_pfx
            row = col_r.row(align=True)
            row.prop_search(props, self.prop_pfx + "_group_targets", bpy.data, "groups", text="")
            row.operator("object.commotion_add_to_group_objects_targets", text="", icon="ZOOMIN").prop_pfx = self.prop_pfx

            group_objects = getattr(props, self.prop_pfx + "_group_objects")
            group_targets = getattr(props, self.prop_pfx + "_group_targets")

            col = layout.column()
            col.enabled = bool(group_objects) and bool(group_targets)
            col.operator("anim.commotion_offset_multitarget", icon="FORCE_HARMONIC").prop_pfx = self.prop_pfx

        elif sort_by == "CURSOR":
            layout.operator("anim.commotion_offset_cursor", icon="FORCE_HARMONIC").prop_pfx = self.prop_pfx

        else:
            layout.operator("anim.commotion_offset_name", icon="FORCE_HARMONIC").prop_pfx = self.prop_pfx


# Panels f-curves/NLA
# ---------------------------


class VIEW3D_PT_commotion_sk_fcurves(Panel, SetupFcuNla):
    bl_label = "ShapeKey F-Curves"
    bl_options = {"DEFAULT_CLOSED"}

    prop_pfx = "sk_fcurves"
    ad_fcurves = True


class VIEW3D_PT_commotion_sk_nla(Panel, SetupFcuNla):
    bl_label = "ShapeKey NLA"
    bl_options = {"DEFAULT_CLOSED"}

    prop_pfx = "sk_nla"
    ad_fcurves = False


class VIEW3D_PT_commotion_ob_fcurves(Panel, SetupFcuNla):
    bl_label = "Object F-Curves"
    bl_options = {"DEFAULT_CLOSED"}

    prop_pfx = "ob_fcurves"
    ad_fcurves = True


class VIEW3D_PT_commotion_ob_nla(Panel, SetupFcuNla):
    bl_label = "Object NLA"
    bl_options = {"DEFAULT_CLOSED"}

    prop_pfx = "ob_nla"
    ad_fcurves = False


# Panels
# ---------------------------


class VIEW3D_PT_commotion_update(Panel, Setup):
    bl_label = "Update"

    @classmethod
    def poll(cls, context):
        return addon_updater_ops.updater.update_ready

    def draw(self, context):
        addon_updater_ops.update_notice_box_ui(self, context)


class VIEW3D_PT_commotion_shape_keys(Panel, Setup):
    bl_label = "Shape Keys"

    def draw(self, context):
        addon_updater_ops.check_for_update_background()

        layout = self.layout
        layout.operator("object.commotion_sk_coll_refresh")

        try:
            sk = context.active_object.data.shape_keys
            kbs = sk.key_blocks
        except:
            return

        skcoll = context.window_manager.commotion_skcoll

        if len(kbs) == len(skcoll):
            split = layout.split()

            col = split.column(align=True)

            for kb in skcoll:
                col.prop(kb, "selected", icon="SHAPEKEY_DATA", text=kb.name)

            col = split.column(align=True)
            prop_name = "value" if sk.use_relative else "interpolation"

            for i, kb in enumerate(kbs):

                if skcoll[i].selected:
                    col.prop(kb, prop_name, text="")
                else:
                    col.label()

            if not sk.use_relative:
                row = layout.row(align=True)
                row.operator("object.commotion_sk_interpolation_set", text=" ", icon="LINCURVE").intr = "KEY_LINEAR"
                row.operator("object.commotion_sk_interpolation_set", text=" ", icon="SMOOTHCURVE").intr = "KEY_CARDINAL"
                row.operator("object.commotion_sk_interpolation_set", text=" ", icon="ROOTCURVE").intr = "KEY_CATMULL_ROM"
                row.operator("object.commotion_sk_interpolation_set", text=" ", icon="SPHERECURVE").intr = "KEY_BSPLINE"

                col = layout.column(align=True)
                col.prop(sk, "eval_time")
                col.operator("anim.commotion_sk_auto_keyframes", icon="IPO_BEZIER")


class VIEW3D_PT_commotion_sk_drivers(Panel, Setup):
    bl_label = "ShapeKey Drivers"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        props = context.scene.commotion

        try:
            sk = context.active_object.data.shape_keys
            ad = sk.animation_data
        except:
            ad = False

        if bpy.app.autoexec_fail:
            layout.label("Auto Run disabled", icon="ERROR")

        if not (ad and ad.drivers):
            layout.operator("anim.commotion_sk_driver_distance_set")
        else:
            fcu = ad.drivers.find("eval_time")

            layout.label("Expression")
            layout.prop(fcu.driver, "expression", text="")

            col = layout.column(align=True)
            col.operator("anim.commotion_sk_driver_expression_copy", icon="COPYDOWN")
            col.operator("anim.commotion_sk_driver_target_remap")

            # Distance trigger
            # ----------------------------

            layout.label(text="Distance Trigger")
            drv_registered = "dis_trig" in bpy.app.driver_namespace

            if not drv_registered:
                layout.operator("anim.commotion_sk_driver_function_register", icon="CONSOLE")
            else:
                row = layout.row(align=True)
                row.prop(props, "sk_drivers_expression_func", text="")
                row.operator("anim.commotion_sk_driver_func_expression_get", text="", icon="EYEDROPPER")

                col = layout.column(align=True)
                col.operator("anim.commotion_sk_driver_func_expression_set", icon="COPYDOWN")
                col.operator("object.commotion_sk_reset_eval_time")


class VIEW3D_PT_commotion_slow_parent(Panel, Setup):
    bl_label = "Slow Parent"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        props = context.scene.commotion

        row = layout.row(align=True)
        row.operator("object.commotion_slow_parent_toggle", text="On")
        row.operator("object.commotion_slow_parent_toggle", text="Off").off = True

        row = layout.row(align=True)
        col_l = row.column(align=True)
        col_l.alignment = "RIGHT"
        col_l.label("Offset")
        col_r = row.column(align=True)
        col_r.prop(props, "slow_parent_offset", text="")

        layout.operator("object.commotion_slow_parent_offset", text="Offset Slow Parent", icon="FORCE_DRAG")
