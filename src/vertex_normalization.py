from hashlib import new
from imageio import save
import pymeshlab

def refineMesh(poorPLYPath: str, desiredVertices: int):
    print(f'Mesh at {poorPLYPath} needs to be refined')

    # TODO
    # Add code that changes mesh so the number of vertices is closer to the desired number of vertices.
    newMesh = "IMPLEMENT"

    saveRefinedMesh(newMesh)

def saveRefinedMesh(refinedPLYFile):
    # TODO
    # Add code to save the refined PLY file.
    refinedPLYLocation = "IMPLEMENT"

    print(f'Saving the new PLY mesh to {refinedPLYLocation}\n')