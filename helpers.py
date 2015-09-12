import bpy


def showErrorMessage(message, wrap=80):
	lines = []
	if wrap > 0:
		while len(message) > wrap:
			i = message.rfind(' ',0,wrap)
			if i == -1:
				lines += [message[:wrap]]
				message = message[wrap:]
			else:
				lines += [message[:i]]
				message = message[i+1:]
	if message:
		lines += [message]
	def draw(self,context):
		for line in lines:
			self.layout.label(line)
	bpy.context.window_manager.popup_menu(draw, title="Error Message", icon="ERROR")
	return








def shape_list_refresh(context):
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


def update_sp(self, context):
	sce = context.scene
	spl = sce.spl
	como = sce.como
	key = context.active_object.data.shape_keys
	obs = context.selected_objects
	
	if key.use_relative:
		for sps in spl:
			if sps.selected:
				key.key_blocks[sps.index].value = como.shape_value
	else:
		for ob in obs:
			for sps in spl:
				if sps.selected:
					ob.data.shape_keys.key_blocks[sps.index].interpolation = como.shape_interpolation








def auto_keyframes(context):
	frame = context.scene.frame_current
	obs = context.selected_objects

	for ob in obs:
		key = ob.data.shape_keys

		key.eval_time = int(key.key_blocks[1].frame)
		key.keyframe_insert(data_path="eval_time", frame=frame)
		key.eval_time = int(key.key_blocks[-1].frame)
		key.keyframe_insert(data_path="eval_time", frame=frame+20)


def keyframes_offset(fcus, i, context):
	sce = context.scene
	frame = sce.frame_current
	
	for fcu in fcus:
		fcu_range = fcu.range()[0]
		for kp in fcu.keyframe_points:
			kp.co[0] = kp.co[0] + frame + i - fcu_range
			kp.handle_left[0] = kp.handle_left[0] + frame + i - fcu_range
			kp.handle_right[0] = kp.handle_right[0] + frame + i - fcu_range


def strips_offset(strip, i, context):
	sce = context.scene
	frame = sce.frame_current
	
	strip.frame_end = frame - 1 + i + strip.frame_end
	strip.frame_start = frame + i
	strip.scale = 1


def data_access(mode, ob, i, context):
	if 'FCURVES' in mode:
		if 'SHAPE_KEYS' in mode:
			fcus = ob.data.shape_keys.animation_data.action.fcurves
		elif 'OBJECT' in mode:
			fcus = ob.animation_data.action.fcurves
		keyframes_offset(fcus, i, context)
	
	elif 'NLA' in mode:
		if 'SHAPE_KEYS' in mode:
			strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]
		elif 'OBJECT' in mode:
			strip = ob.animation_data.nla_tracks[0].strips[0]
		strips_offset(strip, i, context)
	
	elif 'PARENT' in mode:
		ob.use_slow_parent = True
		ob.slow_parent_offset = i


def offset_cursor(offset, threshold, mode, context):
	sce = context.scene
	cursor = sce.cursor_location
	obs = context.selected_objects

	dist = {}
	for ob in obs:
		distance = (cursor - (ob.location + ob.delta_location)).length
		dist[ob] = distance

	if 'REVERSE' in mode:
		dist = sorted(dist, key=dist.get, reverse=True)
	else:
		dist = sorted(dist, key=dist.get)

	i = 0
	i2 = threshold
	for ob in dist:
		
		data_access(mode, ob, i, context)
		
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
		
		data_access(mode, ob, i, context)
		
		if i2 > 1:
			if i2 <= (dist.index(ob) + 1):
				i2 += threshold
				i += offset
		else:
			i += offset


def offset_parent(offset, context):
	mode = ['PARENT']
	obs = context.selected_objects

	dist = {}
	for ob in obs:
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
				
				data_access(mode, ob, i, context)
				
				if i2 > 1:
					obs_thold.append(ob)
					if i2 <= (obs_thold.index(ob) + 1):
						i += offset
						i2 += threshold
				else:
					i += offset








def create_nla_tracks(anim):
	frst_frame = anim.action.frame_range[0]
	
	if not anim.nla_tracks:
		anim.nla_tracks.new()
	
	anim.nla_tracks[0].strips.new('name', frst_frame, anim.action)
	anim.action = None


def create_strips(mode, context):
	obs = context.selected_objects

	if 'SHAPE_KEYS' in mode:
		for ob in obs:
			if ob.data.shape_keys:
				anim = ob.data.shape_keys.animation_data
			else:
				return showErrorMessage('Selected objects have no Shape Keys')
			create_nla_tracks(anim)

	elif 'OBJECT' in mode:
		for ob in obs:
			if ob.animation_data:
				anim = ob.animation_data
			else:
				return showErrorMessage('Selected objects have no Animation')
			create_nla_tracks(anim)









def link_strips(obj_strip, ob_strip):
	obj_a_s = obj_strip.action_frame_start
	obj_a_e = obj_strip.action_frame_end
	
	ob_strip.action = obj_strip.action
	
	ob_strip.action_frame_start = obj_a_s
	ob_strip.action_frame_end = obj_a_e


def link_to_active(mode, context):
	obj = context.active_object
	obs = context.selected_objects

	if 'NLA' in mode:
		if 'SHAPE_KEYS' in mode:
			obj_strip = obj.data.shape_keys.animation_data.nla_tracks[0].strips[0]
			for ob in obs:
				ob_strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]
				link_strips(obj_strip, ob_strip)
		elif 'OBJECT' in mode:
			obj_strip = obj.animation_data.nla_tracks[0].strips[0]
			for ob in obs:
				ob_strip = ob.animation_data.nla_tracks[0].strips[0]
				link_strips(obj_strip, ob_strip)

	elif 'FCURVES' in mode:
		if 'SHAPE_KEYS' in mode:
			action = obj.data.shape_keys.animation_data.action
			for ob in obs:
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










def copy_to_selected(mode, context):
	obj = context.active_object
	obs = context.selected_objects

	if 'SHAPE_KEYS' in mode:
		action = obj.data.shape_keys.animation_data.action
		for ob in obs:
			if ob.data.shape_keys:
				if ob.data.shape_keys.animation_data:
					ob.data.shape_keys.animation_data.action = action.copy()
				else:
					ob.data.shape_keys.animation_data_create()
					ob.data.shape_keys.animation_data.action = action.copy()
			else:
				return showErrorMessage('Selected objects have no Shape Keys')
	
	elif 'OBJECT' in mode:
		action = obj.animation_data.action
		for ob in obs:
			if ob.animation_data:
				ob.animation_data.action = action.copy()
			else:
				ob.animation_data_create()
				ob.animation_data.action = action.copy()








def remove_nla_track(anim):
	trks = anim.nla_tracks
	anim.action = trks[0].strips[0].action
	trks.remove(trks[0])


def strips_to_fcurves(mode, context):
	obs = context.selected_objects

	if 'SHAPE_KEYS' in mode:
		for ob in obs:
			anim = ob.data.shape_keys.animation_data
			remove_nla_track(anim)
	elif 'OBJECT' in mode:
		for ob in obs:
			anim = ob.animation_data
			remove_nla_track(anim)









def sync_len(mode, context):
	obs = context.selected_objects

	if 'SHAPE_KEYS' in mode:
		for ob in obs:
			strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]
			strip.action_frame_end = (strip.action_frame_start + strip.action.frame_range[1] - 1)
	elif 'OBJECT' in mode:
		for ob in obs:
			strip = ob.animation_data.nla_tracks[0].strips[0]
			strip.action_frame_end = (strip.action_frame_start + strip.action.frame_range[1] - 1)










def driver_set(context):
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
		return showErrorMessage('Selected objects have no Shape Keys')


def targets_remap(context):
	obs = context.selected_objects

	for ob in obs:
		fcus = ob.data.shape_keys.animation_data.drivers
		for fcu in fcus:
			if fcu.data_path == 'eval_time':
				for var in fcu.driver.variables:
					if var.name == 'dist':
						var.targets[0].id = ob


def expression_copy(context):
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


def dist_trigger(var, name):
	etm = bpy.context.scene.objects[name].data.shape_keys.eval_time
	
	if var > etm:
		etm = var
	
	return etm


def register_driver_function(context):
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


def expression_func_set(context):
	como = context.scene.como
	expr = como.sk_drivers_expression_func
	obs = context.selected_objects

	for ob in obs:
		func_expr = "dist_trigger(" + expr + ", '" + ob.name + "')"
		fcus = ob.data.shape_keys.animation_data.drivers
		for fcu in fcus:
			if fcu.data_path == 'eval_time':
				fcu.driver.expression = func_expr
