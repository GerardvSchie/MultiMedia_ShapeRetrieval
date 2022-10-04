import open3d as o3d
import numpy as np
from src.object.shape import Shape


def normalize_shape(shape: Shape):
    shape.geometries.load_mesh()

    # Translate to center
    # shape.geometries.mesh.vertices = shape.geometries.mesh.vertices - shape.geometries.mesh.get_center()
   
    shape.geometries.mesh = rot_pca(shape.geometries.mesh)  # Rotate based on PCA
    shape.geometries.mesh = flipper(shape.geometries.mesh)  # Flips the mesh
    # shape.geometries.mesh = scaler(shape.geometries.mesh)  # Scales to a unit bounding box the mesh


def rot_pca(mesh):
    verts = mesh.vertices
    A = np.zeros((3, len(verts)))
    A[0] = np.array([x[0] for x in verts])
    A[1] = np.array([x[1] for x in verts])
    A[2] = np.array([x[2] for x in verts])

    A_cov = np.cov(A)

    eigenvalues, eigenvectors = np.linalg.eig(A_cov)
    min_eigen = np.argmin(eigenvalues)
    max_eigen = np.argmax(eigenvalues)
    mid_eigen = np.setdiff1d([0, 1, 2], [min_eigen, max_eigen])[0]

    new_verts = o3d.utility.Vector3dVector()
    for v in verts:
        v1 = np.dot(v, eigenvectors[:, max_eigen])
        v2 = np.dot(v, eigenvectors[:, mid_eigen])
        v3 = np.dot(v, eigenvectors[:, min_eigen])
        new_verts.append([v1, v2, v3])
    mesh.vertices = new_verts

    return mesh


def flipper(mesh):

    #faces = ( index, ( xcoord, ycoord, zcoord )  )

    triangles = np.zeros((3, len(faces)))
    for i, indexes in enumerate(faces):
        xc, yc, zc = [], [], []
        for inum in indexes:
            verts = mesh.vertices[inum]
            xc.append(verts[0])
            yc.append(verts[1])
            zc.append(verts[2])
        triangles[0][i] = np.sum(xc) / 3
        triangles[1][i] = np.sum(yc) / 3
        triangles[2][i] = np.sum(zc) / 3

        sx = 0
        for x in triangles[0]:
            sx += np.sign(x) * (x ** 2)

        sy = 0
        for y in triangles[1]:
            sy += np.sign(y) * (y ** 2)

        sz = 0
        for z in triangles[2]:
            sz += np.sign(z) * (z ** 2)

        flipping = np.array([[np.sign(sx), 0, 0], [0, np.sign(sy), 0], [0, 0, np.sign(sz)]])

        mesh.vertices = np.matmul(mesh.vertices, flipping)

    return mesh


def scaler(mesh):
    verts = mesh.vertices
    xc = [x[0] for x in verts]
    yc = [x[1] for x in verts]
    zc = [x[2] for x in verts]
    xmin, xmax = min(xc), max(xc)
    ymin, ymax = min(yc), max(yc)
    zmin, zmax = min(zc), max(zc)
    maxbox = max([xmax - xmin, ymax - ymin, zmax - zmin])
    mesh.vertices /= maxbox
    return mesh
