from re import sub

import bpy
from bpy.types import Operator


class ANIM_OT_Commotion_SK_Driver_Distance_Set(Operator):
	"""Set distance driver for absolute shape keys on selected objects. """ \
	"""If active object is not an Empty, then a new Empty object will be created """ \
	"""as a target for driver's distance variable."""
	bl_label = 'Set Distance Driver'
	bl_idname = 'anim.commotion_sk_driver_distance_set'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		obj = context.active_object

		if obj.type != 'EMPTY':
			scene = context.scene
			empty = bpy.data.objects.new('Distance Target', None)
			scene.objects.link(empty)
			empty.location = scene.cursor_location
			empty.select = True
			empty.empty_draw_type = 'SPHERE'
		else:
			empty = obj

		for ob in context.selected_objects:
			if ob.data and ob.data.shape_keys:

				sk = ob.data.shape_keys

				sk.driver_remove('eval_time')

				kb = int(sk.key_blocks[1].frame)
				kb_last = str(int(sk.key_blocks[-1].frame) + 5)

				sk.driver_add('eval_time')

				fcu = ob.data.shape_keys.animation_data.drivers.find('eval_time')

				drv = fcu.driver
				drv.type = 'SCRIPTED'
				drv.expression = kb_last + ' - (dis * 3 / sc)'
				drv.show_debug_info = True

				var = drv.variables.new()
				var.name = 'dis'
				var.type = 'LOC_DIFF'
				var.targets[0].id = ob
				var.targets[1].id = empty

				var = drv.variables.new()
				var.name = 'sc'
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


class ANIM_OT_Commotion_SK_Driver_Expression_Copy(Operator):
	"""Copy driver expression from active to selected objects"""
	bl_label = 'Copy'
	bl_idname = 'anim.commotion_sk_driver_expression_copy'
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


class ANIM_OT_Commotion_SK_Driver_Target_Remap(Operator):
	"""Remap driver's distance variable target property from original to current object. """ \
	"""Useful after Make Single User on linked objects, when distance variable on all objects points only to one object."""
	bl_idname = 'anim.commotion_sk_driver_target_remap'
	bl_label = 'Remap Target'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		for ob in context.selected_objects:
			try:
				fcu = ob.data.shape_keys.animation_data.drivers.find('eval_time')
				var = fcu.driver.variables['dis']
				var.targets[0].id = ob
			except:
				continue

		return {'FINISHED'}


def dis_trig(var, name):
	scene = bpy.context.scene
	etm = scene.objects[name].data.shape_keys.eval_time

	if scene.frame_current <= scene.frame_start:
		etm = 0

	elif var > etm:
		etm = var

	return etm


class ANIM_OT_Commotion_SK_Driver_Function_Register(Operator):
	"""Register Distance Trigger driver function.\n""" \
	"""Use it every time when open blend file, otherwise Distance Trigger drivers won't work."""
	bl_label = 'Register Driver Function'
	bl_idname = 'anim.commotion_sk_driver_function_register'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		bpy.app.driver_namespace['dis_trig'] = dis_trig

		for sk in bpy.data.shape_keys:
			if sk.animation_data and sk.animation_data.drivers:
				fcu = sk.animation_data.drivers.find('eval_time')
				fcu.driver.expression = fcu.driver.expression

		return {'FINISHED'}


class ANIM_OT_Commotion_SK_Driver_Func_Expression_Get(Operator):
	"""Get expression from active object"""
	bl_label = 'Get Expression'
	bl_idname = 'anim.commotion_sk_driver_func_expression_get'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		fcu = context.active_object.data.shape_keys.animation_data.drivers.find('eval_time')
		expression = fcu.driver.expression
		sanitized = sub(r'dis_trig\((.+),.+\)', r'\1', expression)
		context.scene.commotion.sk_drivers_expression_func = sanitized
		return {'FINISHED'}


class ANIM_OT_Commotion_SK_Driver_Func_Expression_SET(Operator):
	"""Set distance trigger expression for selected objects"""
	bl_label = 'Set Expression'
	bl_idname = 'anim.commotion_sk_driver_func_expression_set'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		props = context.scene.commotion
		expr = props.sk_drivers_expression_func

		for ob in context.selected_objects:
			try:
				fcu = ob.data.shape_keys.animation_data.drivers.find('eval_time')
				fcu.driver.expression = 'dis_trig(%s, "%s")' % (expr, ob.name)
			except:
				pass

		return {'FINISHED'}
