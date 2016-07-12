import bpy


def icon_tria(prop):
	if prop:
		return 'TRIA_DOWN'
	else:
		return 'TRIA_RIGHT'


def update_sk(self, context):
	scene = context.scene
	skcoll = scene.commotion_skcoll
	props = scene.commotion
	sk = context.active_object.data.shape_keys

	if sk.use_relative:
		for kb in skcoll:
			if kb.selected:
				sk.key_blocks[kb.index].value = props.sk_shape_value
	else:
		for ob in context.selected_objects:
			for kb in skcoll:
				if kb.selected:
					ob.data.shape_keys.key_blocks[kb.index].interpolation = props.sk_shape_interpolation


def dist_trigger(var, name):
	etm = bpy.context.scene.objects[name].data.shape_keys.eval_time

	if var > etm:
		etm = var

	return etm
