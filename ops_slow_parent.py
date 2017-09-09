from bpy.types import Operator
from bpy.props import FloatProperty, BoolProperty


class OBJECT_OT_Commotion_Slow_Parent_Offset(Operator):
	"""Offset Slow Parent property for selected objects"""
	bl_label = 'Offset Slow Parent'
	bl_idname = 'object.commotion_slow_parent_offset'
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


class OBJECT_OT_Commotion_Slow_Parent_Toggle(Operator):
	"""Toggle Slow Parent property on or off for selected objects"""
	bl_label = 'Toggle Slow Parent'
	bl_idname = 'object.commotion_slow_parent_toggle'
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