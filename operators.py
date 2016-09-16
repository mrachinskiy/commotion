import bpy
from re import sub
from bpy.types import Operator
from bpy.props import (
	StringProperty,
	FloatProperty,
	BoolProperty,
	)


"""
Cannot inherit properties from a base class,
because property order will be random every time in operator redo UI
"""
_offset = FloatProperty(name='Frame Offset', description='Frame step for animation offset', default=1, min=0, step=10, precision=3)
_threshold = FloatProperty(name='Threshold', description='Number of objects to animate per frame step', default=1, min=1, step=100, precision=0)
_reverse = BoolProperty(name='Reverse', description='Reverse animation offset')


class SK_COLL_REFRESH(Operator):
	"""Refresh shape key list for active object"""
	bl_label = 'Refresh Shape List'
	bl_idname = 'commotion.sk_coll_refresh'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		skcoll = context.scene.commotion_skcoll

		skcoll.clear()

		i = 0
		for kb in context.active_object.data.shape_keys.key_blocks:
			skcoll.add()
			skcoll[i].name = kb.name
			skcoll[i].index = i
			i += 1

		return {'FINISHED'}


class SK_INTERPOLATION_SET(Operator):
	"""Set interpolation type for selected shape keys (Linear, Cardinal, Catmull-Rom, BSpline)"""
	bl_label = 'Set Interpolation'
	bl_idname = 'commotion.sk_interpolation_set'
	bl_options = {'INTERNAL'}

	intr = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

	def execute(self, context):
		skcoll = context.scene.commotion_skcoll

		for ob in context.selected_objects:

			try:
				sk = ob.data.shape_keys
			except:
				continue

			for kb in skcoll:
				if kb.selected:
					sk.key_blocks[kb.index].interpolation = self.intr

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


class ANIMATION_LINK(Operator):
	"""Link animation from active to selected objects"""
	bl_label = 'Link'
	bl_idname = 'commotion.animation_link'
	bl_options = {'INTERNAL'}

	ad_type = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

	def execute(self, context):

		def link_strips(ob_strip, obj_strip):
			obj_fstart = obj_strip.action_frame_start
			obj_fend = obj_strip.action_frame_end
			ob_strip.action = obj_strip.action
			ob_strip.action_frame_start = obj_fstart
			ob_strip.action_frame_end = obj_fend

		obj = context.active_object
		obs = context.selected_objects

		if 'FCURVES' in self.ad_type:

			if 'SHAPE_KEYS' in self.ad_type:
				action = obj.data.shape_keys.animation_data.action
				for ob in obs:
					if (ob.data and ob.data.shape_keys):
						sk = ob.data.shape_keys
						if sk.animation_data:
							sk.animation_data.action = action
						else:
							sk.animation_data_create()
							sk.animation_data.action = action

			elif 'OBJECT' in self.ad_type:
				action = obj.animation_data.action
				for ob in obs:
					if ob.animation_data:
						ob.animation_data.action = action
					else:
						ob.animation_data_create()
						ob.animation_data.action = action

		elif 'NLA' in self.ad_type:

			if 'SHAPE_KEYS' in self.ad_type:
				obj_strip = obj.data.shape_keys.animation_data.nla_tracks[0].strips[0]
				for ob in obs:
					try:
						ob_strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]
						link_strips(ob_strip, obj_strip)
					except:
						continue

			elif 'OBJECT' in self.ad_type:
				obj_strip = obj.animation_data.nla_tracks[0].strips[0]
				for ob in obs:
					try:
						ob_strip = ob.animation_data.nla_tracks[0].strips[0]
						link_strips(ob_strip, obj_strip)
					except:
						continue

		return {'FINISHED'}


class ANIMATION_COPY(Operator):
	"""Copy animation from active to selected objects (can also use this to unlink animation)"""
	bl_label = 'Copy'
	bl_idname = 'commotion.animation_copy'
	bl_options = {'INTERNAL'}

	ad_type = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

	def execute(self, context):
		obj = context.active_object
		obs = context.selected_objects

		if 'SHAPE_KEYS' in self.ad_type:
			action = obj.data.shape_keys.animation_data.action
			for ob in obs:
				if (ob.data and ob.data.shape_keys):
					if ob.data.shape_keys.animation_data:
						ob.data.shape_keys.animation_data.action = action.copy()
					else:
						ob.data.shape_keys.animation_data_create()
						ob.data.shape_keys.animation_data.action = action.copy()

		elif 'OBJECT' in self.ad_type:
			action = obj.animation_data.action
			for ob in obs:
				if ob.animation_data:
					ob.animation_data.action = action.copy()
				else:
					ob.animation_data_create()
					ob.animation_data.action = action.copy()

		return {'FINISHED'}


class NLA_TO_STRIPS(Operator):
	"""Convert F-Curves to NLA strips"""
	bl_label = 'F-Curves to Strips'
	bl_idname = 'commotion.nla_to_strips'
	bl_options = {'INTERNAL'}

	ad_type = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

	def execute(self, context):

		def strips_create(ad):
			fstart = ad.action.frame_range[0]
			if not ad.nla_tracks:
				ad.nla_tracks.new()
			ad.nla_tracks[0].strips.new('name', fstart, ad.action)
			ad.action = None

		if 'SHAPE_KEYS' in self.ad_type:
			for ob in context.selected_objects:
				if (ob.data and ob.data.shape_keys):
					ad = ob.data.shape_keys.animation_data
					strips_create(ad)

		elif 'OBJECT' in self.ad_type:
			for ob in context.selected_objects:
				if ob.animation_data:
					ad = ob.animation_data
					strips_create(ad)

		return {'FINISHED'}


class NLA_TO_FCURVES(Operator):
	"""Convert strips back to F-Curves"""
	bl_label = 'Strips to F-Curves'
	bl_idname = 'commotion.nla_to_fcurves'
	bl_options = {'INTERNAL'}

	ad_type = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

	def execute(self, context):

		def remove_nla_track(ad):
			trks = ad.nla_tracks
			ad.action = trks[0].strips[0].action
			trks.remove(trks[0])

		obs = context.selected_objects

		if 'SHAPE_KEYS' in self.ad_type:
			for ob in obs:
				try:
					ad = ob.data.shape_keys.animation_data
					remove_nla_track(ad)
				except:
					continue

		elif 'OBJECT' in self.ad_type:
			for ob in obs:
				try:
					ad = ob.animation_data
					remove_nla_track(ad)
				except:
					continue

		return {'FINISHED'}


class NLA_SYNC_LENGTH(Operator):
	"""Synchronize strip length for selected objects"""
	bl_label = 'Sync Length'
	bl_idname = 'commotion.nla_sync_length'
	bl_options = {'INTERNAL'}

	ad_type = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

	def execute(self, context):
		obs = context.selected_objects

		if 'SHAPE_KEYS' in self.ad_type:
			for ob in obs:
				try:
					strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]
					strip.action_frame_end = (strip.action_frame_start + strip.action.frame_range[1] - 1)
				except:
					continue

		elif 'OBJECT' in self.ad_type:
			for ob in obs:
				try:
					strip = ob.animation_data.nla_tracks[0].strips[0]
					strip.action_frame_end = (strip.action_frame_start + strip.action.frame_range[1] - 1)
				except:
					continue

		return {'FINISHED'}


class AnimationOffset():
	bl_label = 'Offset Animation'
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	ad_type = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})
	prop_pfx = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

	def __init__(self):
		scene = bpy.context.scene
		props = scene.commotion
		self.frame = scene.frame_current
		self.cursor = scene.cursor_location
		self.offset        = getattr(props, self.prop_pfx + '_offset')
		self.threshold     = getattr(props, self.prop_pfx + '_threshold')
		self.reverse       = getattr(props, self.prop_pfx + '_reverse')
		self.sort_options  = getattr(props, self.prop_pfx + '_sort_options')
		self.group_objects = getattr(props, self.prop_pfx + '_group_objects')
		self.group_targets = getattr(props, self.prop_pfx + '_group_targets')

	def preset_add(self, ob):
		ob['commotion_preset'] = {
			'offset'        : self.offset,
			'threshold'     : self.threshold,
			'reverse'       : self.reverse,
			'sort_options'  : self.sort_options,
			'group_objects' : self.group_objects,
			'group_targets' : self.group_targets,
			}

	def offset_simple(self, dist):
		dist = sorted(dist, key=dist.get, reverse=self.reverse)

		i = 0
		i2 = self.threshold
		for ob in dist:

			if self.ad_offset(ob, i) is False:
				continue

			self.preset_add(ob)

			if i2 > 1:
				if i2 <= (dist.index(ob) + 1):
					i2 += self.threshold
					i += self.offset
			else:
				i += self.offset

	def ad_offset(self, ob, i):
		try:

			if 'FCURVES' in self.ad_type:

				if 'SHAPE_KEYS' in self.ad_type:
					fcus = ob.data.shape_keys.animation_data.action.fcurves

				elif 'OBJECT' in self.ad_type:
					fcus = ob.animation_data.action.fcurves

				for fcu in fcus:
					fcu_range = fcu.range()[0]
					for kp in fcu.keyframe_points:
						kp.co[0] = kp.co[0] + self.frame + i - fcu_range
						kp.handle_left[0] = kp.handle_left[0] + self.frame + i - fcu_range
						kp.handle_right[0] = kp.handle_right[0] + self.frame + i - fcu_range

			elif 'NLA' in self.ad_type:

				if 'SHAPE_KEYS' in self.ad_type:
					strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]

				elif 'OBJECT' in self.ad_type:
					strip = ob.animation_data.nla_tracks[0].strips[0]

				strip.frame_end = self.frame - 1 + i + strip.frame_end
				strip.frame_start = self.frame + i
				strip.scale = 1

		except:
			return False


class ANIMATION_OFFSET_CURSOR(AnimationOffset, Operator):
	"""Offset animation from 3D cursor for selected objects (won't work if F-Curves are linked)"""
	bl_idname = 'commotion.animation_offset_cursor'

	offset = _offset
	threshold = _threshold
	reverse = _reverse

	def execute(self, context):
		dist = {}
		for ob in context.selected_objects:
			distance = (self.cursor - (ob.location + ob.delta_location)).length
			dist[ob] = distance

		self.offset_simple(dist)

		return {'FINISHED'}


class ANIMATION_OFFSET_NAME(AnimationOffset, Operator):
	"""Offset animation by object name for selected objects (won't work if F-Curves are linked)"""
	bl_idname = 'commotion.animation_offset_name'

	offset = _offset
	threshold = _threshold
	reverse = _reverse

	def execute(self, context):
		dist = {}
		for ob in context.selected_objects:
			dist[ob] = ob.name

		self.offset_simple(dist)

		return {'FINISHED'}


class ANIMATION_OFFSET_MULTITARGET(AnimationOffset, Operator):
	"""Offset animation from multiple targets for selected objects (won't work if F-Curves are linked)"""
	bl_idname = 'commotion.animation_offset_multitarget'

	offset = _offset
	threshold = _threshold
	reverse = _reverse

	def execute(self, context):
		objects = bpy.data.groups[self.group_objects].objects
		targets = bpy.data.groups[self.group_targets].objects

		obs = {}
		for ob in objects:
			targs = {}
			for t in targets:
				distance = (t.location - (ob.location + ob.delta_location)).length
				targs[distance] = t
				dist = sorted(targs)[0]
			obs[ob] = [dist, targs[dist]]

		for t in targets:
			obs_thold = []
			i = 0
			i2 = self.threshold

			obs_sorted = sorted(obs, key=obs.get, reverse=self.reverse)

			for ob in obs_sorted:
				if obs[ob][1] == t:

					if self.ad_offset(ob, i) is False:
						continue

					self.preset_add(ob)

					if i2 > 1:
						obs_thold.append(ob)
						if i2 <= (obs_thold.index(ob) + 1):
							i += self.offset
							i2 += self.threshold
					else:
						i += self.offset

		return {'FINISHED'}


class OB_SLOW_PARENT_OFFSET(Operator):
	"""Offset Slow Parent property for selected objects"""
	bl_label = 'Offset Slow Parent'
	bl_idname = 'commotion.ob_slow_parent_offset'
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	offset = FloatProperty(name='Offset Factor', default=1, min=0, step=10, precision=1)

	def execute(self, context):
		dist = {}
		for ob in context.selected_objects:
			if ob.parent:
				distance = (ob.parent.location - (ob.location + ob.delta_location + ob.parent.location)).length
				dist[ob] = distance

		dist = sorted(dist, key=dist.get)

		i = self.offset
		for ob in dist:
			ob.use_slow_parent = True
			ob.slow_parent_offset = i
			i += self.offset

		return {'FINISHED'}


class SK_DRIVERS_DISTANCE_SET(Operator):
	"""Set distance driver for absolute shape keys on selected objects. """ \
	"""If active object is not an Empty, then a new Empty object will be created """ \
	"""as a target for driver's distance variable."""
	bl_label = 'Set Distance Driver'
	bl_idname = 'commotion.sk_drivers_distance_set'

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
			if (ob.data and ob.data.shape_keys):

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


class SK_DRIVERS_EXPRESSION_COPY(Operator):
	"""Copy driver's expression from active to selected objects"""
	bl_label = 'Copy'
	bl_idname = 'commotion.sk_drivers_expression_copy'
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


class SK_DRIVERS_TARGET_REMAP(Operator):
	"""Remap driver's distance variable target property from original to current object. """ \
	"""Useful after Make Single User on linked objects, when distance variable on all objects points only to one object."""
	bl_idname = 'commotion.sk_drivers_target_remap'
	bl_label = 'Remap Target'

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


class SK_DRIVERS_FUNCTION_REGISTER(Operator):
	"""Register Distance Trigger driver function.\n""" \
	"""Use it every time when open blend file, otherwise Distance Trigger drivers won't work."""
	bl_label = 'Register Driver Function'
	bl_idname = 'commotion.sk_drivers_function_register'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		bpy.app.driver_namespace['dis_trig'] = dis_trig

		for sk in bpy.data.shape_keys:
			if (sk.animation_data and sk.animation_data.drivers):
				fcu = sk.animation_data.drivers.find('eval_time')
				fcu.driver.expression = fcu.driver.expression

		return {'FINISHED'}


class SK_DRIVERS_EVAL_TIME_RESET(Operator):
	"""Reset Evaluation Time property for selected objects to 0"""
	bl_label = 'Reset Evaluation Time'
	bl_idname = 'commotion.sk_drivers_eval_time_reset'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		for ob in context.selected_objects:
			try:
				ob.data.shape_keys.eval_time = 0
			except:
				pass

		return {'FINISHED'}


class SK_DRIVERS_FUNC_EXPRESSION_GET(Operator):
	"""Get expression from active object"""
	bl_label = 'Get Expression'
	bl_idname = 'commotion.sk_drivers_func_expression_get'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		fcu = context.active_object.data.shape_keys.animation_data.drivers.find('eval_time')
		expression = fcu.driver.expression
		sanitized = sub(r'dis_trig\((.+),.+\)', r'\1', expression)
		context.scene.commotion.sk_drivers_expression_func = sanitized
		return {'FINISHED'}


class SK_DRIVERS_FUNC_EXPRESSION_SET(Operator):
	"""Set distance trigger expression for selected objects"""
	bl_label = 'Set Expression'
	bl_idname = 'commotion.sk_drivers_func_expression_set'
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


class PRESET_APPLY(Operator):
	"""Apply preset from active object"""
	bl_label = 'Apply Preset'
	bl_idname = 'commotion.preset_apply'
	bl_options = {'INTERNAL'}

	prop_pfx = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

	def execute(self, context):
		props = context.scene.commotion
		obj = context.active_object

		if 'commotion_preset' in obj:
			val = obj['commotion_preset']
			setattr(props, self.prop_pfx + '_offset',        val['offset'])
			setattr(props, self.prop_pfx + '_threshold',     val['threshold'])
			setattr(props, self.prop_pfx + '_reverse',       val['reverse'])
			setattr(props, self.prop_pfx + '_sort_options',  val['sort_options'])
			setattr(props, self.prop_pfx + '_group_objects', val['group_objects'])
			setattr(props, self.prop_pfx + '_group_targets', val['group_targets'])
		else:
			self.report({'WARNING'}, 'Active object has no preset')

		return {'FINISHED'}


class AddToGroup:
	bl_label = 'Add to group'
	bl_options = {'INTERNAL'}

	prop_pfx = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

	def execute(self, context):
		group_name = bpy.data.groups.new(self.group).name
		bpy.ops.object.group_link(group=group_name)
		bpy.ops.group.objects_add_active()

		setattr(context.scene.commotion, self.prop_pfx + self.prop_suf, group_name)

		return {'FINISHED'}


class ADD_TO_GROUP_OBJECTS(AddToGroup, Operator):
	"""Add selected objects to Objects group for multi-offset"""
	bl_idname = 'commotion.add_to_group_objects'
	group = 'Objects'
	prop_suf = '_group_objects'


class ADD_TO_GROUP_TARGETS(AddToGroup, Operator):
	"""Add selected objects to Targets group for multi-offset"""
	bl_idname = 'commotion.add_to_group_targets'
	group = 'Targets'
	prop_suf = '_group_targets'


class OB_SLOW_PARENT_TOGGLE(Operator):
	"""Toggle Slow Parent property on or off for selected objects"""
	bl_label = 'Toggle Slow Parent'
	bl_idname = 'commotion.ob_slow_parent_toggle'
	bl_options = {'INTERNAL'}

	off = BoolProperty(options={'HIDDEN', 'SKIP_SAVE'})

	def execute(self, context):
		obs = context.selected_objects

		if self.off:
			for ob in obs:
				if ob.parent:
					ob.use_slow_parent = False
		else:
			for ob in obs:
				if ob.parent:
					ob.use_slow_parent = True

		return {'FINISHED'}
