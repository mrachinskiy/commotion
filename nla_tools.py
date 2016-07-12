def create_strips(mode, context):


	def create_nla_tracks(anim):
		frst_frame = anim.action.frame_range[0]

		if not anim.nla_tracks:
			anim.nla_tracks.new()

		anim.nla_tracks[0].strips.new('name', frst_frame, anim.action)
		anim.action = None


	obs = context.selected_objects

	if 'SHAPE_KEYS' in mode:
		for ob in obs:
			if (ob.data and ob.data.shape_keys):
				anim = ob.data.shape_keys.animation_data
				create_nla_tracks(anim)

	elif 'OBJECT' in mode:
		for ob in obs:
			if ob.animation_data:
				anim = ob.animation_data
				create_nla_tracks(anim)


def strips_to_fcurves(mode, context):


	def remove_nla_track(anim):
		trks = anim.nla_tracks
		anim.action = trks[0].strips[0].action
		trks.remove(trks[0])


	obs = context.selected_objects

	if 'SHAPE_KEYS' in mode:
		for ob in obs:
			if (ob.data and ob.data.shape_keys):
				anim = ob.data.shape_keys.animation_data
				remove_nla_track(anim)

	elif 'OBJECT' in mode:
		for ob in obs:
			if ob.animation_data:
				anim = ob.animation_data
				remove_nla_track(anim)


def sync_len(mode, context):
	obs = context.selected_objects

	if 'SHAPE_KEYS' in mode:
		for ob in obs:
			try:
				strip = ob.data.shape_keys.animation_data.nla_tracks[0].strips[0]
				strip.action_frame_end = (strip.action_frame_start + strip.action.frame_range[1] - 1)
			except:
				pass

	elif 'OBJECT' in mode:
		for ob in obs:
			try:
				strip = ob.animation_data.nla_tracks[0].strips[0]
				strip.action_frame_end = (strip.action_frame_start + strip.action.frame_range[1] - 1)
			except:
				pass
