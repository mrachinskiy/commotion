# SPDX-FileCopyrightText: 2014-2025 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

from bpy.types import Menu, Panel


# Menus
# ---------------------------


def draw_commotion_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.menu("VIEW3D_MT_commotion")


class VIEW3D_MT_commotion(Menu):
    bl_label = "Commotion"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = "INVOKE_DEFAULT"
        layout.operator("wm.call_panel", text="Animation Offset", icon="WINDOW").name = "VIEW3D_PT_commotion_animation_offset"
        layout.separator()
        layout.operator("anim.commotion_animation_copy", text="Copy", icon="COPYDOWN")
        layout.operator("anim.commotion_animation_link", text="Link", icon="LINKED")
        layout.operator_menu_enum("anim.commotion_animation_convert", "ad_type")
        layout.separator()
        layout.operator("wm.call_panel", text="Shape Keys", icon="WINDOW").name = "VIEW3D_PT_commotion_shape_keys"
        layout.separator()
        layout.operator("wm.call_panel", text="Proximity Effector", icon="WINDOW").name = "VIEW3D_PT_commotion_proxy_effector"


# Panels
# ---------------------------


class SidebarSetup:
    bl_category = "Commotion"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"


class VIEW3D_PT_commotion_shape_keys(SidebarSetup, Panel):
    bl_label = "Shape Keys"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        if self.is_popover:
            layout.label(text="Shape Keys")
            layout.separator()

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


class VIEW3D_PT_commotion_animation_offset(SidebarSetup, Panel):
    bl_label = "Animation Offset"

    def draw(self, context):
        layout = self.layout

        if self.is_popover:
            layout.label(text="Animation Offset")

        layout.use_property_split = True
        layout.use_property_decorate = False
        props = context.scene.commotion
        is_proxy = props.offset_sort_method == "MULTI" and props.offset_use_proxy

        col = layout.column(heading="Data")
        sub = col.column(align=True)
        sub.prop(props, "offset_use_ob")
        sub.prop(props, "offset_use_data")
        sub.prop(props, "offset_use_sk")
        sub.prop(props, "offset_use_mat")

        sub = col.column()
        sub.active = not is_proxy
        sub.prop(props, "offset_offset")
        sub.prop(props, "offset_threshold")

        sub = col.column(align=True)
        sub.prop(props, "offset_use_select")
        sub = sub.column()
        sub.active = not is_proxy
        sub.prop(props, "offset_use_reverse")

        col.prop(props, "offset_sort_method")

        if props.offset_sort_method == "MULTI":
            col.prop(props, "offset_coll_animated")
            col.prop(props, "offset_coll_effectors")
            col.prop(props, "offset_use_proxy")
        elif props.offset_sort_method == "RANDOM":
            col.prop(props, "offset_seed")

        row = layout.row(align=True)
        row.operator("anim.commotion_animation_offset", icon="FORCE_HARMONIC")
        row.operator("anim.commotion_animation_offset_eyedropper", text="", icon="EYEDROPPER")


class VIEW3D_PT_commotion_animation_utils(SidebarSetup, Panel):
    bl_label = "Animation Utils"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row(align=True)
        row.operator("anim.commotion_animation_copy", text="Copy", icon="COPYDOWN")
        row.operator("anim.commotion_animation_link", text="Link", icon="LINKED")
        col.operator_menu_enum("anim.commotion_animation_convert", "ad_type")


class VIEW3D_PT_commotion_proxy_effector(SidebarSetup, Panel):
    bl_label = "Proximity Effector"
    bl_options = {"DEFAULT_CLOSED"}

    sub_panels = (
        ("loc", "Location"),
        ("rot", "Rotation"),
        ("sca", "Scale"),
        ("sk", "Shape Keys"),
    )

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.window_manager.commotion, "use_proxy", text="")

    def draw(self, context):
        layout = self.layout

        if self.is_popover:
            row = layout.row(align=True)
            row.prop(context.window_manager.commotion, "use_proxy", text="")
            row.label(text="Proximity Effector")
            layout.separator()

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

        # Subpanel headers
        layout.use_property_split = False

        for sub_id, sub_header in self.sub_panels:
            header, panel = layout.panel(sub_id, default_closed=True)
            header.prop(props, f"proxy_use_{sub_id}", text="")
            header.label(text=sub_header)
            if panel:
                panel.active = getattr(props, f"proxy_use_{sub_id}")
                row = panel.row()
                row.column().prop(props, f"proxy_start_{sub_id}", text="")
                row.column().prop(props, f"proxy_final_{sub_id}", text="")

        header, panel = layout.panel("bake", default_closed=True)
        header.label(text="Bake")
        if panel:
            row = panel.row(align=True)
            row.operator("anim.commotion_bake", text="Bake")
            row.operator("anim.commotion_bake_remove")
