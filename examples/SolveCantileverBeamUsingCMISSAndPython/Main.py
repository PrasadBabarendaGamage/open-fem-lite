import sys,os

# Add mesh generation code and its dependency directories to python search PATH. Update them if you move these folders.
sys.path.append("./Code/")
sys.path.append("../../src/")
rootDirectory = os.getcwd()

# Import the mesh generation code functions
from CMISSGenerateMesh import GenerateCantileverBeamMesh
from CMISSMeshRoutines import ReadInMesh,ExtractNodalParameters

# Generate cubic Hermite cantilever mesh
Extent = [60.0,40.0,40.0]
NumberOfElements = [4,2,2]
OutputDirectory = "./CMISS/Mesh/beam" #Relative to the current (root directory)
GenerateCantileverBeamMesh(Extent,NumberOfElements,OutputDirectory)

# Solve mechanics model
os.chdir("./CMISS/Mechanics/") 
os.system("cm example_5e.com")
os.chdir(rootDirectory) 

# Read in deformed mesh
REGION = ReadInMesh("./CMISS/Mechanics/Output/beam")

# Extract nodal parameters (modify ExtractNodalParameters routine in CMISSMeshRoutines.py to obtain parameter list in shape/form required for the CubicHermite -> Bezier conversion code )
Parameters = ExtractNodalParameters(REGION)
print Parameters
