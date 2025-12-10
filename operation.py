# SEE API DOC : driver_add
# SEE API DOC : FCurve, 

# note : bpy.types.DriverVariable.targets is a list
# also see : DriverVariableHere.targets[0].id (for obj)
# also see : DriverVariableHere.targets[0].data_path (dig in to the property)
#note : bpy.app.handlers.save_pre is the call back list before save file,
#SEE MORE : in bpy.app.handlers

# output from console
# >>> dv_var.targets[0].data_path
# 'pose.bones["shoulder.L"].rotation_euler[0]'
#
# >>> dv_var.targets[0].id
# bpy.data.objects['metarig']



#TODO: auto detect rotation system (euler or quaternion)
#TODO: auto select rotation system driver mapping (euler or quaternion)
#TODO: quaternion swap axis driver

# variable_acronym
# sel       = Select/Selected
# mk        = Mark
# h         = Host
# t         = Target
# p         = Pose
# b         = bone
# L         = list
# fcur      = fcurve
# rtv       = runtime_var

import bpy
from . import common
from . import runtime_var
from . import properties



# Error checking
def is_there_any_bone_to_operate_on(in_list):
    if in_list == None: return False
    if in_list == []: return False
    return True


#marking operation
# Error msg
#TODO: add description detail
ERR_MSG_NO_BONE_SEL = "No pose bones is selected"
#TODO: add description detail
ERR_MSG_NO_MARKED_BONE = "No marked pose bones"
#TODO: add description detail
ERR_MSG_ASYMMETRIC_MARKED_BONE = "Asymmetric marked bone"

BL_ID_ASSIGN_HOST_OPS = f"{common._ID_PREFIX}.assign_host"
class AssignHost(bpy.types.Operator):
    bl_idname = BL_ID_ASSIGN_HOST_OPS
    bl_label = "Assign Host"
    bl_description = "Mark a list of bones as the origin.\nThe list of bones where to take the data from"
    bl_options = {'REGISTER',}

    def execute(self, context):
        sel_pbL = context.selected_pose_bones
        if not is_there_any_bone_to_operate_on(sel_pbL):
            self.report({'ERROR',}, ERR_MSG_NO_BONE_SEL)
            return {'FINISHED'}
        runtime_var.mark_host_pose_bones_list = sel_pbL
        return {'FINISHED'}




BL_ID_ASSIGN_TARGET_OPS = f"{common._ID_PREFIX}.assign_target"
class AssignTarget(bpy.types.Operator):
    bl_idname = BL_ID_ASSIGN_TARGET_OPS
    bl_label = "Assign Target"
    bl_description = "Mark a list of bones as the target.\nThe list of bones where to put the data into"
    bl_options = {'REGISTER',}

    def execute(self, context):
        sel_pbL = context.selected_pose_bones
        if not is_there_any_bone_to_operate_on(sel_pbL):
            self.report({'ERROR',}, ERR_MSG_NO_BONE_SEL)
            return {'FINISHED'}
        runtime_var.mark_target_pose_bones_list = sel_pbL
        return {'FINISHED'}


# select marked bone operation
BL_ID_SELECT_HOST_OPS = f"{common._ID_PREFIX}.select_host"
class SelectHost(bpy.types.Operator):
    bl_idname = BL_ID_SELECT_HOST_OPS
    bl_label = "Select Host"
    bl_description = "" # TODO add description.
    bl_options = {'REGISTER',}

    def execute(self, context):
        mk_h_pbL = runtime_var.mark_host_pose_bones_list
        if not is_there_any_bone_to_operate_on(mk_h_pbL):
            self.report({'ERROR',}, ERR_MSG_NO_MARKED_BONE)
            return {'FINISHED'}
        for pb in mk_h_pbL:
            pb.bone.select = True
        return {'FINISHED'}


BL_ID_SELECT_TARGET_OPS = f"{common._ID_PREFIX}.select_target"
class SelectTarget(bpy.types.Operator):
    bl_idname = BL_ID_SELECT_TARGET_OPS
    bl_label = "Select Target"
    bl_description = "" # TODO add description.
    bl_options = {'REGISTER',}

    def execute(self, context):
        mk_t_pbL = runtime_var.mark_target_pose_bones_list
        if not is_there_any_bone_to_operate_on(mk_t_pbL):
            self.report({'ERROR',}, ERR_MSG_NO_MARKED_BONE)
            return {'FINISHED'}
        for pb in mk_t_pbL:
            pb.bone.select = True
        return {'FINISHED'}


# driver fuckery
BL_ID_BIND_DRIVER_OPS = f"{common._ID_PREFIX}.bind_driver"
class BindDriver(bpy.types.Operator):
    bl_idname = BL_ID_BIND_DRIVER_OPS
    bl_label = "Bind Driver"
    bl_description = "" # TODO add description.
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mk_h_pbL = runtime_var.mark_host_pose_bones_list
        mk_t_pbL = runtime_var.mark_target_pose_bones_list

        if not is_there_any_bone_to_operate_on(mk_h_pbL):
            self.report({'ERROR',}, ERR_MSG_NO_MARKED_BONE)
            return {'FINISHED'}
        if not is_there_any_bone_to_operate_on(mk_t_pbL):
            self.report({'ERROR',}, ERR_MSG_NO_MARKED_BONE)
            return {'FINISHED'}

        # ensure proper selection
        if len(mk_h_pbL) != len(mk_t_pbL):
            self.report({'ERROR',}, ERR_MSG_ASYMMETRIC_MARKED_BONE)
            return {'FINISHED',}

        # it may look stupid, but for sake of consistency.
        AXIS_X = 0
        AXIS_Y = 1
        AXIS_Z = 2

        # blender enum prop can only hold string, so here the conversion func
        def _enum_xyz_to_axis_num(v):
            if v == properties._ENUM_XYZ_ITEMS[0][0]:
                return AXIS_X
            if v == properties._ENUM_XYZ_ITEMS[1][0]:
                return AXIS_Y
            if v == properties._ENUM_XYZ_ITEMS[2][0]:
                return AXIS_Z
            else:
                print(v)
                # If this get send out. HOW THE FUCK did you get here.
                self.report({'ERROR',}, "HOW THE FUCK did you get here.")

        ctx_prop = context.scene.simple_retargetor_prop

        # fcurve holder
        loc_fucr_xyz_list = [[], [], []]
        rot_fucr_xyz_list = [[], [], []]
        scl_fucr_xyz_list = [[], [], []]

        # prop alias
        loc_xyz_yes = [
                ctx_prop.loc_want_to_map[AXIS_X],
                ctx_prop.loc_want_to_map[AXIS_Y],
                ctx_prop.loc_want_to_map[AXIS_Z],
                ]
        #TODO: add UI for loc axis swaping
        loc_xyz_from = [
                AXIS_X,
                AXIS_Y,
                AXIS_Z,
                ]
        #TODO: add UI for loc invert
        loc_xyz_invert = [
                False,
                False,
                False,
                ]

        rot_xyz_yes = [
                ctx_prop.rot_preset_group.to_map_xyz[AXIS_X],
                ctx_prop.rot_preset_group.to_map_xyz[AXIS_Y],
                ctx_prop.rot_preset_group.to_map_xyz[AXIS_Z],
                ]
        rot_xyz_from = [
                _enum_xyz_to_axis_num(ctx_prop.rot_preset_group.x_from),
                _enum_xyz_to_axis_num(ctx_prop.rot_preset_group.y_from),
                _enum_xyz_to_axis_num(ctx_prop.rot_preset_group.z_from),
                ]
        rot_xyz_invert = [
                ctx_prop.rot_preset_group.to_invert_xyz[AXIS_X],
                ctx_prop.rot_preset_group.to_invert_xyz[AXIS_Y],
                ctx_prop.rot_preset_group.to_invert_xyz[AXIS_Z],
                ]
        rot_euler_order = ctx_prop.rot_preset_group.euler_order

        # scl inherit "axis swap" and "axis invert"
        scl_xyz_yes = [
                ctx_prop.scale_want_to_map[AXIS_X],
                ctx_prop.scale_want_to_map[AXIS_Y],
                ctx_prop.scale_want_to_map[AXIS_Z],
                ]
        #TODO: add UI for scl invert
        scl_xyz_invert = [
                False,
                False,
                False,
                ]
        scl_xyz_from = rot_xyz_from
                # AXIS_X,
                # AXIS_Y,
                # AXIS_Z,
                # ]

        # ceate driver on target bones
        for pb in mk_t_pbL:
            for axis in [AXIS_X, AXIS_Y, AXIS_Z]:
                if loc_xyz_yes[axis]:
                    loc_fucr_xyz_list[axis].append(pb.driver_add("location", axis))
                if rot_xyz_yes[axis]:
                    rot_fucr_xyz_list[axis].append(pb.driver_add("rotation_euler", axis))
                if scl_xyz_yes[axis]:
                    scl_fucr_xyz_list[axis].append(pb.driver_add("scale", axis))

        # driver bindding
        def setup_driver(driver, target_id_type, target_id, target_path, inverted_val=False):
            driver.type = 'SCRIPTED'
            d_var = driver.variables.new()
            exprs = f"{driver.variables[0].name}"
            if inverted_val:
                exprs = f"-{driver.variables[0].name}"
            driver.expression = exprs
            d_var.targets[0].id_type = target_id_type
            d_var.targets[0].id = target_id
            d_var.targets[0].data_path = target_path

        def euler_order_guessing(swaped_xyz_list):
            x = AXIS_X
            y = AXIS_Y
            z = AXIS_Z
            # SEE: properties.py -> _ENUM_EULER_ORDER for those magic number
            if swaped_xyz_list == [x, y, z]: return properties._ENUM_EULER_ORDER[1][0]
            if swaped_xyz_list == [x, z, y]: return properties._ENUM_EULER_ORDER[2][0]
            if swaped_xyz_list == [y, x, z]: return properties._ENUM_EULER_ORDER[3][0]
            if swaped_xyz_list == [y, z, x]: return properties._ENUM_EULER_ORDER[4][0]
            if swaped_xyz_list == [z, x, y]: return properties._ENUM_EULER_ORDER[5][0]
            if swaped_xyz_list == [z, y, x]: return properties._ENUM_EULER_ORDER[6][0]
            else: self.report({'ERROR',}, "")

        # the actual driver fuckery happen here
        for idx, pb in enumerate(mk_h_pbL):

            # auto euler order selection
            if rot_euler_order == properties._ENUM_EULER_ORDER[0][0]:
                euler_order = euler_order_guessing(rot_xyz_from)
                if rot_xyz_yes[0] or rot_xyz_yes[1] or rot_xyz_yes[2]:
                    if mk_t_pbL[idx].rotation_mode != euler_order:
                        mk_t_pbL[idx].rotation_mode = euler_order
                else:
                    # if no any ROT axis enable. default to QUATERNION
                    mk_t_pbL[idx].rotation_mode = 'QUATERNION'
            else:
                mk_t_pbL[idx].rotation_mode = rot_euler_order

            # setup driver
            for axis in [AXIS_X, AXIS_Y, AXIS_Z]:
                if loc_xyz_yes[axis]:
                    setup_driver(
                            loc_fucr_xyz_list[axis][idx].driver,
                            'OBJECT',
                            pb.id_data,
                            f"pose.bones[\"{pb.name}\"].location[{loc_xyz_from[axis]}]",
                            loc_xyz_invert[axis]
                            )
                if rot_xyz_yes[axis]:
                    setup_driver(
                            rot_fucr_xyz_list[axis][idx].driver,
                            'OBJECT',
                            pb.id_data,
                            f"pose.bones[\"{pb.name}\"].rotation_euler[{rot_xyz_from[axis]}]",
                            rot_xyz_invert[axis]
                            )
                if scl_xyz_yes[axis]:
                    setup_driver(
                            scl_fucr_xyz_list[axis][idx].driver,
                            'OBJECT',
                            pb.id_data,
                            f"pose.bones[\"{pb.name}\"].scale[{scl_xyz_from[axis]}]",
                            scl_xyz_invert[axis]
                            )
        return {'FINISHED'}


BL_ID_CLEAR_DRIVER_FROM_SELECTED = f"{common._ID_PREFIX}.clear_driver_from_selected"
class ClearDriverFromSelected(bpy.types.Operator):
    bl_idname = BL_ID_CLEAR_DRIVER_FROM_SELECTED
    bl_label = "Clear Driver From Selected"
    bl_description = "" # TODO add description.
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        sel_pbL = context.selected_pose_bones
        if not is_there_any_bone_to_operate_on(sel_pbL):
            self.report({'ERROR',}, ERR_MSG_NO_BONE_SEL)
            return {'FINISHED'}

        sel_pbL.driver_del("location", -1)
        sel_pbL.driver_del("rotation_euler", -1)
        sel_pbL.driver_del("scale", -1)
        return {'FINISHED'}

_classes = (
        AssignHost,
        AssignTarget,
        SelectHost,
        SelectTarget,
        ClearDriverFromSelected,
        BindDriver,
        )

_class_register, _class_unregister = bpy.utils.register_classes_factory(_classes)


def register():
    _class_register()
    pass


def unregister():
    _class_unregister()
    pass


