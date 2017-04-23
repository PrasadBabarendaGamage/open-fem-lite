import fem_topology
import fem_quadratureRoutines
import fem_miscellaneous_routines
import math_routines
from subprocess import call

WORLD_REGION = fem_topology.femInitialize()
#=================================================================================================================================

RegionUserNumber = 1
WORLD_REGION.RegionsCreateStart(RegionUserNumber)
WORLD_REGION.RegionsCreateFinish(RegionUserNumber)
REGION1 = WORLD_REGION.RegionsRegionGet(RegionUserNumber)

#Existing 3D Mesh parameters
NumberOfXi = 3
NumberOfGaussXi = [4,4,4]
BasisUserNumber1 = 1
BasisUserNumber2 = 2
GeneratedMeshUserNumber = 1
MeshUserNumber = 1
MeshNumberOfComponents = 1
MeshTotalNumberOfElements = 1
GeometricFieldUserNumber = 1
GeometricFieldNumberOfVariables = 1
GeometricFieldNumberOfComponents = NumberOfXi

#Create New Basis soley for defining elements based on GuassPoints
BasisNumberOfGaussXi = []
[BasisNumberOfGaussXi.append(value-1) for value in NumberOfGaussXi]
REGION1.BASES.BasesCreateStart(BasisUserNumber1)
REGION1.BASES.BasisTypeSet(BasisUserNumber1,"3DLinearLagrange")
REGION1.BASES.BasisNumberOfXiCoordinatesSet(BasisUserNumber1,NumberOfXi)
REGION1.BASES.BasisNumberOfXiCoordinatesSet(BasisUserNumber1,NumberOfXi)
REGION1.BASES.BasisQuadratureNumberOfGaussXiSet(BasisUserNumber1,BasisNumberOfGaussXi)
REGION1.BASES.BasesCreateFinish(BasisUserNumber1)

#Generate Mesh
REGION1.GENERATED_MESHES.GeneratedMeshesCreateStart(GeneratedMeshUserNumber)
REGION1.GENERATED_MESHES.GeneratedMeshMeshUserNumberSet(GeneratedMeshUserNumber,MeshUserNumber)
REGION1.GENERATED_MESHES.GeneratedMeshBasisSet(GeneratedMeshUserNumber,BasisUserNumber1)
REGION1.GENERATED_MESHES.GeneratedMeshOriginSet(GeneratedMeshUserNumber,[0,0,0])
REGION1.GENERATED_MESHES.GeneratedMeshMaximumExtentSet(GeneratedMeshUserNumber,[1.0,1.0,1.0]) #Size
REGION1.GENERATED_MESHES.GeneratedMeshNumberOfElementsSet(GeneratedMeshUserNumber,NumberOfGaussXi)
REGION1.GENERATED_MESHES.GeneratedMeshesCreateFinish(GeneratedMeshUserNumber)

#Define Geometric Fields
REGION1.FIELDS.FieldCreateStart(GeometricFieldUserNumber)
REGION1.FIELDS.FieldTypeSet(GeometricFieldUserNumber,"FieldGeometricType")
REGION1.FIELDS.FieldMeshSet(GeometricFieldUserNumber,MeshUserNumber)
REGION1.FIELDS.FieldNumberOfFieldVariablesSet(GeometricFieldUserNumber,GeometricFieldNumberOfVariables)
REGION1.FIELDS.FieldNumberOfFieldComponentsSet(GeometricFieldUserNumber,1,GeometricFieldNumberOfComponents)
REGION1.FIELDS.FieldComponentLabelSet(GeometricFieldUserNumber,1,1,"x")
REGION1.FIELDS.FieldComponentLabelSet(GeometricFieldUserNumber,1,2,"y")
REGION1.FIELDS.FieldComponentLabelSet(GeometricFieldUserNumber,1,3,"z")
REGION1.FIELDS.FieldComponentMeshComponentSet(GeometricFieldUserNumber,1,1,1) #FieldUserNumber,FieldVariableUserNumber,FieldComponentUserNumber,MeshComponentUserNumber
REGION1.FIELDS.FieldComponentMeshComponentSet(GeometricFieldUserNumber,1,2,1)
REGION1.FIELDS.FieldComponentMeshComponentSet(GeometricFieldUserNumber,1,3,1)
REGION1.FIELDS.FieldCreateFinish(GeometricFieldUserNumber)

#Update the geometric field parameters
REGION1.GENERATED_MESHES.GeneratedMeshGeometricParametersCalculate(GeometricFieldUserNumber,GeneratedMeshUserNumber)
FieldVariable = 1
print "Element1"
print REGION1.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,1) #element_idx,field_component_idx 
print REGION1.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,2)
print REGION1.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,3)

BASIS = REGION1.BASES.BasisGlobalGet(BasisUserNumber1)
fem_quadratureRoutines.GAUSS1_MATERIAL_POINTS(BASIS)
GaussElementNodePositions = BASIS.QUADRATURE.GAUSS_POSITIONS

FieldVariable = 1
VersionNumber = 1
DerivativeNumber = 1
print GaussElementNodePositions
for ng in range(len(GaussElementNodePositions)):
    MeshNodeNumber = ng+1
    for FieldComponentNumber in range(1,GeometricFieldNumberOfComponents+1):
        REGION1.FIELDS.FieldParameterSetUpdateNode(GeometricFieldUserNumber,FieldVariable,VersionNumber,DerivativeNumber,MeshNodeNumber,FieldComponentNumber,GaussElementNodePositions[ng][FieldComponentNumber-1])

REGION1.WriteIpCoor(GeometricFieldUserNumber,1,"./REGION1")
REGION1.WriteIpBase(GeometricFieldUserNumber,1,"./REGION1")
REGION1.WriteIpNode(GeometricFieldUserNumber,1,"./REGION1")
REGION1.WriteIpElem(GeometricFieldUserNumber,1,"./REGION1")

call(['cm', 'Exportcm'])

#Create Default Basis
REGION1.BASES.BasesCreateStart(BasisUserNumber2)
REGION1.BASES.BasisTypeSet(BasisUserNumber2,"3DCubicHermite")
REGION1.BASES.BasisNumberOfXiCoordinatesSet(BasisUserNumber2,NumberOfXi)
REGION1.BASES.BasisNumberOfXiCoordinatesSet(BasisUserNumber2,NumberOfXi)
REGION1.BASES.BasisQuadratureNumberOfGaussXiSet(BasisUserNumber2,NumberOfGaussXi)
REGION1.BASES.BasesCreateFinish(BasisUserNumber2)

DatapointGroupUserNumber = 1
DatapointGroupNumberOfComponents = 3
REGION1.DATAPOINTS.DatapointGroupCreateStart(DatapointGroupUserNumber)
REGION1.DATAPOINTS.DatapointGroupLabelSet(DatapointGroupUserNumber,"GeometricData")
REGION1.DATAPOINTS.DatapointGroupNumberOfComponentsSet(DatapointGroupUserNumber,DatapointGroupNumberOfComponents)
REGION1.DATAPOINTS.DatapointGroupComponentLabelSet(DatapointGroupUserNumber,1,"x")
REGION1.DATAPOINTS.DatapointGroupComponentLabelSet(DatapointGroupUserNumber,2,"y")
REGION1.DATAPOINTS.DatapointGroupComponentLabelSet(DatapointGroupUserNumber,3,"z")
REGION1.DATAPOINTS.DatapointGroupCreateFinish(DatapointGroupUserNumber)

GaussPositions = REGION1.BASES.BasisQuadratureGaussPositionsGet(BasisUserNumber2)
for nd in range(1,REGION1.BASES.BasisQuadratureNumberOfGaussPositionsGet(BasisUserNumber2)+1):
    REGION1.DATAPOINTS.DatapointAdd(DatapointGroupUserNumber,nd)
    for ni in range(1,DatapointGroupNumberOfComponents+1):
        REGION1.DATAPOINTS.DatapointComponentValueSet(DatapointGroupUserNumber,nd,ni,GaussPositions[nd-1][ni-1])

REGION1.WriteIpData(DatapointGroupUserNumber,"./REGION1")
call(['perl','/home/psam012/usr/cmiss/CmConvert.pm','./REGION1.ipdata','-force'])

DatapointGroupUserNumber2 = 2
REGION1.ReadIpxi(DatapointGroupUserNumber2,'CMISS','test')
print REGION1.DATAPOINTS.DatapointsListGet(DatapointGroupUserNumber2)
print REGION1.DATAPOINTS.DatapointComponentValueGet(DatapointGroupUserNumber2,1,1)
REGION1.WriteIpData(DatapointGroupUserNumber2,"./REGIONipxi1")

def findClosestGausspoint(DATAPOINTS,Mesh):
	for nd in range(DATAPOINTS.n):
		found = False
		while not found:
			for ng in range(Mesh.totalnelem):
				if ((DATAPOINTS.xi[nd][0] >= Mesh.NODES[(Mesh.ELEMENTS[ng].ELEMENT_NODES[0])-1].coordinates[0]) and \
					(DATAPOINTS.xi[nd][0] <= Mesh.NODES[(Mesh.ELEMENTS[ng].ELEMENT_NODES[1])-1].coordinates[0]) and \
					(DATAPOINTS.xi[nd][1] >= Mesh.NODES[(Mesh.ELEMENTS[ng].ELEMENT_NODES[0])-1].coordinates[1]) and \
					(DATAPOINTS.xi[nd][1] <= Mesh.NODES[(Mesh.ELEMENTS[ng].ELEMENT_NODES[2])-1].coordinates[1]) and \
					(DATAPOINTS.xi[nd][2] >= Mesh.NODES[(Mesh.ELEMENTS[ng].ELEMENT_NODES[0])-1].coordinates[2]) and \
					(DATAPOINTS.xi[nd][2] <= Mesh.NODES[(Mesh.ELEMENTS[ng].ELEMENT_NODES[4])-1].coordinates[2])):
					found = True
					DATAPOINTS.ng.append(ng)
					#print 'wha'
					#print ng
					break
