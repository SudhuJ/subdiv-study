import bpy
import bmesh
from mathutils import Vector

def loop_subdivide(obj, levels=1):
    """Performs Loop subdivision on the given object for the specified number of levels"""
    try:
        # Ensure object is in object mode
        if obj.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        mesh = obj.data

        for _ in range(levels):
            bm = bmesh.new()
            bm.from_mesh(mesh)

            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()

            edge_map = {} 
            for edge in bm.edges:
                v1, v2 = edge.verts
                midpoint = (v1.co + v2.co) / 2.0 
                edge_map[edge] = bm.verts.new(midpoint)

            bm.verts.ensure_lookup_table()

            for vertex in bm.verts:
                if len(vertex.link_edges) == 3:
                    vertex.co = (3 / 8) * vertex.co + (1 / 8) * sum((edge.other_vert(vertex).co for edge in vertex.link_edges), Vector())
                else:
                    beta = 3 / (8 * len(vertex.link_edges))
                    neighbor_sum = sum((edge.other_vert(vertex).co for edge in vertex.link_edges), Vector())
                    vertex.co = (1 - len(vertex.link_edges) * beta) * vertex.co + beta * neighbor_sum

            faces_to_remove = []
            new_faces = []
            for face in bm.faces:
                if len(face.verts) != 3:
                    continue  

                v0, v1, v2 = face.verts
                ev0, ev1, ev2 = edge_map[face.edges[0]], edge_map[face.edges[1]], edge_map[face.edges[2]]

                try:
                    new_faces.append(bm.faces.new([v0, ev0, ev2]))
                    new_faces.append(bm.faces.new([v1, ev1, ev0]))
                    new_faces.append(bm.faces.new([v2, ev2, ev1]))
                    new_faces.append(bm.faces.new([ev0, ev1, ev2]))
                    faces_to_remove.append(face)
                except:
                    continue 

            for face in faces_to_remove:
                bm.faces.remove(face)

            bm.to_mesh(mesh)
            bm.free()
            mesh.update()

        return (True, "Loop subdivision applied successfully.")

    except Exception as e:
        return (False, f"Loop subdivision failed: {str(e)}")

