import bpy
import bmesh
from mathutils import Vector

def doosabin_subdivide(obj, levels=1):
    try:
        mesh = obj.data
        for _ in range(levels):
            bm = bmesh.new()
            bm.from_mesh(mesh)

            new_faces = []
            for face in bm.faces:
                face_verts = [v for v in face.verts]
                face_center = sum((v.co for v in face_verts), Vector()) / len(face_verts)

                new_verts = []
                for v in face_verts:
                    mid = (v.co + face_center) / 2
                    new_vert = bm.verts.new(mid)
                    new_verts.append(new_vert)

                for i in range(len(new_verts)):
                    new_faces.append(bm.faces.new([
                        face_verts[i],
                        new_verts[i],
                        new_verts[(i+1)%len(new_verts)],
                        face_verts[(i+1)%len(face_verts)],
                    ]))

            bmesh.ops.delete(bm, geom=bm.faces[:], context='FACES')
            bm.to_mesh(mesh)
            bm.free()
        return (True, "Doo-Sabin subdivision applied.")
    except Exception as e:
        return (False, f"Doo-Sabin subdivision failed: {e}")
