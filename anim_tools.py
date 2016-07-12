import bpy


# Animation link and copy tools


def anim_link_to_active(mode, context):


	def link_strips(obj_strip, ob_strip):
		obj_a_s = obj_strip.action_frame_start
		obj_a_e = obj_strip.action_frame_end

		ob_strip.action = obj_strip.action

		ob_strip.action_frame_start = obj_a_s
		ob_strip.action_frame_end = obj_a_e


	obj = context.active_object
	obs = context.selected_objects

	if 'FCURVES' in mode:

		if 'SHAPE_KEYS' in mode:
			action = obj.data.shape_keys.animation_data.action
			for ob in obs:
				if (ob.data and ob.data.shape_keys):
					if ob.data.shape_keys.animation_data:
						ob.data.shape_keys.animation_data.action = action
					else:
						ob.data.shape_keys.animation_data_create()
						ob.data.shape_keys.animation_data.action = action

		elif 'OBJECT' in mode:
			action = obj.animation_data.action
			for ob in obs:
				if ob.animation_data:
					ob.animation_data.action = action
				else:
					ob.animation_data_create()
					ob.animation_data.action = action

	elif 'NLA' in mode:

		if 'SHAPE_KEYS' in mode:
			obj_strip = obj.data.shape_keys.animation_data.nla_tracks[0].strips[0]
			for ob in obs:
				try:
					ob_strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]
					link_strips(obj_strip, ob_strip)
				except:
					pass

		elif 'OBJECT' in mode:
			obj_strip = obj.animation_data.nla_tracks[0].strips[0]
			for ob in obs:
				try:
					ob_strip = ob.animation_data.nla_tracks[0].strips[0]
					link_strips(obj_strip, ob_strip)
				except:
					pass


def fcurves_copy_to_selected(mode, context):
	obj = context.active_object
	obs = context.selected_objects

	if 'SHAPE_KEYS' in mode:
		action = obj.data.shape_keys.animation_data.action
		for ob in obs:
			if (ob.data and ob.data.shape_keys):
				if ob.data.shape_keys.animation_data:
					ob.data.shape_keys.animation_data.action = action.copy()
				else:
					ob.data.shape_keys.animation_data_create()
					ob.data.shape_keys.animation_data.action = action.copy()

	elif 'OBJECT' in mode:
		action = obj.animation_data.action
		for ob in obs:
			if ob.animation_data:
				ob.animation_data.action = action.copy()
			else:
				ob.animation_data_create()
				ob.animation_data.action = action.copy()






# Animation offset tools


def offset_cursor(offset, threshold, mode, context):
	cursor = context.scene.cursor_location

	dist = {}
	for ob in context.selected_objects:
		distance = (cursor - (ob.location + ob.delta_location)).length
		dist[ob] = distance

	if 'REVERSE' in mode:
		dist = sorted(dist, key=dist.get, reverse=True)
	else:
		dist = sorted(dist, key=dist.get)

	i = 0
	i2 = threshold
	for ob in dist:

		if data_access(mode, ob, i, context) is False:
			continue

		if i2 > 1:
			if i2 <= (dist.index(ob) + 1):
				i2 += threshold
				i += offset
		else:
			i += offset


def offset_name(offset, threshold, mode, context):
	obs = context.selected_objects

	dist = {}
	for ob in obs:
		dist[ob] = ob.name

	if 'REVERSE' in mode:
		dist = sorted(dist, key=dist.get, reverse=True)
	else:
		dist = sorted(dist, key=dist.get)

	i = 0
	i2 = threshold
	for ob in dist:

		if data_access(mode, ob, i, context) is False:
			continue

		if i2 > 1:
			if i2 <= (dist.index(ob) + 1):
				i2 += threshold
				i += offset
		else:
			i += offset


def offset_parent(offset, context):
	mode = ['PARENT']

	dist = {}
	for ob in context.selected_objects:
		if ob.parent:
			distance = (ob.parent.location - (ob.location + ob.delta_location + ob.parent.location)).length
			dist[ob] = distance
	dist = sorted(dist, key=dist.get)

	i = 0 + offset
	for ob in dist:
		data_access(mode, ob, i, context)
		i += offset


def offset_multitarget(objects, targets, offset, threshold, mode, context):

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
		i2 = threshold

		if 'REVERSE' in mode:
			obs_sorted = sorted(obs, key=obs.get, reverse=True)
		else:
			obs_sorted = sorted(obs, key=obs.get)

		for ob in obs_sorted:
			if obs[ob][1] == t:

				if data_access(mode, ob, i, context) is False:
					continue

				if i2 > 1:
					obs_thold.append(ob)
					if i2 <= (obs_thold.index(ob) + 1):
						i += offset
						i2 += threshold
				else:
					i += offset






# Handlers


def add_to_group(name, mode, context):

	props = context.scene.commotion
	gr_name = bpy.data.groups.new(name).name
	bpy.ops.object.group_link(group=gr_name)
	bpy.ops.group.objects_add_active()


	if 'FCURVES' in mode:

		if 'SHAPE_KEYS' in mode:
			if name == 'Objects':
				props.sk_fcurves_group_objects = gr_name
			else:
				props.sk_fcurves_group_targets = gr_name

		elif 'OBJECT' in mode:
			if name == 'Objects':
				props.ob_fcurves_group_objects = gr_name
			else:
				props.ob_fcurves_group_targets = gr_name


	if 'NLA' in mode:

		if 'SHAPE_KEYS' in mode:
			if name == 'Objects':
				props.sk_nla_group_objects = gr_name
			else:
				props.sk_nla_group_targets = gr_name

		elif 'OBJECT' in mode:
			if name == 'Objects':
				props.ob_nla_group_objects = gr_name
			else:
				props.ob_nla_group_targets = gr_name






# Utility


def data_access(mode, ob, i, context):

	frame = context.scene.frame_current

	try:


		if 'FCURVES' in mode:

			if 'SHAPE_KEYS' in mode:
				fcus = ob.data.shape_keys.animation_data.action.fcurves

			elif 'OBJECT' in mode:
				fcus = ob.animation_data.action.fcurves

			for fcu in fcus:
				fcu_range = fcu.range()[0]
				for kp in fcu.keyframe_points:
					kp.co[0] = kp.co[0] + frame + i - fcu_range
					kp.handle_left[0] = kp.handle_left[0] + frame + i - fcu_range
					kp.handle_right[0] = kp.handle_right[0] + frame + i - fcu_range


		elif 'NLA' in mode:

			if 'SHAPE_KEYS' in mode:
				strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]

			elif 'OBJECT' in mode:
				strip = ob.animation_data.nla_tracks[0].strips[0]

			strip.frame_end = frame - 1 + i + strip.frame_end
			strip.frame_start = frame + i
			strip.scale = 1


		elif 'PARENT' in mode:
			ob.use_slow_parent = True
			ob.slow_parent_offset = i


	except:
		return False
