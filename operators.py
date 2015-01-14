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

import bpy
from bpy.types import Operator
from . import helpers


class OT_SHAPE_LIST_REFRESH(Operator):
	"""Refresh the list of active shape keys"""
	bl_idname = "scene.shape_list_refresh"
	bl_label = "Refresh Shape List"

	def execute(self, context):
		sce = context.scene
		spl = sce.spl
		
		if hasattr(sce, 'spl'):
			for sps in spl:
				spl.remove(0)
		
		i=0
		for kb in context.active_object.data.shape_keys.key_blocks:
			spl.add()
			spl[i].name = kb.name
			spl[i].index = i
			i+=1
		
		return {'FINISHED'}


class OT_AUTO_KEYFRAMES(Operator):
	"""Automatic keyframes for Evaluation Time property"""
	bl_idname = "scene.auto_keyframes"
	bl_label = "Auto Keyframes"

	def execute(self, context):
		frame = context.scene.frame_current
		obs = context.selected_objects

		for ob in obs:
			key = ob.data.shape_keys

			key.eval_time = int(key.key_blocks[1].frame)
			key.keyframe_insert(data_path="eval_time", frame=frame)
			key.eval_time = int(key.key_blocks[-1].frame)
			key.keyframe_insert(data_path="eval_time", frame=frame+20)

		return {'FINISHED'}












class OT_SK_FCURVES_LINK(Operator):
	"""Link animation to selected objects"""
	bl_idname = "scene.sk_fcurves_link"
	bl_label = "Link Animation"

	def execute(self, context):
		mode = ['SHAPE_KEYS', 'FCURVES']

		helpers.link_to_active(mode)

		return {'FINISHED'}


class OT_SK_FCURVES_COPY(Operator):
	"""Copy animation to selected objects"""
	bl_idname = "scene.sk_fcurves_copy"
	bl_label = "Copy Animation"

	def execute(self, context):
		mode = ['SHAPE_KEYS']
		
		helpers.copy_to_selected(mode)

		return {'FINISHED'}


class OT_SK_FCURVES_OFFSET_CURSOR(Operator):
	"""Animation offset from Cursor"""
	bl_idname = "scene.sk_fcurves_offset_cursor"
	bl_label = "Offset Animation"

	def execute(self, context):
		como = context.scene.como
		offset = como.sk_fcurves_offset
		threshold = como.sk_fcurves_threshold
		mode = ['SHAPE_KEYS', 'FCURVES']

		helpers.offset_cursor(offset, threshold, mode)

		return {'FINISHED'}


class OT_SK_FCURVES_OFFSET_MULTITARGET(Operator):
	"""Animation offset from multiple targets"""
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
		mode = ['SHAPE_KEYS', 'FCURVES']

		helpers.offset_multitarget(objects, targets, offset, threshold, mode)

		return {'FINISHED'}


class OT_SK_FCURVES_OFFSET_NAME(Operator):
	"""Animation offset by Name"""
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

		helpers.offset_name(offset, threshold, mode)

		return {'FINISHED'}















class OT_SK_NLA_CREATE(Operator):
	"""Create NLA strips from object animation"""
	bl_idname = "scene.sk_nla_create"
	bl_label = "Create NLA Strips"

	def execute(self, context):
		mode = ['SHAPE_KEYS']

		helpers.create_strips(mode)

		return {'FINISHED'}


class OT_SK_NLA_TO_FCURVES(Operator):
	"""Convert NLA strips to F-Curves"""
	bl_idname = "scene.sk_nla_to_fcurves"
	bl_label = "Strips to F-Curves"

	def execute(self, context):
		mode = ['SHAPE_KEYS']

		helpers.strips_to_fcurves(mode)

		return {'FINISHED'}


class OT_SK_NLA_SYNC_LENGTH(Operator):
	"""Sync length of NLA strips"""
	bl_idname = "scene.sk_nla_sync_length"
	bl_label = "Sync Length"

	def execute(self, context):
		mode = ['SHAPE_KEYS']

		helpers.sync_len(mode)

		return {'FINISHED'}


class OT_SK_NLA_LINK_TO_ACTIVE(Operator):
	"""Link strip's action to active object"""
	bl_idname = "scene.sk_nla_link_to_active"
	bl_label = "Link Strips"

	def execute(self, context):
		mode = ['SHAPE_KEYS', 'NLA']

		helpers.link_to_active(mode)

		return {'FINISHED'}


class OT_SK_NLA_OFFSET_CURSOR(Operator):
	"""Automatic offset of NLA strips from cursor"""
	bl_idname = "scene.sk_nla_offset_cursor"
	bl_label = "Offset Strips"

	def execute(self, context):
		como = context.scene.como
		offset = como.sk_nla_offset
		threshold = como.sk_nla_threshold
		mode = ['SHAPE_KEYS', 'NLA']

		helpers.offset_cursor(offset, threshold, mode)

		return {'FINISHED'}


class OT_SK_NLA_OFFSET_MULTITARGET(Operator):
	"""Automatic multi offset of NLA strips"""
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
		mode = ['SHAPE_KEYS', 'NLA']

		helpers.offset_multitarget(objects, targets, offset, threshold, mode)

		return {'FINISHED'}


class OT_SK_NLA_OFFSET_NAME(Operator):
	"""Animation offset by Name"""
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

		helpers.offset_name(offset, threshold, mode)

		return {'FINISHED'}

















class OT_SK_DRIVER_SET(Operator):
	"""Set driver with distance varable for selected objects. """ \
	"""Active object would be considered as target for distance variable."""
	bl_idname = "scene.sk_driver_set"
	bl_label = "Set Distance Driver"

	def execute(self, context):
		obj = context.active_object
		obs = context.selected_objects

		try:
			for ob in obs:
				if ob != obj:
					key = ob.data.shape_keys
					kb = int(key.key_blocks[1].frame)
					kb_last = str(int(key.key_blocks[-1].frame) + 5)
					
					key.driver_add("eval_time")
					
					fcus = ob.data.shape_keys.animation_data.drivers
					for fcu in fcus:
						if fcu.data_path == 'eval_time':
							
							drv = fcu.driver
							drv.type = 'SCRIPTED'
							drv.expression = kb_last + '-(dist*3/sx)'
							drv.show_debug_info = True

							var = drv.variables.new()
							var.name = 'dist'
							var.type = 'LOC_DIFF'
							var.targets[0].id = ob
							var.targets[1].id = obj
						
							var = drv.variables.new()
							var.name = 'sx'
							var.type = 'SINGLE_PROP'
							var.targets[0].id = obj
							var.targets[0].data_path = 'scale[0]'

							if fcu.modifiers:
								fcu.modifiers.remove(fcu.modifiers[0])

							fcu.keyframe_points.insert(0, kb)
							fcu.keyframe_points.insert(kb, kb)
							fcu.keyframe_points.insert(kb + 10, kb + 10)

							fcu.extrapolation = 'LINEAR'
							for kp in fcu.keyframe_points:
								kp.interpolation = 'LINEAR'
		except:
			self.report({'ERROR'}, "Object has no Shape Keys")

		return {'FINISHED'}


class OT_SK_TARGETS_REMAP(Operator):
	"""Remap drivers target property"""
	bl_idname = "scene.sk_targets_remap"
	bl_label = "Remap Targets"

	def execute(self, context):
		obs = context.selected_objects

		for ob in obs:
			fcus = ob.data.shape_keys.animation_data.drivers
			for fcu in fcus:
				if fcu.data_path == 'eval_time':
					for var in fcu.driver.variables:
						if var.name == 'dist':
							var.targets[0].id = ob

		return {'FINISHED'}


class OT_SK_EXPRESSION_COPY(Operator):
	"""Copy driver expression to selected"""
	bl_idname = "scene.sk_expression_copy"
	bl_label = "Copy To Selected"

	def execute(self, context):
		obj = context.active_object
		obs = context.selected_objects

		active_fcus = obj.data.shape_keys.animation_data.drivers
		for active_fcu in active_fcus:
			if active_fcu.data_path == 'eval_time':
				for ob in obs:
					fcus = ob.data.shape_keys.animation_data.drivers
					for fcu in fcus:
						if fcu.data_path == 'eval_time':
							fcu.driver.expression = active_fcu.driver.expression

		return {'FINISHED'}


class OT_SK_DRIVER_FUNC_REG(Operator):
	"""Register driver function and update dependencies (required for “Distance Trigger” to work)"""
	bl_idname = "scene.sk_driver_func_reg"
	bl_label = "Register driver function"

	def execute(self, context):
		obs = context.scene.objects
		bpy.app.driver_namespace['dist_trigger'] = helpers.dist_trigger

		for ob in obs:
			if (ob.data and ob.data.shape_keys and
							ob.data.shape_keys.animation_data and
							ob.data.shape_keys.animation_data.drivers):
				fcus = ob.data.shape_keys.animation_data.drivers
				for fcu in fcus:
					if fcu.data_path == 'eval_time':
						fcu.driver.expression = fcu.driver.expression

		return {'FINISHED'}


class OT_SK_EVAL_TIME_RESET(Operator):
	"""Reset Evaluation Time property of selected objects to 0"""
	bl_idname = "scene.sk_eval_time_reset"
	bl_label = "Reset Eval Time"

	def execute(self, context):
		obs = context.selected_objects

		for ob in obs:
			ob.data.shape_keys.eval_time = 0

		return {'FINISHED'}


class OT_SK_EXPRESSION_FUNC_SET(Operator):
	"""Set special type of expression on selected objects"""
	bl_idname = "scene.sk_expression_func_set"
	bl_label = "Set Function Expression"

	def execute(self, context):
		como = context.scene.como
		expr = como.sk_drivers_expression_func
		obs = context.selected_objects

		for ob in obs:
			func_expr = "dist_trigger("+expr+", '"+ob.name+"')"
			fcus = ob.data.shape_keys.animation_data.drivers
			for fcu in fcus:
				if fcu.data_path == 'eval_time':
					fcu.driver.expression = func_expr

		return {'FINISHED'}












class OT_OB_FCURVES_LINK(Operator):
	"""Link animation to selected objects"""
	bl_idname = "scene.ob_fcurves_link"
	bl_label = "Link Animation"

	def execute(self, context):
		mode = ['OBJECT', 'FCURVES']

		helpers.link_to_active(mode)

		return {'FINISHED'}


class OT_OB_FCURVES_COPY(Operator):
	"""Link animation to selected objects"""
	bl_idname = "scene.ob_fcurves_copy"
	bl_label = "Copy Animation"

	def execute(self, context):
		mode = ['OBJECT']
		
		helpers.copy_to_selected(mode)
			
		return {'FINISHED'}


class OT_OB_FCURVES_OFFSET_CURSOR(Operator):
	"""Animation offset from Cursor"""
	bl_idname = "scene.ob_fcurves_offset_cursor"
	bl_label = "Offset Animation"

	def execute(self, context):
		como = context.scene.como
		offset = como.ob_fcurves_offset
		threshold = como.ob_fcurves_threshold
		mode = ['OBJECT', 'FCURVES']

		helpers.offset_cursor(offset, threshold, mode)

		return {'FINISHED'}


class OT_OB_FCURVES_OFFSET_MULTITARGET(Operator):
	"""Animation offset from multiple targets"""
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
		mode = ['OBJECT', 'FCURVES']

		helpers.offset_multitarget(objects, targets, offset, threshold, mode)

		return {'FINISHED'}


class OT_OB_FCURVES_OFFSET_NAME(Operator):
	"""Animation offset by Name"""
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

		helpers.offset_name(offset, threshold, mode)

		return {'FINISHED'}







class OT_OB_NLA_CREATE(Operator):
	"""Create NLA strips from object animation"""
	bl_idname = "scene.ob_nla_create"
	bl_label = "Create NLA Strips"

	def execute(self, context):
		mode = ['OBJECT']

		helpers.create_strips(mode)

		return {'FINISHED'}


class OT_OB_NLA_TO_FCURVES(Operator):
	"""Convert NLA strips to F-Curves"""
	bl_idname = "scene.ob_nla_to_fcurves"
	bl_label = "Strips to F-Curves"

	def execute(self, context):
		mode = ['OBJECT']

		helpers.strips_to_fcurves(mode)

		return {'FINISHED'}


class OT_OB_NLA_SYNC_LENGTH(Operator):
	"""Sync length of NLA strips"""
	bl_idname = "scene.ob_nla_sync_length"
	bl_label = "Sync Length"

	def execute(self, context):
		mode = ['OBJECT']

		helpers.sync_len(mode)

		return {'FINISHED'}


class OT_OB_NLA_LINK_TO_ACTIVE(Operator):
	"""Link strip's action to active object"""
	bl_idname = "scene.ob_nla_link_to_active"
	bl_label = "Link Strips"

	def execute(self, context):
		mode = ['OBJECT', 'NLA']

		helpers.link_to_active(mode)

		return {'FINISHED'}


class OT_OB_NLA_OFFSET_CURSOR(Operator):
	"""Automatic offset of NLA strips from cursor"""
	bl_idname = "scene.ob_nla_offset_cursor"
	bl_label = "Offset Strips"

	def execute(self, context):
		como = context.scene.como
		offset =  como.ob_nla_offset
		threshold =  como.ob_nla_threshold
		mode = ['OBJECT', 'NLA']

		helpers.offset_cursor(offset, threshold, mode)

		return {'FINISHED'}


class OT_OB_NLA_OFFSET_MULTITARGET(Operator):
	"""Automatic multi offset of NLA strips"""
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
		mode = ['OBJECT', 'NLA']

		helpers.offset_multitarget(objects, targets, offset, threshold, mode)

		return {'FINISHED'}


class OT_OB_NLA_OFFSET_NAME(Operator):
	"""Animation offset by Name"""
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

		helpers.offset_name(offset, threshold, mode)

		return {'FINISHED'}








class OT_SLOW_PARENT_OFFSET(Operator):
	"""Offset Slow Parent property with delay factor value for selected objects"""
	bl_idname = "scene.slow_parent_offset"
	bl_label = "Offset Slow Parent"

	def execute(self, context):
		offset = context.scene.como.slow_parent_offset

		helpers.offset_parent(offset)

		return {'FINISHED'}