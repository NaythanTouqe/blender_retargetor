import bpy
from . import common
from . import operation


class _PROTOTYPE_VIEW_3D_PT_ui():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Retargetor'



class VIEW_3D_PT_ui_master(
        _PROTOTYPE_VIEW_3D_PT_ui,
        bpy.types.Panel
        ):
    bl_label = 'Simple Retargetor'
    bl_idname = f"VIEW_3D_PT_{common._ID_PREFIX}_ui_master"


    # TODO : make sure that UI onlly show in 'POSE'
    @classmethod
    def poll(cls, context):
        # return (context.mode == 'POSE')
        # for testing
        return ((context.mode == 'POSE') or (context.mode == 'OBJECT'))

    def draw(self, context):
        pass




#LOC
class VIEW_3D_PT_ui_sub_location(
        _PROTOTYPE_VIEW_3D_PT_ui,
        bpy.types.Panel
        ):
    bl_label = 'Copy Location'
    bl_idname = f"VIEW_3D_PT_{common._ID_PREFIX}_ui_sub_location"
    bl_parent_id = f"VIEW_3D_PT_{common._ID_PREFIX}_ui_master"


    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        #see: ./properties.py -> def register()
        _CTX_PROP_REF = context.scene.simple_retargetor_prop

        row = layout.row(align=True)
        row.prop(_CTX_PROP_REF, "loc_want_to_map", toggle=1,)

        layout.separator(factor=1.0, type='SPACE')




#ROT
class VIEW_3D_PT_ui_sub_rotation(_PROTOTYPE_VIEW_3D_PT_ui, bpy.types.Panel):
    bl_label = 'Copy Rotation'
    bl_idname = f"VIEW_3D_PT_{common._ID_PREFIX}_ui_sub_rotation"
    bl_parent_id = f"VIEW_3D_PT_{common._ID_PREFIX}_ui_master"


    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        #see: ./properties.py -> def register()
        _CTX_PROP_REF = context.scene.simple_retargetor_prop

        # Axis_to_map
        col = layout.column(align=True)
        col.label(text="Copy Rotation:")
        row = layout.row(align=True)
        row.prop(_CTX_PROP_REF.rot_preset_group, "to_map_xyz", toggle=1,)

        # Rotation Euler XYZ map from
        row = layout.row(align=True)
        #X
        col_x = row.column(align=True)
        col_x.label(text="X from:")
        col_x.prop(_CTX_PROP_REF.rot_preset_group, "x_from", toggle=1,)
        row.separator(factor=1.0, type='SPACE')
        #Y
        col_y = row.column(align=True)
        col_y.label(text="Y from:")
        col_y.prop(_CTX_PROP_REF.rot_preset_group, "y_from", toggle=1,)
        row.separator(factor=1.0, type='SPACE')
        #Z
        col_z = row.column(align=True)
        col_z.label(text="Z from:")
        col_z.prop(_CTX_PROP_REF.rot_preset_group, "z_from", toggle=1,)

        #Axis to inverted
        col = layout.column(align=True)
        col.label(text="Invert:")
        row = col.row(align=True)
        row.prop(_CTX_PROP_REF.rot_preset_group, "to_invert_xyz", toggle=1,)

        # Rotation Euler Order
        col = layout.column(align=True)
        col.label(text="Euler Order")
        row = col.row(align=True)
        row.prop(_CTX_PROP_REF.rot_preset_group, "euler_order")

        layout.separator(factor=1.0, type='SPACE')




#SCALE
class VIEW_3D_PT_ui_sub_scale(_PROTOTYPE_VIEW_3D_PT_ui, bpy.types.Panel):
    bl_label = 'Copy Scale'
    bl_idname = f"VIEW_3D_PT_{common._ID_PREFIX}_ui_sub_scale"
    bl_parent_id = f"VIEW_3D_PT_{common._ID_PREFIX}_ui_master"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        #see: ./properties.py -> def register()
        _CTX_PROP_REF = context.scene.simple_retargetor_prop

        row = layout.row(align=True)
        row.prop(_CTX_PROP_REF, "scale_want_to_map", toggle=1,)
        # Scale axis swap/mapping, inherit from rotation axis swap/mapping




class VIEW_3D_PT_ui_sub_operation(_PROTOTYPE_VIEW_3D_PT_ui, bpy.types.Panel):
    bl_label = 'Operation'
    bl_idname = f"VIEW_3D_PT_{common._ID_PREFIX}_ui_sub_operation"
    bl_parent_id = f"VIEW_3D_PT_{common._ID_PREFIX}_ui_master"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        # marking bones
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator(operation.BL_ID_MARK_HOST_POSE_BONES_OPS)
        row.operator(operation.BL_ID_MARK_TARGET_POSE_BONES_OPS)

        row = col.row(align=True)
        row.operator(operation.BL_ID_SELECT_MARK_HOST_POSE_BONES_OPS)
        row.operator(operation.BL_ID_SELECT_MARK_TARGET_POSE_BONES_OPS)

        # driver fuckery ui
        col = layout.column(align=True)
        col.operator(operation.BL_ID_BIND_DRIVER_OPS)
        col.operator(operation.BL_ID_CLEAR_DRIVER_FROM_SELECTED)





_classes = (
        VIEW_3D_PT_ui_master,
        VIEW_3D_PT_ui_sub_location,
        VIEW_3D_PT_ui_sub_rotation,
        VIEW_3D_PT_ui_sub_scale,
        VIEW_3D_PT_ui_sub_operation,
        )

_class_register, _class_unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _class_register()


def unregister():
    _class_unregister()


