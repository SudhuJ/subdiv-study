import bpy
import bmesh
from mathutils import Vector

def root3_subdivide(obj, levels=1):
    try:
        mesh = obj.data
        for _ in range(levels):
            bm = bmesh.new()
            bm.from_mesh(mesh)
            bmesh.ops.triangulate(bm, faces=bm.faces[:])
            bm.verts.ensure_lookup_table()

            face_centers = []
            for face in bm.faces:
                center = bm.verts.new(sum((v.co for v in face.verts), Vector()) / 3)
                face_centers.append((face, center))

            for face, center in face_centers:
                verts = face.verts[:]
                bm.faces.remove(face)
                for i in range(3):
                    bm.faces.new([verts[i], verts[(i+1)%3], center])

            bm.to_mesh(mesh)
            bm.free()
        return (True, "Root3 subdivision applied.")
    except Exception as e:
        return (False, f"Root3 subdivision failed: {e}")
