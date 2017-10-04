import bpy
from bpy.types import Panel

# Extern
from . import addon_updater_ops


def icon_tria(prop):
	if prop:
		return 'TRIA_DOWN'

	return 'TRIA_RIGHT'


class Setup:
	bl_category = 'Commotion'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = 'objectmode'

	@classmethod
	def poll(cls, context):
		return context.active_object is not None


class VIEW3D_PT_Commotion_Shape_Key_Tools(Panel, Setup):
	bl_label = 'Shape Key Tools'

	def draw(self, context):

		# Updater
		# --------------
		addon_updater_ops.check_for_update_background(context)
		addon_updater_ops.update_notice_box_ui(self, context)
		# --------------

		layout = self.layout
		props = context.scene.commotion
		obj = context.active_object
		try:
			sk = obj.data.shape_keys
			ad = sk.animation_data
		except:
			sk = False
			ad = False

		col = layout.column(align=True)

		box = col.box()
		row = box.row()
		row.prop(props, 'sk_shapekeys', icon=icon_tria(props.sk_shapekeys), icon_only=True, emboss=False)
		row.label(text='Shape Keys', icon='SHAPEKEY_DATA')
		if props.sk_shapekeys:
			skcoll = context.window_manager.commotion_skcoll
			col = box.column(align=True)

			if sk:
				col.operator('object.commotion_sk_coll_refresh')

				if len(sk.key_blocks) == len(skcoll):
					split = box.split()

					sub = split.column(align=True)
					for kb in skcoll:
						sub.prop(kb, 'selected', expand=True, icon='SHAPEKEY_DATA', text=kb.name)

					sub = split.column(align=True)
					if sk.use_relative:
						i = 0
						for kb in sk.key_blocks:
							if skcoll[i].selected:
								sub.prop(kb, 'value', expand=True, icon='GHOST', text=skcoll[i].name)
							i += 1
						col = box.column(align=True)
						col.prop(props, 'sk_value', slider=True)
					else:
						i = 0
						for kb in sk.key_blocks:
							if skcoll[i].selected:
								sub.prop(kb, 'interpolation', text='')
							i += 1
						row = box.row(align=True)
						row.operator('object.commotion_sk_interpolation_set', text=' ', icon='LINCURVE').intr    = 'KEY_LINEAR'
						row.operator('object.commotion_sk_interpolation_set', text=' ', icon='SMOOTHCURVE').intr = 'KEY_CARDINAL'
						row.operator('object.commotion_sk_interpolation_set', text=' ', icon='ROOTCURVE').intr   = 'KEY_CATMULL_ROM'
						row.operator('object.commotion_sk_interpolation_set', text=' ', icon='SPHERECURVE').intr = 'KEY_BSPLINE'

				if not sk.use_relative:
					col = box.column(align=True)
					col.prop(sk, 'eval_time')
					col.operator('anim.commotion_sk_auto_keyframes', icon='IPO_BEZIER')

			else:
				col.label('Object has no Shape Keys')

			col = layout.column(align=True)
			col.separator()

		box = col.box()
		row = box.row()
		row.prop(props, 'sk_fcurves', icon=icon_tria(props.sk_fcurves), icon_only=True, emboss=False)
		row.label(text='F-Curves', icon='IPO')
		if props.sk_fcurves:
			prop_pfx, ad_type = 'sk_fcurves', 'SHAPE_KEYS FCURVES'
			col = box.column(align=True)

			col.operator('view3d.commotion_preset_apply', icon='SETTINGS').prop_pfx = prop_pfx
			col.separator()

			row_ad = col.row(align=True)
			row_ad.enabled = True if (ad and ad.action) else False
			row_ad.operator('anim.commotion_animation_link', icon='LINKED').ad_type = ad_type
			row_ad.operator('anim.commotion_animation_copy', icon='COPYDOWN').ad_type = ad_type
			col.separator()

			col.prop(props, 'sk_fcurves_offset')
			col.prop(props, 'sk_fcurves_threshold')
			col.prop(props, 'sk_fcurves_reverse')

			col.label('Offset from:')
			row = col.row(align=True)
			row.prop(props, 'sk_fcurves_sort_options', expand=True)
			col.separator()

			col = col.column()
			if props.sk_fcurves_sort_options == 'CURSOR':
				ofs = col.operator('anim.commotion_offset_cursor', icon='FORCE_HARMONIC')

			elif props.sk_fcurves_sort_options == 'MULTITARGET':
				row = col.row(align=True)
				row.prop_search(props, 'sk_fcurves_group_objects', bpy.data, 'groups')
				row.operator('object.commotion_add_to_group_objects', text='', icon='ZOOMIN').prop_pfx = prop_pfx

				row = col.row(align=True)
				row.prop_search(props, 'sk_fcurves_group_targets', bpy.data, 'groups')
				row.operator('object.commotion_add_to_group_objects_targets', text='', icon='ZOOMIN').prop_pfx = prop_pfx

				col_ofs = col.column()
				col_ofs.enabled = True if (props.sk_fcurves_group_objects and props.sk_fcurves_group_targets) else False
				ofs = col_ofs.operator('anim.commotion_offset_multitarget', icon='FORCE_HARMONIC')

			else:
				ofs = col.operator('anim.commotion_offset_name', icon='FORCE_HARMONIC')

			ofs.ad_type = ad_type
			ofs.prop_pfx = prop_pfx
			col = layout.column(align=True)
			col.separator()

		box = col.box()
		row = box.row()
		row.prop(props, 'sk_nla', icon=icon_tria(props.sk_nla), icon_only=True, emboss=False)
		row.label(text='NLA', icon='NLA')
		if props.sk_nla:
			prop_pfx, ad_type = 'sk_nla', 'SHAPE_KEYS NLA'
			col = box.column(align=True)

			col.operator('view3d.commotion_preset_apply', icon='SETTINGS').prop_pfx = prop_pfx
			col.separator()

			col_ad = col.column(align=True)
			col_ad.enabled = True if (ad and ad.action) else False
			col_ad.operator('nla.commotion_fcurves_to_nla', icon='NLA_PUSHDOWN').ad_type = ad_type

			col_nla = col.column(align=True)
			col_nla.enabled = True if (ad and ad.nla_tracks and ad.nla_tracks[0].strips) else False
			col_nla.operator('anim.commotion_nla_to_fcurves', icon='IPO_BEZIER').ad_type = ad_type
			col_nla.separator()
			col_nla.operator('anim.commotion_animation_link', icon='LINKED').ad_type = ad_type
			col_nla.operator('nla.commotion_sync_length', icon='TIME').ad_type = ad_type
			col.separator()

			col.prop(props, 'sk_nla_offset')
			col.prop(props, 'sk_nla_threshold')
			col.prop(props, 'sk_nla_reverse')

			col.label('Offset from:')
			row = col.row(align=True)
			row.prop(props, 'sk_nla_sort_options', expand=True)

			col = box.column()
			if props.sk_nla_sort_options == 'CURSOR':
				ofs = col.operator('anim.commotion_offset_cursor', icon='FORCE_HARMONIC')

			elif props.sk_nla_sort_options == 'MULTITARGET':
				row = col.row(align=True)
				row.prop_search(props, 'sk_nla_group_objects', bpy.data, 'groups')
				row.operator('object.commotion_add_to_group_objects', text='', icon='ZOOMIN').prop_pfx = prop_pfx

				row = col.row(align=True)
				row.prop_search(props, 'sk_nla_group_targets', bpy.data, 'groups')
				row.operator('object.commotion_add_to_group_objects_targets', text='', icon='ZOOMIN').prop_pfx = prop_pfx

				col_ofs = col.column()
				col_ofs.enabled = True if (props.sk_nla_group_objects and props.sk_nla_group_targets) else False
				ofs = col_ofs.operator('anim.commotion_offset_multitarget', icon='FORCE_HARMONIC')

			else:
				ofs = col.operator('anim.commotion_offset_name', icon='FORCE_HARMONIC')

			ofs.ad_type = ad_type
			ofs.prop_pfx = prop_pfx
			col = layout.column(align=True)
			col.separator()

		box = col.box()
		row = box.row()
		row.prop(props, 'sk_drivers', icon=icon_tria(props.sk_drivers), icon_only=True, emboss=False)
		row.label(text='Drivers', icon='DRIVER')
		if props.sk_drivers:
			col = box.column(align=True)

			if bpy.app.autoexec_fail:
				col.label('Auto Run disabled', icon='ERROR')
				col.separator()

			if not (ad and ad.drivers):
				col.operator('anim.commotion_sk_driver_distance_set')
			else:
				col.label('Expression:')
				fcu = ad.drivers.find('eval_time')
				col.prop(fcu.driver, 'expression', text='')
				col.operator('anim.commotion_sk_driver_expression_copy', icon='COPYDOWN')

				col.label('Variables:')
				col.operator('anim.commotion_sk_driver_target_remap')
				col.separator()

				row = col.row()
				row.prop(props, 'sk_drivers_dist_trigger', icon=icon_tria(props.sk_drivers_dist_trigger), icon_only=True, emboss=False)
				row.label(text='Distance Trigger', icon='AUTOMERGE_ON')
				if props.sk_drivers_dist_trigger:
					col.separator()
					col = col.column(align=True)
					col.operator('anim.commotion_sk_driver_function_register', icon='COPY_ID')
					col.operator('object.commotion_sk_reset_eval_time', icon='FILE_REFRESH')

					col.label('Expression:')
					row = col.row(align=True)
					row.prop(props, 'sk_drivers_expression_func', text='')
					row.operator('anim.commotion_sk_driver_func_expression_get', text='', icon='EYEDROPPER')
					col.operator('anim.commotion_sk_driver_func_expression_set', icon='COPYDOWN')


class VIEW3D_PT_Commotion_Object_Tools(Panel, Setup):
	bl_label = 'Object Tools'

	def draw(self, context):
		layout = self.layout
		props = context.scene.commotion
		obj = context.active_object
		ad = obj.animation_data

		col = layout.column(align=True)

		box = col.box()
		row = box.row()
		row.prop(props, 'ob_fcurves', icon=icon_tria(props.ob_fcurves), icon_only=True, emboss=False)
		row.label(text='F-Curves', icon='IPO')
		if props.ob_fcurves:
			prop_pfx, ad_type = 'ob_fcurves', 'OBJECT FCURVES'
			col = box.column(align=True)

			col.operator('view3d.commotion_preset_apply', icon='SETTINGS').prop_pfx = prop_pfx
			col.separator()

			row_ad = col.row(align=True)
			row_ad.enabled = True if (ad and ad.action) else False
			row_ad.operator('anim.commotion_animation_link', icon='LINKED').ad_type = ad_type
			row_ad.operator('anim.commotion_animation_copy', icon='COPYDOWN').ad_type = ad_type
			col.separator()

			col.prop(props, 'ob_fcurves_offset')
			col.prop(props, 'ob_fcurves_threshold')
			col.prop(props, 'ob_fcurves_reverse')

			col.label('Offset from:')
			row = col.row(align=True)
			row.prop(props, 'ob_fcurves_sort_options', expand=True)

			col = box.column()
			if props.ob_fcurves_sort_options == 'CURSOR':
				ofs = col.operator('anim.commotion_offset_cursor', icon='FORCE_HARMONIC')

			elif props.ob_fcurves_sort_options == 'MULTITARGET':
				row = col.row(align=True)
				row.prop_search(props, 'ob_fcurves_group_objects', bpy.data, 'groups')
				row.operator('object.commotion_add_to_group_objects', text='', icon='ZOOMIN').prop_pfx = prop_pfx

				row = col.row(align=True)
				row.prop_search(props, 'ob_fcurves_group_targets', bpy.data, 'groups')
				row.operator('object.commotion_add_to_group_objects_targets', text='', icon='ZOOMIN').prop_pfx = prop_pfx

				col_ofs = col.column()
				col_ofs.enabled = True if (props.ob_fcurves_group_objects and props.ob_fcurves_group_targets) else False
				ofs = col_ofs.operator('anim.commotion_offset_multitarget', icon='FORCE_HARMONIC')

			else:
				ofs = col.operator('anim.commotion_offset_name', icon='FORCE_HARMONIC')

			ofs.ad_type = ad_type
			ofs.prop_pfx = prop_pfx
			col = layout.column(align=True)
			col.separator()

		box = col.box()
		row = box.row()
		row.prop(props, 'ob_nla', icon=icon_tria(props.ob_nla), icon_only=True, emboss=False)
		row.label(text='NLA', icon='NLA')
		if props.ob_nla:
			prop_pfx, ad_type = 'ob_nla', 'OBJECT NLA'
			col = box.column(align=True)

			col.operator('view3d.commotion_preset_apply', icon='SETTINGS').prop_pfx = prop_pfx
			col.separator()

			col_ad = col.column(align=True)
			col_ad.enabled = True if (ad and ad.action) else False
			col_ad.operator('nla.commotion_fcurves_to_nla', icon='NLA_PUSHDOWN').ad_type = ad_type

			col_nla = col.column(align=True)
			col_nla.enabled = True if (ad and ad.nla_tracks and ad.nla_tracks[0].strips) else False
			col_nla.operator('anim.commotion_nla_to_fcurves', icon='IPO_BEZIER').ad_type = ad_type
			col_nla.separator()
			col_nla.operator('anim.commotion_animation_link', icon='LINKED').ad_type = ad_type
			col_nla.operator('nla.commotion_sync_length', icon='TIME').ad_type = ad_type
			col.separator()

			col.prop(props, 'ob_nla_offset')
			col.prop(props, 'ob_nla_threshold')
			col.prop(props, 'ob_nla_reverse')

			col.label('Offset from:')
			row = col.row(align=True)
			row.prop(props, 'ob_nla_sort_options', expand=True)

			col = box.column()
			if props.ob_nla_sort_options == 'CURSOR':
				ofs = col.operator('anim.commotion_offset_cursor', icon='FORCE_HARMONIC')

			elif props.ob_nla_sort_options == 'MULTITARGET':
				row = col.row(align=True)
				row.prop_search(props, 'ob_nla_group_objects', bpy.data, 'groups')
				row.operator('object.commotion_add_to_group_objects', text='', icon='ZOOMIN').prop_pfx = prop_pfx

				row = col.row(align=True)
				row.prop_search(props, 'ob_nla_group_targets', bpy.data, 'groups')
				row.operator('object.commotion_add_to_group_objects_targets', text='', icon='ZOOMIN').prop_pfx = prop_pfx

				col_ofs = col.column()
				col_ofs.enabled = True if (props.sk_fcurves_group_objects and props.sk_fcurves_group_targets) else False
				ofs = col_ofs.operator('anim.commotion_offset_multitarget', icon='FORCE_HARMONIC')

			else:
				ofs = col.operator('anim.commotion_offset_name', icon='FORCE_HARMONIC')

			ofs.ad_type = ad_type
			ofs.prop_pfx = prop_pfx
			col = layout.column(align=True)
			col.separator()

		box = col.box()
		row = box.row()
		row.prop(props, 'ob_transforms', icon=icon_tria(props.ob_transforms), icon_only=True, emboss=False)
		row.label(text='Transforms', icon='MANIPUL')
		if props.ob_transforms:
			col = box.column(align=True)

			col.operator('object.anim_transforms_to_deltas', text='Transforms to Deltas', icon='ACTION')
			col.separator()

			col.label('Slow Parent:')
			col.prop(props, 'ob_slow_parent_offset')
			col.operator('object.commotion_slow_parent_offset', icon='FORCE_DRAG').offset = props.ob_slow_parent_offset

			col.label('Toggle Slow Parent:')
			row = col.row(align=True)
			row.operator('object.commotion_slow_parent_toggle', text='On')
			row.operator('object.commotion_slow_parent_toggle', text='Off').off = True
