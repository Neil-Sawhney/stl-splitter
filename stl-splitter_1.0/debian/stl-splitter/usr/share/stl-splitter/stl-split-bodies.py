import bpy
import sys
import os

def separate_and_export_individual_stl(stl_filepath):
    """
    Separates the bodies in an STL file and exports each as a separate STL.
    
    Args:
        stl_filepath: The path to the input STL file.
    """
    try:
        # Clear existing mesh objects
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()

        # Import STL
        bpy.ops.import_mesh.stl(filepath=stl_filepath)

        # Get the imported object
        obj = bpy.context.selected_objects[0]
        bpy.context.view_layer.objects.active = obj

        # Switch to edit mode and separate the meshes by loose parts
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # Get separated parts
        separated_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        output_dir = os.path.dirname(stl_filepath)

        # Export each part as an individual STL
        for i, part in enumerate(separated_objects):
            part.select_set(True)
            export_filepath = os.path.join(output_dir, f"{os.path.basename(stl_filepath).split('.')[0]}_{i + 1}.stl")
            bpy.ops.export_mesh.stl(filepath=export_filepath, use_selection=True)
            part.select_set(False)  # Deselect after export
            print(f"Exported: {export_filepath}")

        print("Successfully exported all separated bodies.")
    
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: blender -b -P separate_stl.py -- <path_to_stl_file>")
        sys.exit(1)

    # Assumes the last command-line argument is the filepath
    stl_filepath = sys.argv[-1]

    if not os.path.isfile(stl_filepath):
        print(f"Error: STL file not found at '{stl_filepath}'")
        sys.exit(1)

    separate_and_export_individual_stl(stl_filepath)