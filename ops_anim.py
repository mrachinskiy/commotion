import bpy
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty, BoolProperty


class ANIM_OT_Commotion_Animation_Link(Operator):
	"""Link animation from active to selected objects"""
	bl_label = 'Link'
	bl_idname = 'anim.commotion_animation_link'
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
					if ob.data and ob.data.shape_keys:
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


class ANIM_OT_Commotion_Animation_Copy(Operator):
	"""Copy animation from active to selected objects (can also use this to unlink animation)"""
	bl_label = 'Copy'
	bl_idname = 'anim.commotion_animation_copy'
	bl_options = {'INTERNAL'}

	ad_type = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

	def execute(self, context):
		obj = context.active_object
		obs = context.selected_objects

		if 'SHAPE_KEYS' in self.ad_type:
			action = obj.data.shape_keys.animation_data.action
			for ob in obs:
				if ob.data and ob.data.shape_keys:
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


class ANIM_OT_Commotion_FCurves_To_NLA(Operator):
	"""Convert F-Curves to NLA strips"""
	bl_label = 'F-Curves to Strips'
	bl_idname = 'nla.commotion_fcurves_to_nla'
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
				if ob.data and ob.data.shape_keys:
					ad = ob.data.shape_keys.animation_data
					strips_create(ad)

		elif 'OBJECT' in self.ad_type:
			for ob in context.selected_objects:
				if ob.animation_data:
					ad = ob.animation_data
					strips_create(ad)

		return {'FINISHED'}


class ANIM_OT_Commotion_NLA_To_FCurves(Operator):
	"""Convert strips back to F-Curves"""
	bl_label = 'Strips to F-Curves'
	bl_idname = 'anim.commotion_nla_to_fcurves'
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


class NLA_OT_Commotion_Sync_Length(Operator):
	"""Synchronize strip length for selected objects"""
	bl_label = 'Sync Length'
	bl_idname = 'nla.commotion_sync_length'
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


class AnimationOffset:
	bl_label = 'Offset Animation'
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	ad_type = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})
	prop_pfx = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

	offset = FloatProperty(name='Frame Offset', description='Frame step for animation offset', default=1, min=0, step=10, precision=3)
	threshold = FloatProperty(name='Threshold', description='Number of objects to animate per frame step', default=1, min=1, step=100, precision=0)
	reverse = BoolProperty(name='Reverse', description='Reverse animation offset')

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

	def draw(self, context):
		layout = self.layout

		layout.prop(self, 'offset')
		layout.prop(self, 'threshold')
		layout.prop(self, 'reverse')

	def preset_add(self, ob):
		ob['commotion_preset'] = {
			'offset': self.offset,
			'threshold': self.threshold,
			'reverse': self.reverse,
			'sort_options': self.sort_options,
			'group_objects': self.group_objects,
			'group_targets': self.group_targets,
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


class ANIM_OT_Commotion_Offset_Cursor(Operator, AnimationOffset):
	"""Offset animation from 3D cursor for selected objects (won't work if F-Curves are linked)"""
	bl_idname = 'anim.commotion_offset_cursor'

	def execute(self, context):
		dist = {}
		for ob in context.selected_objects:
			distance = (self.cursor - (ob.location + ob.delta_location)).length
			dist[ob] = distance

		self.offset_simple(dist)

		return {'FINISHED'}


class ANIM_OT_Commotion_Offset_Name(Operator, AnimationOffset):
	"""Offset animation by object name for selected objects (won't work if F-Curves are linked)"""
	bl_idname = 'anim.commotion_offset_name'

	def execute(self, context):
		dist = {}
		for ob in context.selected_objects:
			dist[ob] = ob.name

		self.offset_simple(dist)

		return {'FINISHED'}


class ANIM_OT_Commotion_Offset_Multitarget(Operator, AnimationOffset):
	"""Offset animation from multiple targets for selected objects (won't work if F-Curves are linked)"""
	bl_idname = 'anim.commotion_offset_multitarget'

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
