class RenderMode:
    SILHOUETTE = "Silhouette"
    LIT = "Lit"
    WIREFRAME = "Wireframe"
    POINT_CLOUD = "Point cloud"
    CONVEX_HULL = "Convex hull"

    ALL = [LIT, SILHOUETTE, WIREFRAME, POINT_CLOUD, CONVEX_HULL]

    # Elements with the same int can be rendered in the same frame
    WINDOW_TYPE = {
        "Lit": 0,
        "Wireframe": 0,
        "Silhouette": 1,
        "Point cloud": 2,
        "Convex hull": 3,
    }
