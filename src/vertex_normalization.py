import pymeshlab
import os

def refine_mesh(normalizedPLYPath: str, desiredVertices: int):
    #print(f"Refining mesh at:\n{normalizedPLYPath}\n")

    refinedMeshSet, finalVertexCount = simplifyMesh(normalizedPLYPath, desiredVertices)

    newPath = createRefinedSavePathLocation(normalizedPLYPath)

    saveRefinedMesh(refinedMeshSet, newPath, 'refined')

    return finalVertexCount


# Source: https://stackoverflow.com/questions/65419221/how-to-use-pymeshlab-to-reduce-vertex-number-to-a-certain-number
def simplifyMesh(oldPath: str, desiredVertices: int):
    # Creating a new MeshSet and only loading the Poisson-sampled mesh seems to be the only way to get Edge Collapse working again.
    # A MeshSet/project results in Edge Collapse not changing the number of faces after the first iteration, even with a decreasing desiredFaces parameter.
    # Also can't find a 'delete mesh/layer from MeshSet' function.
    ms = pymeshlab.MeshSet()

    # ms.load_new_mesh('data/refined meshes/Airplane/61/poisson.ply')
    # ms.load_new_mesh(f'{newPath}/poisson.ply')
    # ms.load_new_mesh(f'{newPath}/montecarlo.ply')
    ms.load_new_mesh(oldPath)

    assert len(ms) == 1

    # According to the Euler characteristic of meshes, the number of faces is roughly twice the number of vertices.
    # Using a to low desired face count might give a number of vertices less than desired.
    # To better ensure that the vertex count doesn't fall beneath the desired amount, add 300 (based on running it on normalized.ply meshes).
    desiredFaces = desiredVertices * 2 + 300

    while (ms.current_mesh().vertex_number() > desiredVertices):
        ms.apply_filter('meshing_decimation_quadric_edge_collapse', targetfacenum=desiredFaces)#, preservenormal=True)
        #print(f"Decimated to {desiredFaces} faces, new mesh has {ms.current_mesh().vertex_number()} vertices")

        # Refine our estimation to slowly converge to TARGET vertex number
        desiredFaces = desiredFaces - (ms.current_mesh().vertex_number() - desiredVertices)

    # Small check to see if the mesh's vertices are now the desired amount.
    newVertices = ms.current_mesh().vertex_number()
    #print(f'{newVertices} =?= {desiredVertices}\n')

    if (newVertices < desiredVertices):
        print(f"Mesh at {oldPath} has gotten {newVertices} instead of {desiredVertices}")

    assert newVertices == desiredVertices

    return ms, newVertices
    #prin()


def saveRefinedMesh(refinedMeshSet, path, fileName):
    refinedPLYComplete = f"{path}/{fileName}.ply"

    # Refined PLY folder does not exist
    if not os.path.exists(path):
        os.makedirs(path)

    # save the current selected mesh
    refinedMeshSet.save_current_mesh(refinedPLYComplete)

    #print(f'\nSaving the new PLY mesh to:\n{refinedPLYComplete}')


def createRefinedSavePathLocation(oldPath: str):
    # print(f"oldPath:\n{oldPath}")

    rest1, plyName = os.path.split(oldPath)
    rest2, plyNumber = os.path.split(rest1)
    rest3, plyType = os.path.split(rest2)

    # print(oldPath)
    # print(plyName)
    # print(plyNumber)
    # print(plyType)

    return f"data/refined meshes/{plyType}/{plyNumber}"