import bpy
from .algorithms.utils import apply_subdivision

class OBJECT_OT_ApplySubdivision(bpy.types.Operator):
    bl_idname = "object.apply_subdivision"
    bl_label = "Apply Subdivision"
    bl_options = {'REGISTER', 'UNDO'}

    algorithm: bpy.props.EnumProperty(
        name="Algorithm",
        items=[
            ('CATMULL_CLARK', "Catmull-Clark", "Standard subdivision algorithm"),
            ('DOO_SABIN', "Doo-Sabin", "Preserves face shapes better"),
        ],
        default='CATMULL_CLARK'
    )

    iterations: bpy.props.IntProperty(
        name="Iterations",
        description="Number of subdivision iterations",
        min=1,
        max=6,
        default=1
    )

    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object")
            return {'CANCELLED'}

        try:
            original_name = obj.data.name
            new_mesh = apply_subdivision(obj.data, self.algorithm, self.iterations)
            new_obj = bpy.data.objects.new(f"{obj.name}_subdivided", new_mesh)
            new_obj.matrix_world = obj.matrix_world
            
            # Link to collection and set selection
            context.collection.objects.link(new_obj)
            bpy.ops.object.select_all(action='DESELECT')
            new_obj.select_set(True)
            context.view_layer.objects.active = new_obj
            
            self.report({'INFO'}, f"Applied {self.algorithm} subdivision")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

def register():
    bpy.utils.register_class(OBJECT_OT_ApplySubdivision)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ApplySubdivision)