import pymeshlab
import os

def refine_mesh(poorPLYPath: str, originalVertices: str, desiredVertices: int):
    print(f"Refining mesh at:\n{poorPLYPath}\n")

    newPath = createRefinedSavePathLocation(poorPLYPath)

    #print(f'newPath = {newPath}')
    #prin()

    montecarloMeshSet = upsampleMesh(poorPLYPath, newPath, originalVertices, desiredVertices)
    saveRefinedMesh(montecarloMeshSet, newPath, 'montecarlo')

    #prin()

    #print('==========================================================================')
    #print('Mesh is now ready to be simplified:')

    refinedMeshSet, finalVertexCount = simplifyMesh(newPath, desiredVertices)
    saveRefinedMesh(refinedMeshSet, newPath, 'refined')

    return finalVertexCount


def upsampleMesh(originalPath: str, newPath: str, originalVertices: int, desiredVertices: int):
    # create a new MeshSet
    ms = pymeshlab.MeshSet()

    # load a new mesh in the MeshSet, and sets it as current mesh
    ms.load_new_mesh(originalPath)
    #print(f'ms length after loading original = {len(ms)}')
    #print(f'Current mesh = {ms.current_mesh()}\n')
    
    # A MeshSet (and MeshLab) can open multiple meshes in the same Project.
    # For refinement, we must only load one mesh at a time.
    assert len(ms) == 1

    # set the first mesh (id 0) as current mesh
    ms.set_current_mesh(0)

    # Small check to see if the right mesh was loaded.
    assert ms.current_mesh().vertex_number() == originalVertices



    # Montecarlo gives an exact number of samples.
    montecarloSamples = desiredVertices

    # Create an uniformly sampled point cloud.
    ms.apply_filter('generate_sampling_montecarlo', samplenum = montecarloSamples)

    # Note that this creates a new layer/mesh in MeshLab.
    assert len(ms) == 2

    # Small check to see if the point cloud has the right number of samples.
    assert ms.current_mesh().vertex_number() == desiredVertices

    # Save the point cloud before surface reconstruction.
    saveRefinedMesh(ms, newPath, 'point cloud')

    #print(f'Point cloud has {ms.current_mesh().vertex_number()} vertices')
    #print(f'Current mesh = {ms.current_mesh()}\n')

    # Once we have a good point cloud, create a mesh with uniform faces from it.
    print('Executing Screened Poisson surface reconstruction algorithm:')
    ms.apply_filter('generate_surface_reconstruction_screened_poisson')

    # # Screened Poisson creates a new layer.
    # print(f"\nMesh set size after upsampling = {len(ms)}")
    # print(f'Current mesh = {ms.current_mesh()} and has {ms.current_mesh().vertex_number()} vertices\n')

    #for i, mesh in enumerate(ms):
    #    print(f'Mesh {i} = {mesh} -> {mesh.vertex_number()}')

    return ms


# Source: https://stackoverflow.com/questions/65419221/how-to-use-pymeshlab-to-reduce-vertex-number-to-a-certain-number
def simplifyMesh(newPath: str, desiredVertices: int):
    # Creating a new MeshSet and only loading the Poisson-sampled mesh seems to be the only way to get Edge Collapse working again.
    # A MeshSet/project results in Edge Collapse not changing the number of faces after the first iteration, even with a decreasing desiredFaces parameter.
    # Also can't find a 'delete mesh/layer from MeshSet' function.
    ms = pymeshlab.MeshSet()
    # ms.load_new_mesh('data/refined meshes/Airplane/61/poisson.ply')
    # ms.load_new_mesh(f'{newPath}/poisson.ply')
    ms.load_new_mesh(f'{newPath}/montecarlo.ply')

    assert len(ms) == 1

    # According to the Euler characteristic of meshes, the number of faces is roughly twice the number of vertices.
    # To better ensure that the vertex count doesn't fall beneath the desired amount, add 100.
    desiredFaces = desiredVertices * 2 #+ 100

    # 30.000 vertices -roughly-> 15.000 vertices
    #desiredFaces = desiredVertices * 3 

    #print(f'desiredFaces: {desiredFaces}')

    #print(f'Current mesh = {ms.current_mesh()} -> {ms.current_mesh().vertex_number()}\n')
    #prin()

    while (ms.current_mesh().vertex_number() > desiredVertices):
        ms.apply_filter('meshing_decimation_quadric_edge_collapse', targetfacenum=desiredFaces)#, preservenormal=True)
        #print(f"Decimated to {desiredFaces} faces, new mesh has {ms.current_mesh().vertex_number()} vertices")

        #print(f'Current mesh = {ms.current_mesh()} -> {ms.current_mesh().vertex_number()}\n')
        #prin()

        #Refine our estimation to slowly converge to TARGET vertex number
        desiredFaces = desiredFaces - (ms.current_mesh().vertex_number() - desiredVertices)
        #desiredFaces = desiredFaces - 1

    # Small check to see if the mesh's vertices are now the desired amount.
    newVertices = ms.current_mesh().vertex_number()
    #print(f'{newVertices} =?= {desiredVertices}\n')

    if (newVertices < desiredVertices):
        print(f"This mesh has {newVertices} instead of {desiredVertices}")

    # TODO Allow vertex counts close to desired?
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

    print(f'\nSaving the new PLY mesh to:\n{refinedPLYComplete}')


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