# Multimedia retrieval 
This is a multimedia retrieval system, which takes a query shape and returns similar shapes from the database.
Use alt and control with the mouse to move the shape. It uses Open3D to render the shapes.

## How to run the project
The full application only works on Windows. I have verified with PyCharm that the script can run.
Please install all the packages from the requirements.txt located on the same layer as this readme.

Then run the main.py in src for the offline part.
Or run main.py in the app folder for the GUI

Important: Run from the repository root like this. It will indicate with a warning if it is done incorrectly
```commandline
python3 src/main.py
```

or

```commandline
python3 app/main.py
```

## Other notes
Please be aware that querying takes a long time since the convex hull etc. is computed for the shapes.
It didn't take more than 30 seconds on my system, but maybe some large shapes will slow it down substantially

The paths are printed to the command line after the query has been performed if it would take too long. 
They are in the correct ordering and can then be used in the ply viewer tab.
