import bpy
from bpy.types import Operator
from . import helpers


class OT_SHAPE_LIST_REFRESH(Operator):
	"""Refresh list of toggles for available shape keys on active object"""
	bl_idname = "scene.shape_list_refresh"
	bl_label = "Refresh Shape List"

	def execute(self, context):
		helpers.shape_list_refresh(context)
		return {'FINISHED'}


class OT_AUTO_KEYFRAMES(Operator):
	"""Create keyframes for Evaluation Time property for selected objects, """ \
	"""based on current frame, amount and timings of absolute shape keys"""
	bl_idname = "scene.auto_keyframes"
	bl_label = "Auto Keyframes"

	def execute(self, context):
		helpers.auto_keyframes(context)
		return {'FINISHED'}












class OT_SK_FCURVES_LINK(Operator):
	"""Link animation from active to selected objects"""
	bl_idname = "scene.sk_fcurves_link"
	bl_label = "Link Animation"

	def execute(self, context):
		mode = ['SHAPE_KEYS', 'FCURVES']

		helpers.link_to_active(mode, context)

		return {'FINISHED'}


class OT_SK_FCURVES_COPY(Operator):
	"""Copy animation from active to selected objects (can also use this to unlink animation)"""
	bl_idname = "scene.sk_fcurves_copy"
	bl_label = "Copy Animation"

	def execute(self, context):
		mode = ['SHAPE_KEYS']

		helpers.copy_to_selected(mode, context)

		return {'FINISHED'}


class OT_SK_FCURVES_OFFSET_CURSOR(Operator):
	"""Offset animation for selected objects (wont work if F-Curves are linked, for obvious reasons)"""
	bl_idname = "scene.sk_fcurves_offset_cursor"
	bl_label = "Offset Animation"

	def execute(self, context):
		como = context.scene.como
		offset = como.sk_fcurves_offset
		threshold = como.sk_fcurves_threshold
		reverse = como.sk_fcurves_reverse
		mode = ['SHAPE_KEYS', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_cursor(offset, threshold, mode, context)

		return {'FINISHED'}


class OT_SK_FCURVES_OFFSET_MULTITARGET(Operator):
	"""Offset animation for selected objects (wont work if F-Curves are linked, for obvious reasons)"""
	bl_idname = "scene.sk_fcurves_offset_multitarget"
	bl_label = "Offset Animation"

	@classmethod
	def poll(cls, context):
		como = context.scene.como
		return (como.sk_fcurves_group_objects and como.sk_fcurves_group_targets)

	def execute(self, context):
		como = context.scene.como
		objects = bpy.data.groups[como.sk_fcurves_group_objects].objects
		targets = bpy.data.groups[como.sk_fcurves_group_targets].objects
		offset = como.sk_fcurves_offset
		threshold = como.sk_fcurves_threshold
		reverse = como.sk_fcurves_reverse
		mode = ['SHAPE_KEYS', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_multitarget(objects, targets, offset, threshold, mode, context)

		return {'FINISHED'}


class OT_SK_FCURVES_OFFSET_NAME(Operator):
	"""Offset animation for selected objects (wont work if F-Curves are linked, for obvious reasons)"""
	bl_idname = "scene.sk_fcurves_offset_name"
	bl_label = "Offset Animation"

	def execute(self, context):
		como = context.scene.como
		offset = como.sk_fcurves_offset
		threshold = como.sk_fcurves_threshold
		reverse = como.sk_fcurves_reverse
		mode = ['SHAPE_KEYS', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_name(offset, threshold, mode, context)

		return {'FINISHED'}















class OT_SK_NLA_CREATE(Operator):
	"""Create NLA strips from absolute shape keys animation"""
	bl_idname = "scene.sk_nla_create"
	bl_label = "Create NLA Strips"

	def execute(self, context):
		mode = ['SHAPE_KEYS']

		helpers.create_strips(mode, context)

		return {'FINISHED'}


class OT_SK_NLA_TO_FCURVES(Operator):
	"""Convert NLA strips to F-Curves"""
	bl_idname = "scene.sk_nla_to_fcurves"
	bl_label = "Strips to F-Curves"

	def execute(self, context):
		mode = ['SHAPE_KEYS']

		helpers.strips_to_fcurves(mode, context)

		return {'FINISHED'}


class OT_SK_NLA_SYNC_LENGTH(Operator):
	"""Sync length of NLA strips for selected objects"""
	bl_idname = "scene.sk_nla_sync_length"
	bl_label = "Sync Length"

	def execute(self, context):
		mode = ['SHAPE_KEYS']

		helpers.sync_len(mode, context)

		return {'FINISHED'}


class OT_SK_NLA_LINK_TO_ACTIVE(Operator):
	"""Link strips from active to selected objects"""
	bl_idname = "scene.sk_nla_link_to_active"
	bl_label = "Link Strips"

	def execute(self, context):
		mode = ['SHAPE_KEYS', 'NLA']

		helpers.link_to_active(mode, context)

		return {'FINISHED'}


class OT_SK_NLA_OFFSET_CURSOR(Operator):
	"""Offset animation for selected objects"""
	bl_idname = "scene.sk_nla_offset_cursor"
	bl_label = "Offset Strips"

	def execute(self, context):
		como = context.scene.como
		offset = como.sk_nla_offset
		threshold = como.sk_nla_threshold
		reverse = como.sk_nla_reverse
		mode = ['SHAPE_KEYS', 'NLA']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_cursor(offset, threshold, mode, context)

		return {'FINISHED'}


class OT_SK_NLA_OFFSET_MULTITARGET(Operator):
	"""Offset animation for selected objects"""
	bl_idname = "scene.sk_nla_offset_multitarget"
	bl_label = "Offset Strips"

	@classmethod
	def poll(cls, context):
		como = context.scene.como
		return (como.sk_nla_group_objects and como.sk_nla_group_targets)

	def execute(self, context):
		como = context.scene.como
		objects = bpy.data.groups[como.sk_nla_group_objects].objects
		targets = bpy.data.groups[como.sk_nla_group_targets].objects
		offset = como.sk_nla_offset
		threshold = como.sk_nla_threshold
		reverse = como.sk_nla_reverse
		mode = ['SHAPE_KEYS', 'NLA']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_multitarget(objects, targets, offset, threshold, mode, context)

		return {'FINISHED'}


class OT_SK_NLA_OFFSET_NAME(Operator):
	"""Offset animation for selected objects"""
	bl_idname = "scene.sk_nla_offset_name"
	bl_label = "Offset Strips"

	def execute(self, context):
		como = context.scene.como
		offset = como.sk_nla_offset
		threshold = como.sk_nla_threshold
		reverse = como.sk_nla_reverse
		mode = ['SHAPE_KEYS', 'NLA']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_name(offset, threshold, mode, context)

		return {'FINISHED'}

















class OT_SK_DRIVER_SET(Operator):
	"""Set driver with distance varable for selected objects. """ \
	"""Active object would be considered as target for a distance variable."""
	bl_idname = "scene.sk_driver_set"
	bl_label = "Set Distance Driver"

	def execute(self, context):
		helpers.driver_set(context)
		return {'FINISHED'}


class OT_SK_TARGETS_REMAP(Operator):
	"""Remap driver’s distance variable target property, from original to current object"""
	bl_idname = "scene.sk_targets_remap"
	bl_label = "Remap Targets"

	def execute(self, context):
		helpers.targets_remap(context)
		return {'FINISHED'}


class OT_SK_EXPRESSION_COPY(Operator):
	"""Copy driver's expression from active to selected objects"""
	bl_idname = "scene.sk_expression_copy"
	bl_label = "Copy To Selected"

	def execute(self, context):
		helpers.expression_copy(context)
		return {'FINISHED'}


class OT_SK_DRIVER_FUNC_REG(Operator):
	"""Register driver function and update driver dependencies (required for “Distance Trigger” to work)"""
	bl_idname = "scene.sk_driver_func_reg"
	bl_label = "Register driver function"

	def execute(self, context):
		helpers.register_driver_function(context)
		return {'FINISHED'}


class OT_SK_EVAL_TIME_RESET(Operator):
	"""Reset Evaluation Time property of selected objects to 0"""
	bl_idname = "scene.sk_eval_time_reset"
	bl_label = "Reset Eval Time"

	def execute(self, context):
		for ob in context.selected_objects:
			ob.data.shape_keys.eval_time = 0

		return {'FINISHED'}


class OT_SK_EXPRESSION_FUNC_SET(Operator):
	"""Set distance trigger expression for selected objects"""
	bl_idname = "scene.sk_expression_func_set"
	bl_label = "Set Function Expression"

	def execute(self, context):
		helpers.expression_func_set(context)
		return {'FINISHED'}












class OT_OB_FCURVES_LINK(Operator):
	"""Link animation from active to selected objects"""
	bl_idname = "scene.ob_fcurves_link"
	bl_label = "Link Animation"

	def execute(self, context):
		mode = ['OBJECT', 'FCURVES']

		helpers.link_to_active(mode, context)

		return {'FINISHED'}


class OT_OB_FCURVES_COPY(Operator):
	"""Copy animation from active to selected objects (can also use this to unlink animation)"""
	bl_idname = "scene.ob_fcurves_copy"
	bl_label = "Copy Animation"

	def execute(self, context):
		mode = ['OBJECT']
		
		helpers.copy_to_selected(mode, context)
			
		return {'FINISHED'}


class OT_OB_FCURVES_OFFSET_CURSOR(Operator):
	"""Offset animation for selected objects (wont work if F-Curves are linked, for obvious reasons)"""
	bl_idname = "scene.ob_fcurves_offset_cursor"
	bl_label = "Offset Animation"

	def execute(self, context):
		como = context.scene.como
		offset = como.ob_fcurves_offset
		threshold = como.ob_fcurves_threshold
		reverse = como.ob_fcurves_reverse
		mode = ['OBJECT', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_cursor(offset, threshold, mode, context)

		return {'FINISHED'}


class OT_OB_FCURVES_OFFSET_MULTITARGET(Operator):
	"""Offset animation for selected objects (wont work if F-Curves are linked, for obvious reasons)"""
	bl_idname = "scene.ob_fcurves_offset_multitarget"
	bl_label = "Offset Animation"

	@classmethod
	def poll(cls, context):
		como = context.scene.como
		return (como.ob_fcurves_group_objects and como.ob_fcurves_group_targets)

	def execute(self, context):
		como = context.scene.como
		objects = bpy.data.groups[como.ob_fcurves_group_objects].objects
		targets = bpy.data.groups[como.ob_fcurves_group_targets].objects
		offset = como.ob_fcurves_offset
		threshold = como.ob_fcurves_threshold
		reverse = como.ob_fcurves_reverse
		mode = ['OBJECT', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_multitarget(objects, targets, offset, threshold, mode, context)

		return {'FINISHED'}


class OT_OB_FCURVES_OFFSET_NAME(Operator):
	"""Offset animation for selected objects (wont work if F-Curves are linked, for obvious reasons)"""
	bl_idname = "scene.ob_fcurves_offset_name"
	bl_label = "Offset Animation"

	def execute(self, context):
		como = context.scene.como
		offset = como.ob_fcurves_offset
		threshold = como.ob_fcurves_threshold
		reverse = como.ob_fcurves_reverse
		mode = ['OBJECT', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_name(offset, threshold, mode, context)

		return {'FINISHED'}







class OT_OB_NLA_CREATE(Operator):
	"""Create NLA strips from object animation"""
	bl_idname = "scene.ob_nla_create"
	bl_label = "Create NLA Strips"

	def execute(self, context):
		mode = ['OBJECT']

		helpers.create_strips(mode, context)

		return {'FINISHED'}


class OT_OB_NLA_TO_FCURVES(Operator):
	"""Convert NLA strips to F-Curves"""
	bl_idname = "scene.ob_nla_to_fcurves"
	bl_label = "Strips to F-Curves"

	def execute(self, context):
		mode = ['OBJECT']

		helpers.strips_to_fcurves(mode, context)

		return {'FINISHED'}


class OT_OB_NLA_SYNC_LENGTH(Operator):
	"""Sync length of NLA strips for selected objects"""
	bl_idname = "scene.ob_nla_sync_length"
	bl_label = "Sync Length"

	def execute(self, context):
		mode = ['OBJECT']

		helpers.sync_len(mode, context)

		return {'FINISHED'}


class OT_OB_NLA_LINK_TO_ACTIVE(Operator):
	"""Link strips from active to selected objects"""
	bl_idname = "scene.ob_nla_link_to_active"
	bl_label = "Link Strips"

	def execute(self, context):
		mode = ['OBJECT', 'NLA']

		helpers.link_to_active(mode, context)

		return {'FINISHED'}


class OT_OB_NLA_OFFSET_CURSOR(Operator):
	"""Offset animation for selected objects"""
	bl_idname = "scene.ob_nla_offset_cursor"
	bl_label = "Offset Strips"

	def execute(self, context):
		como = context.scene.como
		offset =  como.ob_nla_offset
		threshold =  como.ob_nla_threshold
		reverse = como.ob_nla_reverse
		mode = ['OBJECT', 'NLA']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_cursor(offset, threshold, mode, context)

		return {'FINISHED'}


class OT_OB_NLA_OFFSET_MULTITARGET(Operator):
	"""Offset animation for selected objects"""
	bl_idname = "scene.ob_nla_offset_multitarget"
	bl_label = "Offset Strips"

	@classmethod
	def poll(cls, context):
		como = context.scene.como
		return (como.ob_nla_group_objects and como.ob_nla_group_targets)

	def execute(self, context):
		como = context.scene.como
		objects = bpy.data.groups[como.ob_nla_group_objects].objects
		targets = bpy.data.groups[como.ob_nla_group_targets].objects
		offset = como.ob_nla_offset
		threshold = como.ob_nla_threshold
		reverse = como.ob_nla_reverse
		mode = ['OBJECT', 'NLA']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_multitarget(objects, targets, offset, threshold, mode, context)

		return {'FINISHED'}


class OT_OB_NLA_OFFSET_NAME(Operator):
	"""Offset animation for selected objects"""
	bl_idname = "scene.ob_nla_offset_name"
	bl_label = "Offset Strips"

	def execute(self, context):
		como = context.scene.como
		offset = como.ob_nla_offset
		threshold = como.ob_nla_threshold
		reverse = como.ob_nla_reverse
		mode = ['OBJECT', 'NLA']
		if reverse:
			mode += ['REVERSE']

		helpers.offset_name(offset, threshold, mode, context)

		return {'FINISHED'}








class OT_SLOW_PARENT_OFFSET(Operator):
	"""Offset “Slow Parent” object property for selected objects"""
	bl_idname = "scene.slow_parent_offset"
	bl_label = "Offset Slow Parent"

	def execute(self, context):
		offset = context.scene.como.slow_parent_offset

		helpers.offset_parent(offset, context)

		return {'FINISHED'}