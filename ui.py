import bpy

class VIEW3D_PT_SubdivisionPanel(bpy.types.Panel):
    bl_label = "Subdivision Methods"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Subdiv"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        row.prop(scene, "subd_iterations", text="Iterations")
        
        col = layout.column(align=True)
        props = col.operator("object.apply_subdivision", text="Apply Catmull-Clark")
        props.algorithm = 'CATMULL_CLARK'
        props.iterations = scene.subd_iterations
        
        props = col.operator("object.apply_subdivision", text="Apply Doo-Sabin")
        props.algorithm = 'DOO_SABIN'
        props.iterations = scene.subd_iterations

def register():
    bpy.utils.register_class(VIEW3D_PT_SubdivisionPanel)
    bpy.types.Scene.subd_iterations = bpy.props.IntProperty(
        name="Subdivision Iterations",
        default=1,
        min=1,
        max=6
    )

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_SubdivisionPanel)
    del bpy.types.Scene.subd_iterations