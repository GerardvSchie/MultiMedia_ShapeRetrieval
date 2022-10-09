import pymeshlab
import os

def refineMesh(poorPLYPath: str, originalVertices: str, desiredVertices: int):
    newPath = createRefinedSavePathLocation(poorPLYPath)

    #print(f'newPath = {newPath}')
    #prin()

    poissonMeshSet = upsampleMesh(poorPLYPath, originalVertices, desiredVertices)
    saveRefinedMesh(poissonMeshSet, newPath, 'poisson')

    #prin()

    #print('==========================================================================')
    #print('Mesh is now ready to be simplified:')

    refinedMeshSet, finalVertexCount = simplifyMesh(newPath, desiredVertices)
    saveRefinedMesh(refinedMeshSet, newPath, 'refined')

    return finalVertexCount


def upsampleMesh(originalPath: str, originalVertices: int, desiredVertices: int):
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



    # Increase gently until number of points in the cloud is bigger than desired.
    poissonSamples = desiredVertices

    #print(f'Trying {poissonSamples} Poisson sample size:')

    # Create an uniformly sampled point cloud.
    ms.apply_filter('generate_sampling_poisson_disk', exactnumflag = True, samplenum = poissonSamples)

    # Note that this creates a new layer/mesh in MeshLab.
    assert len(ms) == 2

    #print(f'(Current mesh =) Point cloud has {ms.current_mesh().vertex_number()} vertices')
    #print(f'Current mesh = {ms.current_mesh()}\n')

    cloudLimit = desiredVertices #+ 100
    #cloudLimit = desiredVertices * 1.02

    # The cloud isn't big enough, keep trying.
    # Add a little bit more than desired so the chances of decimation going below desired occurs.
    while (ms.current_mesh().vertex_number() < cloudLimit):
        #print('=======================  Point cloud was to small, trying again:')

        # 'Reset' the MeshSet by selecting the original mesh again.
        ms.set_current_mesh(0)

        #print(f'ms length after setting current mesh to original again = {len(ms)}')
        #print(f'Current mesh = {ms.current_mesh()}')

        # Small check to see if the right mesh was loaded.
        assert ms.current_mesh().vertex_number() == originalVertices

        # Increase the Poisson sample size.
        #poissonSamples += 100
        poissonSamples += 10

        #print(f'Trying {poissonSamples} Poisson sample size:')

        # Try again
        ms.apply_filter('generate_sampling_poisson_disk', exactnumflag = True, samplenum = poissonSamples)

        #print(f'(Current mesh =) Point cloud has {ms.current_mesh().vertex_number()} vertices')
        #print(f'Current mesh = {ms.current_mesh()}\n')

    #print('THE POINT CLOUD IS BIG ENOUGH NOW:')
    #print(f'{ms.current_mesh().vertex_number()} vertices > {desiredVertices}')

    # Once we have a good point cloud, create a mesh with uniform faces from it.
    ms.apply_filter('generate_surface_reconstruction_ball_pivoting')
    #print('Executing Ball Pivoting algorithm')

    # Ball pivoting changes the point cloud layer instead of putting the result in a new layer.
    #print(len(ms))

    # Ball pivoting may leave holes in the mesh.
    # Close any holes in the mesh to make it watertight.
    ms.apply_filter('meshing_close_holes')
    #print('Mesh made watertight\n')

    # Close holes also changes the layer itself.
    #print(f'Final len(ms) = {len(ms)}')

    #for i, mesh in enumerate(ms):
    #    print(f'Mesh {i} = {mesh} -> {mesh.vertex_number()}')

    # Sometimes the Poisson sampling isn't big enough and the first decimation creates less than 10.000 vertices.
    # What causes the crash?
    print(f'Final Poisson mesh vertex number = {ms.current_mesh().vertex_number()}')

    #print(f'Current mesh = {ms.current_mesh()} -> {ms.current_mesh().vertex_number()}\n')

    return ms


# Source: https://stackoverflow.com/questions/65419221/how-to-use-pymeshlab-to-reduce-vertex-number-to-a-certain-number
def simplifyMesh(newPath: str, desiredVertices: int):
    # Creating a new MeshSet and only loading the Poisson-sampled mesh seems to be the only way to get Edge Collapse working again.
    # A MeshSet/project results in Edge Collapse not changing the number of faces after the first iteration, even with a decreasing desiredFaces parameter.
    # Also can't find a 'delete mesh/layer from MeshSet' function.
    ms = pymeshlab.MeshSet()
    # ms.load_new_mesh('data/refined meshes/Airplane/61/poisson.ply')
    ms.load_new_mesh(f'{newPath}/poisson.ply')

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
    print(f'{newVertices} =?= {desiredVertices}\n')
    # TODO Allow vertex counts close to desired?
    #assert newVertices == desiredVertices

    return ms, newVertices
    #prin()


def saveRefinedMesh(refinedMeshSet, path, fileName):
    refinedPLYComplete = f"{path}/{fileName}.ply"

    # Refined PLY folder does not exist
    if not os.path.exists(path):
        os.makedirs(path)

    # save the current selected mesh
    refinedMeshSet.save_current_mesh(refinedPLYComplete)

    #print(f'Saving the new PLY mesh to:\n{refinedPLYComplete}\n')


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