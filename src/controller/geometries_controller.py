import os
import logging
import open3d as o3d
import numpy as np

from src.object.geometries import Geometries


class GeometriesController:
    @staticmethod
    def load_all_from_file(geometries: Geometries) -> None:
        """Load mesh from file and compute all other geometries

        :param geometries: Object to save the geometries in
        """
        GeometriesController.set_mesh_from_file(geometries, True)
        GeometriesController.calculate_all_from_mesh(geometries, True)

    @staticmethod
    def calculate_all_from_mesh(geometries: Geometries, force_reload=False) -> None:
        """Calculate the point cloud, convex hull, and bounding box

        :param geometries: Object to save geometries in
        :param force_reload: Force reloading the geometries
        """
        GeometriesController.calculate_point_cloud(geometries, force_reload)
        GeometriesController.calculate_all_other_geometries(geometries, force_reload)

    @staticmethod
    def calculate_all_other_geometries(geometries: Geometries, force_reload=False) -> None:
        """Computes the convex hull and AABB

        :param geometries: Object to save the geometries to
        :param force_reload: Force to recompute the geometries
        """
        GeometriesController.calculate_convex_hull(geometries, force_reload)
        GeometriesController.calculate_aligned_bounding_box(geometries, force_reload)

    @staticmethod
    def calculate_mesh(geometries: Geometries, force_reload=False) -> None:
        """Loads the mesh from file

        :param geometries: Object to save the geometry to
        :param force_reload: Force to reload the mesh
        """
        if geometries.mesh and not force_reload:
            return

        if not geometries.point_cloud:
            GeometriesController.set_mesh_from_file(geometries, force_reload)

    @staticmethod
    def set_mesh_from_file(geometries: Geometries, force_reload=False) -> bool:
        """Sets the point cloud from a file

        :param geometries: Object to save the geometry to
        :param force_reload: Force to recompute the point cloud
        :return: Whether the point got updated
        """
        # Mesh is already loaded and no force
        if geometries.mesh and not force_reload:
            return True

        # Filetype contains triangles
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
        """Sets the point cloud from a file

        :param geometries: Object to save the geometry to
        :param force_reload: Force to recompute the point cloud
        :return: Whether the point got updated
        """
        if geometries.point_cloud and not force_reload:
            return True

        # Check whether pcd file exists
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
        """Computes the point cloud, if *.pcd does not exist the construct it from vertices of mesh

        :param geometries: Object to save the geometry to
        :param force_reload: Force to recompute the point cloud
        :return: Whether the point got updated
        """
        if geometries.point_cloud and not force_reload:
            return True

        # Point cloud already existed
        if os.path.exists(geometries.path.split('.')[0] + '.pcd'):
            return GeometriesController.set_pcd_from_file(geometries, force_reload)
        else:
            logging.warning('Will create pdc from mesh vertices')

        if not GeometriesController.set_mesh_from_file(geometries):
            return False

        # Set point cloud and indicate it got recomputed
        geometries.point_cloud = o3d.geometry.PointCloud(geometries.mesh.vertices)
        return True

    @staticmethod
    def calculate_convex_hull(geometries: Geometries, force_reload=False) -> bool:
        """Computes the convex hull, used for convexity and diameter

        :param geometries: Object to save the geometry to
        :param force_reload: Force to recompute the convex hull
        :return: Whether the convex hull got updated
        """
        if geometries.convex_hull_mesh and not force_reload:
            return True

        if not geometries.point_cloud:
            GeometriesController.calculate_point_cloud(geometries, force_reload)

        geometries.convex_hull_mesh, _ = geometries.point_cloud.compute_convex_hull()
        return True

    @staticmethod
    def calculate_aligned_bounding_box(geometries: Geometries, force_reload=False) -> bool:
        """Computes the axis aligned bounding box, after alignment this is also the oriented bounding box

        :param geometries: Object to save the geometry to
        :param force_reload: Force to recompute the bounding box
        :return: Whether the bounding box got updated
        """
        if geometries.axis_aligned_bounding_box and not force_reload:
            return True

        if not geometries.point_cloud:
            GeometriesController.calculate_point_cloud(geometries, force_reload)

        geometries.axis_aligned_bounding_box = geometries.point_cloud.get_axis_aligned_bounding_box()
        return True

    @staticmethod
    def calculate_center_mesh(geometries: Geometries, force_reload=False) -> bool:
        """Computes mesh cell normals

        :param geometries: Object containing the geometries
        :param force_reload: Force re-computation of the pcd normals
        :return: Whether this mesh has been recomputed
        """
        if geometries.center_mesh and not force_reload:
            return True

        # Compute center based on point cloud
        if not geometries.point_cloud:
            GeometriesController.calculate_point_cloud(geometries, force_reload)

        # This is barycenter
        center = geometries.point_cloud.get_center()

        # Create small sphere mesh and place it at the origin
        geometries.center_mesh = o3d.geometry.TriangleMesh().create_sphere(0.015)
        geometries.center_mesh.translate(center)
        geometries.center_mesh.paint_uniform_color([1, 0, 1])
        return True

    @staticmethod
    def calculate_mesh_normals(geometries: Geometries, force_reload=False) -> None:
        """Computes mesh cell normals

        :param geometries: Object containing the geometries
        :param force_reload: Force re-computation of the pcd normals
        """
        if not geometries.mesh.has_vertex_normals() and not force_reload:
            return

        # Get the normals of the mesh after orientating them
        geometries.mesh.compute_triangle_normals(True)
        geometries.mesh.compute_vertex_normals(True)
        if not geometries.mesh.has_vertex_colors():
            geometries.mesh.paint_uniform_color([1, 1, 1])

    @staticmethod
    def calculate_point_cloud_normals(geometries: Geometries, force_reload=False) -> None:
        """Computes point cloud normals based on 10 near points

        :param geometries: Object containing the geometries
        :param force_reload: Force re-computation of the pcd normals
        """
        if not geometries.point_cloud.has_normals() and not force_reload:
            return

        # Estimate normals and orient them to be pointing the same direction
        geometries.point_cloud.estimate_normals()
        geometries.point_cloud.orient_normals_consistent_tangent_plane(10)

    @staticmethod
    def get_coordinate_axes() -> o3d.geometry.TriangleMesh:
        """Object that represents the X, Y, and Z axis

        :return: Axis mesh
        """
        return o3d.geometry.TriangleMesh().create_coordinate_frame(0.1, np.zeros(3))

    @staticmethod
    def calculate_gui_geometries(geometries: Geometries, force_reload=False) -> None:
        """Compute the convex hull and other items required. Their line set

        :param geometries: Geometries
        :param force_reload: Force recomputing these geometries
        """
        # Load center mesh
        if not geometries.center_mesh or force_reload:
            GeometriesController.calculate_center_mesh(geometries, force_reload)

        # Convex hull line set
        if not geometries.convex_hull_line_set or force_reload:
            geometries.convex_hull_line_set = o3d.geometry.LineSet().create_from_triangle_mesh(geometries.convex_hull_mesh)
            geometries.convex_hull_line_set.paint_uniform_color((1, 0, 0))

        # Compute bounding box line set
        if not geometries.axis_aligned_bounding_box_line_set or force_reload:
            geometries.axis_aligned_bounding_box_line_set = \
                o3d.geometry.LineSet().create_from_axis_aligned_bounding_box(geometries.axis_aligned_bounding_box)
            geometries.axis_aligned_bounding_box_line_set.paint_uniform_color((0.5, 0, 0))
