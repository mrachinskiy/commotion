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
from bpy.types import Panel

from . import addon_updater_ops


# Utils
# ---------------------------


class Setup:
    bl_category = "Commotion"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"


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
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        addon_updater_ops.check_for_update_background()

        layout = self.layout
        layout.operator("object.commotion_sk_coll_refresh")

        try:
            sk = context.active_object.data.shape_keys
            kbs = sk.key_blocks
        except:
            return

        skcoll = context.window_manager.commotion.skcoll

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
                col.operator("anim.commotion_sk_auto_keyframes", text="Auto Keyframes", icon="IPO_BEZIER")


class VIEW3D_PT_commotion_animation_offset(Panel, Setup):
    bl_label = "Animation Offset"

    def draw(self, context):
        layout = self.layout
        props = context.scene.commotion
        rand = props.offset_sort_method == "RANDOM"
        multi = props.offset_sort_method == "MULTI"
        multi_use_proxy = props.offset_use_proxy

        col = layout.column()
        col.row().prop(props, "offset_id_type", expand=True)
        col.row().prop(props, "offset_ad_type", expand=True)

        # F-Curves/NLA operators
        # ------------------------------

        col = layout.column()
        row = col.row(align=True)
        row.operator("anim.commotion_animation_link", text="Link", icon="LINKED")
        row.operator("anim.commotion_animation_copy", text="Copy", icon="COPYDOWN")

        if props.offset_ad_type == "NLA":
            col.operator_menu_enum("anim.commotion_animation_convert", "ad_type", text="Convert to")

        # Offset properties
        # ------------------------------

        row = layout.row(align=True)
        col_l = row.column(align=True)
        col_l.alignment = "RIGHT"
        col_l.scale_x = 0.8
        col_l.label("Offset")
        col_l.label("Threshold")
        col_l.label("Reverse")
        col_l.label("Sort")

        if rand:
            col_l.label("Seed")

        if multi:
            col_l.label("Animated")
            col_l.label("Effectors")
            col_l.label("Proximity")

            if multi_use_proxy:
                col_l.label("Radius")

        col_r = row.column(align=True)
        sub = col_r.column(align=True)
        sub.active = not (multi and multi_use_proxy)
        sub.prop(props, "offset_offset", text="")
        sub.prop(props, "offset_threshold", text="")
        sub.prop(props, "offset_use_reverse", text="")
        col_r.prop(props, "offset_sort_method", text="")

        if rand:
            col_r.prop(props, "offset_seed", text="")

        if multi:
            row = col_r.row(align=True)
            row.prop_search(props, "offset_group_animated", bpy.data, "groups", text="")
            row.operator("object.commotion_add_to_group_animated", text="", icon="ZOOMIN").prop_pfx = "offset"
            row = col_r.row(align=True)
            row.prop_search(props, "offset_group_effectors", bpy.data, "groups", text="")
            row.operator("object.commotion_add_to_group_objects_effector", text="", icon="ZOOMIN").prop_pfx = "offset"

            col_r.prop(props, "offset_use_proxy", text="")

            if multi_use_proxy:
                col_r.prop(props, "offset_proxy_radius", text="")

        row = layout.row(align=True)
        row.operator("anim.commotion_animation_offset", text="Offset Animation", icon="FORCE_HARMONIC")
        row.operator("object.commotion_preset_apply", text="", icon="EYEDROPPER")


class VIEW3D_PT_commotion_slow_parent(Panel, Setup):
    bl_label = "Slow Parent"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        props = context.scene.commotion

        row = layout.row(align=True)
        row.operator("object.commotion_slow_parent_toggle", text="On").enable = True
        row.operator("object.commotion_slow_parent_toggle", text="Off")

        row = layout.row(align=True)
        col_l = row.column(align=True)
        col_l.alignment = "RIGHT"
        col_l.label("Offset")
        col_r = row.column(align=True)
        col_r.prop(props, "slow_parent_offset", text="")

        layout.operator("object.commotion_slow_parent_offset", text="Offset Slow Parent", icon="FORCE_DRAG")


class VIEW3D_PT_commotion_proxy_effector(Panel, Setup):
    bl_label = "Proximity Effector"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.window_manager.commotion, "use_proxy", text="")

    def draw(self, context):
        layout = self.layout
        layout.active = context.window_manager.commotion.use_proxy
        props = context.scene.commotion

        row = layout.row(align=True)
        col_l = row.column(align=True)
        col_l.alignment = "RIGHT"
        col_l.scale_x = 0.8
        col_l.label("Animated")
        col_l.label("Effectors")
        col_l.label("Radius")
        col_l.label("Falloff")
        col_l.label("Trail")
        if props.proxy_use_trail:
            col_l.label("Fade")

        col_r = row.column(align=True)
        row = col_r.row(align=True)
        row.prop_search(props, "proxy_group_animated", bpy.data, "groups", text="")
        row.operator("object.commotion_add_to_group_animated", text="", icon="ZOOMIN").prop_pfx = "proxy"
        row = col_r.row(align=True)
        row.prop_search(props, "proxy_group_effectors", bpy.data, "groups", text="")
        row.operator("object.commotion_add_to_group_objects_effector", text="", icon="ZOOMIN").prop_pfx = "proxy"
        col_r.prop(props, "proxy_radius", text="")
        col_r.prop(props, "proxy_falloff", text="")
        col_r.prop(props, "proxy_use_trail", text="")
        if props.proxy_use_trail:
            col_r.prop(props, "proxy_trail_fade", text="")

        col = layout.column()
        col.prop(props, "proxy_use_loc")
        if props.proxy_use_loc:
            row = col.row()
            row.column().prop(props, "proxy_start_loc", text="")
            row.column().prop(props, "proxy_final_loc", text="")

        col = layout.column()
        col.prop(props, "proxy_use_rot")
        if props.proxy_use_rot:
            row = col.row()
            row.column().prop(props, "proxy_start_rot", text="")
            row.column().prop(props, "proxy_final_rot", text="")

        col = layout.column()
        col.prop(props, "proxy_use_sca")
        if props.proxy_use_sca:
            row = col.row()
            row.column().prop(props, "proxy_start_sca", text="")
            row.column().prop(props, "proxy_final_sca", text="")

        col = layout.column()
        col.prop(props, "proxy_use_sk")
        if props.proxy_use_sk:
            row = col.row()
            row.column().prop(props, "proxy_start_sk")
            row.column().prop(props, "proxy_final_sk")

        row = layout.row(align=True)
        row.operator("anim.commotion_bake", text="Bake")
        row.operator("anim.commotion_bake_remove", text="Free Bake")
