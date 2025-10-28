import bpy


# SEE: PROP_simple_retargetor -> rot_mapping_preset
class PROP_rot_maping_preset(bpy.types.PropertyGroup):

    to_map_xyz: bpy.props.BoolVectorProperty(
            name="",
            default=(True,True,True,),
            subtype='XYZ',
            )

    invert_preset: bpy.props.BoolVectorProperty(
            name="",
            default=(False,False,False,),
            subtype='XYZ',
            )

    _ENUM_EULER_ORDER = [
            ('AUTO',"Auto selected", "", '', 0),
            ('XYZ', "XYZ Euler",     "", '', 1),
            ('XZY', "XZY Euler",     "", '', 2),
            ('YXZ', "YXZ Euler",     "", '', 3),
            ('YZX', "YZX Euler",     "", '', 4),
            ('ZXY', "ZXY Euler",     "", '', 5),
            ('ZYX', "ZYX Euler",     "", '', 6),
            ]

    euler_order_preset: bpy.props.EnumProperty(
            items=_ENUM_EULER_ORDER,
            name="",
            default='AUTO',
            )

    _ENUM_XYZ_ITEMS = [
                ('x', "X", "", '', 0),
                ('y', "Y", "", '', 1),
                ('z', "Z", "", '', 2),
                ]

    x_from: bpy.props.EnumProperty(
            items=_ENUM_XYZ_ITEMS,
            name="",
            default='x',
            )

    y_from: bpy.props.EnumProperty(
            items=_ENUM_XYZ_ITEMS,
            name="",
            default='y',
            )

    z_from: bpy.props.EnumProperty(
            items=_ENUM_XYZ_ITEMS,
            name="",
            default='z',
            )


# SEE: _prop_register()
class PROP_simple_retargetor(bpy.types.PropertyGroup):
    loc_maping_preset: bpy.props.BoolVectorProperty(
            name="",
            default=(True,True,True,),
            subtype='XYZ'
            )

    rot_mapping_preset: bpy.props.PointerProperty(
            type=PROP_rot_maping_preset
            )


    scale_mapping_preset: bpy.props.BoolVectorProperty(
            name="",
            default=(True,True,True,),
            subtype='XYZ'
            )

    mark_host_bones: list[bpy.types.PoseBone]
    mark_target_bones: list[bpy.types.PoseBone]


_class = (
        PROP_rot_maping_preset,
        PROP_simple_retargetor,
        )

_class_register, _class_unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _class_register()
    bpy.types.Scene.simple_retargetor_prop = bpy.props.PointerProperty(type=PROP_simple_retargetor)


def unregister():
    _class_unregister()
    del bpy.types.Scene.PROP_simple_retageting
