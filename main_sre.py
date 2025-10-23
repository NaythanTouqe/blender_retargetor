import bpy

_ID_PREFIX = "simple_retargetor"




# SEE: RNA_PROP_simple_retargeting -> rot_maping_from_preset
class RNA_PROP_rot_maping_from_preset(bpy.types.PropertyGroup):
    _ENUM_XYZ = [
                ('x', "X", "", '', 0),
                ('y', "Y", "", '', 1),
                ('z', "Z", "", '', 2),
                ]

    x_from: bpy.props.EnumProperty(
            items=_ENUM_XYZ,
            name="",
            default='x', # X from X
            )

    y_from: bpy.props.EnumProperty(
            items=_ENUM_XYZ,
            name="",
            default='y', # Y from Y
            )

    z_from: bpy.props.EnumProperty(
            items=_ENUM_XYZ,
            name="",
            default='z', # Z from Z
            )


# SEE: _prop_register()
class RNA_PROP_simple_retargeting(bpy.types.PropertyGroup):
    loc_maping_preset: bpy.props.BoolVectorProperty(name="", default=(True,True,True,) ,subtype='XYZ')

    _ENUM_EULER_ORDER = [
            ('AUTO',"Auto selected", "", '', 0),
            ('XYZ', "XYZ Euler",     "", '', 1),
            ('XZY', "XZY Euler",     "", '', 2),
            ('YXZ', "YXZ Euler",     "", '', 3),
            ('YZX', "YZX Euler",     "", '', 4),
            ('ZXY', "ZXY Euler",     "", '', 5),
            ('ZYX', "ZYX Euler",     "", '', 6),
            ]
    rot_maping_to_preset: bpy.props.BoolVectorProperty(name="", default=(True,True,True,) ,subtype='XYZ')
    rot_maping_from_preset: bpy.props.PointerProperty(type=RNA_PROP_rot_maping_from_preset)
    rot_maping_invert_preset: bpy.props.BoolVectorProperty(name="", default=(False,False,False,) ,subtype='XYZ')
    rot_maping_euler_order_preset: bpy.props.EnumProperty(items=_ENUM_EULER_ORDER, name="", default='AUTO')

    scale_mapping_preset: bpy.props.BoolVectorProperty(name="", default=(True,True,True,) ,subtype='XYZ')

    mark_host_bones: list[bpy.types.PoseBone]
    mark_target_bones: list[bpy.types.PoseBone]


class _PROTOTYPE_VIEW_3D_PT_ui():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Retargetor'
    bl_label = 'Simple Retargetor'


class VIEW_3D_PT_ui_master(_PROTOTYPE_VIEW_3D_PT_ui, bpy.types.Panel):
    bl_idname = f"VIEW_3D_PT_{_ID_PREFIX}_ui_obj"


    # TODO : make sure that UI onlly show in 'POSE'
    # @classmethod
    # def poll(cls, context):
    #     return context.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        row = layout.row(align=True)
        row.label(text="In Object mode", icon='OBJECT_DATAMODE')

        _ctx_prop_ref = context.scene.simple_retargeting_prop


        # TODO : split location, rotation, scale In to it's own sub panel
        # SEE API DOC : bl_owner_id

        # Location
        layout.separator(factor=1.0, type='LINE')
        col = layout.column(align=True)
        row = layout.row(align=True)
        col.label(text="Copy Location:")
        row.prop(_ctx_prop_ref, "loc_maping_preset", toggle=1,)

        layout.separator(factor=1.0, type='SPACE')

        # Rotation
        col = layout.column(align=True)
        col.label(text="Copy Rotation:")
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(_ctx_prop_ref, "rot_maping_to_preset", toggle=1,)


        # Rotation Euler XYZ map from
        row = layout.row(align=True)

        #X
        col_x = row.column(align=True)
        col_x.label(text="X from:")
        col_x.prop(_ctx_prop_ref.rot_maping_from_preset, "x_from", toggle=1,)

        row.separator(factor=1.0, type='SPACE')


        #Y
        col_y = row.column(align=True)
        col_y.label(text="Y from:")
        col_y.prop(_ctx_prop_ref.rot_maping_from_preset, "y_from", toggle=1,)

        row.separator(factor=1.0, type='SPACE')


        #Z
        col_z = row.column(align=True)
        col_z.label(text="Z from:")
        col_z.prop(_ctx_prop_ref.rot_maping_from_preset, "z_from", toggle=1,)

        col = layout.column(align=True)
        col.label(text="Invert:")
        row = col.row(align=True)
        row.prop(_ctx_prop_ref, "rot_maping_invert_preset", toggle=1,)

        # Rotation Euler Order
        col = layout.column(align=True)
        col.label(text="Euler Order")
        row = col.row(align=True)
        row.prop(_ctx_prop_ref, "rot_maping_euler_order_preset")


        # Scale
        col = layout.column(align=True)
        col.separator(factor=2.0, type='SPACE')
        col.label(text="Copy Scale:")
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(_ctx_prop_ref, "scale_mapping_preset", toggle=1,)
        # Scale axis swap/mapping, inherit from rotation axis swap/mapping


def _prop_register():
    bpy.types.Scene.simple_retargeting_prop = bpy.props.PointerProperty(type=RNA_PROP_simple_retargeting)


def _prop_unregister():
    del bpy.types.Scene.PROP_simple_retageting


_classes = (
        RNA_PROP_rot_maping_from_preset,
        RNA_PROP_simple_retargeting,
        VIEW_3D_PT_ui_master,
        )

_class_register, _class_unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _class_register()
    _prop_register()


def unregister():
    _class_unregister()
    _prop_unregister()

