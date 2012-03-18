#/usr/bin/env python

#> \file
#> \author Thiranja Prasad Babarenda Gamage
#> \brief 
#>
#> \section LICENSE
#>
#> Version: MPL 1.1/GPL 2.0/LGPL 2.1
#>
#> The contents of this file are subject to the Mozilla Public License
#> Version 1.1 (the "License"); you may not use this file except in
#> compliance with the License. You may obtain a copy of the License at
#> http://www.mozilla.org/MPL/
#>
#> Software distributed under the License is distributed on an "AS IS"
#> basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
#> License for the specific language governing rights and limitations
#> under the License.
#>
#> The Original Code is Numerical Validation of elasticity problems in OpenCMISS
#>
#> The Initial Developer of the Original Code is Thiranja Prasad Babarenda Gamage,
#> Auckland, New Zealand, 
#> All Rights Reserved.
#>
#> Contributor(s):
#>
#> Alternatively, the contents of this file may be used under the terms of
#> either the GNU General Public License Version 2 or later (the "GPL"), or
#> the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
#> in which case the provisions of the GPL or the LGPL are applicable instead
#> of those above. If you wish to allow use of your version of this file only
#> under the terms of either the GPL or the LGPL, and not to allow others to
#> use your version of this file under the terms of the MPL, indicate your
#> decision by deleting the provisions above and replace them with the notice
#> and other provisions required by the GPL or the LGPL. If you do not delete
#> the provisions above, a recipient may use your version of this file under
#> the terms of any one of the MPL, the GPL or the LGPL.
#>

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
REGION.FIELDS.FieldComponentLabelSet(GeometricFieldUserNumber,1,2,"z")
REGION.FIELDS.FieldComponentMeshComponentSet(GeometricFieldUserNumber,1,1,1) #FieldUserNumber,FieldVariableUserNumber,FieldComponentUserNumber,MeshComponentUserNumber
REGION.FIELDS.FieldComponentMeshComponentSet(GeometricFieldUserNumber,1,2,1)
REGION.FIELDS.FieldComponentMeshComponentSet(GeometricFieldUserNumber,1,3,1)
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
print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,3)

REGION.WriteIpCoor(GeometricFieldUserNumber,1,"Output/2DMeshIn3DSpace")
REGION.WriteIpBase(GeometricFieldUserNumber,1,"Output/2DMeshIn3DSpace")
REGION.WriteIpNode(GeometricFieldUserNumber,1,"Output/2DMeshIn3DSpace")
REGION.WriteIpElem(GeometricFieldUserNumber,1,"Output/2DMeshIn3DSpace")
REGION.WriteCmCom(GeometricFieldUserNumber,1,"Output/2DMeshIn3DSpace")
REGION.WriteCmguiCom(GeometricFieldUserNumber,1,"Output/2DMeshIn3DSpace")

