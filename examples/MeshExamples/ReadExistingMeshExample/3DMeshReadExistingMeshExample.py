import fem_topology

NumberOfXi = 3

#User Numbers
RegionUserNumber = 1
BasisUserNumber = 1
GeneratedMeshUserNumber = 1
MeshNumberOfComponents = 1
MeshTotalNumberOfElements = 1
GeometricFieldNumberOfVariables = 1
GeometricFieldNumberOfComponents = NumberOfXi

#Initialize and Create Regions
WORLD_REGION = fem_topology.femInitialize()
WORLD_REGION.RegionsCreateStart(RegionUserNumber)
WORLD_REGION.RegionsCreateFinish(RegionUserNumber)
REGION = WORLD_REGION.RegionsRegionGet(RegionUserNumber)

#Create Basis
REGION.BASES.BasesCreateStart(BasisUserNumber)
REGION.BASES.BasisTypeSet(BasisUserNumber,"3DCubicHermite")
REGION.BASES.BasisNumberOfXiCoordinatesSet(BasisUserNumber,NumberOfXi)
REGION.BASES.BasesCreateFinish(BasisUserNumber)

MeshUserNumber = 1
GeometricFieldUserNumber = 1
REGION.ReadMesh(BasisUserNumber,MeshUserNumber,GeometricFieldUserNumber,"CMISS","Input/BeamCHComp1V1NodeVersions1","Input/BeamCHComp1V1ElementsVersions1")

FieldVariable = 1
print "Element1"
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,1) #element_idx,field_component_idx 
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,2)
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,3)
print "Element2"
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,2,1) #element_idx,field_component_idx 
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,2,2)
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,2,3)
print "Element4"
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,4,1) #element_idx,field_component_idx 
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,4,2)
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,4,3)

