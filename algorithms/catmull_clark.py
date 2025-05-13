import bmesh
import bpy
from mathutils import Vector

def subdivide(mesh):
    if not mesh.polygons:
        raise ValueError("Mesh has no faces.")

    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    # Stage 1: Create face points
    face_points = []
    face_point_indices = {}
    for face in bm.faces:
        face_point = sum((v.co for v in face.verts), Vector()) / len(face.verts)
        face_point_indices[face.index] = len(face_points)
        face_points.append(face_point)

    # Stage 2: Create edge points
    edge_points = []
    edge_point_indices = {}
    for edge in bm.edges:
        # Get adjacent faces (0-2 faces)
        adj_faces = list(edge.link_faces)
        
        edge_point = edge.verts[0].co + edge.verts[1].co
        
        if len(adj_faces) == 2:
            edge_point += face_points[face_point_indices[adj_faces[0].index]]
            edge_point += face_points[face_point_indices[adj_faces[1].index]]
            edge_point /= 4
        else:
            edge_point /= 2
        
        edge_point_indices[edge.index] = len(edge_points)
        edge_points.append(edge_point)

    # Stage 3: Create new vertex points
    new_vert_points = []
    for vert in bm.verts:
        # Average of adjacent face points
        adj_faces = list(vert.link_faces)
        F = sum((face_points[face_point_indices[f.index]] for f in adj_faces), Vector())
        if adj_faces:
            F /= len(adj_faces)
        
        # Average of edge midpoints
        adj_edges = list(vert.link_edges)
        R = sum(((e.verts[0].co + e.verts[1].co)/2 for e in adj_edges), Vector())
        if adj_edges:
            R /= len(adj_edges)
        
        # Original point
        P = vert.co
        
        # New position calculation
        n = len(adj_edges)
        if n > 0:
            new_pos = (F + 2*R + (n-3)*P) / n
            new_vert_points.append(new_pos)
        else:
            new_vert_points.append(P)

    # Create new BMesh
    new_bm = bmesh.new()
    
    # Add all points to new BMesh
    new_verts = []
    for point in new_vert_points:
        new_verts.append(new_bm.verts.new(point))
    
    for point in edge_points:
        new_verts.append(new_bm.verts.new(point))
    
    for point in face_points:
        new_verts.append(new_bm.verts.new(point))
    
    new_bm.verts.ensure_lookup_table()
    
    # Create new faces
    for face in bm.faces:
        face_point_idx = len(new_vert_points) + len(edge_points) + face_point_indices[face.index]
        
        for loop in face.loops:
            vert_idx = loop.vert.index
            edge_idx = loop.edge.index
            
            edge_point_idx = len(new_vert_points) + edge_point_indices[edge_idx]
            
            next_edge = loop.link_loop_next.edge
            next_edge_point_idx = len(new_vert_points) + edge_point_indices[next_edge.index]
            
            new_bm.faces.new((
                new_verts[vert_idx],
                new_verts[edge_point_idx],
                new_verts[face_point_idx],
                new_verts[next_edge_point_idx]
            ))
    
    # Free original BMesh
    bm.free()
    
    # Create resulting mesh
    result = bpy.data.meshes.new(mesh.name + "_cc_subd")
    new_bm.to_mesh(result)
    new_bm.free()
    
    return result