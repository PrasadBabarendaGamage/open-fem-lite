import fem_topology

NumberOfXi = 3

#User Numbers
RegionUserNumber = 1
BasisUserNumber = 1
GeneratedMeshUserNumber = 1
MeshUserNumber = 1
MeshNumberOfComponents = 1
MeshTotalNumberOfElements = 1
GeometricFieldUserNumber = 1
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

#Generate Mesh
REGION.GENERATED_MESHES.GeneratedMeshesCreateStart(GeneratedMeshUserNumber)
REGION.GENERATED_MESHES.GeneratedMeshMeshUserNumberSet(GeneratedMeshUserNumber,MeshUserNumber)
REGION.GENERATED_MESHES.GeneratedMeshBasisSet(GeneratedMeshUserNumber,BasisUserNumber)
REGION.GENERATED_MESHES.GeneratedMeshOriginSet(GeneratedMeshUserNumber,[0,0,0])
REGION.GENERATED_MESHES.GeneratedMeshMaximumExtentSet(GeneratedMeshUserNumber,[10,10,10]) #Size
REGION.GENERATED_MESHES.GeneratedMeshNumberOfElementsSet(GeneratedMeshUserNumber,[2,2,2])
REGION.GENERATED_MESHES.GeneratedMeshesCreateFinish(GeneratedMeshUserNumber)

#Define Geometric Fields
REGION.FIELDS.FieldCreateStart(GeometricFieldUserNumber)
REGION.FIELDS.FieldTypeSet(GeometricFieldUserNumber,"FieldGeometricType")
REGION.FIELDS.FieldMeshSet(GeometricFieldUserNumber,MeshUserNumber)
REGION.FIELDS.FieldNumberOfFieldVariablesSet(GeometricFieldUserNumber,GeometricFieldNumberOfVariables)
REGION.FIELDS.FieldNumberOfFieldComponentsSet(GeometricFieldUserNumber,1,GeometricFieldNumberOfComponents)
REGION.FIELDS.FieldComponentLabelSet(GeometricFieldUserNumber,1,1,"x")
REGION.FIELDS.FieldComponentLabelSet(GeometricFieldUserNumber,1,2,"y")
REGION.FIELDS.FieldComponentLabelSet(GeometricFieldUserNumber,1,3,"z")
REGION.FIELDS.FieldComponentMeshComponentSet(GeometricFieldUserNumber,1,1,1) #FieldUserNumber,FieldVariableUserNumber,FieldComponentUserNumber,MeshComponentUserNumber
REGION.FIELDS.FieldComponentMeshComponentSet(GeometricFieldUserNumber,1,2,1)
REGION.FIELDS.FieldComponentMeshComponentSet(GeometricFieldUserNumber,1,3,1)
REGION.FIELDS.FieldCreateFinish(GeometricFieldUserNumber)

#Update the geometric field parameters
REGION.GENERATED_MESHES.GeneratedMeshGeometricParametersCalculate(GeometricFieldUserNumber,GeneratedMeshUserNumber)
FieldVariable = 1
print "Element1"
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,1) #element_idx,field_component_idx 
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,2)
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,3)

REGION.WriteIpCoor(GeometricFieldUserNumber,1,"Output/3D/REGION")
REGION.WriteIpBase(GeometricFieldUserNumber,1,"Output/3D/REGION")
REGION.WriteIpNode(GeometricFieldUserNumber,1,"Output/3D/REGION")
REGION.WriteIpElem(GeometricFieldUserNumber,1,"Output/3D/REGION")
