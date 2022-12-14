import open3d as o3d


class Geometries:
    def __init__(self, path: str):
        """Sets all geometries to none, only get computed in GUI or when it is required for feature extraction"""
        self.path: str = path

        self.mesh: o3d.geometry.TriangleMesh = None
        self.point_cloud: o3d.geometry.PointCloud = None
        self.convex_hull_mesh: o3d.geometry.TriangleMesh = None
        self.convex_hull_line_set: o3d.geometry.LineSet = None
        self.axis_aligned_bounding_box: o3d.geometry.AxisAlignedBoundingBox = None
        self.axis_aligned_bounding_box_line_set: o3d.geometry.LineSet = None
        self.center_mesh: o3d.geometry.TriangleMesh = None
