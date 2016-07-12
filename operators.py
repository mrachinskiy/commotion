import bpy
from bpy.types import Operator
from re import sub
from . import (
	anim_tools,
	nla_tools,
	utility,
)


class SK_REFRESH(Operator):
	"""Refresh shape key list for active object"""
	bl_label = 'Refresh Shape List'
	bl_idname = 'commotion.sk_refresh'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		scene = context.scene
		skcoll = scene.commotion_skcoll

		if hasattr(scene, 'commotion_skcoll'):
			for kb in skcoll:
				skcoll.remove(0)

		i = 0
		for kb in context.active_object.data.shape_keys.key_blocks:
			skcoll.add()
			skcoll[i].name = kb.name
			skcoll[i].index = i
			i += 1

		return {'FINISHED'}


class SK_AUTO_KEYFRAMES(Operator):
	"""Create keyframes for absolute shape keys on selected objects, """ \
	"""based on the current frame and shape keys timings"""
	bl_label = 'Auto Keyframes'
	bl_idname = 'commotion.sk_auto_keyframes'

	def execute(self, context):
		frame = context.scene.frame_current

		for ob in context.selected_objects:
			try:
				sk = ob.data.shape_keys
			except:
				continue

			if not sk.use_relative:
				sk.eval_time = int(sk.key_blocks[1].frame)
				sk.keyframe_insert(data_path='eval_time', frame=frame)
				sk.eval_time = int(sk.key_blocks[-1].frame)
				sk.keyframe_insert(data_path='eval_time', frame=frame + 20)

				for fcu in sk.animation_data.action.fcurves:
					fcu.color_mode = 'AUTO_RAINBOW'

		return {'FINISHED'}






class SK_FCURVES_LINK(Operator):
	"""Link animation from active to selected objects"""
	bl_label = 'Link Animation'
	bl_idname = 'commotion.sk_fcurves_link'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		try:
			return context.active_object.data.shape_keys.animation_data.action
		except:
			return False

	def execute(self, context):
		mode = ['SHAPE_KEYS', 'FCURVES']
		anim_tools.anim_link_to_active(mode, context)
		return {'FINISHED'}


class SK_FCURVES_COPY(Operator):
	"""Copy animation from active to selected objects (can also use this to unlink animation)"""
	bl_label = 'Copy Animation'
	bl_idname = 'commotion.sk_fcurves_copy'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		try:
			return context.active_object.data.shape_keys.animation_data.action
		except:
			return False

	def execute(self, context):
		mode = ['SHAPE_KEYS']
		anim_tools.fcurves_copy_to_selected(mode, context)
		return {'FINISHED'}


class SK_FCURVES_OFFSET_CURSOR(Operator):
	"""Offset animation for selected objects (won't work if F-Curves are linked)"""
	bl_label = 'Offset Animation'
	bl_idname = 'commotion.sk_fcurves_offset_cursor'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.sk_fcurves_offset
		threshold = props.sk_fcurves_threshold
		reverse = props.sk_fcurves_reverse
		mode = ['SHAPE_KEYS', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		anim_tools.offset_cursor(offset, threshold, mode, context)

		return {'FINISHED'}


class SK_FCURVES_OFFSET_MULTITARGET(Operator):
	"""Offset animation for selected objects (won't work if F-Curves are linked)"""
	bl_label = 'Offset Animation'
	bl_idname = 'commotion.sk_fcurves_offset_multitarget'
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

		anim_tools.offset_multitarget(objects, targets, offset, threshold, mode, context)

		return {'FINISHED'}


class SK_FCURVES_OFFSET_NAME(Operator):
	"""Offset animation for selected objects (won't work if F-Curves are linked)"""
	bl_label = 'Offset Animation'
	bl_idname = 'commotion.sk_fcurves_offset_name'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.sk_fcurves_offset
		threshold = props.sk_fcurves_threshold
		reverse = props.sk_fcurves_reverse
		mode = ['SHAPE_KEYS', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		anim_tools.offset_name(offset, threshold, mode, context)

		return {'FINISHED'}


class SK_FCURVES_ADD_TO_GROUP_OBJECTS(Operator):
	"""Add selected objects to group"""
	bl_label = 'Add to group'
	bl_idname = 'commotion.sk_fcurves_add_to_group_objects'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['SHAPE_KEYS', 'FCURVES']
		anim_tools.add_to_group('Objects', mode, context)
		return {'FINISHED'}


class SK_FCURVES_ADD_TO_GROUP_TARGETS(Operator):
	"""Add selected objects to group"""
	bl_label = 'Add to group'
	bl_idname = 'commotion.sk_fcurves_add_to_group_targets'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['SHAPE_KEYS', 'FCURVES']
		anim_tools.add_to_group('Targets', mode, context)
		return {'FINISHED'}






class SK_NLA_CREATE(Operator):
	"""Create NLA strips from shape keys animation"""
	bl_label = 'Create NLA Strips'
	bl_idname = 'commotion.sk_nla_create'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		try:
			return context.active_object.data.shape_keys.animation_data.action
		except:
			return False

	def execute(self, context):
		mode = ['SHAPE_KEYS']
		nla_tools.create_strips(mode, context)
		return {'FINISHED'}


class SK_NLA_TO_FCURVES(Operator):
	"""Convert NLA strips back to F-Curves"""
	bl_label = 'Strips to F-Curves'
	bl_idname = 'commotion.sk_nla_to_fcurves'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		try:
			return context.active_object.data.shape_keys.animation_data.nla_tracks[0].strips
		except:
			return False

	def execute(self, context):
		mode = ['SHAPE_KEYS']
		nla_tools.strips_to_fcurves(mode, context)
		return {'FINISHED'}


class SK_NLA_SYNC_LENGTH(Operator):
	"""Synchronize length of NLA strips for selected objects"""
	bl_label = 'Sync Length'
	bl_idname = 'commotion.sk_nla_sync_length'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		try:
			return context.active_object.data.shape_keys.animation_data.nla_tracks[0].strips
		except:
			return False

	def execute(self, context):
		mode = ['SHAPE_KEYS']
		nla_tools.sync_len(mode, context)
		return {'FINISHED'}


class SK_NLA_LINK_TO_ACTIVE(Operator):
	"""Link strips from active to selected objects"""
	bl_label = 'Link Strips'
	bl_idname = 'commotion.sk_nla_link_to_active'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		try:
			return context.active_object.data.shape_keys.animation_data.nla_tracks[0].strips
		except:
			return False

	def execute(self, context):
		mode = ['SHAPE_KEYS', 'NLA']
		anim_tools.anim_link_to_active(mode, context)
		return {'FINISHED'}


class SK_NLA_OFFSET_CURSOR(Operator):
	"""Offset animation for selected objects"""
	bl_label = 'Offset Strips'
	bl_idname = 'commotion.sk_nla_offset_cursor'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.sk_nla_offset
		threshold = props.sk_nla_threshold
		reverse = props.sk_nla_reverse
		mode = ['SHAPE_KEYS', 'NLA']
		if reverse:
			mode += ['REVERSE']

		anim_tools.offset_cursor(offset, threshold, mode, context)

		return {'FINISHED'}


class SK_NLA_OFFSET_MULTITARGET(Operator):
	"""Offset animation for selected objects"""
	bl_label = 'Offset Strips'
	bl_idname = 'commotion.sk_nla_offset_multitarget'
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

		anim_tools.offset_multitarget(objects, targets, offset, threshold, mode, context)

		return {'FINISHED'}


class SK_NLA_OFFSET_NAME(Operator):
	"""Offset animation for selected objects"""
	bl_label = 'Offset Strips'
	bl_idname = 'commotion.sk_nla_offset_name'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.sk_nla_offset
		threshold = props.sk_nla_threshold
		reverse = props.sk_nla_reverse
		mode = ['SHAPE_KEYS', 'NLA']
		if reverse:
			mode += ['REVERSE']

		anim_tools.offset_name(offset, threshold, mode, context)

		return {'FINISHED'}


class SK_NLA_ADD_TO_GROUP_OBJECTS(Operator):
	"""Add selected objects to group"""
	bl_label = 'Add to group'
	bl_idname = 'commotion.sk_nla_add_to_group_objects'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['SHAPE_KEYS', 'NLA']
		anim_tools.add_to_group('Objects', mode, context)
		return {'FINISHED'}


class SK_NLA_ADD_TO_GROUP_TARGETS(Operator):
	"""Add selected objects to group"""
	bl_label = 'Add to group'
	bl_idname = 'commotion.sk_nla_add_to_group_targets'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['SHAPE_KEYS', 'NLA']
		anim_tools.add_to_group('Targets', mode, context)
		return {'FINISHED'}






class SK_DRIVERS_SET_DISTANCE(Operator):
	"""Set distance driver for absolute shape keys on selected objects. """ \
	"""Empty created as a target for driver's distance variable."""
	bl_label = 'Set Distance Driver'
	bl_idname = 'commotion.sk_drivers_set_distance'

	def execute(self, context):
		scene = context.scene
		empty = bpy.data.objects.new('Distance Target', None)
		scene.objects.link(empty)
		empty.location = scene.cursor_location
		empty.select = True
		empty.empty_draw_type = 'SPHERE'
		empty.empty_draw_size = 2.0

		for ob in context.selected_objects:

			if (ob.data and ob.data.shape_keys):

				sk = ob.data.shape_keys

				if (sk.animation_data and sk.animation_data.drivers):
					continue

				kb = int(sk.key_blocks[1].frame)
				kb_last = str(int(sk.key_blocks[-1].frame) + 5)

				sk.driver_add('eval_time')

				fcu = ob.data.shape_keys.animation_data.drivers.find('eval_time')

				drv = fcu.driver
				drv.type = 'SCRIPTED'
				drv.expression = kb_last + ' - (dist * 3 / scale)'
				drv.show_debug_info = True

				var = drv.variables.new()
				var.name = 'dist'
				var.type = 'LOC_DIFF'
				var.targets[0].id = ob
				var.targets[1].id = empty

				var = drv.variables.new()
				var.name = 'scale'
				var.type = 'SINGLE_PROP'
				var.targets[0].id = empty
				var.targets[0].data_path = 'scale[0]'

				if fcu.modifiers:
					fcu.modifiers.remove(fcu.modifiers[0])

				fcu.keyframe_points.insert(0, kb)
				fcu.keyframe_points.insert(kb, kb)
				fcu.keyframe_points.insert(kb + 10, kb + 10)

				fcu.extrapolation = 'LINEAR'
				for kp in fcu.keyframe_points:
					kp.interpolation = 'LINEAR'

		return {'FINISHED'}


class SK_DRIVERS_COPY_EXPRESSION(Operator):
	"""Copy driver's expression from active to selected objects"""
	bl_label = 'Copy To Selected'
	bl_idname = 'commotion.sk_drivers_copy_expression'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		active_fcu = context.active_object.data.shape_keys.animation_data.drivers.find('eval_time')
		for ob in context.selected_objects:
			try:
				fcu = ob.data.shape_keys.animation_data.drivers.find('eval_time')
				fcu.driver.expression = active_fcu.driver.expression
			except:
				pass

		return {'FINISHED'}


class SK_DRIVERS_REGISTER_FUNCTION(Operator):
	"""Register Distance Trigger driver function.\n""" \
	"""Use it every time when open blend file, otherwise Distance Trigger drivers won't work."""
	bl_label = 'Register driver function'
	bl_idname = 'commotion.sk_drivers_register_function'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		bpy.app.driver_namespace['dist_trigger'] = utility.dist_trigger

		for sk in bpy.data.shape_keys:
			if (sk.animation_data and sk.animation_data.drivers):
				fcu = sk.animation_data.drivers.find('eval_time')
				fcu.driver.expression = fcu.driver.expression

		return {'FINISHED'}


class SK_DRIVERS_RESET_EVAL_TIME(Operator):
	"""Reset Evaluation Time property for selected objects to 0"""
	bl_label = 'Reset Evaluation Time'
	bl_idname = 'commotion.sk_drivers_reset_eval_time'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		for ob in context.selected_objects:
			try:
				ob.data.shape_keys.eval_time = 0
			except:
				pass

		return {'FINISHED'}


class SK_DRIVERS_GET_FUNC_EXPRESSION(Operator):
	"""Get expression from active object"""
	bl_label = 'Get Expression'
	bl_idname = 'commotion.sk_drivers_get_func_expression'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		fcu = context.active_object.data.shape_keys.animation_data.drivers.find('eval_time')
		expression = fcu.driver.expression
		sanitized = sub(r'dist_trigger\((.+),.+\)', r'\1', expression)
		context.scene.commotion.sk_drivers_expression_func = sanitized
		return {'FINISHED'}


class SK_DRIVERS_SET_FUNC_EXPRESSION(Operator):
	"""Set distance trigger expression for selected objects"""
	bl_label = 'Set Expression'
	bl_idname = 'commotion.sk_drivers_set_func_expression'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		expr = props.sk_drivers_expression_func

		for ob in context.selected_objects:
			try:
				fcu = ob.data.shape_keys.animation_data.drivers.find('eval_time')
				fcu.driver.expression = "dist_trigger(%s, '%s')" % (expr, ob.name)
			except:
				pass

		return {'FINISHED'}






class OB_FCURVES_LINK(Operator):
	"""Link animation from active to selected objects"""
	bl_label = 'Link Animation'
	bl_idname = 'commotion.ob_fcurves_link'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		try:
			return context.active_object.animation_data.action
		except:
			return False

	def execute(self, context):
		mode = ['OBJECT', 'FCURVES']
		anim_tools.anim_link_to_active(mode, context)
		return {'FINISHED'}


class OB_FCURVES_COPY(Operator):
	"""Copy animation from active to selected objects (can also use this to unlink animation)"""
	bl_label = 'Copy Animation'
	bl_idname = 'commotion.ob_fcurves_copy'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		try:
			return context.active_object.animation_data.action
		except:
			return False

	def execute(self, context):
		mode = ['OBJECT']
		anim_tools.fcurves_copy_to_selected(mode, context)
		return {'FINISHED'}


class OB_FCURVES_OFFSET_CURSOR(Operator):
	"""Offset animation for selected objects (won't work if F-Curves are linked)"""
	bl_label = 'Offset Animation'
	bl_idname = 'commotion.ob_fcurves_offset_cursor'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.ob_fcurves_offset
		threshold = props.ob_fcurves_threshold
		reverse = props.ob_fcurves_reverse
		mode = ['OBJECT', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		anim_tools.offset_cursor(offset, threshold, mode, context)

		return {'FINISHED'}


class OB_FCURVES_OFFSET_MULTITARGET(Operator):
	"""Offset animation for selected objects (won't work if F-Curves are linked)"""
	bl_label = 'Offset Animation'
	bl_idname = 'commotion.ob_fcurves_offset_multitarget'
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

		anim_tools.offset_multitarget(objects, targets, offset, threshold, mode, context)

		return {'FINISHED'}


class OB_FCURVES_OFFSET_NAME(Operator):
	"""Offset animation for selected objects (won't work if F-Curves are linked)"""
	bl_label = 'Offset Animation'
	bl_idname = 'commotion.ob_fcurves_offset_name'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.ob_fcurves_offset
		threshold = props.ob_fcurves_threshold
		reverse = props.ob_fcurves_reverse
		mode = ['OBJECT', 'FCURVES']
		if reverse:
			mode += ['REVERSE']

		anim_tools.offset_name(offset, threshold, mode, context)

		return {'FINISHED'}


class OB_FCURVES_ADD_TO_GROUP_OBJECTS(Operator):
	"""Add selected objects to group"""
	bl_label = 'Add to group'
	bl_idname = 'commotion.ob_fcurves_add_to_group_objects'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['OBJECT', 'FCURVES']
		anim_tools.add_to_group('Objects', mode, context)
		return {'FINISHED'}


class OB_FCURVES_ADD_TO_GROUP_TARGETS(Operator):
	"""Add selected objects to group"""
	bl_label = 'Add to group'
	bl_idname = 'commotion.ob_fcurves_add_to_group_targets'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['OBJECT', 'FCURVES']
		anim_tools.add_to_group('Targets', mode, context)
		return {'FINISHED'}






class OB_NLA_CREATE(Operator):
	"""Create NLA strips from object animation"""
	bl_label = 'Create NLA Strips'
	bl_idname = 'commotion.ob_nla_create'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		try:
			return context.active_object.animation_data.action
		except:
			return False

	def execute(self, context):
		mode = ['OBJECT']
		nla_tools.create_strips(mode, context)
		return {'FINISHED'}


class OB_NLA_TO_FCURVES(Operator):
	"""Convert NLA strips back to F-Curves"""
	bl_label = 'Strips to F-Curves'
	bl_idname = 'commotion.ob_nla_to_fcurves'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		try:
			return context.active_object.animation_data.nla_tracks[0].strips
		except:
			return False

	def execute(self, context):
		mode = ['OBJECT']
		nla_tools.strips_to_fcurves(mode, context)
		return {'FINISHED'}


class OB_NLA_SYNC_LENGTH(Operator):
	"""Synchronize length of NLA strips for selected objects"""
	bl_label = 'Sync Length'
	bl_idname = 'commotion.ob_nla_sync_length'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		try:
			return context.active_object.animation_data.nla_tracks[0].strips
		except:
			return False

	def execute(self, context):
		mode = ['OBJECT']
		nla_tools.sync_len(mode, context)
		return {'FINISHED'}


class OB_NLA_LINK_TO_ACTIVE(Operator):
	"""Link strips from active to selected objects"""
	bl_label = 'Link Strips'
	bl_idname = 'commotion.ob_nla_link_to_active'
	bl_options = {'INTERNAL'}

	@classmethod
	def poll(cls, context):
		try:
			return context.active_object.animation_data.nla_tracks[0].strips
		except:
			return False

	def execute(self, context):
		mode = ['OBJECT', 'NLA']
		anim_tools.anim_link_to_active(mode, context)
		return {'FINISHED'}


class OB_NLA_OFFSET_CURSOR(Operator):
	"""Offset animation for selected objects"""
	bl_label = 'Offset Strips'
	bl_idname = 'commotion.ob_nla_offset_cursor'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset =  props.ob_nla_offset
		threshold =  props.ob_nla_threshold
		reverse = props.ob_nla_reverse
		mode = ['OBJECT', 'NLA']
		if reverse:
			mode += ['REVERSE']

		anim_tools.offset_cursor(offset, threshold, mode, context)

		return {'FINISHED'}


class OB_NLA_OFFSET_MULTITARGET(Operator):
	"""Offset animation for selected objects"""
	bl_label = 'Offset Strips'
	bl_idname = 'commotion.ob_nla_offset_multitarget'
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

		anim_tools.offset_multitarget(objects, targets, offset, threshold, mode, context)

		return {'FINISHED'}


class OB_NLA_OFFSET_NAME(Operator):
	"""Offset animation for selected objects"""
	bl_label = 'Offset Strips'
	bl_idname = 'commotion.ob_nla_offset_name'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		offset = props.ob_nla_offset
		threshold = props.ob_nla_threshold
		reverse = props.ob_nla_reverse
		mode = ['OBJECT', 'NLA']
		if reverse:
			mode += ['REVERSE']

		anim_tools.offset_name(offset, threshold, mode, context)

		return {'FINISHED'}


class OB_NLA_ADD_TO_GROUP_OBJECTS(Operator):
	"""Add selected objects to group"""
	bl_label = 'Add to group'
	bl_idname = 'commotion.ob_nla_add_to_group_objects'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['OBJECT', 'NLA']
		anim_tools.add_to_group('Objects', mode, context)
		return {'FINISHED'}


class OB_NLA_ADD_TO_GROUP_TARGETS(Operator):
	"""Add selected objects to group"""
	bl_label = 'Add to group'
	bl_idname = 'commotion.ob_nla_add_to_group_targets'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		mode = ['OBJECT', 'NLA']
		anim_tools.add_to_group('Targets', mode, context)
		return {'FINISHED'}






class OB_OFFSET_SLOW_PARENT(Operator):
	"""Offset Slow Parent property for selected objects"""
	bl_label = 'Offset Slow Parent'
	bl_idname = 'commotion.ob_offset_slow_parent'

	def execute(self, context):
		offset = context.scene.commotion.ob_offset_slow_parent
		anim_tools.offset_parent(offset, context)
		return {'FINISHED'}


class OB_SLOW_PARENT_ON(Operator):
	"""Toggle Slow Parent property on for selected objects"""
	bl_label = 'On'
	bl_idname = 'commotion.ob_slow_parent_on'

	def execute(self, context):
		for ob in context.selected_objects:
			if ob.parent:
				ob.use_slow_parent = True
		return {'FINISHED'}


class OB_SLOW_PARENT_OFF(Operator):
	"""Toggle Slow Parent property off for selected objects"""
	bl_label = 'Off'
	bl_idname = 'commotion.ob_slow_parent_off'

	def execute(self, context):
		for ob in context.selected_objects:
			if ob.parent:
				ob.use_slow_parent = False
		return {'FINISHED'}
