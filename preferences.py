from bpy.types import PropertyGroup, AddonPreferences
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

# Extern
from . import addon_updater_ops


# Add-on preferences
# -----------------------------------


class PREFS_Commotion_Props(AddonPreferences):
	bl_idname = __package__

	# Updater settings
	# --------------------------

	auto_check_update = BoolProperty(
		name='Auto-check for Update',
		description='If enabled, auto-check for updates using an interval',
		default=True,
		)
	updater_intrval_months = IntProperty(
		name='Months',
		description='Number of months between checking for updates',
		default=0,
		min=0,
		)
	updater_intrval_days = IntProperty(
		name='Days',
		description='Number of days between checking for updates',
		default=7,
		min=0,
		)
	updater_intrval_hours = IntProperty(
		name='Hours',
		description='Number of hours between checking for updates',
		default=0,
		min=0,
		max=23,
		)
	updater_intrval_minutes = IntProperty(
		name='Minutes',
		description='Number of minutes between checking for updates',
		default=0,
		min=0,
		max=59,
		)

	def draw(self, context):
		addon_updater_ops.update_settings_ui(self, context)


# Scene properties
# -----------------------------------


def sk_value_update(self, context):
	props = context.scene.commotion
	sk = context.active_object.data.shape_keys

	for kb in context.window_manager.commotion_skcoll:
		if kb.selected:
			sk.key_blocks[kb.index].value = props.sk_value


def generateprops(self):
	offset = FloatProperty(name='Frame Offset', description='Frame step for animation offset', default=1, min=0, step=10, precision=3)
	threshold = FloatProperty(name='Threshold', description='Number of objects to animate per frame step', default=1, min=1, step=100, precision=0)
	reverse = BoolProperty(name='Reverse', description='Reverse animation offset')
	sort_options = EnumProperty(
		items=(('CURSOR', 'Cursor', ''),
		       ('MULTITARGET', 'Multi-target', ''),
		       ('NAME', 'Name', '')),
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
class SCENE_Commotion_Props(PropertyGroup):
	sk_shapekeys = BoolProperty()
	sk_value = FloatProperty(name='Value', min=0.0, max=1.0, update=sk_value_update)
	sk_drivers = BoolProperty()
	sk_drivers_dist_trigger = BoolProperty()
	sk_drivers_expression_func = StringProperty(description='Distance trigger expression')
	ob_transforms = BoolProperty()
	ob_slow_parent_offset = FloatProperty(name='Offset Factor', description='Offset step for slow parent offset', default=1, min=0, step=10, precision=1)


# Shape Key collection properties
# -----------------------------------


class WM_Commotion_SK_Collection(PropertyGroup):
	selected = BoolProperty(description='Affect referenced shape key')
	index = IntProperty()
	name = StringProperty()
