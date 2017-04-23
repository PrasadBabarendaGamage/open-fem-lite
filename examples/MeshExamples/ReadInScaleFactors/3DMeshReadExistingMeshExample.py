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


import re
ipline_input_filename = 'mesh1_scale_factor_reference'
ipline_input_file = open(ipline_input_filename + '.ipline').read()
ipline_lines = re.split(r'[\n\\]', ipline_input_file)

ipline_output_filename = 'mesh1_scale_factor_reference_updated'
ipline_output_file = open(ipline_output_filename +'.ipline', 'w')

for line_idx, line in enumerate(ipline_lines):
    split_line = line.split()
    if line_idx>2:
        if not split_line ==[]:
            element = int(split_line[3].split(';')[0])
            element_node_idx = int(split_line[5].split(':')[0])
            derivative = int(split_line[9].split('=')[-1])
            ipline_output_file.write(' Basis 1; element {0}; vertex {1}: scale factor for nk={2} is    {3:17.16E}\n'.format(
                element, element_node_idx, derivative, 0.0))
    else:
        ipline_output_file.write(line+'\n')
ipline_output_file.close()
#BASIS = REGION.BASES.BasisGlobalGet(BASIS_USER_NUMBER)

##Create the default node set
#TOTAL_NUMBER_OF_NODES = int(IPNODE_LINES[3].split()[-1]) #Extract last number of line 3
#REGION.NODES.NodesCreateStart(TOTAL_NUMBER_OF_NODES)

##Create the mesh
##TOTAL_NUMBER_OF_ELEMENTS = int(IPELEM_LINES[3].split()[-1]) #Extract last number of line 3
#NUMBER_OF_FIELD_COMPONENTS = 1
#REGION.MESHES.MeshesCreateStart(MESH_USER_NUMBER)
#REGION.MESHES.MeshNumberOfDimensionsSet(MESH_USER_NUMBER,BASIS.NUMBER_OF_XIC)
#REGION.MESHES.MeshNumberOfComponentsSet(MESH_USER_NUMBER,NUMBER_OF_FIELD_COMPONENTS)

##!Create the elements
##Initialize Mesh Elements
#MESH_COMPONENT_NUMBER = 1
#REGION.MESHES.MeshElementsCreateStart(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,BASIS.USER_NUMBER)

##Loop through and read element node numbers
#for line in range(len(IPELEM_LINES)):
#    
#    if IPELEM_LINES[line][0:16] == " Element number ":
#        LOCAL_ELEMENT_NUMBER = int(IPELEM_LINES[line].split()[-1])
#        ELEMENT_NODES = [int(values) for values in IPELEM_LINES[line+BASIS.NUMBER_OF_XIC+2].split()[8:8+BASIS.NUMBER_OF_NODES]]
#        if DEBUG==True: print "Element Number:{0}, element nodes: {1}".format(LOCAL_ELEMENT_NUMBER,ELEMENT_NODES)
#        REGION.MESHES.MeshElementsNodesSet(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,LOCAL_ELEMENT_NUMBER,ELEMENT_NODES)
#        line = line + 1 + BASIS.NUMBER_OF_XIC+2
#        while IPELEM_LINES[line][0:12] == " The version":
#            VERSION_NUMBER = int(IPELEM_LINES[line].split()[-1])
#            LOCAL_NODE_NUMBER = int(IPELEM_LINES[line].split()[8].rstrip(","))
#            occurrence=int(IPELEM_LINES[line].split()[5])
#            component=int(IPELEM_LINES[line].split()[9].split('=')[-1])
#            element_node_idx = fem_miscellaneous_routines.indexOfNthOccurrence(occurrence, LOCAL_NODE_NUMBER, ELEMENT_NODES)
#            for derivative_idx in range(BASIS.NUMBER_OF_PARTIAL_DERIVATIVES):
#                REGION.MESHES.MeshElementsNodeVersionSet(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,LOCAL_ELEMENT_NUMBER,element_node_idx+1,derivative_idx+1,VERSION_NUMBER,component) 
#            line +=1
##            line = line + 1 + BASIS.NUMBER_OF_XIC+2
##            VERSION_NUMBER = 1
##            for node_idx in range(BASIS.NUMBER_OF_NODES):
##                for derivative_idx in range(BASIS.NUMBER_OF_PARTIAL_DERIVATIVES):
##                    REGION.MESHES.MeshElementsNodeVersionSet(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,LOCAL_ELEMENT_NUMBER,node_idx+1,derivative_idx+1,VERSION_NUMBER) 
##            while IPELEM_LINES[line][0:12] == " The version":
##                VERSION_NUMBER = int(IPELEM_LINES[line].split()[-1])
##                LOCAL_NODE_NUMBER = int(IPELEM_LINES[line].split()[8].rstrip(","))
##                if DEBUG==True: print "Local Node Number:{0}, version number: {1}".format(LOCAL_NODE_NUMBER,VERSION_NUMBER)
##                node_idx = ELEMENT_NODES.index(LOCAL_NODE_NUMBER)
##                for derivative_idx in range(BASIS.NUMBER_OF_PARTIAL_DERIVATIVES):
##                    REGION.MESHES.MeshElementsNodeVersionSet(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,LOCAL_ELEMENT_NUMBER,node_idx+1,derivative_idx+1,VERSION_NUMBER) 
##                    #GlobalElementNumber,NodeIndex,DerivativeNumber,VersionNumber
##                line = line + 3

#REGION.MESHES.MeshElementsCreateFinish(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER)
#REGION.MESHES.MeshesCreateFinish(MESH_USER_NUMBER)

##Define Geometric Fields
#REGION.FIELDS.FieldCreateStart(FIELD_USER_NUMBER)
#REGION.FIELDS.FieldTypeSet(FIELD_USER_NUMBER,"FieldGeometricType")
#REGION.FIELDS.FieldMeshSet(FIELD_USER_NUMBER,MESH_USER_NUMBER)
#REGION.FIELDS.FieldNumberOfFieldVariablesSet(FIELD_USER_NUMBER,1)
#REGION.FIELDS.FieldNumberOfFieldComponentsSet(FIELD_USER_NUMBER,1,BASIS.NUMBER_OF_XIC)
#COORDINATE_LABELS = ['x','y','z']
#FIELD_VARIABLE_USER_NUMBER = 1
#for component_idx in range(1,BASIS.NUMBER_OF_XIC+1):
#    REGION.FIELDS.FieldComponentLabelSet(FIELD_USER_NUMBER,1,component_idx,COORDINATE_LABELS[component_idx-1])
#    REGION.FIELDS.FieldComponentMeshComponentSet(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,component_idx,MESH_COMPONENT_NUMBER) #FieldUserNumber,FieldVariableUserNumber,FieldComponentUserNumber,MeshComponentUserNumber
#REGION.FIELDS.FieldCreateFinish(FIELD_USER_NUMBER)

#NUMBER_OF_COMPONENT_DERIVATIVES = [0]*BASIS.NUMBER_OF_XIC
#COMPONENT_VERSIONS_PRESENT = [False]*BASIS.NUMBER_OF_XIC

#for component_idx in range(BASIS.NUMBER_OF_XIC):
#    if BASIS.NUMBER_OF_XIC == 2:
#      NUMBER_OF_COMPONENT_DERIVATIVES[component_idx] = int(IPNODE_LINES[component_idx+7].split()[-1]) #Extract last number of line 3
#    else:
#      NUMBER_OF_COMPONENT_DERIVATIVES[component_idx] = int(IPNODE_LINES[component_idx+8].split()[-1]) #Extract last number of line 3
#      if IPNODE_LINES[component_idx+5].split()[-1] == "Y" or IPNODE_LINES[component_idx+5].split()[-1] == "y":
#          COMPONENT_VERSIONS_PRESENT[component_idx] = True

##Loop through and read node derivatives
#if sum(COMPONENT_VERSIONS_PRESENT) > 0:
#    for line in range(len(IPNODE_LINES)):
#        if IPNODE_LINES[line][0:13] == " Node number ":
#            LOCAL_NODE_NUMBER = int(IPNODE_LINES[line].split()[-1])
#            if DEBUG==True: print "LOCAL_NODE_NUMBER %s" %LOCAL_NODE_NUMBER
#            if sum(COMPONENT_VERSIONS_PRESENT) > 0:
#                line = line + 1
#            for component_idx in range(BASIS.NUMBER_OF_XIC):
#                if COMPONENT_VERSIONS_PRESENT[component_idx] == True:
#                    NUMBER_OF_VERSIONS = int(IPNODE_LINES[line].split()[-1].rstrip())
#                    if NUMBER_OF_VERSIONS > 1:
#                        line = line + 1
#                else:
#                    NUMBER_OF_VERSIONS = 1
#                line = line + 1
#                if DEBUG==True: print "  component_idx %d" %(component_idx+1)
#                ###################### TEMP
#                #NUMBER_OF_VERSIONS = 1
#                ###################### TEMP
#                for version_idx in range(NUMBER_OF_VERSIONS):
#                    if DEBUG==True: print "   version_idx %d" %(version_idx+1)
#                    for derivative_idx in range(NUMBER_OF_COMPONENT_DERIVATIVES[component_idx]+1):
#                        if DEBUG==True: print "   derivative_idx %d" %(derivative_idx+1)
#                        if DEBUG==True: print IPNODE_LINES[line]
#                        VALUE = float(IPNODE_LINES[line].split()[-1])
#                        REGION.FIELDS.FieldParameterSetUpdateNode(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,version_idx+1,derivative_idx+1,LOCAL_NODE_NUMBER,component_idx+1,VALUE)
#                        line = line + 1
#                    if (NUMBER_OF_VERSIONS > 1) and (version_idx!=NUMBER_OF_VERSIONS-1):
#                        line = line + 1
#else:
#    VERSION_NUMBER = 1
#    for line in range(len(IPNODE_LINES)):
#        if DEBUG==True: print IPNODE_LINES[line]
#        if IPNODE_LINES[line][0:13] == " Node number ":
#            LOCAL_NODE_NUMBER = int(IPNODE_LINES[line].split()[-1])
#            if DEBUG==True: print "LOCAL_NODE_NUMBER %s" %LOCAL_NODE_NUMBER
#            line = line + 1
#            for component_idx in range(BASIS.NUMBER_OF_XIC):
#                FIELD_NODE_EXISTS = REGION.FIELDS.FieldParameterNodeCheckExists(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,LOCAL_NODE_NUMBER,component_idx+1)
#                if FIELD_NODE_EXISTS == True:
#                    if DEBUG==True: print "  component_idx %d" %(component_idx+1)
#                    for derivative_idx in range(NUMBER_OF_COMPONENT_DERIVATIVES[component_idx]+1):
#                        if DEBUG==True: print "   derivative_idx %d" %(derivative_idx+1)
#                        if DEBUG==True: print IPNODE_LINES[line]
#                        VALUE = float(IPNODE_LINES[line].split()[-1])
#                        REGION.FIELDS.FieldParameterSetUpdateNode(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,VERSION_NUMBER,derivative_idx+1,LOCAL_NODE_NUMBER,component_idx+1,VALUE)
#                        line = line + 1






#def ReadElementScaleFactors(filename):

#    readdata = open(filename).read()
#    array = re.split(r'[\n\\]', readdata)

#    elementNodes = []
#    elementNodeScaleFactors = []
#    for line in range(len(array)):
#        if array[line][0:9] == "   Nodes:":
#            temp = array[line+1].split()
#            temp = [int(node) for node in temp]
#            elementNodes.append(temp)
#            tempScaleFactors = []
#            for scaleFactorLine in range(1,14):
#                temp = array[line+2+scaleFactorLine].split()
#                temp = [float(node) for node in temp]
#                tempScaleFactors = tempScaleFactors + temp
#            elementNodeScaleFactors.append(tempScaleFactors)

#    return [elementNodes,elementNodeScaleFactors]

#[elementNodes,elementNodeScaleFactors] = ReadElementScaleFactors("beam.exelem")

#print elementNodes[0]
#print elementNodes[0][0]
#print elementNodeScaleFactors



#import fem_topology

#NumberOfXi = 3

##User Numbers
#RegionUserNumber = 1
#BasisUserNumber = 1
#GeneratedMeshUserNumber = 1
#MeshNumberOfComponents = 1
#MeshTotalNumberOfElements = 1
#GeometricFieldNumberOfVariables = 1
#GeometricFieldNumberOfComponents = NumberOfXi

##Initialize and Create Regions
#WORLD_REGION = fem_topology.femInitialize()
#WORLD_REGION.RegionsCreateStart(RegionUserNumber)
#WORLD_REGION.RegionsCreateFinish(RegionUserNumber)
#REGION = WORLD_REGION.RegionsRegionGet(RegionUserNumber)

##Create Basis
#REGION.BASES.BasesCreateStart(BasisUserNumber)
#REGION.BASES.BasisTypeSet(BasisUserNumber,"3DCubicHermite")
#REGION.BASES.BasisNumberOfXiCoordinatesSet(BasisUserNumber,NumberOfXi)
#REGION.BASES.BasesCreateFinish(BasisUserNumber)

#MeshUserNumber = 1
#GeometricFieldUserNumber = 1
#REGION.ReadMesh(BasisUserNumber,MeshUserNumber,GeometricFieldUserNumber,"CMISS","Input/BeamCHComp1V1NodeVersions1","Input/BeamCHComp1V1ElementsVersions1")

#FieldVariable = 1
#print "Element1"
#print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,1) #element_idx,field_component_idx 
#print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,2)
#print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,1,3)
#print "Element2"
#print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,2,1) #element_idx,field_component_idx 
#print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,2,2)
#print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,2,3)
#print "Element4"
#print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,4,1) #element_idx,field_component_idx 
#print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,4,2)
#print REGION.FIELDS.FieldParameterElementValuesGet(GeometricFieldUserNumber,FieldVariable,4,3)

