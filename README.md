Embed in PyQt:
https://github.com/isl-org/Open3D/discussions/4668

Put qml into widget:
https://stackoverflow.com/questions/59828470/how-use-qml-drawer-with-qt-widgets
https://github.com/eyllanesc/stackoverflow/blob/master/questions/59828470/main.py


https://github.com/isl-org/Open3D/issues/2063

Open3D github repository:

## Compute bary-center of object
Geometry.GetCenter()
Geometry3D::ComputeCenter(points)

```c++
Eigen::Vector3d Geometry3D::ComputeCenter(
        const std::vector<Eigen::Vector3d>& points) const {
    Eigen::Vector3d center(0, 0, 0);
    if (points.empty()) {
        return center;
    }
    center = std::accumulate(points.begin(), points.end(), center);
    center /= double(points.size());
    return center;
}
```

Camera viewpoint:
https://github.com/isl-org/Open3D/issues/1553

Faster iteration:
https://numpy.org/doc/stable/reference/arrays.nditer.html

Random points:
https://stackoverflow.com/questions/14262654/numpy-get-random-set-of-rows-from-2d-array

Angle:
https://stackoverflow.com/questions/35176451/python-code-to-calculate-angle-between-three-point-using-their-3d-coordinates

Performance:
https://mmas.github.io/python-image-processing-libraries-performance-opencv-scipy-scikit-image

Alternatives for pywin32?:
https://stackoverflow.com/questions/373020/finding-the-current-active-window-in-mac-os-x-using-python
https://pypi.org/project/PyGetWindow/
https://developer.apple.com/documentation/appkit/nsworkspace#//apple_ref/occ/instm/NSWorkspace/frontmostApplication
