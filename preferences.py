# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2014-2022 Mikhail Rachinskiy

from bpy.types import PropertyGroup, AddonPreferences, Collection
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    EnumProperty,
    FloatVectorProperty,
    CollectionProperty,
    PointerProperty,
)

from . import mod_update


# Proximity Effector utils
# -----------------------------------


def upd_proxy(self, context):
    from . import proxy_effector
    proxy_effector.handler_toggle(self, context)


def upd_proxy_loc(self, context):
    if not self.proxy_coll_animated or self.proxy_use_loc:
        return

    for ob in self.proxy_coll_animated.objects:
        ob.delta_location = (0.0, 0.0, 0.0)


def upd_proxy_rot(self, context):
    if not self.proxy_coll_animated or self.proxy_use_rot:
        return

    for ob in self.proxy_coll_animated.objects:
        ob.delta_rotation_euler = (0.0, 0.0, 0.0)


def upd_proxy_sca(self, context):
    if not self.proxy_coll_animated or self.proxy_use_sca:
        return

    for ob in self.proxy_coll_animated.objects:
        ob.delta_scale = (1.0, 1.0, 1.0)


def upd_proxy_sk(self, context):
    if not self.proxy_coll_animated or self.proxy_use_sk:
        return

    for ob in self.proxy_coll_animated.objects:
        try:
            ob.data.shape_keys.eval_time = 0.0
        except AttributeError:
            continue


# Custom properties
# -----------------------------------


class CommotionShapeKeyCollection(PropertyGroup):
    selected: BoolProperty(description="Affect referenced shape key", default=True)


# Add-on preferences
# -----------------------------------


class CommotionPreferences(mod_update.Preferences, AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        props_wm = context.window_manager.commotion

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        split = layout.split(factor=0.25)
        col = split.column()
        col.use_property_split = False
        col.scale_y = 1.3
        col.prop(props_wm, "prefs_active_tab", expand=True)

        box = split.box()
        mod_update.prefs_ui(self, box)


# Scene properties
# -----------------------------------


class SceneProperties(PropertyGroup):
    offset_sort_method: EnumProperty(
        name="Sort By",
        description="Sort objects method",
        items=(
            ("CURSOR", "Cursor", ""),
            ("NAME", "Name", ""),
            ("MULTI", "Multi-Offset", ""),
            ("RANDOM", "Random", ""),
        ),
        default="CURSOR",
    )
    offset_threshold: IntProperty(
        name="Threshold",
        description="Number of objects to animate per frame step",
        default=1,
        min=1,
    )
    offset_seed: IntProperty(
        name="Seed",
        description="Seed value for randomizer to get different offset patterns",
        min=0,
    )
    offset_offset: FloatProperty(
        name="Offset",
        description="Frame step for animation offset",
        default=1.0,
        min=0,
        step=10,
        precision=3,
    )
    offset_use_reverse: BoolProperty(
        name="Reverse",
        description="Reverse sort order",
    )
    offset_use_proxy: BoolProperty(
        name="Proxymity",
        description="Enable offset by proximity from effector (effector range controlled by object size)",
    )
    offset_use_ob: BoolProperty(
        name="Object",
        description="Affect object animation data",
        default=True,
    )
    offset_use_data: BoolProperty(
        name="Object Data",
        description="Affect object data animation data",
        default=True,
    )
    offset_use_sk: BoolProperty(
        name="Shape Keys",
        description="Affect shape keys animation data",
        default=True,
    )
    offset_use_mat: BoolProperty(
        name="Material",
        description="Affect material animation data",
        default=True,
    )
    offset_coll_animated: PointerProperty(
        name="Animated",
        description="Collection for animated objects",
        type=Collection,
    )
    offset_coll_effectors: PointerProperty(
        name="Effectors",
        description="Collection for effector objects (to affect objects from animated collection)",
        type=Collection,
    )

    proxy_use_loc: BoolProperty(name="Location", update=upd_proxy_loc)
    proxy_use_rot: BoolProperty(name="Rotation", update=upd_proxy_rot)
    proxy_use_sca: BoolProperty(name="Scale", update=upd_proxy_sca)
    proxy_use_sk: BoolProperty(name="Absolute Shape Keys", update=upd_proxy_sk)
    proxy_use_trail: BoolProperty(
        name="Trail",
        description="Leave permanent trail after effector left the effective range",
    )
    proxy_start_loc: FloatVectorProperty(
        description="Start location",
        subtype="TRANSLATION",
        unit="LENGTH",
    )
    proxy_final_loc: FloatVectorProperty(
        description="Final location",
        subtype="TRANSLATION",
        unit="LENGTH",
    )
    proxy_start_rot: FloatVectorProperty(
        description="Start rotation",
        subtype="EULER",
        unit="ROTATION",
    )
    proxy_final_rot: FloatVectorProperty(
        description="Final rotation",
        subtype="EULER",
        unit="ROTATION",
    )
    proxy_start_sca: FloatVectorProperty(
        description="Start scale",
        subtype="TRANSLATION",
        default=(1.0, 1.0, 1.0),
    )
    proxy_final_sca: FloatVectorProperty(
        description="Final scale",
        subtype="TRANSLATION",
        default=(1.0, 1.0, 1.0),
    )
    proxy_start_sk: FloatProperty(
        name="Evaluation Time",
        description="Start evaluation time",
        min=0.0,
    )
    proxy_final_sk: FloatProperty(
        name="Evaluation Time",
        description="Final evaluation time",
        min=0.0,
    )
    proxy_falloff: FloatProperty(
        name="Falloff",
        description="Effector radius falloff",
        min=0.0,
        max=1.0,
        subtype="FACTOR",
    )
    proxy_trail_fade: FloatProperty(
        name="Fade",
        description="Fade trail over time",
        default=0.05,
        min=0.0,
        max=1.0,
        soft_max=0.3,
        precision=3,
        subtype="FACTOR",
    )
    proxy_coll_animated: PointerProperty(
        type=Collection,
        name="Animated",
        description="Collection for animated objects",
    )
    proxy_coll_effectors: PointerProperty(
        type=Collection,
        name="Effectors",
        description="Collection for effector objects (to affect objects from animated collection)",
    )


# Window manager properties
# ------------------------------------------


class WmProperties(PropertyGroup):
    prefs_active_tab: EnumProperty(
        items=(
            ("UPDATES", "Updates", ""),
        ),
    )
    skcoll: CollectionProperty(type=CommotionShapeKeyCollection)
    use_proxy: BoolProperty(
        name="Proximity Effector",
        description=(
            "Enable proxymity effector (effector range controlled by object size)"
            "\nWARNING: works only on animation playback"
        ),
        update=upd_proxy,
    )
