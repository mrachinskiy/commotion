# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2014 Mikhail Rachinskiy
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####

bl_info = {
	"name": "Commotion",
	"author": "Mikhail Rachinskiy +MikhailRachinskiyByDesign",
	"version": (1, 2, 1),
	"blender": (2, 7, 3),
	"location": "3D View → Tool Shelf",
	"description": "Animation Tools for motion graphics.",
	"warning": "",
	"wiki_url": "https://github.com/mrachinskiy/blender-addon-commotion",
	"tracker_url": "https://github.com/mrachinskiy/blender-addon-commotion/issues",
	"category": "Animation"}

if "bpy" in locals():
	import importlib
	importlib.reload(helpers)
	importlib.reload(operators)
	importlib.reload(ui)
else:
	import bpy
	from bpy.props import (
		StringProperty,
		BoolProperty,
		IntProperty,
		FloatProperty,
		EnumProperty,
		PointerProperty,
		CollectionProperty,
	)
	from bpy.types import PropertyGroup
	from . import helpers
	from . import operators
	from . import ui


class ShapeKeyPropreties(PropertyGroup):
	selected = BoolProperty(name="selected", description="Affect referenced shape key")
	index = IntProperty(name="index")
	name = StringProperty(name="name")


class CommotionProperties(PropertyGroup):


	shapekeys = BoolProperty(name="Shape Keys", default=True)
	shape_value = FloatProperty(name="Value", min=0.0, max=1.0, update=helpers.update_sp)
	shape_interpolation = EnumProperty(
		items=(
			('KEY_LINEAR',      'Linear',      ''),
			('KEY_CARDINAL',    'Cardinal',    ''),
			('KEY_CATMULL_ROM', 'Catmull-Rom', ''),
			('KEY_BSPLINE',     'BSpline',     ''),
		),
		name="Interpolation",
		description="Set interpolation type for selected shape keys",
		default="KEY_LINEAR",
		update=helpers.update_sp)


	sk_fcurves = BoolProperty(name="F-Curves")
	sk_fcurves_offset = FloatProperty(name="Frame Offset", description="Frame step for animation offset", default=1, min=0, step=10, precision=3)
	sk_fcurves_threshold = FloatProperty(name="Threshold", description="Number of objects to animate per frame step", default=1, min=1, step=100, precision=0)
	sk_fcurves_sort_options = EnumProperty(
		items=(
			('CURSOR',      'Cursor',       ''),
			('MULTITARGET', 'Multi-target', ''),
			('NAME',        'Name',         ''),
		),
		name="Sort Options",
		description="Offset object animation by",
		default="CURSOR")
	sk_fcurves_reverse = BoolProperty(name="Reverse", description="Reverse animation offset")
	sk_fcurves_group_objects = StringProperty(name="Objects", description="Object group for animation offset")
	sk_fcurves_group_targets = StringProperty(name="Targets", description="Object group for targets, from which animation would be offseted")


	sk_nla = BoolProperty(name="NLA")
	sk_nla_offset = FloatProperty(name="Frame Offset", description="Frame step for animation offset", default=1, min=0, step=10, precision=3)
	sk_nla_threshold = FloatProperty(name="Threshold", description="Number of objects to animate per frame step", default=1, min=1, step=100, precision=0)
	sk_nla_sort_options = EnumProperty(
		items=(
			('CURSOR',      'Cursor',       ''),
			('MULTITARGET', 'Multi-target', ''),
			('NAME',        'Name',         ''),
		),
		name="Sort Options",
		description="Offset object animation by",
		default="CURSOR")
	sk_nla_reverse = BoolProperty(name="Reverse", description="Reverse animation offset")
	sk_nla_group_objects = StringProperty(name="Objects", description="Object group for animation offset")
	sk_nla_group_targets = StringProperty(name="Targets", description="Object group for targets, from which animation would be offseted")


	sk_drivers = BoolProperty(name="Drivers")
	sk_drivers_dist_trigger = BoolProperty(name="Distance Trigger")
	sk_drivers_expression_func = StringProperty(name="Functional Expression", description="Distance trigger expression")


	ob_fcurves = BoolProperty(name="F-Curves")
	ob_fcurves_offset = FloatProperty(name="Frame Offset", description="Frame step for animation offset", default=1, min=0, step=10, precision=3)
	ob_fcurves_threshold = FloatProperty(name="Threshold", description="Number of objects to animate per frame step", default=1, min=1, step=100, precision=0)
	ob_fcurves_sort_options = EnumProperty(
		items=(
			('CURSOR',      'Cursor',       ''),
			('MULTITARGET', 'Multi-target', ''),
			('NAME',        'Name',         ''),
		),
		name="Sort Options",
		description="Offset object animation by",
		default="CURSOR")
	ob_fcurves_reverse = BoolProperty(name="Reverse", description="Reverse animation offset")
	ob_fcurves_group_objects = StringProperty(name="Objects", description="Object group for animation offset")
	ob_fcurves_group_targets = StringProperty(name="Targets", description="Object group for targets, from which animation would be offseted")


	ob_nla = BoolProperty(name="NLA")
	ob_nla_offset = FloatProperty(name="Frame Offset", description="Frame step for animation offset", default=1, min=0, step=10, precision=3)
	ob_nla_threshold = FloatProperty(name="Threshold", description="Number of objects to animate per frame step", default=1, min=1, step=100, precision=0)
	ob_nla_sort_options = EnumProperty(
		items=(
			('CURSOR',      'Cursor',       ''),
			('MULTITARGET', 'Multi-target', ''),
			('NAME',        'Name',         ''),
		),
		name="Sort Options",
		description="Offset object animation by",
		default="CURSOR")
	ob_nla_reverse = BoolProperty(name="Reverse", description="Reverse animation offset")
	ob_nla_group_objects = StringProperty(name="Objects", description="Object group for animation offset")
	ob_nla_group_targets = StringProperty(name="Targets", description="Object group for targets, from which animation would be offseted")


	transforms = BoolProperty(name="Transforms")
	slow_parent_offset = FloatProperty(name="Offset Factor", description="Offset step for slow parent offset", default=1, min=0, step=10, precision=1)


classes = [
	ui.ShapeKeyTools,
	ui.ObjectTools,

	operators.OT_SHAPE_LIST_REFRESH,
	operators.OT_AUTO_KEYFRAMES,

	operators.OT_SK_FCURVES_LINK,
	operators.OT_SK_FCURVES_COPY,
	operators.OT_SK_FCURVES_OFFSET_CURSOR,
	operators.OT_SK_FCURVES_OFFSET_MULTITARGET,
	operators.OT_SK_FCURVES_OFFSET_NAME,

	operators.OT_SK_NLA_CREATE,
	operators.OT_SK_NLA_TO_FCURVES,
	operators.OT_SK_NLA_SYNC_LENGTH,
	operators.OT_SK_NLA_LINK_TO_ACTIVE,
	operators.OT_SK_NLA_OFFSET_CURSOR,
	operators.OT_SK_NLA_OFFSET_MULTITARGET,
	operators.OT_SK_NLA_OFFSET_NAME,

	operators.OT_SK_DRIVER_SET,
	operators.OT_SK_TARGETS_REMAP,
	operators.OT_SK_EXPRESSION_COPY,
	# Distance trigger
	operators.OT_SK_DRIVER_FUNC_REG,
	operators.OT_SK_EVAL_TIME_RESET,
	operators.OT_SK_EXPRESSION_FUNC_SET,

	operators.OT_OB_FCURVES_LINK,
	operators.OT_OB_FCURVES_COPY,
	operators.OT_OB_FCURVES_OFFSET_CURSOR,
	operators.OT_OB_FCURVES_OFFSET_MULTITARGET,
	operators.OT_OB_FCURVES_OFFSET_NAME,

	operators.OT_OB_NLA_CREATE,
	operators.OT_OB_NLA_TO_FCURVES,
	operators.OT_OB_NLA_SYNC_LENGTH,
	operators.OT_OB_NLA_LINK_TO_ACTIVE,
	operators.OT_OB_NLA_OFFSET_CURSOR,
	operators.OT_OB_NLA_OFFSET_MULTITARGET,
	operators.OT_OB_NLA_OFFSET_NAME,

	operators.OT_SLOW_PARENT_OFFSET,

	ShapeKeyPropreties,
	CommotionProperties,
]


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.Scene.spl = CollectionProperty(type=ShapeKeyPropreties)
	bpy.types.Scene.como = PointerProperty(type=CommotionProperties)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.spl
	del bpy.types.Scene.como

if __name__ == "__main__":
	register()