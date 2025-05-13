# Blender Subdivision Addon

This addon implements advanced subdivision surface algorithms in Blender, providing alternatives to Blender's native subdivision modifier. It includes:

1. **Catmull-Clark Subdivision** (standard smoothing)
2. **Doo-Sabin Subdivision** (face-preserving)

## Features
- **Non-destructive workflow**: Creates new subdivided objects while keeping originals
- **Iteration Control**: Set subdivision levels (1-5)

## Installation
1. Download the `.zip` of this repository
2. In Blender: `Edit > Preferences > Add-ons > Install`
3. Select the `.zip` file and enable "Subdivision Methods"

## Usage
1. Select a mesh object
2. Open the "Subdiv" panel in the 3D View sidebar
3. Choose iterations and click your preferred algorithm:
   - **Catmull-Clark**: Smooths surfaces
   - **Doo-Sabin**: Better preserves face shapes

## Requirements
- Blender 3.0+
- Python 3.7+