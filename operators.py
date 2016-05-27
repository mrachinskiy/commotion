import bpy
from bpy.types import Operator
from . import helpers


class SHAPE_LIST_REFRESH(Operator):
	"""Refresh list of toggles for available shape keys on active object"""
	bl_idname = 'commotion.shape_list_refresh'
	bl_label = 'Refresh Shape List'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		helpers.shape_list_refresh(context)
		return {'FINISHED'}


class AUTO_KEYFRAMES(Operator):
	"""Create keyframes for Evaluation Time property for selected objects, """ \
	"""based on current frame, amount and timings of absolute shape keys"""
	bl_idname = 'commotion.auto_keyframes'
	bl_label = 'Auto Keyframes'

	def execute(self, context):
		helpers.auto_keyframes(context)
		return {'FINISHED'}






class SK_FCURVES_LINK(Operator):
	"""Link animation from active to selected objects"""
	bl_idname = 'commotion.sk_fcurves_link'
	bl_label = 'Link Animation'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['SHAPE_KEYS', 'FCURVES']
		helpers.link_to_active(mode, context)
		return {'FINISHED'}


class SK_FCURVES_COPY(Operator):
	"""Copy animation from active to selected objects (can also use this to unlink animation)"""
	bl_idname = 'commotion.sk_fcurves_copy'
	bl_label = 'Copy Animation'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['SHAPE_KEYS']
		helpers.copy_to_selected(mode, context)
		return {'FINISHED'}


class SK_FCURVES_OFFSET_CURSOR(Operator):
	"""Offset animation for selected objects (won't work if F-Curves are linked)"""
	bl_idname = 'commotion.sk_fcurves_offset_cursor'
	bl_label = 'Offset Animation'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.sk_fcurves_offset
		threshold = props.sk_fcurves_threshold
		reverse = props.sk_fcurves_reverse
		mode = ['SHAPE_KEYS', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_cursor(offset, threshold, mode, context)

		return {'FINISHED'}


class SK_FCURVES_OFFSET_MULTITARGET(Operator):
	"""Offset animation for selected objects (won't work if F-Curves are linked)"""
	bl_idname = 'commotion.sk_fcurves_offset_multitarget'
	bl_label = 'Offset Animation'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		props = context.scene.commotion
		return (props.sk_fcurves_group_objects and props.sk_fcurves_group_targets)

	def execute(self, context):
		props = context.scene.commotion
		objects = bpy.data.groups[props.sk_fcurves_group_objects].objects
		targets = bpy.data.groups[props.sk_fcurves_group_targets].objects
		offset = props.sk_fcurves_offset
		threshold = props.sk_fcurves_threshold
		reverse = props.sk_fcurves_reverse
		mode = ['SHAPE_KEYS', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_multitarget(objects, targets, offset, threshold, mode, context)

		return {'FINISHED'}


class SK_FCURVES_OFFSET_NAME(Operator):
	"""Offset animation for selected objects (won't work if F-Curves are linked)"""
	bl_idname = 'commotion.sk_fcurves_offset_name'
	bl_label = 'Offset Animation'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.sk_fcurves_offset
		threshold = props.sk_fcurves_threshold
		reverse = props.sk_fcurves_reverse
		mode = ['SHAPE_KEYS', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_name(offset, threshold, mode, context)

		return {'FINISHED'}






class SK_NLA_CREATE(Operator):
	"""Create NLA strips from absolute shape keys animation"""
	bl_idname = 'commotion.sk_nla_create'
	bl_label = 'Create NLA Strips'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['SHAPE_KEYS']
		helpers.create_strips(mode, context)
		return {'FINISHED'}


class SK_NLA_TO_FCURVES(Operator):
	"""Convert NLA strips to F-Curves"""
	bl_idname = 'commotion.sk_nla_to_fcurves'
	bl_label = 'Strips to F-Curves'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['SHAPE_KEYS']
		helpers.strips_to_fcurves(mode, context)
		return {'FINISHED'}


class SK_NLA_SYNC_LENGTH(Operator):
	"""Sync length of NLA strips for selected objects"""
	bl_idname = 'commotion.sk_nla_sync_length'
	bl_label = 'Sync Length'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['SHAPE_KEYS']
		helpers.sync_len(mode, context)
		return {'FINISHED'}


class SK_NLA_LINK_TO_ACTIVE(Operator):
	"""Link strips from active to selected objects"""
	bl_idname = 'commotion.sk_nla_link_to_active'
	bl_label = 'Link Strips'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['SHAPE_KEYS', 'NLA']
		helpers.link_to_active(mode, context)
		return {'FINISHED'}


class SK_NLA_OFFSET_CURSOR(Operator):
	"""Offset animation for selected objects"""
	bl_idname = 'commotion.sk_nla_offset_cursor'
	bl_label = 'Offset Strips'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.sk_nla_offset
		threshold = props.sk_nla_threshold
		reverse = props.sk_nla_reverse
		mode = ['SHAPE_KEYS', 'NLA']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_cursor(offset, threshold, mode, context)

		return {'FINISHED'}


class SK_NLA_OFFSET_MULTITARGET(Operator):
	"""Offset animation for selected objects"""
	bl_idname = 'commotion.sk_nla_offset_multitarget'
	bl_label = 'Offset Strips'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		props = context.scene.commotion
		return (props.sk_nla_group_objects and props.sk_nla_group_targets)

	def execute(self, context):
		props = context.scene.commotion
		objects = bpy.data.groups[props.sk_nla_group_objects].objects
		targets = bpy.data.groups[props.sk_nla_group_targets].objects
		offset = props.sk_nla_offset
		threshold = props.sk_nla_threshold
		reverse = props.sk_nla_reverse
		mode = ['SHAPE_KEYS', 'NLA']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_multitarget(objects, targets, offset, threshold, mode, context)

		return {'FINISHED'}


class SK_NLA_OFFSET_NAME(Operator):
	"""Offset animation for selected objects"""
	bl_idname = 'commotion.sk_nla_offset_name'
	bl_label = 'Offset Strips'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.sk_nla_offset
		threshold = props.sk_nla_threshold
		reverse = props.sk_nla_reverse
		mode = ['SHAPE_KEYS', 'NLA']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_name(offset, threshold, mode, context)

		return {'FINISHED'}






class SK_DRIVER_SET(Operator):
	"""Set driver with distance varable for selected objects. Active object would be considered as target for a distance variable."""
	bl_idname = 'commotion.sk_driver_set'
	bl_label = 'Set Distance Driver'

	def execute(self, context):
		helpers.driver_set(context)
		return {'FINISHED'}


class SK_TARGETS_REMAP(Operator):
	"""Remap driver's distance variable target property, from original to current object"""
	bl_idname = 'commotion.sk_targets_remap'
	bl_label = 'Remap Targets'

	def execute(self, context):
		helpers.targets_remap(context)
		return {'FINISHED'}


class SK_EXPRESSION_COPY(Operator):
	"""Copy driver's expression from active to selected objects"""
	bl_idname = 'commotion.sk_expression_copy'
	bl_label = 'Copy To Selected'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		helpers.expression_copy(context)
		return {'FINISHED'}


class SK_DRIVER_FUNC_REG(Operator):
	"""Register driver function and update driver dependencies (required for "Distance Trigger" to work)"""
	bl_idname = 'commotion.sk_driver_func_reg'
	bl_label = 'Register driver function'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		helpers.register_driver_function(context)
		return {'FINISHED'}


class SK_EVAL_TIME_RESET(Operator):
	"""Reset Evaluation Time property of selected objects to 0"""
	bl_idname = 'commotion.sk_eval_time_reset'
	bl_label = 'Reset Eval Time'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		for ob in context.selected_objects:
			ob.data.shape_keys.eval_time = 0
		return {'FINISHED'}


class SK_EXPRESSION_FUNC_GET(Operator):
	"""Get expression from current object"""
	bl_idname = 'commotion.sk_expression_func_get'
	bl_label = 'Get Expression'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		fcus = context.active_object.data.shape_keys.animation_data.drivers
		for fcu in fcus:
			if fcu.data_path == 'eval_time':
				drv = fcu.driver
		context.scene.commotion.sk_drivers_expression_func = drv.expression
		return {'FINISHED'}


class SK_EXPRESSION_FUNC_SET(Operator):
	"""Set distance trigger expression for selected objects"""
	bl_idname = 'commotion.sk_expression_func_set'
	bl_label = 'Set Expression'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		helpers.expression_func_set(context)
		return {'FINISHED'}






class OB_FCURVES_LINK(Operator):
	"""Link animation from active to selected objects"""
	bl_idname = 'commotion.ob_fcurves_link'
	bl_label = 'Link Animation'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['OBJECT', 'FCURVES']
		helpers.link_to_active(mode, context)
		return {'FINISHED'}


class OB_FCURVES_COPY(Operator):
	"""Copy animation from active to selected objects (can also use this to unlink animation)"""
	bl_idname = 'commotion.ob_fcurves_copy'
	bl_label = 'Copy Animation'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['OBJECT']
		helpers.copy_to_selected(mode, context)
		return {'FINISHED'}


class OB_FCURVES_OFFSET_CURSOR(Operator):
	"""Offset animation for selected objects (won't work if F-Curves are linked)"""
	bl_idname = 'commotion.ob_fcurves_offset_cursor'
	bl_label = 'Offset Animation'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.ob_fcurves_offset
		threshold = props.ob_fcurves_threshold
		reverse = props.ob_fcurves_reverse
		mode = ['OBJECT', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_cursor(offset, threshold, mode, context)

		return {'FINISHED'}


class OB_FCURVES_OFFSET_MULTITARGET(Operator):
	"""Offset animation for selected objects (won't work if F-Curves are linked)"""
	bl_idname = 'commotion.ob_fcurves_offset_multitarget'
	bl_label = 'Offset Animation'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		props = context.scene.commotion
		return (props.ob_fcurves_group_objects and props.ob_fcurves_group_targets)

	def execute(self, context):
		props = context.scene.commotion
		objects = bpy.data.groups[props.ob_fcurves_group_objects].objects
		targets = bpy.data.groups[props.ob_fcurves_group_targets].objects
		offset = props.ob_fcurves_offset
		threshold = props.ob_fcurves_threshold
		reverse = props.ob_fcurves_reverse
		mode = ['OBJECT', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_multitarget(objects, targets, offset, threshold, mode, context)

		return {'FINISHED'}


class OB_FCURVES_OFFSET_NAME(Operator):
	"""Offset animation for selected objects (won't work if F-Curves are linked)"""
	bl_idname = 'commotion.ob_fcurves_offset_name'
	bl_label = 'Offset Animation'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.ob_fcurves_offset
		threshold = props.ob_fcurves_threshold
		reverse = props.ob_fcurves_reverse
		mode = ['OBJECT', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_name(offset, threshold, mode, context)

		return {'FINISHED'}






class OB_NLA_CREATE(Operator):
	"""Create NLA strips from object animation"""
	bl_idname = 'commotion.ob_nla_create'
	bl_label = 'Create NLA Strips'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['OBJECT']
		helpers.create_strips(mode, context)
		return {'FINISHED'}


class OB_NLA_TO_FCURVES(Operator):
	"""Convert NLA strips to F-Curves"""
	bl_idname = 'commotion.ob_nla_to_fcurves'
	bl_label = 'Strips to F-Curves'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['OBJECT']
		helpers.strips_to_fcurves(mode, context)
		return {'FINISHED'}


class OB_NLA_SYNC_LENGTH(Operator):
	"""Sync length of NLA strips for selected objects"""
	bl_idname = 'commotion.ob_nla_sync_length'
	bl_label = 'Sync Length'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['OBJECT']
		helpers.sync_len(mode, context)
		return {'FINISHED'}


class OB_NLA_LINK_TO_ACTIVE(Operator):
	"""Link strips from active to selected objects"""
	bl_idname = 'commotion.ob_nla_link_to_active'
	bl_label = 'Link Strips'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['OBJECT', 'NLA']
		helpers.link_to_active(mode, context)
		return {'FINISHED'}


class OB_NLA_OFFSET_CURSOR(Operator):
	"""Offset animation for selected objects"""
	bl_idname = 'commotion.ob_nla_offset_cursor'
	bl_label = 'Offset Strips'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset =  props.ob_nla_offset
		threshold =  props.ob_nla_threshold
		reverse = props.ob_nla_reverse
		mode = ['OBJECT', 'NLA']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_cursor(offset, threshold, mode, context)

		return {'FINISHED'}


class OB_NLA_OFFSET_MULTITARGET(Operator):
	"""Offset animation for selected objects"""
	bl_idname = 'commotion.ob_nla_offset_multitarget'
	bl_label = 'Offset Strips'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		props = context.scene.commotion
		return (props.ob_nla_group_objects and props.ob_nla_group_targets)

	def execute(self, context):
		props = context.scene.commotion
		objects = bpy.data.groups[props.ob_nla_group_objects].objects
		targets = bpy.data.groups[props.ob_nla_group_targets].objects
		offset = props.ob_nla_offset
		threshold = props.ob_nla_threshold
		reverse = props.ob_nla_reverse
		mode = ['OBJECT', 'NLA']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_multitarget(objects, targets, offset, threshold, mode, context)

		return {'FINISHED'}


class OB_NLA_OFFSET_NAME(Operator):
	"""Offset animation for selected objects"""
	bl_idname = 'commotion.ob_nla_offset_name'
	bl_label = 'Offset Strips'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.ob_nla_offset
		threshold = props.ob_nla_threshold
		reverse = props.ob_nla_reverse
		mode = ['OBJECT', 'NLA']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_name(offset, threshold, mode, context)

		return {'FINISHED'}






class SLOW_PARENT_OFFSET(Operator):
	"""Offset "Slow Parent" object property for selected objects"""
	bl_idname = 'commotion.slow_parent_offset'
	bl_label = 'Offset Slow Parent'

	def execute(self, context):
		offset = context.scene.commotion.slow_parent_offset
		helpers.offset_parent(offset, context)
		return {'FINISHED'}
