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


from bpy.types import PropertyGroup, AddonPreferences
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

from . import addon_updater_ops


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


def generate_fcu_nla_properties(self):
    offset = FloatProperty(name="Frame Offset", description="Frame step for animation offset", default=1, min=0, step=10, precision=3)
    threshold = IntProperty(name="Threshold", description="Number of objects to animate per frame step", default=1, min=1)
    reverse = BoolProperty(name="Reverse", description="Reverse animation offset")
    sort_options = EnumProperty(
        name="Sort By",
        description="Animation offset by",
        items=(
            ("CURSOR", "Cursor", ""),
            ("MULTITARGET", "Multi-Target", ""),
            ("NAME", "Name", ""),
        ),
        default="CURSOR",
    )
    group_objects = StringProperty(name="Objects", description="Object group for animation offset")
    group_targets = StringProperty(name="Targets", description="Object group for targets, from which animation would be offseted")

    for prefix in ("sk_fcurves", "sk_nla", "ob_fcurves", "ob_nla"):
        setattr(self, prefix + "_offset", offset)
        setattr(self, prefix + "_threshold", threshold)
        setattr(self, prefix + "_reverse", reverse)
        setattr(self, prefix + "_sort_options", sort_options)
        setattr(self, prefix + "_group_objects", group_objects)
        setattr(self, prefix + "_group_targets", group_targets)

    return self


@generate_fcu_nla_properties
class CommotionPropertiesScene(PropertyGroup):
    sk_drivers_expression_func = StringProperty(description="Distance trigger expression")
    slow_parent_offset = FloatProperty(name="Offset Factor", description="Offset step for slow parent offset", default=1, min=0, step=10, precision=3)
