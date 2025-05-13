bl_info = {
    "name": "Subdivision Methods",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > UI > Subdiv",
    "description": "Advanced subdivision surface algorithms",
    "category": "Mesh",
}

from . import operators, ui

def register():
    operators.register()
    ui.register()

def unregister():
    ui.unregister()
    operators.unregister()