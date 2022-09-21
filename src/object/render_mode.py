class RenderMode:
    UNLIT = "Unlit"
    LIT = "Lit"
    NORMALS = "Normals"
    DEPTH = "Depth"
    WIREFRAME = "Wireframe"
    POINT_CLOUD = "Point cloud"
    CONVEX_HULL = "Convex hull"

    ALL = [UNLIT, LIT, NORMALS, DEPTH, WIREFRAME, POINT_CLOUD, CONVEX_HULL]

    # Elements with the same int can be rendered in the same frame
    WINDOW_TYPE = {
        "Unlit": 0,
        "Lit": 0,
        "Normals": 0,
        "Depth": 0,
        "Wireframe": 1,
        "Point cloud": 1,
        "Convex hull": 2,
    }
