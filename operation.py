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

class MarkHostPoseBonesOperator(bpy.types.Operator):
    bl_idname = f"{common._ID_PREFIX}.mark_host_pose_bones"
    bl_label = "Mark Host Bones"
    bl_description = "" # TODO <-
    bl_options = {'REGISTOR', 'UNDO'}

    def execute(self, context):
        print("Hello World")
        return {'FINISHED'}

