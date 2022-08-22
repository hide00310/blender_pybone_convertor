import bpy
import importlib
import os
from mathutils import Matrix, Vector

bl_info = {
    'name': 'PyBone Convertor',
    'blender': (3, 2, 1),
    'location': '3D View > Right side panel > Misc > PyBone Convertor',
    'description': 'Convert bones using the user defined python script',
    'category': 'Rigging'
}

# =============================================
# UTILS


def _import_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _get_y_axis_roll_matrix(dst_bone_matrix, target_matrix):
    """
    get y-axis roll of target_matrix
    y-axis direction is same as dst_bone_matrix
    """
    # y-axis is dst y-axis
    ey = Vector( (dst_bone_matrix @ Vector([0, 1, 0, 0]))[:3] )
    # z-axis is cross product of target x-axis and dst y-axis
    ez = Vector( (target_matrix @ Vector([1, 0, 0, 0]))[:3] ).cross(ey)
    # x-axis
    ex = ey.cross(ez)
    # change-of-basis matrix
    R = Matrix([
        [ex[0], ey[0], ez[0], 0],
        [ex[1], ey[1], ez[1], 0],
        [ex[2], ey[2], ez[2], 0],
        [0, 0, 0, 1]
    ])
    return R

# =============================================
# PROPERTIES


class PyBoneConvertorPropertyGroup(bpy.types.PropertyGroup):
    script: bpy.props.StringProperty(
        name='Script',
        description='User defined python script path.\n"${.}" will resolve to "this_addon_file_directory/presets"',
        subtype='FILE_PATH',
    )
    source_armature: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name='Source Armature'
    )
    align_roll: bpy.props.BoolProperty(
        name='Align Roll',
        description='Align the roll of bones to the Source Armature'
    )
    add_not_existing_bones: bpy.props.BoolProperty(
        name='Add not existing bones',
        description='Add bones that exist in the Source Armature but not in the target armature'
    )
    remove_not_existing_bones: bpy.props.BoolProperty(
        name='Remove not existing bones',
        description='Remove bones that exist in the target armature but not in the Source Armature'
    )
    change_not_existing_bones_to_layers: bpy.props.BoolVectorProperty(
        name='Layers',
        description='Change the bones to the layers. The bones exist in the target armature but not in the Source Armature',
        subtype='LAYER',
        size=32,
    )


# =============================================
# OPERATOR CLASSES


class OBJECT_OT_pybone_convertor_convert(bpy.types.Operator):
    bl_idname = 'object.pybone_convertor_convert'
    bl_label = 'Convert bones using the user defined python script'
    bl_options = {'UNDO', 'REGISTER'}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object and
            context.active_object.type == 'ARMATURE'
        )

    def execute(self, context):
        props = bpy.context.scene.pybone_convertor_props
        armature = bpy.context.active_object
        if props.script != '':
            script_path = self._get_script_path(props.script)
            if not os.path.exists(script_path):
                self.report({'ERROR'}, 'Script file not exist:'+script_path)
                return {'CANCELLED'}

            script_module = _import_module('script_module', script_path)

            if not hasattr(script_module, 'rename'):
                self.report({'ERROR'}, 'Function "rename(context, name)" is not defined')
                return {'CANCELLED'}

            self._rename_bones(context, armature, script_module)

        src_armature = props.source_armature
        if src_armature:
            if props.align_roll:
                self._align_roll(armature, src_armature)
            if props.add_not_existing_bones:
                self._add_not_existing_bones(armature, src_armature)
            if props.remove_not_existing_bones:
                self._remove_not_existing_bones(armature, src_armature)
            layers = props.change_not_existing_bones_to_layers
            if any(layers):
                self._change_not_existing_bones_to_layers(armature, src_armature, layers)

        return {'FINISHED'}

    def _get_script_path(self, script_path):
        script_path = script_path.replace('${.}', os.path.dirname(__file__)+'/presets')
        return bpy.path.abspath(script_path)

    def _rename_bones(self, context, armature, script_module):
        for bone in armature.data.bones:
            bone.name = script_module.rename(context, bone.name)

    def _align_roll(self, dst_armature, src_armature):
        bpy.ops.object.mode_set(mode='EDIT')
        dst_bones = dst_armature.data.edit_bones
        src_bones = src_armature.data.bones

        for bone_name, src_bone in src_bones.items():
            if bone_name not in dst_bones:
                continue
            dst_bone = dst_bones[bone_name]
            # matrix that transforms a point from dst bone space into dst armature space.
            # the pose is same as the src bone viewed from world space.
            target_matrix = (
                dst_armature.matrix_world.inverted() @
                src_armature.matrix_world @
                src_bone.matrix_local
            )

            # only copy target y-axis roll
            R = _get_y_axis_roll_matrix(dst_bone.matrix, target_matrix)
            dst_bone.matrix = Matrix.Translation(Vector(dst_bone.head)) @ R
            bpy.context.view_layer.update()

    def _add_not_existing_bones(self, dst_armature, src_armature):
        bpy.ops.object.mode_set(mode='EDIT')
        dst_bones = dst_armature.data.edit_bones
        src_bones = src_armature.data.bones

        for bone_name, src_bone in src_bones.items():
            if bone_name in dst_bones:
                continue
            if not src_bone.parent:
                continue
            parent_name = src_bone.parent.name
            dst_parent_bone = dst_bones[parent_name]
            src_parent_bone = src_bones[parent_name]

            dst_bone = dst_bones.new(bone_name)
            dst_bone.parent = dst_parent_bone
            # matrix that transforms a point from dst bone space into dst armature space.
            # the pose is same as the src bone viewed from parent bone space.
            target_matrix = (
                dst_parent_bone.matrix @ 
                src_parent_bone.matrix_local.inverted() @
                src_bone.matrix_local
            )
            if src_bone.children:
                # divide dst parent bone in half
                dst_parent_bone.length /= 2
                dst_bone.head = dst_parent_bone.tail
                dst_bone.tail = dst_bones[src_bone.children[0].name].head
                # only copy target y-axis roll
                R = _get_y_axis_roll_matrix(dst_bone.matrix, target_matrix)
                dst_bone.matrix = Matrix.Translation(Vector(dst_bone.head)) @ R
                for child in src_bone.children:
                    dst_bones[child.name].parent = dst_bone
            else:
                dst_bone.head = dst_parent_bone.tail
                dst_bone.length = src_bone.length
                # only copy target rotation
                dst_bone.matrix = Matrix.LocRotScale(dst_parent_bone.tail, target_matrix.to_quaternion(), None)
            bpy.context.view_layer.update()

    def _remove_not_existing_bones(self, dst_armature, src_armature):
        bpy.ops.object.mode_set(mode='EDIT')
        dst_bones = dst_armature.data.edit_bones
        src_bones = src_armature.data.bones

        for bone_name in list(dst_bones.keys()):
            if bone_name not in src_bones:
                dst_bones.remove(dst_bones[bone_name])

    def _change_not_existing_bones_to_layers(self, dst_armature, src_armature, layers):
        bpy.ops.object.mode_set(mode='OBJECT')
        dst_bones = dst_armature.data.bones
        src_bones = src_armature.data.bones

        for bone_name, dst_bone in dst_bones.items():
            if bone_name not in src_bones:
                dst_bone.layers = layers


# =============================================
# UI PANEL CLASSES


class _PanelBase:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    columns = []

    def draw(self, context):
        col_layout = self.layout.column(align=True)
        for col in self.columns:
            if 'label' in col:
                text = (
                    col['label'](context)
                    if callable(col['label'])
                    else col['label']
                )
                col_layout.row().label(text=text)
            if 'prop' in col:
                col_layout.row().prop(context.scene.pybone_convertor_props, col['prop'])
            if 'operator' in col:
                col_layout.operator(col['operator'].bl_idname, text=col['text'])
        col_layout.separator()


class VIEW3D_PT_PyBoneConvertor(_PanelBase, bpy.types.Panel):
    bl_label = 'PyBone Convertor'

    columns = [
        {
            'label': lambda context: (
                'Target Armature: ' + context.active_object.name
                if (
                    context.active_object and
                    context.active_object.type == 'ARMATURE'
                )
                else 'Target Armature: None'
            )
        },
        {
            'prop': 'script',
        },
        {
            'operator': OBJECT_OT_pybone_convertor_convert,
            'text': 'Convert'
        }
    ]


class VIEW3D_PT_Source(_PanelBase, bpy.types.Panel):
    bl_label = 'Source'
    bl_parent_id = 'VIEW3D_PT_PyBoneConvertor'

    columns = [
        {
            'prop': 'source_armature',
        },
        {
            'prop': 'align_roll',
        },
        {
            'prop': 'add_not_existing_bones',
        },
        {
            'prop': 'remove_not_existing_bones',
        },
        {
            'prop': 'change_not_existing_bones_to_layers',
            'label': 'Change not existing bones to layers',
        },
    ]


# =============================================
# REGISTER


classes = [
    PyBoneConvertorPropertyGroup,
    OBJECT_OT_pybone_convertor_convert,
    VIEW3D_PT_PyBoneConvertor,
    VIEW3D_PT_Source,
]


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.pybone_convertor_props = bpy.props.PointerProperty(type=PyBoneConvertorPropertyGroup)


def unregister():
    from bpy.utils import unregister_class
    del bpy.types.Scene.pybone_convertor_props
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == '__main__':
    register()
