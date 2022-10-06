from hashlib import new
from imageio import save
import pymeshlab
import os

def refineMesh(poorPLYPath: str, originalVertices: str, desiredVertices: int):
    print(f'Mesh at {poorPLYPath} needs to be refined')

    # create a new MeshSet
    ms = pymeshlab.MeshSet()

    # load a new mesh in the MeshSet, and sets it as current mesh
    # the path of the mesh can be absolute or relative
    ms.load_new_mesh(poorPLYPath)
    
    # A MeshSet (and MeshLab) can open multiple meshes in the same Project.
    # For refinement, we must only load one mesh at a time.
    assert len(ms) == 1

    # set the first mesh (id 0) as current mesh
    ms.set_current_mesh(0)

    # Small check to see if the right mesh was loaded.
    assert ms.current_mesh().vertex_number() == originalVertices

    # Apply 1 iteration of Catmull-Clark subdivision.
    ms.apply_filter('meshing_surface_subdivision_catmull_clark')

    # Small check to see if the mesh's vertices were changed.
    newVertices = ms.current_mesh().vertex_number()
    assert newVertices != originalVertices

    print(f'After applying Catmull-Clark, the mesh went from {originalVertices} vertices to {newVertices} vertices.\nWe want a number near {desiredVertices} vertices.\n')

    saveRefinedMesh(ms, poorPLYPath)


def saveRefinedMesh(refinedMesh, oldPath):
    # print(f"oldPath:\n{oldPath}")

    rest1, plyName = os.path.split(oldPath)
    rest2, plyNumber = os.path.split(rest1)
    rest3, plyType = os.path.split(rest2)

    # print(oldPath)
    # print(plyName)
    # print(plyNumber)
    # print(plyType)

    refinedPLYLocation = f"data/refined meshes/{plyType}/{plyNumber}"
    refinedPLYComplete = f"{refinedPLYLocation}/refined.ply"

    # Refined PLY folder does not exist
    if not os.path.exists(refinedPLYLocation):
        os.makedirs(refinedPLYLocation)

    # save the current selected mesh
    refinedMesh.save_current_mesh(refinedPLYComplete)

    print(f'Saving the new PLY mesh to:\n{refinedPLYComplete}\n')