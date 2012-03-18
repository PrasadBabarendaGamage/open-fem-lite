import fem_topology

NumberOfXi = 2

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
REGION.BASES.BasisTypeSet(BasisUserNumber,"2DCubicHermite")
REGION.BASES.BasisNumberOfXiCoordinatesSet(BasisUserNumber,NumberOfXi)
REGION.BASES.BasesCreateFinish(BasisUserNumber)

TotalNumberOfNodes = 6
REGION.NODES.NodesCreateStart(TotalNumberOfNodes)

MeshNumberOfComponents = 1
MeshTotalNumberOfElements = 2
MeshUserNumber = 1
REGION.MESHES.MeshesCreateStart(MeshUserNumber)
REGION.MESHES.MeshNumberOfDimensionsSet(MeshUserNumber,NumberOfXi)
REGION.MESHES.MeshNumberOfComponentsSet(MeshUserNumber,MeshNumberOfComponents)
MeshComponent = 1
REGION.MESHES.MeshElementsCreateStart(MeshUserNumber,MeshComponent,BasisUserNumber)
REGION.MESHES.MeshElementsNodesSet(MeshUserNumber,MeshComponent,1,[1,2,3,4])
REGION.MESHES.MeshElementsNodesSet(MeshUserNumber,MeshComponent,2,[3,4,5,6]) #element,element_nodes
#REGION.MESHES.MeshElementsNodeVersionSet(MeshUserNumber,MeshComponent,1,8,1,7) #element,node,derivative,version
#REGION.MESHES.MeshElementsNodeVersionSet(MeshUserNumber,MeshComponent,2,5,1,6) #element,node,derivative,version
REGION.MESHES.MeshElementsCreateFinish(MeshUserNumber,MeshComponent)
REGION.MESHES.MeshesCreateFinish(MeshUserNumber)

#Define Geometric Fields
REGION.FIELDS.FieldCreateStart(GeometricFieldUserNumber)
REGION.FIELDS.FieldTypeSet(GeometricFieldUserNumber,"FieldGeometricType")
REGION.FIELDS.FieldMeshSet(GeometricFieldUserNumber,MeshUserNumber)
REGION.FIELDS.FieldNumberOfFieldVariablesSet(GeometricFieldUserNumber,GeometricFieldNumberOfVariables)
REGION.FIELDS.FieldNumberOfFieldComponentsSet(GeometricFieldUserNumber,1,GeometricFieldNumberOfComponents)
REGION.FIELDS.FieldComponentLabelSet(GeometricFieldUserNumber,1,1,"x")
REGION.FIELDS.FieldComponentLabelSet(GeometricFieldUserNumber,1,2,"y")
REGION.FIELDS.FieldComponentMeshComponentSet(GeometricFieldUserNumber,1,1,1) #FieldUserNumber,FieldVariableUserNumber,FieldComponentUserNumber,MeshComponentUserNumber
REGION.FIELDS.FieldComponentMeshComponentSet(GeometricFieldUserNumber,1,2,1)
REGION.FIELDS.FieldCreateFinish(GeometricFieldUserNumber)

FieldVariable = 1
REGION.FIELDS.FieldParameterSetUpdateNode(GeometricFieldUserNumber,FieldVariable,1,1,6,1,30.0)#version_idx,derivative_idx,node_idx,field_component_idx,value
REGION.FIELDS.FieldParameterSetUpdateNode(GeometricFieldUserNumber,FieldVariable,1,1,2,1,30.0)
REGION.FIELDS.FieldParameterSetUpdateNode(GeometricFieldUserNumber,FieldVariable,1,1,2,2,40.0)
REGION.FIELDS.FieldParameterSetUpdateNode(GeometricFieldUserNumber,FieldVariable,1,1,3,1,30.0)
REGION.FIELDS.FieldParameterSetUpdateNode(GeometricFieldUserNumber,FieldVariable,1,1,3,2,40.0)
REGION.FIELDS.FieldParameterSetUpdateNode(GeometricFieldUserNumber,FieldVariable,1,1,4,1,30.0)
REGION.FIELDS.FieldParameterSetUpdateNode(GeometricFieldUserNumber,FieldVariable,1,1,4,2,40.0)


print "Element1"
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,1) #element_idx,field_component_idx 
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,2)

REGION.WriteIpCoor(GeometricFieldUserNumber,1,"Output/2DMeshIn2DSpace")
REGION.WriteIpBase(GeometricFieldUserNumber,1,"Output/2DMeshIn2DSpace")
REGION.WriteIpNode(GeometricFieldUserNumber,1,"Output/2DMeshIn2DSpace")
REGION.WriteIpElem(GeometricFieldUserNumber,1,"Output/2DMeshIn2DSpace")
REGION.WriteCmCom(GeometricFieldUserNumber,1,"Output/2DMeshIn2DSpace")
REGION.WriteCmguiCom(GeometricFieldUserNumber,1,"Output/2DMeshIn2DSpace")

