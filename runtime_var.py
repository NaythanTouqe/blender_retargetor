# Runtime reference holder.
# what a fucking dragon dent.

mark_host_pose_bones_list = []
mark_target_pose_bones_list = []


loc_fcurve_list = []
rot_fcurve_list = []
scale_fcurve_list = []

bone_mapping_dict = {}


# structure of driver binding journals
# [
#         host_bone.obj,
#         host_bone.name,
#         target_bone.obj,
#         target_bone.name,
#
#         global_from[xfrom,yfrom,zfrom],
#
#         loc_yes[x,y,z],
#         loc_inherit_global_from,
#         loc_from[xfrom,yfrom,zfrom],
#
#         rot_yes[x,y,z],
#         rot_inherit_global_from,
#         rot_from[xfrom,yfrom,zfrom],
#         rot_order
#
#         scl_yes[x,y,z],
#         scl_inherit_global_from,
#         scl_from[xfrom,yfrom,zfrom],
#         ]

