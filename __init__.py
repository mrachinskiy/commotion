bl_info = {
	'name': 'Commotion',
	'author': 'Mikhail Rachinskiy',
	'version': (1, 5, 0),
	'blender': (2, 77, 0),
	'location': '3D View > Tool Shelf',
	'description': 'Animation offset tools for motion graphics.',
	'wiki_url': 'https://github.com/mrachinskiy/commotion#readme',
	'tracker_url': 'https://github.com/mrachinskiy/commotion/issues',
	'category': 'Animation',
	}


if 'bpy' in locals():
	import importlib
	importlib.reload(preferences)
	importlib.reload(ui)
	importlib.reload(ops_anim)
	importlib.reload(ops_driver)
	importlib.reload(ops_shapekey)
	importlib.reload(ops_slow_parent)
	importlib.reload(ops_utils)
else:
	import bpy
	from bpy.props import PointerProperty, CollectionProperty
	from . import (
		preferences,
		ui,
		ops_anim,
		ops_driver,
		ops_shapekey,
		ops_slow_parent,
		ops_utils,
		)

	# Extern
	from . import addon_updater_ops


classes = (
	preferences.PREFS_Commotion_Props,
	preferences.SCENE_Commotion_Props,
	preferences.WM_Commotion_SK_Collection,

	ui.VIEW3D_PT_Commotion_Shape_Key_Tools,
	ui.VIEW3D_PT_Commotion_Object_Tools,

	ops_shapekey.OBJECT_OT_Commotion_SK_Coll_Refresh,
	ops_shapekey.OBJECT_OT_Commotion_SK_Interpolation_Set,
	ops_shapekey.ANIM_OT_Commotion_SK_Auto_Keyframes,
	ops_shapekey.OBJECT_OT_Commotion_SK_Reset_Eval_Time,

	ops_anim.ANIM_OT_Commotion_Animation_Link,
	ops_anim.ANIM_OT_Commotion_Animation_Copy,
	ops_anim.ANIM_OT_Commotion_FCurves_To_NLA,
	ops_anim.ANIM_OT_Commotion_NLA_To_FCurves,
	ops_anim.NLA_OT_Commotion_Sync_Length,
	ops_anim.ANIM_OT_Commotion_Offset_Cursor,
	ops_anim.ANIM_OT_Commotion_Offset_Multitarget,
	ops_anim.ANIM_OT_Commotion_Offset_Name,

	ops_driver.ANIM_OT_Commotion_SK_Driver_Distance_Set,
	ops_driver.ANIM_OT_Commotion_SK_Driver_Expression_Copy,
	ops_driver.ANIM_OT_Commotion_SK_Driver_Target_Remap,
	ops_driver.ANIM_OT_Commotion_SK_Driver_Function_Register,
	ops_driver.ANIM_OT_Commotion_SK_Driver_Func_Expression_Get,
	ops_driver.ANIM_OT_Commotion_SK_Driver_Func_Expression_SET,

	ops_slow_parent.OBJECT_OT_Commotion_Slow_Parent_Offset,
	ops_slow_parent.OBJECT_OT_Commotion_Slow_Parent_Toggle,

	ops_utils.VIEW3D_OT_Commotion_Preset_Apply,
	ops_utils.OBJECT_OT_Commotion_Add_To_Group_Objects,
	ops_utils.OBJECT_OT_Commotion_Add_To_Group_Targets,
	)


def register():
	addon_updater_ops.register(bl_info)

	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.Scene.commotion = PointerProperty(type=preferences.SCENE_Commotion_Props)
	bpy.types.WindowManager.commotion_skcoll = CollectionProperty(type=preferences.WM_Commotion_SK_Collection)


def unregister():
	addon_updater_ops.unregister()

	for cls in classes:
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.commotion
	del bpy.types.WindowManager.commotion_skcoll


if __name__ == '__main__':
	register()
