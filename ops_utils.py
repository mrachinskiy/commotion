import bpy
from bpy.types import Operator
from bpy.props import StringProperty


class VIEW3D_OT_Commotion_Preset_Apply(Operator):
	"""Apply preset from active object"""
	bl_label = 'Apply Preset'
	bl_idname = 'view3d.commotion_preset_apply'
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


class OBJECT_OT_Commotion_Add_To_Group_Objects(Operator, AddToGroup):
	"""Add selected objects to Objects group for multi-offset"""
	bl_idname = 'object.commotion_add_to_group_objects'
	group = 'Objects'
	prop_suf = '_group_objects'


class OBJECT_OT_Commotion_Add_To_Group_Targets(Operator, AddToGroup):
	"""Add selected objects to Targets group for multi-offset"""
	bl_idname = 'object.commotion_add_to_group_objects_targets'
	group = 'Targets'
	prop_suf = '_group_targets'
