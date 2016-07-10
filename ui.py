import bpy
from bpy.types import Panel
from .modules.utility import icon_tria


class ShapeKeyTools(Panel):
	bl_category = 'Commotion'
	bl_label = 'Shape Key Tools'
	bl_idname = 'commotion_sk_tools'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = 'objectmode'

	@classmethod
	def poll(cls, context):
		return context.active_object

	def draw(self, context):
		props = context.scene.commotion
		skcoll = context.scene.commotion_skcoll
		obj = context.active_object
		obj_has_sk = True if (obj.data and obj.data.shape_keys) else False
		obj_has_ad = True if (obj_has_sk and obj.data.shape_keys.animation_data) else False



		layout = self.layout
		col = layout.column(align=True)



		box = col.box()
		row = box.row()
		row.prop(props, 'sk_shapekeys', icon=icon_tria(props.sk_shapekeys), icon_only=True)
		row.label(text='Shape Keys', icon='SHAPEKEY_DATA')
		if props.sk_shapekeys:
			col = box.column(align=True)

			if obj_has_sk:
				key = obj.data.shape_keys
				col.operator('commotion.sk_refresh')

				if len(key.key_blocks) == len(skcoll):
					split = box.split()
					col = split.column(align=True)
					for sk in skcoll:
						col.prop(sk, 'selected', expand=True, icon='SHAPEKEY_DATA', text=sk.name)

					col = split.column(align=True)
					if key.use_relative:
						i = 0
						for kb in key.key_blocks:
							if skcoll[i].selected:
								col.prop(kb, 'value', expand=True, icon='GHOST', text=skcoll[i].name)
							i += 1
					else:
						i = 0
						for kb in key.key_blocks:
							if skcoll[i].selected:
								col.prop(kb, 'interpolation', text='')
							i += 1

					if key.use_relative:
						col = box.column(align=True)
						col.prop(props, 'sk_shape_value', slider=True)
					else:
						row = box.row()
						row.prop(props, 'sk_shape_interpolation', expand=True)

				if not key.use_relative:
					col = box.column(align=True)
					col.prop(key, 'eval_time')
					col.operator('commotion.sk_auto_keyframes', icon='IPO_BEZIER')
			else:
				col.label('Object has no Shape Keys')
			col = layout.column(align=True)
			col.separator()



		box = col.box()
		row = box.row()
		row.prop(props, 'sk_fcurves', icon=icon_tria(props.sk_fcurves), icon_only=True)
		row.label(text='F-Curves', icon='IPO')
		if props.sk_fcurves:
			col = box.column(align=True)

			if (obj_has_ad and obj.data.shape_keys.animation_data.action):
				col.operator('commotion.sk_fcurves_link', icon='LINKED')
				col.operator('commotion.sk_fcurves_copy', icon='COPYDOWN')
				col.separator()
				col.prop(props, 'sk_fcurves_offset')
				col.prop(props, 'sk_fcurves_threshold')
				col.prop(props, 'sk_fcurves_reverse')
				col.label('Offset from:')
				col = col.row(align=True)
				col.prop(props, 'sk_fcurves_sort_options', expand=True)
				col = box.column()
				if props.sk_fcurves_sort_options == 'CURSOR':
					col.operator('commotion.sk_fcurves_offset_cursor', icon='FORCE_HARMONIC')
				elif props.sk_fcurves_sort_options == 'MULTITARGET':
					row = col.row(align=True)
					row.label('Objects:')
					row.prop_search(props, 'sk_fcurves_group_objects', bpy.data, 'groups', text='')
					row.operator('commotion.sk_fcurves_add_to_group_objects', text='', icon='ZOOMIN')
					row = col.row(align=True)
					row.label('Targets:')
					row.prop_search(props, 'sk_fcurves_group_targets', bpy.data, 'groups', text='')
					row.operator('commotion.sk_fcurves_add_to_group_targets', text='', icon='ZOOMIN')
					col.operator('commotion.sk_fcurves_offset_multitarget', icon='FORCE_HARMONIC')
				elif props.sk_fcurves_sort_options == 'NAME':
					col.operator('commotion.sk_fcurves_offset_name', icon='FORCE_HARMONIC')
			else:
				col.label('Shape Keys have no animation')
			col = layout.column(align=True)
			col.separator()



		box = col.box()
		row = box.row()
		row.prop(props, 'sk_nla', icon=icon_tria(props.sk_nla), icon_only=True)
		row.label(text='NLA', icon='NLA')
		if props.sk_nla:
			col = box.column(align=True)

			if obj_has_ad:
				anim = obj.data.shape_keys.animation_data
				if anim.action:
					col.operator('commotion.sk_nla_create', icon='NLA_PUSHDOWN')
				if (anim.nla_tracks and anim.nla_tracks[0].strips):
					col.operator('commotion.sk_nla_to_fcurves', icon='IPO_BEZIER')
					col.operator('commotion.sk_nla_sync_length', icon='TIME')
					col.operator('commotion.sk_nla_link_to_active', icon='LINKED')
					col.separator()
					col.prop(props, 'sk_nla_offset')
					col.prop(props, 'sk_nla_threshold')
					col.prop(props, 'sk_nla_reverse')
					col.label('Offset from:')
					col = col.row(align=True)
					col.prop(props, 'sk_nla_sort_options', expand=True)
					col = box.column()
					if props.sk_nla_sort_options == 'CURSOR':
						col.operator('commotion.sk_nla_offset_cursor', icon='FORCE_HARMONIC')
					elif props.sk_nla_sort_options == 'MULTITARGET':
						row = col.row(align=True)
						row.label('Objects:')
						row.prop_search(props, 'sk_nla_group_objects', bpy.data, 'groups', text='')
						row.operator('commotion.sk_nla_add_to_group_objects', text='', icon='ZOOMIN')
						row = col.row(align=True)
						row.label('Targets:')
						row.prop_search(props, 'sk_nla_group_targets', bpy.data, 'groups', text='')
						row.operator('commotion.sk_nla_add_to_group_targets', text='', icon='ZOOMIN')
						col.operator('commotion.sk_nla_offset_multitarget', icon='FORCE_HARMONIC')
					elif props.sk_nla_sort_options == 'NAME':
						col.operator('commotion.sk_nla_offset_name', icon='FORCE_HARMONIC')
			else:
				col.label('Shape Keys have no animation')
			col = layout.column(align=True)
			col.separator()



		box = col.box()
		row = box.row()
		row.prop(props, 'sk_drivers', icon=icon_tria(props.sk_drivers), icon_only=True)
		row.label(text='Drivers', icon='DRIVER')
		if props.sk_drivers:
			col = box.column(align=True)

			warn = col.column(align=True)
			col = col.column(align=True)

			if context.user_preferences.system.use_scripts_auto_execute is False:
				warn.label('Auto Run disabled', icon='ERROR')
				warn.separator()
				col.enabled = False

			if (obj_has_sk and not obj.data.shape_keys.use_relative):
				if not (obj_has_ad and obj.data.shape_keys.animation_data.drivers):
					col.operator('commotion.sk_drivers_set_distance')
				else:
					col.label('Expression:')
					fcu = obj.data.shape_keys.animation_data.drivers.find('eval_time')
					col.prop(fcu.driver, 'expression', text='')
					col.operator('commotion.sk_drivers_copy_expression', icon='COPYDOWN')
					col.separator()

					row = col.row()
					row.prop(props, 'sk_drivers_dist_trigger', icon=icon_tria(props.sk_drivers_dist_trigger), icon_only=True)
					row.label(text='Distance Trigger', icon='AUTOMERGE_ON')
					if props.sk_drivers_dist_trigger:
						col.separator()
						col = col.column(align=True)
						col.operator('commotion.sk_drivers_register_drv_function', icon='COPY_ID')
						col.operator('commotion.sk_drivers_reset_eval_time', icon='FILE_REFRESH')
						col.separator()
						row = col.row(align=True)
						row.prop(props, 'sk_drivers_expression_func', text='')
						row.operator('commotion.sk_drivers_get_drv_func_expression', text='', icon='EYEDROPPER')
						col.operator('commotion.sk_drivers_set_drv_func_expression', icon='COPYDOWN')
			else:
				col.label('Object has no Absolute Shape Keys')






class ObjectTools(Panel):
	bl_category = 'Commotion'
	bl_label = 'Object Tools'
	bl_idname = 'commotion_ob_tools'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = 'objectmode'

	@classmethod
	def poll(cls, context):
		return context.active_object

	def draw(self, context):
		props = context.scene.commotion
		obj = context.active_object
		obj_has_ad = True if obj.animation_data else False



		layout = self.layout
		col = layout.column(align=True)



		box = col.box()
		row = box.row()
		row.prop(props, 'ob_fcurves', icon=icon_tria(props.ob_fcurves), icon_only=True)
		row.label(text='F-Curves', icon='IPO')
		if props.ob_fcurves:
			col = box.column(align=True)

			if (obj_has_ad and obj.animation_data.action):
				col.operator('commotion.ob_fcurves_link', icon='LINKED')
				col.operator('commotion.ob_fcurves_copy', icon='COPYDOWN')
				col.separator()
				col.prop(props, 'ob_fcurves_offset')
				col.prop(props, 'ob_fcurves_threshold')
				col.prop(props, 'ob_fcurves_reverse')
				col.label('Offset from:')
				col = col.row(align=True)
				col.prop(props, 'ob_fcurves_sort_options', expand=True)
				col = box.column()
				if props.ob_fcurves_sort_options == 'CURSOR':
					col.operator('commotion.ob_fcurves_offset_cursor', icon='FORCE_HARMONIC')
				elif props.ob_fcurves_sort_options == 'MULTITARGET':
					row = col.row(align=True)
					row.label('Objects:')
					row.prop_search(props, 'ob_fcurves_group_objects', bpy.data, 'groups', text='')
					row.operator('commotion.ob_fcurves_add_to_group_objects', text='', icon='ZOOMIN')
					row = col.row(align=True)
					row.label('Targets:')
					row.prop_search(props, 'ob_fcurves_group_targets', bpy.data, 'groups', text='')
					row.operator('commotion.ob_fcurves_add_to_group_targets', text='', icon='ZOOMIN')
					col.operator('commotion.ob_fcurves_offset_multitarget', icon='FORCE_HARMONIC')
				elif props.ob_fcurves_sort_options == 'NAME':
					col.operator('commotion.ob_fcurves_offset_name', icon='FORCE_HARMONIC')
			else:
				col.label('Object has no animation')
			col = layout.column(align=True)
			col.separator()



		box = col.box()
		row = box.row()
		row.prop(props, 'ob_nla', icon=icon_tria(props.ob_nla), icon_only=True)
		row.label(text='NLA', icon='NLA')
		if props.ob_nla:
			col = box.column(align=True)

			if obj_has_ad:
				anim = obj.animation_data
				if anim.action:
					col.operator('commotion.ob_nla_create', icon='NLA_PUSHDOWN')

				if (anim.nla_tracks and anim.nla_tracks[0].strips):
					col.operator('commotion.ob_nla_to_fcurves', icon='IPO_BEZIER')
					col.operator('commotion.ob_nla_sync_length', icon='TIME')
					col.operator('commotion.ob_nla_link_to_active', icon='LINKED')
					col.separator()
					col.prop(props, 'ob_nla_offset')
					col.prop(props, 'ob_nla_threshold')
					col.prop(props, 'ob_nla_reverse')
					col.label('Offset from:')
					col = col.row(align=True)
					col.prop(props, 'ob_nla_sort_options', expand=True)
					col = box.column()
					if props.ob_nla_sort_options == 'CURSOR':
						col.operator('commotion.ob_nla_offset_cursor', icon='FORCE_HARMONIC')
					elif props.ob_nla_sort_options == 'MULTITARGET':
						row = col.row(align=True)
						row.label('Objects:')
						row.prop_search(props, 'ob_nla_group_objects', bpy.data, 'groups', text='')
						row.operator('commotion.ob_nla_add_to_group_objects', text='', icon='ZOOMIN')
						row = col.row(align=True)
						row.label('Targets:')
						row.prop_search(props, 'ob_nla_group_targets', bpy.data, 'groups', text='')
						row.operator('commotion.ob_nla_add_to_group_targets', text='', icon='ZOOMIN')
						col.operator('commotion.ob_nla_offset_multitarget', icon='FORCE_HARMONIC')
					elif props.ob_nla_sort_options == 'NAME':
						col.operator('commotion.ob_nla_offset_name', icon='FORCE_HARMONIC')
			else:
				col.label('Object has no animation')
			col = layout.column(align=True)
			col.separator()



		box = col.box()
		row = box.row()
		row.prop(props, 'ob_transforms', icon=icon_tria(props.ob_transforms), icon_only=True)
		row.label(text='Transforms', icon='MANIPUL')
		if props.ob_transforms:
			col = box.column(align=True)

			col.operator('object.anim_transforms_to_deltas', text='Transforms to Deltas', icon='ACTION')
			col.label('Slow Parent:')
			col.prop(props, 'ob_offset_slow_parent')
			col.operator('commotion.ob_offset_slow_parent', icon='FORCE_DRAG')
