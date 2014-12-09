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
from bpy.types import Panel




class ShapeKeyTools(Panel):
	
	bl_label = "Shape Key Tools"
	bl_idname = "VIEW3D_PT_shape_key_tools"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "objectmode"
	bl_category = "Shape Tools"

	@classmethod
	def poll(cls, context):
		return context.active_object

	def draw(self, context):
		sce = context.scene
		spl = sce.spl
		stProps = sce.stProps
		obj = context.active_object
		
		layout = self.layout
		col = layout.column(align=True)





		col.prop(stProps, "shapekeys", icon="SHAPEKEY_DATA")
		if stProps.shapekeys:
			box = layout.box()
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
						col.prop(stProps, "shape_value", slider=True)
					else:
						row = box.row()
						row.prop(stProps, "shape_interpolation", expand=True)
				
				if not key.use_relative:
					col = box.column(align=True)
					col.prop(key, "eval_time")
					col.operator("scene.auto_keyframes", icon="IPO_BEZIER")
			else:
				col.label("No Shape Keys on object")

			col = layout.column(align=True)
			col.separator()





		col.prop(stProps, "sk_fcurves", icon="IPO")
		if stProps.sk_fcurves:
			box = layout.box()
			col = box.column(align=True)
			
			if (obj.data and obj.data.shape_keys and
			                 obj.data.shape_keys.animation_data and
			                 obj.data.shape_keys.animation_data.action):
				col.operator("scene.sk_fcurves_link", icon="LINKED")
				col.operator("scene.sk_fcurves_copy", icon="COPYDOWN")
				col.separator()
				col.prop(stProps, "sk_fcurves_offset")
				col.prop(stProps, "sk_fcurves_threshold")
				col.operator("scene.sk_fcurves_offset", icon="FORCE_HARMONIC")
				col = box.column()
				col.prop_search(stProps, "sk_fcurves_group_objects", bpy.data, "groups")
				col.prop_search(stProps, "sk_fcurves_group_targets", bpy.data, "groups")
				col.operator("scene.sk_fcurves_multi_offset", icon="FORCE_HARMONIC")
			else:
				col.label("No animation on Shape Keys")
			
			col = layout.column(align=True)
			col.separator()





		col.prop(stProps, "sk_nla", icon="NLA")
		if stProps.sk_nla:
			box = layout.box()
			col = box.column(align=True)

			if (obj.data and obj.data.shape_keys and
			                 obj.data.shape_keys.animation_data):
				anim = obj.data.shape_keys.animation_data
				if anim.action:
					col.operator("scene.sk_nla_strips_create", icon="NLA_PUSHDOWN")
				
				if (anim.nla_tracks and anim.nla_tracks[0].strips):
					col.operator("scene.sk_nla_strips_to_fcurves", icon="IPO_BEZIER")
					col.operator("scene.sk_nla_sync_length", icon="TIME")
					col.operator("scene.sk_nla_link_to_active", icon="LINKED")
					col.separator()
					col.prop(stProps, "sk_nla_offset")
					col.prop(stProps, "sk_nla_threshold")
					col.operator("scene.sk_nla_strips_offset", icon="FORCE_HARMONIC")
					col = box.column()
					col.prop_search(stProps, "sk_nla_group_objects", bpy.data, "groups")
					col.prop_search(stProps, "sk_nla_group_targets", bpy.data, "groups")
					col.operator("scene.sk_nla_strips_multi_offset", icon="FORCE_HARMONIC")
			else:
				col.label("No animation on Shape Keys")
				
			col = layout.column(align=True)
			col.separator()





		col.prop(stProps, "sk_drivers", icon="DRIVER")
		if stProps.sk_drivers:
			box = layout.box()
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
				col.separator()
				col.separator()

				col.prop(stProps, "sk_drivers_dist_trigger", icon="AUTOMERGE_ON")
				if stProps.sk_drivers_dist_trigger:
					col.separator()
					col.operator("scene.sk_driver_func_reg", icon="COPY_ID")
					col.operator("scene.sk_eval_time_reset", icon="FILE_REFRESH")
					col.separator()
					col.prop(stProps, "sk_drivers_expression_func", text="")
					col.operator("scene.sk_expression_func_set", icon="COPYDOWN")









class ObjectTools(Panel):
	
	bl_label = "Object Tools"
	bl_idname = "VIEW3D_PT_object_tools"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "objectmode"
	bl_category = "Shape Tools"

	@classmethod
	def poll(cls, context):
		return context.active_object

	def draw(self, context):
		sce = context.scene
		stProps = sce.stProps
		obj = context.active_object
		
		layout = self.layout
		col = layout.column(align=True)


		col.prop(stProps, "ob_fcurves", icon="IPO")
		if stProps.ob_fcurves:
			box = layout.box()
			col = box.column(align=True)
			
			if (obj.animation_data and obj.animation_data.action):
				col.operator("scene.ob_fcurves_link", icon="LINKED")
				col.operator("scene.ob_fcurves_copy", icon="COPYDOWN")
				col.separator()
				col.prop(stProps, "ob_fcurves_offset")
				col.prop(stProps, "ob_fcurves_threshold")
				col.operator("scene.ob_fcurves_offset", icon="FORCE_HARMONIC")
				col = box.column()
				col.prop_search(stProps, "ob_fcurves_group_objects", bpy.data, "groups")
				col.prop_search(stProps, "ob_fcurves_group_targets", bpy.data, "groups")
				col.operator("scene.ob_fcurves_multi_offset", icon="FORCE_HARMONIC")
			else:
				col.label("No Animation on object")
			
			col = layout.column(align=True)
			col.separator()






		col.prop(stProps, "ob_nla", icon="NLA")
		if stProps.ob_nla:
			box = layout.box()
			col = box.column(align=True)
		
			if obj.animation_data:
				anim = obj.animation_data
				if anim.action:
					col.operator("scene.ob_nla_strips_create", icon="NLA_PUSHDOWN")
				
				if (anim.nla_tracks and anim.nla_tracks[0].strips):
					col.operator("scene.ob_nla_strips_to_fcurves", icon="IPO_BEZIER")
					col.operator("scene.ob_nla_sync_length", icon="TIME")
					col.operator("scene.ob_nla_link_to_active", icon="LINKED")
					col.separator()
					col.prop(stProps, "ob_nla_offset")
					col.prop(stProps, "ob_nla_threshold")
					col.operator("scene.ob_nla_strips_offset", icon="FORCE_HARMONIC")
					col = box.column()
					col.prop_search(stProps, "ob_nla_group_objects", bpy.data, "groups")
					col.prop_search(stProps, "ob_nla_group_targets", bpy.data, "groups")
					col.operator("scene.ob_nla_strips_multi_offset", icon="FORCE_HARMONIC")
			else:
				col.label("No animation on object")
			
			col = layout.column(align=True)
			col.separator()






		col.prop(stProps, "transforms", icon="MANIPUL")
		if stProps.transforms:

			box = layout.box()
			col = box.column(align=True)
			
			col.operator("object.anim_transforms_to_deltas", icon="ACTION", text="Transforms to Deltas")
			
			col.label("Slow Parent:")
			col.prop(stProps, "slow_parent_offset")
			col.operator("scene.slow_parent_offset", icon="FORCE_DRAG")
