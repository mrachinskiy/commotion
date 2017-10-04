from bpy.types import Operator
from bpy.props import StringProperty


class OBJECT_OT_Commotion_SK_Coll_Refresh(Operator):
	"""Refresh shape key list for active object"""
	bl_label = 'Refresh Shape List'
	bl_idname = 'object.commotion_sk_coll_refresh'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		skcoll = context.window_manager.commotion_skcoll
		skcoll.clear()
		i = 0

		for kb in context.active_object.data.shape_keys.key_blocks:
			skcoll.add()
			skcoll[i].name = kb.name
			skcoll[i].index = i
			i += 1

		return {'FINISHED'}


class OBJECT_OT_Commotion_SK_Interpolation_Set(Operator):
	"""Set interpolation type for selected shape keys (Linear, Cardinal, Catmull-Rom, BSpline)"""
	bl_label = 'Set Interpolation'
	bl_idname = 'object.commotion_sk_interpolation_set'
	bl_options = {'INTERNAL'}

	intr = StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

	def execute(self, context):
		skcoll = context.window_manager.commotion_skcoll

		for ob in context.selected_objects:

			try:
				sk = ob.data.shape_keys
			except:
				continue

			for kb in skcoll:
				if kb.selected:
					sk.key_blocks[kb.index].interpolation = self.intr

		return {'FINISHED'}


class ANIM_OT_Commotion_SK_Auto_Keyframes(Operator):
	"""Create keyframes for absolute shape keys on selected objects, """ \
	"""based on the current frame and shape keys timings"""
	bl_label = 'Auto Keyframes'
	bl_idname = 'anim.commotion_sk_auto_keyframes'
	bl_options = {'INTERNAL'}

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


class OBJECT_OT_Commotion_SK_Reset_Eval_Time(Operator):
	"""Reset Evaluation Time property for selected objects to 0"""
	bl_label = 'Reset Evaluation Time'
	bl_idname = 'object.commotion_sk_reset_eval_time'
	bl_options = {'INTERNAL'}

	def execute(self, context):
		for ob in context.selected_objects:
			try:
				ob.data.shape_keys.eval_time = 0
			except:
				pass

		return {'FINISHED'}

