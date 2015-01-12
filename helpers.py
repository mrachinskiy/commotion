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









def keyframes_offset(fcus, i):
	sce = bpy.context.scene
	frame = sce.frame_current
	
	for fcu in fcus:
		fcu_range = fcu.range()[0]
		for kp in fcu.keyframe_points:
			kp.co[0] = kp.co[0] + frame + i - fcu_range
			kp.handle_left[0] = kp.handle_left[0] + frame + i - fcu_range
			kp.handle_right[0] = kp.handle_right[0] + frame + i - fcu_range


def strips_offset(strip, i):
	sce = bpy.context.scene
	frame = sce.frame_current
	
	strip.frame_end = frame - 1 + i + strip.frame_end
	strip.frame_start = frame + i
	strip.scale = 1


def data_access(mode, ob, i):
	if mode[0] == 'FCURVES':
		if mode[1] == 'SHAPE_KEYS':
			fcus = ob.data.shape_keys.animation_data.action.fcurves
		elif mode[1] == 'OBJECT':
			fcus = ob.animation_data.action.fcurves
		keyframes_offset(fcus, i)
	
	elif mode[0] == 'NLA':
		if mode[1] == 'SHAPE_KEYS':
			strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]
		elif mode[1] == 'OBJECT':
			strip = ob.animation_data.nla_tracks[0].strips[0]
		strips_offset(strip, i)
	
	elif mode[0] == 'PARENT':
		ob.use_slow_parent = True
		ob.slow_parent_offset = i


def offset_cursor(offset, threshold, mode):
	sce = bpy.context.scene
	cursor = sce.cursor_location
	obs = bpy.context.selected_objects

	dist = {}
	for ob in obs:
		distance = (cursor - (ob.location + ob.delta_location)).length
		dist[ob] = distance
	dist = sorted(dist, key=dist.get)

	i = 0
	i2 = threshold
	for ob in dist:
		
		data_access(mode, ob, i)
		
		if i2 > 1:
			if i2 <= (dist.index(ob) + 1):
				i2 += threshold
				i += offset
		else:
			i += offset


def offset_name(offset, threshold, mode):
	obs = bpy.context.selected_objects

	dist = {}
	for ob in obs:
		dist[ob] = ob.name
	if mode[2]:
		dist = sorted(dist, key=dist.get, reverse=True)
	else:
		dist = sorted(dist, key=dist.get)

	i = 0
	i2 = threshold
	for ob in dist:
		
		data_access(mode, ob, i)
		
		if i2 > 1:
			if i2 <= (dist.index(ob) + 1):
				i2 += threshold
				i += offset
		else:
			i += offset


def offset_parent(offset):
	mode = ['PARENT']
	obs = bpy.context.selected_objects

	dist = {}
	for ob in obs:
		distance = (ob.parent.location - (ob.location + ob.delta_location + ob.parent.location)).length
		dist[ob] = distance
	dist = sorted(dist, key=dist.get)

	i = 0 + offset
	for ob in dist:
		data_access(mode, ob, i)
		i += offset
			


def offset_multitarget(objects, targets, offset, threshold, mode):
	obs = {}
	for ob in objects:
		targs = {}
		for t in targets:
			distance = (t.location - (ob.location + ob.delta_location)).length
			targs[distance] = t
			dist = sorted(targs)[0]
		obs[ob] = [dist, targs[dist]]

	for t in targets:
		obs_th = []
		i = 0
		i2 = threshold
		for ob in sorted(obs, key=obs.get):
			if obs[ob][1] == t:
				
				data_access(mode, ob, i)
				
				if i2 > 1:
					obs_th.append(ob)
					if i2 <= (obs_th.index(ob) + 1):
						i += offset
						i2 += threshold
				else:
					i += offset










def create_strips(mode):
	obs = bpy.context.selected_objects

	for ob in obs:
		
		if mode == 'SHAPE_KEYS':
			anim = ob.data.shape_keys.animation_data
		elif mode == 'OBJECT':
			anim = ob.animation_data

		frst_frame = anim.action.frame_range[0]
		
		if not anim.nla_tracks:
			anim.nla_tracks.new()
		
		anim.nla_tracks[0].strips.new('name', frst_frame, anim.action)
		anim.action = None


def link_to_active(mode):
	obj = bpy.context.active_object
	obs = bpy.context.selected_objects

	if mode[0] == 'NLA':
		for ob in obs:
			
			if mode[1] == 'SHAPE_KEYS':
				obj_strip = obj.data.shape_keys.animation_data.nla_tracks[0].strips[0]
				ob_strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]
			elif mode[1] == 'OBJECT':
				obj_strip = obj.animation_data.nla_tracks[0].strips[0]
				ob_strip = ob.animation_data.nla_tracks[0].strips[0]
			
			obj_a_s = obj_strip.action_frame_start
			obj_a_e = obj_strip.action_frame_end
			
			ob_strip.action = obj_strip.action
			
			ob_strip.action_frame_start = obj_a_s
			ob_strip.action_frame_end = obj_a_e

	elif mode[0] == 'FCURVES':
		for ob in obs:
			
			if mode[1] == 'SHAPE_KEYS':
				action = obj.data.shape_keys.animation_data.action
				if ob.data.shape_keys.animation_data:
					ob.data.shape_keys.animation_data.action = action
				else:
					ob.data.shape_keys.animation_data_create()
					ob.data.shape_keys.animation_data.action = action
			
			elif mode[1] == 'OBJECT':
				action = obj.animation_data.action
				if ob.animation_data:
					ob.animation_data.action = action
				else:
					ob.animation_data_create()
					ob.animation_data.action = action


def copy_to_selected(mode):
	obj = bpy.context.active_object
	obs = bpy.context.selected_objects
	
	for ob in obs:
		
		if mode == 'SHAPE_KEYS':
			action = obj.data.shape_keys.animation_data.action
			if ob.data.shape_keys.animation_data:
				ob.data.shape_keys.animation_data.action = action.copy()
			else:
				ob.data.shape_keys.animation_data_create()
				ob.data.shape_keys.animation_data.action = action.copy()
		
		elif mode == 'OBJECT':
			action = obj.animation_data.action
			if ob.animation_data:
				ob.animation_data.action = action.copy()
			else:
				ob.animation_data_create()
				ob.animation_data.action = action.copy()


def strips_to_fcurves(mode):
	obs = bpy.context.selected_objects

	for ob in obs:
		if mode == 'SHAPE_KEYS':
			anim = ob.data.shape_keys.animation_data
		elif mode == 'OBJECT':
			anim = ob.animation_data
		
		trks = anim.nla_tracks
		anim.action = trks[0].strips[0].action
		trks.remove(trks[0])


def sync_len(mode):
	obs = bpy.context.selected_objects
	
	for ob in obs:
		if mode == 'SHAPE_KEYS':
			strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]
		elif mode == 'OBJECT':
			strip = ob.animation_data.nla_tracks[0].strips[0]
		
		strip.action_frame_end = (strip.action_frame_start + strip.action.frame_range[1] - 1)









def dist_trigger(var, name):
	etm = bpy.context.scene.objects[name].data.shape_keys.eval_time
	
	if var > etm:
		etm = var
	
	return etm
