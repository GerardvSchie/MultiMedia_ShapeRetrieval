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
