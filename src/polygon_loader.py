import os
import open3d as o3d


def load_file(filepath: str):
    # Path relative to data folder
    data_folder = "data"
    filepath = os.path.join(data_folder, filepath)
    filepath = os.path.abspath(filepath)

    # Check file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File \"{filepath}\" not found")

    if filepath.endswith(".ply") or filepath.endswith(".off"):
        return o3d.io.read_triangle_mesh(filepath)
    else:
        raise NotImplementedError(f"No reader defined for format \"{filepath.split('.')[-1]}\"")

#
# def _load_triangle_mesh(filepath: str):
#     pcd = o3d.io.read_triangle_mesh(filepath)
#     return pcd
#
#
# def _load_file_format(filepath: str):
#     pcd = o3d.io.read_triangle_mesh(filepath)