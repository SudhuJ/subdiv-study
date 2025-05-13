bl_info = {
    "name": "Subdivision Methods",
    "author": "Sudhanva Joshi",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Tool",
    "description": "Apply subdivision algorithms with customizable levels",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}

from . import operators
from . import panels

def register():
    operators.register()  # Register the operators
    panels.register()  # Register the panels

def unregister():
    panels.unregister()  # Unregister the panels
    operators.unregister()  # Unregister the operators

