import os.path
import logging
import open3d as o3d
import numpy as np

from src.object.geometries import Geometries


class GeometriesController:
    # A big portion of these two methods comes from the Open3D example, see license in app folder.
    @staticmethod
    def load_all_from_file(geometries: Geometries) -> None:
        GeometriesController.set_mesh_from_file(geometries, True)
        GeometriesController.calculate_all_from_mesh(geometries, True)

    @staticmethod
    def calculate_all_from_mesh(geometries: Geometries, force_reload=False) -> None:
        GeometriesController.calculate_point_cloud(geometries, force_reload)
        GeometriesController.calculate_all_other_geometries(geometries, force_reload)

    @staticmethod
    def calculate_all_other_geometries(geometries: Geometries, force_reload=False) -> None:
        GeometriesController.calculate_convex_hull(geometries, force_reload)
        GeometriesController.calculate_aligned_bounding_box(geometries, force_reload)

    @staticmethod
    def calculate_mesh(geometries: Geometries, force_reload=False) -> None:
        if geometries.mesh and not force_reload:
            return

        if not geometries.point_cloud:
            GeometriesController.set_mesh_from_file(geometries, force_reload)
        # else:
        #     GeometriesController.point_cloud_to_mesh(geometries, force_reload)

    @staticmethod
    def set_mesh_from_file(geometries: Geometries, force_reload=False) -> bool:
        # Mesh is already loaded and no force
        if geometries.mesh and not force_reload:
            return True

        geometry_type = o3d.io.read_file_geometry_type(geometries.path)

        if geometry_type & o3d.io.CONTAINS_TRIANGLES:
            geometries.mesh = o3d.io.read_triangle_mesh(geometries.path)

        # Could not load mesh
        if geometries.mesh is None:
            logging.warning(
                f"Shape at path '{os.path.abspath(geometries.path)}' appears to be a point cloud, cannot load mesh")
            return False
        if not geometries.mesh.triangles:
            logging.warning(f"Shape at path '{os.path.abspath(geometries.path)}' has 0 triangles, will read as point cloud")
            return False

        return True

    @staticmethod
    def set_pcd_from_file(geometries: Geometries, force_reload=False) -> bool:
        # Mesh is already loaded and no force
        if geometries.point_cloud and not force_reload:
            return True

        pcd_path = geometries.path.split('.')[0] + '.pcd'
        if not os.path.exists(pcd_path):
            logging.warning(f"Shape at path '{os.path.abspath(pcd_path)}' does not exist")

        geometries.point_cloud = o3d.io.read_point_cloud(pcd_path)

        # Could not load mesh
        if geometries.point_cloud is None:
            logging.warning(f"Shape at path '{os.path.abspath(pcd_path)}' cannot be read as a point cloud")
            return False

        return True

    @staticmethod
    def calculate_point_cloud(geometries: Geometries, force_reload=False) -> bool:
        if geometries.point_cloud and not force_reload:
            return True

        # Point cloud already existed
        if os.path.exists(geometries.path.split('.')[0] + '.pcd'):
            return GeometriesController.set_pcd_from_file(geometries, force_reload)
        else:
            logging.warning('TEMPORARY: point cloud should not be computed in current logic')
            return False

        if not GeometriesController.set_mesh_from_file(geometries):
            return False

        geometries.point_cloud = o3d.geometry.PointCloud(geometries.mesh.vertices)
        return True

    @staticmethod
    def calculate_convex_hull(geometries: Geometries, force_reload=False) -> bool:
        if geometries.convex_hull_mesh and not force_reload:
            return True

        if not geometries.point_cloud:
            GeometriesController.calculate_point_cloud(geometries, force_reload)

        geometries.convex_hull_mesh, _ = geometries.point_cloud.compute_convex_hull()
        return True

    @staticmethod
    def calculate_aligned_bounding_box(geometries: Geometries, force_reload=False) -> bool:
        if geometries.axis_aligned_bounding_box and not force_reload:
            return True

        if not geometries.point_cloud:
            GeometriesController.calculate_point_cloud(geometries, force_reload)

        geometries.axis_aligned_bounding_box = geometries.point_cloud.get_axis_aligned_bounding_box()
        return True

    @staticmethod
    def calculate_center_mesh(geometries: Geometries, force_reload=False) -> bool:
        if geometries.center_mesh and not force_reload:
            return True

        if not geometries.point_cloud:
            GeometriesController.calculate_point_cloud(geometries, force_reload)

        center = geometries.point_cloud.get_center()
        geometries.center_mesh = o3d.geometry.TriangleMesh().create_sphere(0.015)
        geometries.center_mesh.translate(center)
        geometries.center_mesh.paint_uniform_color([1, 0, 1])
        return True

    @staticmethod
    def calculate_mesh_normals(geometries: Geometries, force_reload=False) -> None:
        if not geometries.mesh.has_vertex_normals() and not force_reload:
            return

        # Get the normals of the mesh after orientating them
        # geometries.mesh.orient_triangles()
        geometries.mesh.compute_triangle_normals(True)
        geometries.mesh.compute_vertex_normals(True)
        if not geometries.mesh.has_vertex_colors():
            geometries.mesh.paint_uniform_color([1, 1, 1])

    @staticmethod
    def calculate_point_cloud_normals(geometries: Geometries, force_reload=False) -> None:
        if not geometries.point_cloud.has_normals() and not force_reload:
            return

        geometries.point_cloud.estimate_normals()
        geometries.point_cloud.orient_normals_consistent_tangent_plane(10)

    @staticmethod
    def get_coordinate_axes() -> o3d.geometry.TriangleMesh:
        return o3d.geometry.TriangleMesh().create_coordinate_frame(0.1, np.array([0, 0, 0]))

    @staticmethod
    def calculate_gui_geometries(geometries: Geometries, force_reload=False) -> None:
        if not geometries.center_mesh or force_reload:
            GeometriesController.calculate_center_mesh(geometries, force_reload)

        if not geometries.convex_hull_line_set or force_reload:
            geometries.convex_hull_line_set = o3d.geometry.LineSet().create_from_triangle_mesh(geometries.convex_hull_mesh)
            geometries.convex_hull_line_set.paint_uniform_color((1, 0, 0))

        if not geometries.axis_aligned_bounding_box_line_set or force_reload:
            geometries.axis_aligned_bounding_box_line_set = \
                o3d.geometry.LineSet().create_from_axis_aligned_bounding_box(geometries.axis_aligned_bounding_box)
            geometries.axis_aligned_bounding_box_line_set.paint_uniform_color((0.5, 0, 0))
