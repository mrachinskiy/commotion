bl_info = {
	'name': 'Commotion',
	'author': 'Mikhail Rachinskiy (@_rachinskiy)',
	'version': (1, 3),
	'blender': (2, 77, 0),
	'location': '3D View > Tool Shelf',
	'description': 'Animation offset tools for motion graphics.',
	'wiki_url': 'https://github.com/mrachinskiy/commotion#readme',
	'tracker_url': 'https://github.com/mrachinskiy/commotion/issues',
	'category': 'Animation'}


if 'bpy' in locals():
	from importlib import reload
	reload(operators)
	reload(ui)
	reload(modules.anim_tools)
	reload(modules.nla)
	reload(modules.utility)
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
		operators,
		ui,
	)
	from .modules.utility import update_sk






class CommotionProperties(PropertyGroup):


	sk_shapekeys = BoolProperty(default=True)
	sk_shape_value = FloatProperty(name='Value', min=0.0, max=1.0, update=update_sk)
	sk_shape_interpolation = EnumProperty(
		items=(
			('KEY_LINEAR',      'Linear',      ''),
			('KEY_CARDINAL',    'Cardinal',    ''),
			('KEY_CATMULL_ROM', 'Catmull-Rom', ''),
			('KEY_BSPLINE',     'BSpline',     ''),
		),
		default='KEY_LINEAR',
		description='Set interpolation type for selected shape keys',
		update=update_sk)


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


	ob_transforms = BoolProperty()
	ob_offset_slow_parent = FloatProperty(name='Offset Factor', description='Offset step for slow parent offset', default=1, min=0, step=10, precision=1)






class ShapeKeysCollection(PropertyGroup):
	selected = BoolProperty(description='Affect referenced shape key')
	index = IntProperty()
	name = StringProperty()






classes = (
	CommotionProperties,
	ShapeKeysCollection,

	ui.ShapeKeyTools,
	ui.ObjectTools,

	operators.SK_REFRESH,
	operators.SK_AUTO_KEYFRAMES,

	operators.SK_FCURVES_LINK,
	operators.SK_FCURVES_COPY,
	operators.SK_FCURVES_OFFSET_CURSOR,
	operators.SK_FCURVES_OFFSET_MULTITARGET,
	operators.SK_FCURVES_OFFSET_NAME,
	operators.SK_FCURVES_ADD_TO_GROUP_OBJECTS,
	operators.SK_FCURVES_ADD_TO_GROUP_TARGETS,

	operators.SK_NLA_CREATE,
	operators.SK_NLA_TO_FCURVES,
	operators.SK_NLA_SYNC_LENGTH,
	operators.SK_NLA_LINK_TO_ACTIVE,
	operators.SK_NLA_OFFSET_CURSOR,
	operators.SK_NLA_OFFSET_MULTITARGET,
	operators.SK_NLA_OFFSET_NAME,
	operators.SK_NLA_ADD_TO_GROUP_OBJECTS,
	operators.SK_NLA_ADD_TO_GROUP_TARGETS,

	operators.SK_DRIVERS_SET_DISTANCE,
	operators.SK_DRIVERS_COPY_EXPRESSION,
	operators.SK_DRIVERS_REGISTER_DRV_FUNCTION,
	operators.SK_DRIVERS_RESET_EVAL_TIME,
	operators.SK_DRIVERS_GET_DRV_FUNC_EXPRESSION,
	operators.SK_DRIVERS_SET_DRV_FUNC_EXPRESSION,

	operators.OB_FCURVES_LINK,
	operators.OB_FCURVES_COPY,
	operators.OB_FCURVES_OFFSET_CURSOR,
	operators.OB_FCURVES_OFFSET_MULTITARGET,
	operators.OB_FCURVES_OFFSET_NAME,
	operators.OB_FCURVES_ADD_TO_GROUP_OBJECTS,
	operators.OB_FCURVES_ADD_TO_GROUP_TARGETS,

	operators.OB_NLA_CREATE,
	operators.OB_NLA_TO_FCURVES,
	operators.OB_NLA_SYNC_LENGTH,
	operators.OB_NLA_LINK_TO_ACTIVE,
	operators.OB_NLA_OFFSET_CURSOR,
	operators.OB_NLA_OFFSET_MULTITARGET,
	operators.OB_NLA_OFFSET_NAME,
	operators.OB_NLA_ADD_TO_GROUP_OBJECTS,
	operators.OB_NLA_ADD_TO_GROUP_TARGETS,

	operators.OB_OFFSET_SLOW_PARENT,
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
