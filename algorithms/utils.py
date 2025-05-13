import bpy

def apply_subdivision(mesh, algorithm, iterations=1):
    if iterations < 1:
        return mesh.copy()

    if algorithm == 'CATMULL_CLARK':
        from .catmull_clark import subdivide
    elif algorithm == 'DOO_SABIN':
        from .doo_sabin import subdivide
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    result = mesh.copy()
    for _ in range(iterations):
        new_mesh = subdivide(result)
        bpy.data.meshes.remove(result)  # Cleanup previous mesh
        result = new_mesh
        
    return result