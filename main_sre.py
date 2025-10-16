import bpy

_ID_PREFIX = "simple_retargeting"

# Bones mapper
class bone_node:
    def __init__(
            self,
            bone_idx
            ):
        self.bone_idx = bone_idx
        self.childs_idx_list = []

    def append_child_idx(self, child_idx):
        self.childs_idx_list.append(child_idx)


class bones_mapper:
    def __init__(
            self,
            master_bones_list,
            ):
        self.master_bones_list = master_bones_list
        self.bones_node_list = []


    def mapping(self):
        name_to_idx_dict = {}
        # Construct Node
        for i, b in  enumerate(self.master_bones_list):
            name_to_idx_dict[b.name] = i
            node = bone_node(name_to_idx_dict[b.name])
            self.bones_node_list.append()
        # Link child-parent
        for i, b in  enumerate(self.master_bones_list):
        pass
        
        pass





# SEE: def _prop_register()
class RNA_PROP_Simple_retargeting(bpy.types.PropertyGroup):
    armature_host: bpy.props.PointerProperty(type=bpy.types.Armature)
    armature_target: bpy.props.PointerProperty(type=bpy.types.Armature)


class VIEW_3D_PT_ui_proto():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Retargeter'
    bl_label = 'Simple Retargeter'


class VIEW_3D_PT_ui_obj(VIEW_3D_PT_ui_proto, bpy.types.Panel):
    bl_idname = f"VIEW_3D_PT_{_ID_PREFIX}_ui_obj"

    @classmethod
    def poll(cls, context):
        return bpy.context.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.label(text="In Object mode", icon='OBJECT_DATAMODE')

        layout.separator(factor=1.0, type='LINE')

        warning_counter = 0

        col = layout.column(align=True)
        armature_prop = context.scene.simple_retargeting_prop
        if armature_prop.armature_host == None:
            col.label(text="WARNING : please select armature host")
            warning_counter+=1
        if armature_prop.armature_host == None:
            col.label(text="WARNING : please select armature target")
            warning_counter+=1
        if warning_counter == 0:
            col.label(text="NO WARNING")
        else:
            col.label(text=f"WARNING count {warning_counter}")
        layout.separator(factor=1.0, type='LINE')
        col = layout.column(align=False)
        # SEE: def _prop_register()
        col.prop(context.scene.simple_retargeting_prop, 'armature_host', text="Host")
        col.prop(context.scene.simple_retargeting_prop, 'armature_target', text="Target")




def _prop_register():
    bpy.types.Scene.simple_retargeting_prop = bpy.props.PointerProperty(type=RNA_PROP_Simple_retargeting)


def _prop_unregister():
    del bpy.types.Scene.PROP_simple_retageting


_classes = (
        RNA_PROP_Simple_retargeting,
        VIEW_3D_PT_ui_obj,
        )

_class_register, _class_unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _class_register()
    _prop_register()


def unregister():
    _class_unregister()
    _prop_unregister()


