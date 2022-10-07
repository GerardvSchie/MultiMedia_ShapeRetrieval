from hashlib import new
from imageio import save
import pymeshlab
import os

# Source: https://stackoverflow.com/questions/65419221/how-to-use-pymeshlab-to-reduce-vertex-number-to-a-certain-number
def refineMesh(poorPLYPath: str, originalVertices: str, desiredVertices: int):
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

    # Close any holes in the mesh to make it watertight.
    ms.apply_filter('meshing_close_holes')
    # print('Mesh made watertight')


    oldVertices = ms.current_mesh().vertex_number()

    # Increase the vertex count for meshes with vertext counts lower than desired.
    # Simplification tool doesn't work with smaller than desired counts.    
    while (ms.current_mesh().vertex_number() < desiredVertices):
        # Apply 1 iteration of Catmull-Clark subdivision.
        ms.apply_filter('meshing_surface_subdivision_catmull_clark')
        newVertices = ms.current_mesh().vertex_number()
        
        print(f'After applying 1 iteration of Catmull-Clark on a smaller mesh, the mesh went from {oldVertices} vertices to {newVertices} vertices.\nWe want a number above {desiredVertices} vertices before simplification.\n')



    # According to the Euler characteristic of meshes, the number of faces is roughly twice the number of vertices.
    # To better ensure that the vertex count doesn't fall beneath the desired amount, add 100.
    desiredFaces = desiredVertices * 2 + 100
    print(f'desiredFaces: {desiredFaces}')

    while (ms.current_mesh().vertex_number() > desiredVertices):
        ms.apply_filter('meshing_decimation_quadric_edge_collapse', targetfacenum=desiredFaces, preservenormal=True)
        print(f"Decimated to {desiredFaces} faces, new mesh has {ms.current_mesh().vertex_number()} vertices")
        #Refine our estimation to slowly converge to TARGET vertex number
        desiredFaces = desiredFaces - (ms.current_mesh().vertex_number() - desiredVertices)


    # Small check to see if the mesh's vertices are now the desired amount.
    newVertices = ms.current_mesh().vertex_number()
    print(f'{newVertices} =?= {desiredVertices}')
    assert newVertices == desiredVertices

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