# operators.py
import bpy
from .algorithms import loop, doosabin, root3

class SUBDIV_OT_apply_subdivision(bpy.types.Operator):
    bl_idname = "subdiv.apply_subdivision"
    bl_label = "Apply Subdivision"

    @classmethod
    def poll(cls, context):
        return (context.active_object and context.active_object.type == 'MESH')

    def execute(self, context):
        obj = context.active_object
        wm = context.window_manager

        method = wm.subdiv_method
        levels = wm.subdiv_levels

        # Ensure the object is selected and active
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj

        current_mode = obj.mode

        try:
            # Apply subdivision in Object Mode
            bpy.ops.object.mode_set(mode='OBJECT')  # Switch to Object Mode if in Edit Mode

            if method == 'CATMULL_CLARK':
                mod = obj.modifiers.new(name="Subdiv", type='SUBSURF')
                mod.levels = levels
                mod.render_levels = levels
                mod.subdivision_type = 'CATMULL_CLARK'
                bpy.ops.object.modifier_apply(modifier=mod.name)

            elif method == 'SIMPLE':
                mod = obj.modifiers.new(name="SimpleSubdiv", type='SUBSURF')
                mod.levels = levels
                mod.render_levels = levels
                mod.subdivision_type = 'SIMPLE'
                bpy.ops.object.modifier_apply(modifier=mod.name)

            elif method == 'DOO_SABIN':
                success, msg = doosabin.doosabin_subdivide(obj, levels)
                if not success:
                    self.report({'ERROR'}, msg)
                    return {'CANCELLED'}

            elif method == 'LOOP':
                success, msg = loop.loop_subdivide(obj, levels)
                if not success:
                    self.report({'ERROR'}, msg)
                    return {'CANCELLED'}

            elif method == 'ROOT3':
                success, msg = root3.root3_subdivide(obj, levels)
                if not success:
                    self.report({'ERROR'}, msg)
                    return {'CANCELLED'}

        except Exception as e:
            self.report({'ERROR'}, f"Subdivision failed: {str(e)}")
            return {'CANCELLED'}

        finally:
            # Always return to original mode
            bpy.ops.object.mode_set(mode=current_mode)

        self.report({'INFO'}, f"Applied {method} subdivision ({levels} levels)")
        return {'FINISHED'}

def register():
    """Register the operator"""
    bpy.utils.register_class(SUBDIV_OT_apply_subdivision)

def unregister():
    """Unregister the operator"""
    bpy.utils.unregister_class(SUBDIV_OT_apply_subdivision)
