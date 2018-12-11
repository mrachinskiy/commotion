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


from bpy.types import PropertyGroup, AddonPreferences
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    EnumProperty,
    FloatVectorProperty,
    CollectionProperty,
)

from . import proxy_effector, addon_updater_ops


# Custom properties
# -----------------------------------


class CommotionShapeKeyCollection(PropertyGroup):
    index = IntProperty()
    selected = BoolProperty(description="Affect referenced shape key")
    name = StringProperty()


# Add-on preferences
# -----------------------------------


class CommotionPreferences(AddonPreferences):
    bl_idname = __package__

    update_auto_check = BoolProperty(name="Automatically check for updates", description="Automatically check for updates with specified interval", default=True)
    update_interval = EnumProperty(
        name="Interval",
        description="Interval",
        items=(
            ("1", "Once a day", ""),
            ("7", "Once a week", ""),
            ("30", "Once a month", ""),
        ),
        default="7",
    )

    def draw(self, context):
        addon_updater_ops.update_settings_ui(self, context)


# Scene properties
# -----------------------------------


class CommotionPropertiesScene(PropertyGroup):
    offset_id_type = EnumProperty(
        name="Data",
        description="Data type",
        items=(
            ("OBJECT", "Object", "", "OBJECT_DATA", 0),
            ("SHAPE_KEYS", "Shape Keys", "", "SHAPEKEY_DATA", 1),
        ),
    )
    offset_ad_type = EnumProperty(
        name="Animation Data",
        description="Animation data type",
        items=(
            ("FCURVES", "F-Curves", "", "IPO_BEZIER", 0),
            ("NLA", "NLA", "", "NLA", 1),
        ),
    )
    offset_sort_method = EnumProperty(
        name="Sort By",
        description="Offset animation by",
        items=(
            ("CURSOR", "Cursor", ""),
            ("NAME", "Name", ""),
            ("MULTI", "Multi-Offset", ""),
            ("RANDOM", "Random", ""),
        ),
        default="CURSOR",
    )
    offset_threshold = IntProperty(name="Threshold", description="Number of objects to animate per frame step", default=1, min=1)
    offset_seed = IntProperty(name="Seed", description="Seed value for randomizer to get different offset patterns", min=0)
    offset_offset = FloatProperty(name="Frame Offset", description="Frame step for animation offset", default=1, min=0, step=10, precision=3)
    offset_proxy_radius = FloatProperty(name="Effector Radius", description="Effective range at which effectors can influence animated objects", soft_min=0.0, default=5.0)
    offset_use_reverse = BoolProperty(name="Reverse", description="Reverse animation offset")
    offset_use_proxy = BoolProperty(name="Proxymity", description="Enable offset by proximity from effector")
    offset_group_animated = StringProperty(name="Animated", description="Group for animated objects")
    offset_group_effectors = StringProperty(name="Effectors", description="Group for effector objects (to affect objects from animated group)")

    slow_parent_offset = FloatProperty(name="Offset Factor", description="Offset step for slow parent offset", default=1, min=0, step=10, precision=3)

    proxy_radius = offset_proxy_radius
    proxy_group_animated = offset_group_animated
    proxy_group_effectors = offset_group_effectors
    proxy_use_loc = BoolProperty(name="Location", update=proxy_effector.update_proxy_use_loc)
    proxy_use_rot = BoolProperty(name="Rotation", update=proxy_effector.update_proxy_use_rot)
    proxy_use_sca = BoolProperty(name="Scale", update=proxy_effector.update_proxy_use_sca)
    proxy_use_sk = BoolProperty(name="Absolute Shape Keys", update=proxy_effector.update_proxy_use_sk)
    proxy_use_trail = BoolProperty(name="Leave Trail", description="Leave permanent trail after effector left the effective range")
    proxy_start_loc = FloatVectorProperty(description="Start location", subtype="TRANSLATION", unit="LENGTH")
    proxy_final_loc = FloatVectorProperty(description="Final location", subtype="TRANSLATION", unit="LENGTH")
    proxy_start_rot = FloatVectorProperty(description="Start rotation", subtype="EULER", unit="ROTATION")
    proxy_final_rot = FloatVectorProperty(description="Final rotation", subtype="EULER", unit="ROTATION")
    proxy_start_sca = FloatVectorProperty(description="Start scale", subtype="TRANSLATION", default=(1.0, 1.0, 1.0))
    proxy_final_sca = FloatVectorProperty(description="Final scale", subtype="TRANSLATION", default=(1.0, 1.0, 1.0))
    proxy_start_sk = FloatProperty(name="Evaluation Time", description="Start evaluation time", min=0.0)
    proxy_final_sk = FloatProperty(name="Evaluation Time", description="Final evaluation time", min=0.0)
    proxy_falloff = FloatProperty(name="Falloff", description="Effector radius falloff", min=0.0, max=1.0, subtype="FACTOR")
    proxy_trail_fade = FloatProperty(name="Fade", description="Fade trail over time", min=0.0, max=1.0, precision=3, subtype="FACTOR")


# Window manager properties
# ------------------------------------------


class CommotionPropertiesWm(PropertyGroup):
    skcoll = CollectionProperty(type=CommotionShapeKeyCollection)
    use_proxy = BoolProperty(description="Enable proxymity effector\nWARNING: works only on animation playback", update=proxy_effector.handler_toggle)
