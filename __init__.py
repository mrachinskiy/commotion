bl_info = {
	'name': 'Commotion',
	'author': 'Mikhail Rachinskiy (@_rachinskiy)',
	'version': (1, 4),
	'blender': (2, 77, 0),
	'location': '3D View > Tool Shelf',
	'description': 'Animation offset tools for motion graphics.',
	'wiki_url': 'https://github.com/mrachinskiy/commotion#readme',
	'tracker_url': 'https://github.com/mrachinskiy/commotion/issues',
	'category': 'Animation',
	}


if 'bpy' in locals():
	from importlib import reload
	reload(ui)
	reload(operators)
	del reload
else:
	import bpy
	from bpy.types import PropertyGroup
	from bpy.props import (
		StringProperty,
		BoolProperty,
		IntProperty,
		FloatProperty,
		EnumProperty,
		PointerProperty,
		CollectionProperty,
		)
	from . import (
		ui,
		operators,
		)


def sk_value_update(self, context):
	scene = context.scene
	props = scene.commotion
	sk = context.active_object.data.shape_keys

	for kb in scene.commotion_skcoll:
		if kb.selected:
			sk.key_blocks[kb.index].value = props.sk_value


def generateprops(self):
	offset = FloatProperty(name='Frame Offset', description='Frame step for animation offset', default=1, min=0, step=10, precision=3)
	threshold = FloatProperty(name='Threshold', description='Number of objects to animate per frame step', default=1, min=1, step=100, precision=0)
	reverse = BoolProperty(name='Reverse', description='Reverse animation offset')
	sort_options = EnumProperty(
		items=(('CURSOR',      'Cursor',       ''),
		       ('MULTITARGET', 'Multi-target', ''),
		       ('NAME',        'Name',         '')),
		default='CURSOR',
		description='Animation offset by',
		)
	group_objects = StringProperty(name='Objects', description='Object group for animation offset')
	group_targets = StringProperty(name='Targets', description='Object group for targets, from which animation would be offseted')

	for prefix in ('sk_fcurves', 'sk_nla', 'ob_fcurves', 'ob_nla'):
		setattr(self, prefix,                    BoolProperty())
		setattr(self, prefix + '_offset',        offset)
		setattr(self, prefix + '_threshold',     threshold)
		setattr(self, prefix + '_reverse',       reverse)
		setattr(self, prefix + '_sort_options',  sort_options)
		setattr(self, prefix + '_group_objects', group_objects)
		setattr(self, prefix + '_group_targets', group_targets)

	return self


@generateprops
class Properties(PropertyGroup):
	sk_shapekeys = BoolProperty(default=True)
	sk_value = FloatProperty(name='Value', min=0.0, max=1.0, update=sk_value_update)
	sk_drivers = BoolProperty()
	sk_drivers_dist_trigger = BoolProperty()
	sk_drivers_expression_func = StringProperty(description='Distance trigger expression')
	ob_transforms = BoolProperty()
	ob_slow_parent_offset = FloatProperty(name='Offset Factor', description='Offset step for slow parent offset', default=1, min=0, step=10, precision=1)


class ShapeKeysCollection(PropertyGroup):
	selected = BoolProperty(description='Affect referenced shape key')
	index = IntProperty()
	name = StringProperty()


classes = (
	Properties,
	ShapeKeysCollection,

	ui.ShapeKeyTools,
	ui.ObjectTools,

	operators.SK_COLL_REFRESH,
	operators.SK_INTERPOLATION_SET,
	operators.SK_AUTO_KEYFRAMES,

	operators.ANIMATION_LINK,
	operators.ANIMATION_COPY,
	operators.NLA_TO_STRIPS,
	operators.NLA_TO_FCURVES,
	operators.NLA_SYNC_LENGTH,
	operators.ANIMATION_OFFSET_CURSOR,
	operators.ANIMATION_OFFSET_MULTITARGET,
	operators.ANIMATION_OFFSET_NAME,
	operators.OB_SLOW_PARENT_OFFSET,

	operators.SK_DRIVERS_DISTANCE_SET,
	operators.SK_DRIVERS_EXPRESSION_COPY,
	operators.SK_DRIVERS_TARGET_REMAP,
	operators.SK_DRIVERS_FUNCTION_REGISTER,
	operators.SK_DRIVERS_EVAL_TIME_RESET,
	operators.SK_DRIVERS_FUNC_EXPRESSION_GET,
	operators.SK_DRIVERS_FUNC_EXPRESSION_SET,

	operators.PRESET_APPLY,
	operators.ADD_TO_GROUP_OBJECTS,
	operators.ADD_TO_GROUP_TARGETS,
	operators.OB_SLOW_PARENT_TOGGLE,
	)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.Scene.commotion = PointerProperty(type=Properties)
	bpy.types.Scene.commotion_skcoll = CollectionProperty(type=ShapeKeysCollection)


def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.commotion
	del bpy.types.Scene.commotion_skcoll


if __name__ == '__main__':
	register()
