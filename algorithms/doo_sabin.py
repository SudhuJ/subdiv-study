import bmesh
import bpy
import math
from mathutils import Vector

def subdivide(mesh):
    if not mesh.polygons:
        raise ValueError("Mesh has no faces.")
    
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    # Create new vertices
    new_verts = []
    vert_face_map = {v.index: [] for v in bm.verts}

    for vert in bm.verts:
        adj_faces = list(vert.link_faces)
        
        for face in adj_faces:
            n = len(face.verts)
            
            # Calculate weights based on face valence
            if n == 4:
                alpha = 9/16
                beta = 3/8
            else:
                alpha = (n + 5) / (4 * n)
                beta = (3 + 2 * math.cos(2 * math.pi / n)) / (4 * n)
            
            # Face center
            face_center = sum((v.co for v in face.verts), Vector()) / n
            
            # Edge midpoints
            edge_midpoints = []
            for edge in vert.link_edges:
                if edge in face.edges:
                    other_vert = edge.other_vert(vert)
                    edge_midpoints.append((vert.co + other_vert.co) / 2)
            
            avg_edge_mid = sum(edge_midpoints, Vector()) / len(edge_midpoints)
            
            # New vertex position
            new_pos = (alpha * vert.co + 
                      beta * avg_edge_mid + 
                      (1 - alpha - beta) * face_center)
            
            vert_face_map[vert.index].append(len(new_verts))
            new_verts.append(new_pos)

    # Create new BMesh
    new_bm = bmesh.new()
    
    # Add all new vertices
    bm_new_verts = [new_bm.verts.new(v) for v in new_verts]
    new_bm.verts.ensure_lookup_table()
    
    # Create face-face polygons
    for face in bm.faces:
        face_vert_indices = []
        for vert in face.verts:
            for i, f in enumerate(vert.link_faces):
                if f == face:
                    face_vert_indices.append(vert_face_map[vert.index][i])
                    break
        
        if len(face_vert_indices) >= 3:
            new_bm.faces.new([bm_new_verts[i] for i in face_vert_indices])

    # Create edge-edge polygons
    for edge in bm.edges:
        adj_faces = list(edge.link_faces)
        if len(adj_faces) == 2:
            face1, face2 = adj_faces
            quad_verts = []
            
            for vert in edge.verts:
                # Find index in face1
                for i, f in enumerate(vert.link_faces):
                    if f == face1:
                        quad_verts.append(vert_face_map[vert.index][i])
                        break
                
                # Find index in face2
                for i, f in enumerate(vert.link_faces):
                    if f == face2:
                        quad_verts.append(vert_face_map[vert.index][i])
                        break
            
            if len(quad_verts) == 4:
                new_bm.faces.new([
                    bm_new_verts[quad_verts[0]],
                    bm_new_verts[quad_verts[1]],
                    bm_new_verts[quad_verts[3]],
                    bm_new_verts[quad_verts[2]]
                ])

    # Create vertex-vertex polygons
    for vert in bm.verts:
        adj_faces = list(vert.link_faces)
        if adj_faces:
            vert_indices = []
            for face in adj_faces:
                for i, f in enumerate(vert.link_faces):
                    if f == face:
                        vert_indices.append(vert_face_map[vert.index][i])
                        break
            
            if len(vert_indices) >= 3:
                new_bm.faces.new([bm_new_verts[i] for i in vert_indices])

    # Free original BMesh
    bm.free()
    
    # Create resulting mesh
    result = bpy.data.meshes.new(mesh.name + "_ds_subd")
    new_bm.to_mesh(result)
    new_bm.free()
    
    return result