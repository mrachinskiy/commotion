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


from bpy.types import Panel

from . import var, mod_update


# Utils
# ---------------------------


class Setup:
    bl_category = "Commotion"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"


# Panels
# ---------------------------


class VIEW3D_PT_commotion_update(Panel, Setup):
    bl_label = "Update"

    @classmethod
    def poll(cls, context):
        return var.update_available

    def draw(self, context):
        mod_update.sidebar_ui(self, context)


class VIEW3D_PT_commotion_shape_keys(Panel, Setup):
    bl_label = "Shape Keys"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.operator("object.commotion_sk_coll_refresh")

        try:
            sk = context.object.data.shape_keys
            kbs = sk.key_blocks
        except:
            return

        skcoll = context.window_manager.commotion.skcoll

        if len(kbs) == len(skcoll):
            prop_name = "value" if sk.use_relative else "interpolation"

            col = layout.column(align=True)
            col.use_property_split = False

            for i, kb in enumerate(kbs):
                kb_sel = skcoll[i]
                row = col.row()
                row.prop(kb_sel, "selected", text=kb.name)

                if kb_sel.selected:
                    row.prop(kb, prop_name, text="")
                else:
                    row.label()

            if not sk.use_relative:
                layout.operator_menu_enum("object.commotion_sk_interpolation_set", "interp", text="Set Interpolation")
                layout.prop(sk, "eval_time", text="Time")
                layout.operator("anim.commotion_sk_generate_keyframes", text="Generate Keyframes", icon="IPO_BEZIER")


class VIEW3D_PT_commotion_animation_offset(Panel, Setup):
    bl_label = "Animation Offset"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        props = context.scene.commotion
        multi = props.offset_sort_method == "MULTI"
        multi_use_proxy = props.offset_use_proxy

        col = layout.column()
        col.prop(props, "offset_id_type")

        sub = col.column()
        sub.active = not (multi and multi_use_proxy)
        sub.prop(props, "offset_offset")
        sub.prop(props, "offset_threshold")
        sub.prop(props, "offset_use_reverse")

        col.prop(props, "offset_sort_method")

        if props.offset_sort_method == "RANDOM":
            col.prop(props, "offset_seed")

        if multi:
            col.prop(props, "offset_coll_animated")
            col.prop(props, "offset_coll_effectors")
            col.prop(props, "offset_use_proxy")

            if multi_use_proxy:
                col.prop(props, "offset_proxy_radius")

        row = layout.row(align=True)
        row.operator("anim.commotion_animation_offset", text="Offset Animation", icon="FORCE_HARMONIC")


class VIEW3D_PT_commotion_animation_utils(Panel, Setup):
    bl_label = "Animation Utils"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row(align=True)
        row.operator("anim.commotion_animation_copy", text="Copy", icon="COPYDOWN")
        row.operator("anim.commotion_animation_link", text="Link", icon="LINKED")
        col.operator_menu_enum("anim.commotion_animation_convert", "ad_type", text="Convert to")


class VIEW3D_PT_commotion_proxy_effector(Panel, Setup):
    bl_label = "Proximity Effector"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.window_manager.commotion, "use_proxy", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.active = context.window_manager.commotion.use_proxy
        props = context.scene.commotion

        col = layout.column()
        col.prop(props, "proxy_coll_animated")
        col.prop(props, "proxy_coll_effectors")
        col.prop(props, "proxy_radius")
        col.prop(props, "proxy_falloff")
        col.prop(props, "proxy_use_trail")

        if props.proxy_use_trail:
            col.prop(props, "proxy_trail_fade")

        col = col.column()
        col.use_property_split = False

        col.prop(props, "proxy_use_loc")
        if props.proxy_use_loc:
            row = col.row()
            row.column().prop(props, "proxy_start_loc", text="")
            row.column().prop(props, "proxy_final_loc", text="")

        col.prop(props, "proxy_use_rot")
        if props.proxy_use_rot:
            row = col.row()
            row.column().prop(props, "proxy_start_rot", text="")
            row.column().prop(props, "proxy_final_rot", text="")

        col.prop(props, "proxy_use_sca")
        if props.proxy_use_sca:
            row = col.row()
            row.column().prop(props, "proxy_start_sca", text="")
            row.column().prop(props, "proxy_final_sca", text="")

        col.prop(props, "proxy_use_sk")
        if props.proxy_use_sk:
            row = col.row()
            row.column().prop(props, "proxy_start_sk", text="")
            row.column().prop(props, "proxy_final_sk", text="")

        row = layout.row(align=True)
        row.operator("anim.commotion_bake", text="Bake")
        row.operator("anim.commotion_bake_remove", text="Free Bake")
