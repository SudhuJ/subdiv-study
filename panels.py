# panel.py
import bpy
from bpy.types import Panel

class SUBDIV_PT_control_panel(Panel):
    """Creates the UI panel in the 3D View sidebar"""
    bl_idname = "SUBDIV_PT_control_panel"
    bl_label = "Subdivision Methods"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    bl_context = "objectmode"  # Ensure this shows in Object Mode

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        layout.label(text="Subdivision Method:")
        layout.prop(wm, "subdiv_method", text="")

        layout.label(text="Subdivision Levels:")
        layout.prop(wm, "subdiv_levels")

        layout.operator("subdiv.apply_subdivision", text="Apply Subdivision", icon='MOD_SUBSURF')


def register():
    """Register panel and UI properties"""
    bpy.types.WindowManager.subdiv_method = bpy.props.EnumProperty(
        items=[
            ('CATMULL_CLARK', "Catmull-Clark", "Quad-based smoothing"),
            ('SIMPLE', "Simple", "Basic linear subdivision"),
            ('LOOP', "Loop", "Triangle-based smoothing"),
            ('DOO_SABIN', "Doo-Sabin", "Face-based smoothing subdivision"),
            ('ROOT3', "Root3", "Root3 subdivision (face-based)"),
        ],
        default='CATMULL_CLARK',
        name="Method"
    )

    bpy.types.WindowManager.subdiv_levels = bpy.props.IntProperty(
        name="Levels",
        default=1,
        min=0,
        max=6,
        description="Number of subdivision iterations"
    )

    bpy.utils.register_class(SUBDIV_PT_control_panel)


def unregister():
    """Unregister panel and properties"""
    del bpy.types.WindowManager.subdiv_method
    del bpy.types.WindowManager.subdiv_levels
    bpy.utils.unregister_class(SUBDIV_PT_control_panel)
