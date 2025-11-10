# SEE API DOC : driver_add
# SEE API DOC : FCurve, 

# note : bpy.types.DriverVariable.targets is a list
# also see : DriverVariableHere.targets[0].id (for obj)
# also see : DriverVariableHere.targets[0].data_path (dig in to the property)

# output from console
# >>> dv_var.targets[0].data_path
# 'pose.bones["shoulder.L"].rotation_euler[0]'
#
# >>> dv_var.targets[0].id
# bpy.data.objects['metarig']



import bpy
from . import common
from . import runtime_var




def check_is_selected(self, selected_pose_bones_list):
    if selected_pose_bones_list == None:
        self.report({'ERROR',}, "No Pose Bone' is selected")
        return False
    if selected_pose_bones_list == []:
        self.report({'ERROR',}, "No Pose Bone is selected")
        return False
    return True


BL_ID_MARK_HOST_POSE_BONES_OPS = f"{common._ID_PREFIX}.mark_host_pose_bones"
class MarkHostPoseBones(bpy.types.Operator):
    bl_idname = BL_ID_MARK_HOST_POSE_BONES_OPS
    bl_label = "Mark Host Bones"
    bl_description = "" # TODO add description.
    bl_options = {'REGISTER',}

    def execute(self, context):
        selected_pose_bones_list = context.selected_pose_bones
        print(runtime_var.mark_host_pose_bones_list)
        if check_is_selected(self, selected_pose_bones_list):
            runtime_var.mark_host_pose_bones_list = selected_pose_bones_list
        return {'FINISHED'}




BL_ID_MARK_TARGET_POSE_BONES_OPS = f"{common._ID_PREFIX}.mark_target_pose_bones"
class MarkTargetPoseBones(bpy.types.Operator):
    bl_idname = BL_ID_MARK_TARGET_POSE_BONES_OPS
    bl_label = "Mark Target Bones"
    bl_description = "" # TODO add description.
    bl_options = {'REGISTER',}

    def execute(self, context):
        selected_pose_bones_list = context.selected_pose_bones
        print(runtime_var.mark_target_pose_bones_list)
        if check_is_selected(self, selected_pose_bones_list):
            runtime_var.mark_target_pose_bones_list = selected_pose_bones_list
        return {'FINISHED'}





BL_ID_BIND_DRIVER_OPS = f"{common._ID_PREFIX}.bind_driver"
class BindDriver(bpy.types.Operator):
    bl_idname = BL_ID_BIND_DRIVER_OPS
    bl_label = "Bind Driver"
    bl_description = "" # TODO add description.
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # ctx_prop = context.scene.simple_retargetor_prop
        #
        # # driver_sub_ops Driver Creation
        # loc_fcurve_xyz_list = []
        # rot_fcurve_xyz_list = []
        # scl_fcurve_xyz_list = []
        # for p_bone in runtime_var.mark_target_pose_bones_list:
        #     loc_x_fcurve = p_bone.driver_add("location", 0)
        #     loc_y_fcurve = p_bone.driver_add("location", 1)
        #     loc_z_fcurve = p_bone.driver_add("location", 2)
        #
        #     rot_fcurve_xyz_list.append(p_bone..driver_add("rotation_euler"))
        #     scl_fcurve_xyz_list.append(p_bone..driver_add("scale"))
        #
        #
        return {'FINISHED'}




_classes = (
        MarkHostPoseBones,
        MarkTargetPoseBones,
        BindDriver,
        )

_class_register, _class_unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _class_register()
    pass


def unregister():
    _class_unregister()
    pass



