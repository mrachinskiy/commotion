import bpy
from bpy.types import Panel


class ShapeKeyTools(Panel):
	
	bl_label = "Shape Key Tools"
	bl_idname = "VIEW3D_PT_shape_key_tools"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "objectmode"
	bl_category = "Commotion"

	@classmethod
	def poll(cls, context):
		return context.active_object

	def draw(self, context):
		sce = context.scene
		spl = sce.spl
		como = sce.como
		obj = context.active_object
		layout = self.layout




		col = layout.column(align=True)
		box = col.box()
		row = box.row()
		if not como.shapekeys:
			row.prop(como, "shapekeys", icon="TRIA_RIGHT", icon_only=True)
		else:
			row.prop(como, "shapekeys", icon="TRIA_DOWN", icon_only=True)
		row.label(text="Shape Keys", icon="SHAPEKEY_DATA")
		if como.shapekeys:
			col = box.column(align=True)

			if (obj.data and obj.data.shape_keys):
				key = obj.data.shape_keys
				col.operator("scene.shape_list_refresh")

				if len(key.key_blocks) == len(spl):
					split = box.split()
					col = split.column(align=True)
					for sk in spl:
						col.prop(sk, "selected", expand=True, icon='SHAPEKEY_DATA', text=sk.name)
				
					col = split.column(align=True)
					if key.use_relative:
						i=0
						for kb in key.key_blocks:
							if spl[i].selected:
								col.prop(kb, "value", expand=True, icon='GHOST', text=spl[i].name)
							i+=1
					else:
						i=0
						for kb in key.key_blocks:
							if spl[i].selected:
								col.prop(kb, "interpolation", text="")
							i+=1

					if key.use_relative:
						col = box.column(align=True)
						col.prop(como, "shape_value", slider=True)
					else:
						row = box.row()
						row.prop(como, "shape_interpolation", expand=True)
				
				if not key.use_relative:
					col = box.column(align=True)
					col.prop(key, "eval_time")
					col.operator("scene.auto_keyframes", icon="IPO_BEZIER")
			else:
				col.label("No Shape Keys on object")
			col = layout.column(align=True)
			col.separator()




		box = col.box()
		row = box.row()
		if not como.sk_fcurves:
			row.prop(como, "sk_fcurves", icon="TRIA_RIGHT", icon_only=True)
		else:
			row.prop(como, "sk_fcurves", icon="TRIA_DOWN", icon_only=True)
		row.label(text="F-Curves", icon="IPO")
		if como.sk_fcurves:
			col = box.column(align=True)
			
			if (obj.data and obj.data.shape_keys and
			                 obj.data.shape_keys.animation_data and
			                 obj.data.shape_keys.animation_data.action):
				col.operator("scene.sk_fcurves_link", icon="LINKED")
				col.operator("scene.sk_fcurves_copy", icon="COPYDOWN")
				col.separator()
				col.prop(como, "sk_fcurves_offset")
				col.prop(como, "sk_fcurves_threshold")
				col.prop(como, "sk_fcurves_reverse")
				col.label('Offset from:')
				col = col.row(align=True)
				col.prop(como, "sk_fcurves_sort_options", expand=True)
				col = box.column()
				if como.sk_fcurves_sort_options == 'CURSOR':
					col.operator("scene.sk_fcurves_offset_cursor", icon="FORCE_HARMONIC")
				elif como.sk_fcurves_sort_options == 'MULTITARGET':
					col.prop_search(como, "sk_fcurves_group_objects", bpy.data, "groups")
					col.prop_search(como, "sk_fcurves_group_targets", bpy.data, "groups")
					col.operator("scene.sk_fcurves_offset_multitarget", icon="FORCE_HARMONIC")
				elif como.sk_fcurves_sort_options == 'NAME':
					col.operator("scene.sk_fcurves_offset_name", icon="FORCE_HARMONIC")
			else:
				col.label("No animation on Shape Keys")
			col = layout.column(align=True)
			col.separator()




		box = col.box()
		row = box.row()
		if not como.sk_nla:
			row.prop(como, "sk_nla", icon="TRIA_RIGHT", icon_only=True)
		else:
			row.prop(como, "sk_nla", icon="TRIA_DOWN", icon_only=True)
		row.label(text="NLA", icon="NLA")
		if como.sk_nla:
			col = box.column(align=True)

			if (obj.data and obj.data.shape_keys and
			                 obj.data.shape_keys.animation_data):
				anim = obj.data.shape_keys.animation_data
				if anim.action:
					col.operator("scene.sk_nla_create", icon="NLA_PUSHDOWN")
				
				if (anim.nla_tracks and anim.nla_tracks[0].strips):
					col.operator("scene.sk_nla_to_fcurves", icon="IPO_BEZIER")
					col.operator("scene.sk_nla_sync_length", icon="TIME")
					col.operator("scene.sk_nla_link_to_active", icon="LINKED")
					col.separator()
					col.prop(como, "sk_nla_offset")
					col.prop(como, "sk_nla_threshold")
					col.prop(como, "sk_nla_reverse")
					col.label('Offset from:')
					col = col.row(align=True)
					col.prop(como, "sk_nla_sort_options", expand=True)
					col = box.column()
					if como.sk_nla_sort_options == 'CURSOR':
						col.operator("scene.sk_nla_offset_cursor", icon="FORCE_HARMONIC")
					elif como.sk_nla_sort_options == 'MULTITARGET':
						col.prop_search(como, "sk_nla_group_objects", bpy.data, "groups")
						col.prop_search(como, "sk_nla_group_targets", bpy.data, "groups")
						col.operator("scene.sk_nla_offset_multitarget", icon="FORCE_HARMONIC")
					elif como.sk_nla_sort_options == 'NAME':
						col.operator("scene.sk_nla_offset_name", icon="FORCE_HARMONIC")
			else:
				col.label("No animation on Shape Keys")
			col = layout.column(align=True)
			col.separator()




		box = col.box()
		row = box.row()
		if not como.sk_drivers:
			row.prop(como, "sk_drivers", icon="TRIA_RIGHT", icon_only=True)
		else:
			row.prop(como, "sk_drivers", icon="TRIA_DOWN", icon_only=True)
		row.label(text="Drivers", icon="DRIVER")
		if como.sk_drivers:
			col = box.column(align=True)
			col.operator("scene.sk_driver_set")

			if (obj.data and obj.data.shape_keys and
			             not obj.data.shape_keys.use_relative and
			                 obj.data.shape_keys.animation_data and
			                 obj.data.shape_keys.animation_data.drivers):
				col.operator("scene.sk_targets_remap")
				col.label("Expression:")
				fcus = obj.data.shape_keys.animation_data.drivers
				for fcu in fcus:
					if fcu.data_path == 'eval_time':
						col.prop(fcu.driver, "expression", text="")
				col.operator("scene.sk_expression_copy", icon="COPYDOWN")

				row = box.row()
				if not como.sk_drivers_dist_trigger:
					row.prop(como, "sk_drivers_dist_trigger", icon="TRIA_RIGHT", icon_only=True)
				else:
					row.prop(como, "sk_drivers_dist_trigger", icon="TRIA_DOWN", icon_only=True)
				row.label(text="Distance Trigger", icon="AUTOMERGE_ON")
				if como.sk_drivers_dist_trigger:
					col = box.column(align=True)
					col.operator("scene.sk_driver_func_reg", icon="COPY_ID")
					col.operator("scene.sk_eval_time_reset", icon="FILE_REFRESH")
					col.separator()
					col.prop(como, "sk_drivers_expression_func", text="")
					col.operator("scene.sk_expression_func_set", icon="COPYDOWN")




class ObjectTools(Panel):
	
	bl_label = "Object Tools"
	bl_idname = "VIEW3D_PT_object_tools"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "objectmode"
	bl_category = "Commotion"

	@classmethod
	def poll(cls, context):
		return context.active_object

	def draw(self, context):
		sce = context.scene
		como = sce.como
		obj = context.active_object
		layout = self.layout
		col = layout.column(align=True)




		box = col.box()
		row = box.row()
		if not como.ob_fcurves:
			row.prop(como, "ob_fcurves", icon="TRIA_RIGHT", icon_only=True)
		else:
			row.prop(como, "ob_fcurves", icon="TRIA_DOWN", icon_only=True)
		row.label(text="F-Curves", icon="IPO")
		if como.ob_fcurves:
			col = box.column(align=True)
			
			if (obj.animation_data and obj.animation_data.action):
				col.operator("scene.ob_fcurves_link", icon="LINKED")
				col.operator("scene.ob_fcurves_copy", icon="COPYDOWN")
				col.separator()
				col.prop(como, "ob_fcurves_offset")
				col.prop(como, "ob_fcurves_threshold")
				col.prop(como, "ob_fcurves_reverse")
				col.label('Offset from:')
				col = col.row(align=True)
				col.prop(como, "ob_fcurves_sort_options", expand=True)
				col = box.column()
				if como.ob_fcurves_sort_options == 'CURSOR':
					col.operator("scene.ob_fcurves_offset_cursor", icon="FORCE_HARMONIC")
				elif como.ob_fcurves_sort_options == 'MULTITARGET':
					col.prop_search(como, "ob_fcurves_group_objects", bpy.data, "groups")
					col.prop_search(como, "ob_fcurves_group_targets", bpy.data, "groups")
					col.operator("scene.ob_fcurves_offset_multitarget", icon="FORCE_HARMONIC")
				elif como.ob_fcurves_sort_options == 'NAME':
					col.operator("scene.ob_fcurves_offset_name", icon="FORCE_HARMONIC")
			else:
				col.label("No Animation on object")
			col = layout.column(align=True)
			col.separator()




		box = col.box()
		row = box.row()
		if not como.ob_nla:
			row.prop(como, "ob_nla", icon="TRIA_RIGHT", icon_only=True)
		else:
			row.prop(como, "ob_nla", icon="TRIA_DOWN", icon_only=True)
		row.label(text="NLA", icon="NLA")
		if como.ob_nla:
			col = box.column(align=True)
		
			if obj.animation_data:
				anim = obj.animation_data
				if anim.action:
					col.operator("scene.ob_nla_create", icon="NLA_PUSHDOWN")
				
				if (anim.nla_tracks and anim.nla_tracks[0].strips):
					col.operator("scene.ob_nla_to_fcurves", icon="IPO_BEZIER")
					col.operator("scene.ob_nla_sync_length", icon="TIME")
					col.operator("scene.ob_nla_link_to_active", icon="LINKED")
					col.separator()
					col.prop(como, "ob_nla_offset")
					col.prop(como, "ob_nla_threshold")
					col.prop(como, "ob_nla_reverse")
					col.label('Offset from:')
					col = col.row(align=True)
					col.prop(como, "ob_nla_sort_options", expand=True)
					col = box.column()
					if como.ob_nla_sort_options == 'CURSOR':
						col.operator("scene.ob_nla_offset_cursor", icon="FORCE_HARMONIC")
					elif como.ob_nla_sort_options == 'MULTITARGET':
						col.prop_search(como, "ob_nla_group_objects", bpy.data, "groups")
						col.prop_search(como, "ob_nla_group_targets", bpy.data, "groups")
						col.operator("scene.ob_nla_offset_multitarget", icon="FORCE_HARMONIC")
					elif como.ob_nla_sort_options == 'NAME':
						col.operator("scene.ob_nla_offset_name", icon="FORCE_HARMONIC")
			else:
				col.label("No animation on object")
			col = layout.column(align=True)
			col.separator()




		box = col.box()
		row = box.row()
		if not como.transforms:
			row.prop(como, "transforms", icon="TRIA_RIGHT", icon_only=True)
		else:
			row.prop(como, "transforms", icon="TRIA_DOWN", icon_only=True)
		row.label(text="Transforms", icon="MANIPUL")
		if como.transforms:
			col = box.column(align=True)
			
			col.operator("object.anim_transforms_to_deltas", icon="ACTION", text="Transforms to Deltas")
			
			col.label("Slow Parent:")
			col.prop(como, "slow_parent_offset")
			col.operator("scene.slow_parent_offset", icon="FORCE_DRAG")
