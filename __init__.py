bl_info = {
	'name': 'Commotion',
	'author': 'Mikhail Rachinskiy (@_rachinskiy)',
	'version': (1, 2),
	'blender': (2, 74, 0),
	'location': '3D View > Tool Shelf',
	'description': 'Animation offset tools for motion graphics.',
	'wiki_url': 'https://github.com/mrachinskiy/blender-addon-commotion#readme',
	'tracker_url': 'https://github.com/mrachinskiy/blender-addon-commotion/issues',
	'category': 'Animation'}


if 'bpy' in locals():
	from importlib import reload
	reload(helpers)
	reload(operators)
	reload(ui)
	del reload
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
	from . import (
		helpers,
		operators,
		ui,
	)






class CommotionProperties(PropertyGroup):


	shapekeys = BoolProperty(default=True)
	shape_value = FloatProperty(name='Value', min=0.0, max=1.0, update=helpers.update_sp)
	shape_interpolation = EnumProperty(
		items=(
			('KEY_LINEAR',      'Linear',      ''),
			('KEY_CARDINAL',    'Cardinal',    ''),
			('KEY_CATMULL_ROM', 'Catmull-Rom', ''),
			('KEY_BSPLINE',     'BSpline',     ''),
		),
		default='KEY_LINEAR',
		description='Set interpolation type for selected shape keys',
		update=helpers.update_sp)


	sk_fcurves = BoolProperty()
	sk_fcurves_offset = FloatProperty(name='Frame Offset', description='Frame step for animation offset', default=1, min=0, step=10, precision=3)
	sk_fcurves_threshold = FloatProperty(name='Threshold', description='Number of objects to animate per frame step', default=1, min=1, step=100, precision=0)
	sk_fcurves_sort_options = EnumProperty(
		items=(
			('CURSOR',      'Cursor',       ''),
			('MULTITARGET', 'Multi-target', ''),
			('NAME',        'Name',         ''),
		),
		default='CURSOR',
		description='Animation offset by')
	sk_fcurves_reverse = BoolProperty(name='Reverse', description='Reverse animation offset')
	sk_fcurves_group_objects = StringProperty(name='Objects', description='Object group for animation offset')
	sk_fcurves_group_targets = StringProperty(name='Targets', description='Object group for targets, from which animation would be offseted')


	sk_nla = BoolProperty()
	sk_nla_offset = FloatProperty(name='Frame Offset', description='Frame step for animation offset', default=1, min=0, step=10, precision=3)
	sk_nla_threshold = FloatProperty(name='Threshold', description='Number of objects to animate per frame step', default=1, min=1, step=100, precision=0)
	sk_nla_sort_options = EnumProperty(
		items=(
			('CURSOR',      'Cursor',       ''),
			('MULTITARGET', 'Multi-target', ''),
			('NAME',        'Name',         ''),
		),
		default='CURSOR',
		description='Animation offset by')
	sk_nla_reverse = BoolProperty(name='Reverse', description='Reverse animation offset')
	sk_nla_group_objects = StringProperty(name='Objects', description='Object group for animation offset')
	sk_nla_group_targets = StringProperty(name='Targets', description='Object group for targets, from which animation would be offseted')


	sk_drivers = BoolProperty()
	sk_drivers_dist_trigger = BoolProperty()
	sk_drivers_expression_func = StringProperty(description='Distance trigger expression')


	ob_fcurves = BoolProperty()
	ob_fcurves_offset = FloatProperty(name='Frame Offset', description='Frame step for animation offset', default=1, min=0, step=10, precision=3)
	ob_fcurves_threshold = FloatProperty(name='Threshold', description='Number of objects to animate per frame step', default=1, min=1, step=100, precision=0)
	ob_fcurves_sort_options = EnumProperty(
		items=(
			('CURSOR',      'Cursor',       ''),
			('MULTITARGET', 'Multi-target', ''),
			('NAME',        'Name',         ''),
		),
		default='CURSOR',
		description='Animation offset by')
	ob_fcurves_reverse = BoolProperty(name='Reverse', description='Reverse animation offset')
	ob_fcurves_group_objects = StringProperty(name='Objects', description='Object group for animation offset')
	ob_fcurves_group_targets = StringProperty(name='Targets', description='Object group for targets, from which animation would be offseted')


	ob_nla = BoolProperty()
	ob_nla_offset = FloatProperty(name='Frame Offset', description='Frame step for animation offset', default=1, min=0, step=10, precision=3)
	ob_nla_threshold = FloatProperty(name='Threshold', description='Number of objects to animate per frame step', default=1, min=1, step=100, precision=0)
	ob_nla_sort_options = EnumProperty(
		items=(
			('CURSOR',      'Cursor',       ''),
			('MULTITARGET', 'Multi-target', ''),
			('NAME',        'Name',         ''),
		),
		default='CURSOR',
		description='Animation offset by')
	ob_nla_reverse = BoolProperty(name='Reverse', description='Reverse animation offset')
	ob_nla_group_objects = StringProperty(name='Objects', description='Object group for animation offset')
	ob_nla_group_targets = StringProperty(name='Targets', description='Object group for targets, from which animation would be offseted')


	transforms = BoolProperty()
	slow_parent_offset = FloatProperty(name='Offset Factor', description='Offset step for slow parent offset', default=1, min=0, step=10, precision=1)






class ShapeKeysCollection(PropertyGroup):
	selected = BoolProperty(description='Affect referenced shape key')
	index = IntProperty()
	name = StringProperty()






classes = (
	ui.ShapeKeyTools,
	ui.ObjectTools,

	operators.SHAPE_LIST_REFRESH,
	operators.AUTO_KEYFRAMES,

	operators.SK_FCURVES_LINK,
	operators.SK_FCURVES_COPY,
	operators.SK_FCURVES_OFFSET_CURSOR,
	operators.SK_FCURVES_OFFSET_MULTITARGET,
	operators.SK_FCURVES_OFFSET_NAME,

	operators.SK_NLA_CREATE,
	operators.SK_NLA_TO_FCURVES,
	operators.SK_NLA_SYNC_LENGTH,
	operators.SK_NLA_LINK_TO_ACTIVE,
	operators.SK_NLA_OFFSET_CURSOR,
	operators.SK_NLA_OFFSET_MULTITARGET,
	operators.SK_NLA_OFFSET_NAME,

	operators.SK_DRIVER_SET,
	operators.SK_TARGETS_REMAP,
	operators.SK_EXPRESSION_COPY,
	# Distance trigger
	operators.SK_DRIVER_FUNC_REG,
	operators.SK_EVAL_TIME_RESET,
	operators.SK_EXPRESSION_FUNC_GET,
	operators.SK_EXPRESSION_FUNC_SET,

	operators.OB_FCURVES_LINK,
	operators.OB_FCURVES_COPY,
	operators.OB_FCURVES_OFFSET_CURSOR,
	operators.OB_FCURVES_OFFSET_MULTITARGET,
	operators.OB_FCURVES_OFFSET_NAME,

	operators.OB_NLA_CREATE,
	operators.OB_NLA_TO_FCURVES,
	operators.OB_NLA_SYNC_LENGTH,
	operators.OB_NLA_LINK_TO_ACTIVE,
	operators.OB_NLA_OFFSET_CURSOR,
	operators.OB_NLA_OFFSET_MULTITARGET,
	operators.OB_NLA_OFFSET_NAME,

	operators.SLOW_PARENT_OFFSET,

	CommotionProperties,
	ShapeKeysCollection,
)






def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.Scene.commotion = PointerProperty(type=CommotionProperties)
	bpy.types.Scene.commotion_skcoll = CollectionProperty(type=ShapeKeysCollection)


def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.commotion
	del bpy.types.Scene.commotion_skcoll


if __name__ == '__main__':
	register()
