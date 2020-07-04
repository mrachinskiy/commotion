# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Commotion motion graphics add-on for Blender.
#  Copyright (C) 2014-2020  Mikhail Rachinskiy
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

from . import mod_update


# Utils
# ---------------------------


class Setup:
    bl_category = "Commotion"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"


# Panels
# ---------------------------


class VIEW3D_PT_commotion_update(Setup, Panel):
    bl_label = "Update"

    @classmethod
    def poll(cls, context):
        return mod_update.state.update_available

    def draw(self, context):
        mod_update.sidebar_ui(self, context)


class VIEW3D_PT_commotion_shape_keys(Setup, Panel):
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
        except AttributeError:
            return

        skcoll = context.window_manager.commotion.skcoll

        if len(kbs) == len(skcoll):
            prop_name = "value" if sk.use_relative else "interpolation"

            col = layout.column(align=True)
            col.use_property_split = False

            for i, kb in enumerate(kbs):
                kb_sel = skcoll[i]
                row = col.column().row(align=True)  # Additional column to prevent vertical align
                row.prop(kb_sel, "selected", text=kb.name)

                if kb_sel.selected:
                    row.prop(kb, prop_name, text="")
                else:
                    row.label()

            if not sk.use_relative:
                layout.prop(sk, "eval_time", text="Time")
                layout.operator_menu_enum("object.commotion_sk_interpolation_set", "interp")
                layout.operator("anim.commotion_sk_generate_keyframes", text="Generate Keyframes", icon="IPO_BEZIER")


class VIEW3D_PT_commotion_animation_offset(Setup, Panel):
    bl_label = "Animation Offset"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        props = context.scene.commotion
        multi = props.offset_sort_method == "MULTI"

        col = layout.column(heading="Data")
        col.prop(props, "offset_use_ob")
        col.prop(props, "offset_use_data")
        col.prop(props, "offset_use_sk")
        col.prop(props, "offset_use_mat")

        sub = col.column()
        sub.active = not (multi and props.offset_use_proxy)
        sub.prop(props, "offset_offset")
        sub.prop(props, "offset_threshold")
        sub.prop(props, "offset_use_reverse")

        col.prop(props, "offset_sort_method")

        if props.offset_sort_method == "RANDOM":
            col.prop(props, "offset_seed")
        elif multi:
            col.prop(props, "offset_coll_animated")
            col.prop(props, "offset_coll_effectors")
            col.prop(props, "offset_use_proxy")

        row = layout.row(align=True)
        row.operator("anim.commotion_animation_offset", text="Offset Animation", icon="FORCE_HARMONIC")
        row.operator("anim.commotion_animation_offset_eyedropper", text="", icon="EYEDROPPER")


class VIEW3D_PT_commotion_animation_utils(Setup, Panel):
    bl_label = "Animation Utils"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row(align=True)
        row.operator("anim.commotion_animation_copy", text="Copy", icon="COPYDOWN")
        row.operator("anim.commotion_animation_link", text="Link", icon="LINKED")
        col.operator_menu_enum("anim.commotion_animation_convert", "ad_type", text="Convert to")


class VIEW3D_PT_commotion_proxy_effector(Setup, Panel):
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
        col.prop(props, "proxy_falloff")

        sub = col.column(heading="Trail")

        row = sub.row()
        row.prop(props, "proxy_use_trail", text="")

        subrow = row.row()
        subrow.active = props.proxy_use_trail
        subrow.prop(props, "proxy_trail_fade", text="")


class VIEW3D_PT_commotion_proxy_effector_loc(Setup, Panel):
    bl_label = "Location"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "VIEW3D_PT_commotion_proxy_effector"

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.scene.commotion, "proxy_use_loc", text="")

    def draw(self, context):
        layout = self.layout

        props = context.scene.commotion
        layout.active = props.proxy_use_loc

        row = layout.row()
        row.column().prop(props, "proxy_start_loc", text="")
        row.column().prop(props, "proxy_final_loc", text="")


class VIEW3D_PT_commotion_proxy_effector_rot(Setup, Panel):
    bl_label = "Rotation"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "VIEW3D_PT_commotion_proxy_effector"

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.scene.commotion, "proxy_use_rot", text="")

    def draw(self, context):
        layout = self.layout

        props = context.scene.commotion
        layout.active = props.proxy_use_rot

        row = layout.row()
        row.column().prop(props, "proxy_start_rot", text="")
        row.column().prop(props, "proxy_final_rot", text="")


class VIEW3D_PT_commotion_proxy_effector_sca(Setup, Panel):
    bl_label = "Scale"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "VIEW3D_PT_commotion_proxy_effector"

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.scene.commotion, "proxy_use_sca", text="")

    def draw(self, context):
        layout = self.layout

        props = context.scene.commotion
        layout.active = props.proxy_use_sca

        row = layout.row()
        row.column().prop(props, "proxy_start_sca", text="")
        row.column().prop(props, "proxy_final_sca", text="")


class VIEW3D_PT_commotion_proxy_effector_sk(Setup, Panel):
    bl_label = "Shape Keys"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "VIEW3D_PT_commotion_proxy_effector"

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.scene.commotion, "proxy_use_sk", text="")

    def draw(self, context):
        layout = self.layout

        props = context.scene.commotion
        layout.active = props.proxy_use_sk

        row = layout.row()
        row.column().prop(props, "proxy_start_sk", text="")
        row.column().prop(props, "proxy_final_sk", text="")


class VIEW3D_PT_commotion_proxy_effector_bake(Setup, Panel):
    bl_label = "Bake"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "VIEW3D_PT_commotion_proxy_effector"

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.operator("anim.commotion_bake", text="Bake")
        row.operator("anim.commotion_bake_remove", text="Free Bake")
