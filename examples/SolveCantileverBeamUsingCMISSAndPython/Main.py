import sys,os

# Add mesh generation code and its dependency directories to python search PATH. Update them if you move these folders.
sys.path.append("./Code/")
sys.path.append("../../src/")
rootDirectory = os.getcwd()

# Import the mesh generation code functions
from GenerateCMISSMesh import GenerateCantileverBeamMesh

# Generate cubic Hermite cantilever mesh
Extent = [60.0,40.0,40.0]
NumberOfElements = [4,2,2]
OutputDirectory = "./CMISS/Mesh/beam" #Relative to the current (root directory)
GenerateCantileverBeamMesh(Extent,NumberOfElements,OutputDirectory)

# Solve mechanics model
os.chdir("./CMISS/Mechanics/") 
os.system("cm example_5e.com")
os.chdir(rootDirectory) 

