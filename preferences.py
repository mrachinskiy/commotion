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

from . import proxy_effector, mod_update


# Custom properties
# -----------------------------------


class CommotionShapeKeyCollection(PropertyGroup):
    selected: BoolProperty(description="Affect referenced shape key", default=True)


# Add-on preferences
# -----------------------------------


class CommotionPreferences(AddonPreferences):
    bl_idname = __package__

    update_use_auto_check: BoolProperty(
        name="Automatically check for updates",
        description="Automatically check for updates with specified interval",
        default=True,
    )
    update_interval: EnumProperty(
        name="Auto-check interval",
        description="Auto-check interval",
        items=(
            ("1", "Once a day", ""),
            ("7", "Once a week", ""),
            ("30", "Once a month", ""),
        ),
        default="7",
    )
    update_use_prerelease: BoolProperty(
        name="Update to pre-release",
        description="Update add-on to pre-release version if available",
    )

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
    offset_id_type: EnumProperty(
        name="Data",
        description="Animation data type",
        items=(
            ("ALL", "All", ""),
            ("OBJECT", "Object", ""),
            ("OBJECT_DATA", "Object Data", ""),
            ("SHAPE_KEYS", "Shape Keys", ""),
            ("MATERIAL", "Material", ""),
        ),
    )
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
        default=1,
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

    proxy_use_loc: BoolProperty(name="Location", update=proxy_effector.update_proxy_use_loc)
    proxy_use_rot: BoolProperty(name="Rotation", update=proxy_effector.update_proxy_use_rot)
    proxy_use_sca: BoolProperty(name="Scale", update=proxy_effector.update_proxy_use_sca)
    proxy_use_sk: BoolProperty(name="Absolute Shape Keys", update=proxy_effector.update_proxy_use_sk)
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
        min=0.0,
        max=1.0,
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
        update=proxy_effector.handler_toggle,
    )
