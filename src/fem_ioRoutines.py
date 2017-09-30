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

import os
import re
import fem_topology
import fem_miscellaneous_routines

#=======================================================================#

#Format

# Group name: database
# #Fields=3
# 1) coordinates, coordinate, rectangular cartesian, #Components=3
#  x.  Value index=1, #Derivatives=0, #Versions=1
#  y.  Value index=2, #Derivatives=0, #Versions=1
#  z.  Value index=3, #Derivatives=0, #Versions=1
# 2) groupName, field, string, #Components=1
#  value.  Value index=4, #Derivatives=0, #Versions=1
# 3) sliceName, field, string, #Components=1
#  value.  Value index=5, #Derivatives=0, #Versions=1
# Node: 1
# 2.660284e+002
# 2.584666e+002
# 4.588235e+001
# SKIN
# image(119)

#=======================================================================#

def throws(error):
    raise RuntimeError(error)

def removeDuplicates(seq,idfun=None):
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

def readvalues(array,currentLine,lineIncrement,valueType):
    temp = array[currentLine+lineIncrement].split()
    if (valueType == "float"):
        temp = float(temp[len(temp)-1])
    elif (valueType == "string"):
        temp = temp[len(temp)-1]
    elif (valueType == "int"):
        temp = int(temp[len(temp)-1])
    else:
        throws("invalid valueType of %s in readvalues routine. Only 'float',,int', and 'string'allowed.")
    return temp

def writeexdataAllGroups(REGION,prefix):
    GROUP_NAMES = removeDuplicates(REGION.FIELDS.FieldComponentAllValuesGet(2,1))
    #print REGION.FIELDS.FieldComponentNumberOfValuesGet(2,1)
    #print GROUP_NAMES 
    #print REGION.FIELDS.FieldComponentAllValuesGet(2,1)
    FILE_OUTPUT = []
    for group in range(len(GROUP_NAMES)):
        FILE_OUTPUT.append(open(prefix+GROUP_NAMES[group]+'.exdata', 'w'))
        FILE_OUTPUT[group].write(' Group name: '+GROUP_NAMES[group]+'\n')
        FILE_OUTPUT[group].write(' #Fields=3\n')
        FILE_OUTPUT[group].write(' 1) coordinates, coordinate, rectangular cartesian, #Components=3\n')
        FILE_OUTPUT[group].write('  x.  Value index=1, #Derivatives=0, #Versions=1\n')
        FILE_OUTPUT[group].write('  y.  Value index=2, #Derivatives=0, #Versions=1\n')
        FILE_OUTPUT[group].write('  z.  Value index=3, #Derivatives=0, #Versions=1\n')
        FILE_OUTPUT[group].write(' 2) groupName, field, string, #Components=1\n')
        FILE_OUTPUT[group].write('  value.  Value index=4, #Derivatives=0, #Versions=1\n')
        FILE_OUTPUT[group].write(' 3) sliceName, field, string, #Components=1\n')
        FILE_OUTPUT[group].write('  value.  Value index=5, #Derivatives=0, #Versions=1\n')
        for globalnode in range(REGION.FIELDS.FieldComponentNumberOfValuesGet(2,1)):
            if GROUP_NAMES[group] == REGION.FIELDS.FieldComponentSingleValueGet(2,1,globalnode):
              FILE_OUTPUT[group].write(' Node: %s\n' % REGION.NODES.NodeLocalNumberGet(globalnode))
              FILE_OUTPUT[group].write(' %e\n' % REGION.FIELDS.FieldComponentSingleValueGet(1,1,globalnode))
              FILE_OUTPUT[group].write(' %e\n' % REGION.FIELDS.FieldComponentSingleValueGet(1,2,globalnode))
              FILE_OUTPUT[group].write(' %e\n' % REGION.FIELDS.FieldComponentSingleValueGet(1,3,globalnode))
              FILE_OUTPUT[group].write(' %s\n' % REGION.FIELDS.FieldComponentSingleValueGet(2,1,globalnode))
              FILE_OUTPUT[group].write(' %s\n' % REGION.FIELDS.FieldComponentSingleValueGet(3,1,globalnode))
              #FILE_OUTPUT[group].write('\n')
    for group in range(len(GROUP_NAMES)):
        FILE_OUTPUT[group].close()

def writeexdatabaseSelectedGroups(REGION,prefix,SELECTED_GROUP_NAMES_LIST):
    GROUP_NAMES = removeDuplicates(REGION.FIELDS.FieldComponentAllValuesGet(2,1))
    #print REGION.FIELDS.FieldComponentNumberOfValuesGet(2,1)
    #print GROUP_NAMES 
    #print REGION.FIELDS.FieldComponentAllValuesGet(2,1)
    FILE_OUTPUT = open(prefix+'ALL.exdata', 'w')
    FILE_OUTPUT.write(' Group name: database\n')
    FILE_OUTPUT.write(' #Fields=3\n')
    FILE_OUTPUT.write(' 1) coordinates, coordinate, rectangular cartesian, #Components=3\n')
    FILE_OUTPUT.write('  x.  Value index=1, #Derivatives=0, #Versions=1\n')
    FILE_OUTPUT.write('  y.  Value index=2, #Derivatives=0, #Versions=1\n')
    FILE_OUTPUT.write('  z.  Value index=3, #Derivatives=0, #Versions=1\n')
    FILE_OUTPUT.write(' 2) groupName, field, string, #Components=1\n')
    FILE_OUTPUT.write('  value.  Value index=4, #Derivatives=0, #Versions=1\n')
    FILE_OUTPUT.write(' 3) sliceName, field, string, #Components=1\n')
    FILE_OUTPUT.write('  value.  Value index=5, #Derivatives=0, #Versions=1\n')
    for globalnode in range(REGION.FIELDS.FieldComponentNumberOfValuesGet(2,1)):
        EXISTS = True
        try:
            SELECTED_GROUP_NAMES_LIST.index(REGION.FIELDS.FieldComponentSingleValueGet(2,1,globalnode))
        except ValueError:
            EXISTS = False
        else:
            #print SELECTED_GROUP_NAMES_LIST.index(REGION.FIELDS.FieldComponentSingleValueGet(2,1,globalnode))
            FILE_OUTPUT.write(' Node: %s\n' % REGION.NODES.NodeLocalNumberGet(globalnode))
            FILE_OUTPUT.write(' %e\n' % REGION.FIELDS.FieldComponentSingleValueGet(1,1,globalnode))
            FILE_OUTPUT.write(' %e\n' % REGION.FIELDS.FieldComponentSingleValueGet(1,2,globalnode))
            FILE_OUTPUT.write(' %e\n' % REGION.FIELDS.FieldComponentSingleValueGet(1,3,globalnode))
            FILE_OUTPUT.write(' %s\n' % REGION.FIELDS.FieldComponentSingleValueGet(2,1,globalnode))
            FILE_OUTPUT.write(' %s\n' % REGION.FIELDS.FieldComponentSingleValueGet(3,1,globalnode))
    FILE_OUTPUT.close()

def writeexdatabaseSelectedGroupsMod(REGION,prefix,SELECTED_GROUP_NAMES_LIST):
    GROUP_NAMES = removeDuplicates(REGION.FIELDS.FieldComponentAllValuesGet(2,1))
    #print REGION.FIELDS.FieldComponentNumberOfValuesGet(2,1)
    #print GROUP_NAMES 
    #print REGION.FIELDS.FieldComponentAllValuesGet(2,1)
    FILE_OUTPUT = open(prefix+'ALL.exdata', 'w')
    FILE_OUTPUT.write(' Group name: database\n')
    FILE_OUTPUT.write(' #Fields=3\n')
    FILE_OUTPUT.write(' 1) coordinates, coordinate, rectangular cartesian, #Components=3\n')
    FILE_OUTPUT.write('  x.  Value index=1, #Derivatives=0, #Versions=1\n')
    FILE_OUTPUT.write('  y.  Value index=2, #Derivatives=0, #Versions=1\n')
    FILE_OUTPUT.write('  z.  Value index=3, #Derivatives=0, #Versions=1\n')
    FILE_OUTPUT.write(' 2) groupName, field, string, #Components=1\n')
    FILE_OUTPUT.write('  value.  Value index=4, #Derivatives=0, #Versions=1\n')
    FILE_OUTPUT.write(' 3) sliceName, field, string, #Components=1\n')
    FILE_OUTPUT.write('  value.  Value index=5, #Derivatives=0, #Versions=1\n')
    for globalnode in range(REGION.FIELDS.FieldComponentNumberOfValuesGet(2,1)):
        EXISTS = True
        try:
            SELECTED_GROUP_NAMES_LIST.index(REGION.FIELDS.FieldComponentSingleValueGet(2,1,globalnode))
        except ValueError:
            EXISTS = False
        else:
            #print SELECTED_GROUP_NAMES_LIST.index(REGION.FIELDS.FieldComponentSingleValueGet(2,1,globalnode))
            FILE_OUTPUT.write(' Node: %s\n' % REGION.NODES.NodeLocalNumberGet(globalnode))
            FILE_OUTPUT.write(' %e\n' % REGION.FIELDS.FieldComponentSingleValueGet(1,1,globalnode))
            FILE_OUTPUT.write(' %e\n' % REGION.FIELDS.FieldComponentSingleValueGet(1,2,globalnode))
            FILE_OUTPUT.write(' %e\n' % float(REGION.FIELDS.FieldComponentSingleValueGet(1,3,globalnode)*(130.0/150.0)))
            FILE_OUTPUT.write(' %s\n' % REGION.FIELDS.FieldComponentSingleValueGet(2,1,globalnode))
            FILE_OUTPUT.write(' %s\n' % REGION.FIELDS.FieldComponentSingleValueGet(3,1,globalnode))
    FILE_OUTPUT.close()

#Standard test
#REGION = readexdata('TEST_DATA_INPUT/testexdataio.exdata')
#writeexdataAllGroups(REGION,'TEST_DATA_OUTPUT/V1PR_')
#writeexdatabaseSelectedGroups(REGION,'V1PR_',['SKIN','LANDMARKS','NIPPLE'])

#Fix a zinc database file when the data has accidentally been digitized with a larger Z dimension.
#REGION = readexdata('V1PR_ALLWRONG.exdata')
#writeexdatabaseSelectedGroupsMod(REGION,'ModV1RD_',['SKIN','BONE''LANDMARKS','NIPPLE'])

#============================================================================

def WriteIpElem(FIELD_VARIABLE,OUTPUT_FILENAME):
    #Get mesh component from the first field component
    NUMBER_OF_FIELD_COMPONENTS = FIELD_VARIABLE.NUMBER_OF_FIELD_COMPONENTS
    FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(1)
    MESH_COMPONENT = FIELD_COMPONENT.MESH_COMPONENT
    NUMBER_OF_ELEMENTS = MESH_COMPONENT.ELEMENTS.NUMBER_OF_ELEMENTS
    FILE = open(OUTPUT_FILENAME + ".ipelem", 'w')
    OUTPUT = \
" CMISS Version 2.1  ipelem File Version 2\n\
 Heading:\n\
 \n\
 The number of elements is ["+"%5d" %NUMBER_OF_ELEMENTS +"]: "+"%5d" %NUMBER_OF_ELEMENTS
    for element_idx in range(NUMBER_OF_ELEMENTS):
        MESH_ELEMENT = MESH_COMPONENT.ELEMENTS.ELEMENTS[element_idx]
        BASIS = MESH_ELEMENT.BASIS
        OUTPUT = OUTPUT +\
" \n\
 Element number ["+"%5d" %MESH_ELEMENT.USER_NUMBER +"]: "+"%5d" %MESH_ELEMENT.USER_NUMBER +"\n\
 The number of geometric Xj-coordinates is [%d]: %d\n" %(NUMBER_OF_FIELD_COMPONENTS,NUMBER_OF_FIELD_COMPONENTS)
        for component_idx in range(NUMBER_OF_FIELD_COMPONENTS):
            OUTPUT = OUTPUT + " The basis function type for geometric variable %d is [1]:  1\n" %(component_idx+1)
        OUTPUT = OUTPUT + " Enter the %d global numbers for basis 1:" % BASIS.NUMBER_OF_NODES
        for node_idx in range(BASIS.NUMBER_OF_NODES):
            user_element_node_number = MESH_ELEMENT.USER_ELEMENT_NODES[node_idx]
            if BASIS.TYPE == '3DQuadraticLagrange' and node_idx == 15:
                OUTPUT = OUTPUT + " " + "%d\n" % user_element_node_number
            else:
                OUTPUT = OUTPUT + " "+"%d" %user_element_node_number

        OUTPUT = OUTPUT + " \n"
        if MESH_COMPONENT.NODES.MULTIPLE_VERSIONS:
            for element_node_idx, user_element_node_number in enumerate(MESH_ELEMENT.USER_ELEMENT_NODES):
                for component in range(1,NUMBER_OF_FIELD_COMPONENTS + 1):
                    number_of_versions = 1
                    FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(component)
                    FIELD_NODE = FIELD_COMPONENT.FieldNodeGlobalGet(user_element_node_number)
                    for MESH_NODE_DERIVATIVE_GLOBAL_NUMBER in range(FIELD_NODE.NUMBER_OF_DERIVATIVES):
                        FIELD_NODE_DERIVATIVE = FIELD_NODE.DERIVATIVES[MESH_NODE_DERIVATIVE_GLOBAL_NUMBER]
                        if FIELD_NODE_DERIVATIVE.NUMBER_OF_VERSIONS > number_of_versions:
                            number_of_versions = FIELD_NODE_DERIVATIVE.NUMBER_OF_VERSIONS
                    if number_of_versions > 1:
                        #TODO:: currently version output only looks at the versions for node derivative = 1, generalize.
                        OUTPUT = OUTPUT +\
" The version number for occurrence  1 of node "+"%5d" %user_element_node_number +", njj=%d"%component +" is [ 1]: "+"%d" %MESH_ELEMENT.COMPONENTS[component-1].USER_ELEMENT_NODE_VERSIONS[element_node_idx][0] +" \n"
   #     OUTPUT = OUTPUT +" \n"
    OUTPUT = OUTPUT + "\n"
#    output = output + "\n"
    FILE.write(OUTPUT)
    FILE.close()

def WriteIpElemAndLinearHydrostaticPressure(FIELD_VARIABLE,OUTPUT_FILENAME):
    #Get mesh component from the first field component
    NUMBER_OF_FIELD_COMPONENTS = FIELD_VARIABLE.NUMBER_OF_FIELD_COMPONENTS
    FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(1)
    MESH_COMPONENT = FIELD_COMPONENT.MESH_COMPONENT
    NUMBER_OF_ELEMENTS = MESH_COMPONENT.ELEMENTS.NUMBER_OF_ELEMENTS
    FILE = open(OUTPUT_FILENAME + ".ipelem", 'w')
    OUTPUT = \
" CMISS Version 2.1  ipelem File Version 2\n\
 Heading:\n\
 \n\
 The number of elements is ["+"%5d" %NUMBER_OF_ELEMENTS +"]: "+"%5d" %NUMBER_OF_ELEMENTS
    for element_idx in range(NUMBER_OF_ELEMENTS):
        MESH_ELEMENT = MESH_COMPONENT.ELEMENTS.ELEMENTS[element_idx]
        BASIS = MESH_ELEMENT.BASIS
        OUTPUT = OUTPUT +\
" \n\
 Element number ["+"%5d" %MESH_ELEMENT.USER_NUMBER +"]: "+"%5d" %MESH_ELEMENT.USER_NUMBER +"\n\
 The number of geometric Xj-coordinates is [%d]: %d\n" %(NUMBER_OF_FIELD_COMPONENTS,NUMBER_OF_FIELD_COMPONENTS)
        for component_idx in range(NUMBER_OF_FIELD_COMPONENTS):
            OUTPUT = OUTPUT + " The basis function type for geometric variable %d is [1]:  1\n" %(component_idx+1)
        OUTPUT = OUTPUT + " Enter the %d global numbers for basis 1:" % BASIS.NUMBER_OF_NODES
        for node_idx in range(BASIS.NUMBER_OF_NODES):
            OUTPUT = OUTPUT + " "+"%5d" %MESH_ELEMENT.USER_ELEMENT_NODES[node_idx]
        OUTPUT = OUTPUT + "\n Enter the %d numbers for basis 3 [prev]:" % BASIS.NUMBER_OF_NODES
        for node_idx in range(BASIS.NUMBER_OF_NODES):
            OUTPUT = OUTPUT + " "+"%5d" %MESH_ELEMENT.USER_ELEMENT_NODES[node_idx]
#        if Mesh.ELEMENTS[i-1].hasVersions:
#            for k in range(0,len(Mesh.ELEMENTS[i-1].versionNodes)):
#                output = output +\
#"\n\
# The version number for occurrence  1 of node "+"%5d" %Mesh.ELEMENTS[i-1].versionNodes[k] +", njj=1 is [ 1]: "+"%d" %Mesh.ELEMENTS[i-1].versionNodesNumber[k] +" \n\
# The version number for occurrence  1 of node "+"%5d" %Mesh.ELEMENTS[i-1].versionNodes[k] +", njj=2 is [ 1]: "+"%d" %Mesh.ELEMENTS[i-1].versionNodesNumber[k] +" \n\
# The version number for occurrence  1 of node "+"%5d" %Mesh.ELEMENTS[i-1].versionNodes[k] +", njj=3 is [ 1]: "+"%d" %Mesh.ELEMENTS[i-1].versionNodesNumber[k] +" "
        OUTPUT = OUTPUT +" \n"
    OUTPUT = OUTPUT + "\n"
#    output = output + "\n"
    FILE.write(OUTPUT)
    FILE.close()

#============================================================================

def WriteIpNode(FIELD_VARIABLE,OUTPUT_FILENAME):
    REGION = FIELD_VARIABLE.REGION
    FIELD_VARIABLE_USER_NUMBER = FIELD_VARIABLE.USER_NUMBER
    FIELD = FIELD_VARIABLE.FIELD
    FIELD_USER_NUMBER = FIELD.USER_NUMBER
    FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(1)
    MESH_COMPONENT = FIELD_COMPONENT.MESH_COMPONENT
    NUMBER_OF_NODES = MESH_COMPONENT.NODES.NUMBER_OF_NODES
    NUMBER_OF_FIELD_COMPONENTS = FIELD_VARIABLE.NUMBER_OF_FIELD_COMPONENTS
    NUMBER_OF_DERIVATIVES = MESH_COMPONENT.NODES.BASIS_MAX_NUMBER_OF_DERIVATIVES
    FILE = open(OUTPUT_FILENAME + ".ipnode", 'w')
    OUTPUT = \
" CMISS Version 1.21 ipnode File Version 2\n\
 Heading: \n\
 \n\
 The number of nodes is ["+"%5d" %NUMBER_OF_NODES +"]: "+"%5d" %NUMBER_OF_NODES +"\n\
 Number of coordinates [%d]: %d" %(NUMBER_OF_FIELD_COMPONENTS,NUMBER_OF_FIELD_COMPONENTS) +"\n"
    #Check if versions exist TODO:: currently component versions are available but not setup to count the number of versions.
    ANSWER = "N"
    if MESH_COMPONENT.NODES.MULTIPLE_VERSIONS == True:
        ANSWER = "Y"
    for component_idx in range(NUMBER_OF_FIELD_COMPONENTS):
        OUTPUT = OUTPUT + " Do you want prompting for different versions of nj=%d [N]? %s \n" %(component_idx+1,ANSWER)
    for component_idx in range(NUMBER_OF_FIELD_COMPONENTS):
        OUTPUT = OUTPUT + " The number of derivatives for coordinate %d is [%d]: %d\n" %(component_idx+1,NUMBER_OF_DERIVATIVES-1,NUMBER_OF_DERIVATIVES-1)
    for node_idx in range(NUMBER_OF_NODES):
        MESH_NODE = MESH_COMPONENT.NODES.NODES[node_idx]
        MESH_NODE_USER_NUMBER = MESH_NODE.USER_NUMBER
        OUTPUT = OUTPUT + " \n Node number ["+"%5d" %MESH_NODE_USER_NUMBER +"]: "+"%5d \n" %MESH_NODE_USER_NUMBER
        for component_idx in range(NUMBER_OF_FIELD_COMPONENTS):
            number_of_versions = 1
            FIELD_COMPONENT = FIELD_VARIABLE.COMPONENTS[component_idx]
            FIELD_COMPONENT_USER_NUMBER = FIELD_COMPONENT.USER_NUMBER
            if MESH_COMPONENT.NODES.MULTIPLE_VERSIONS == True:
                FIELD_NODE = FIELD_COMPONENT.NODES[node_idx]
                for MESH_NODE_DERIVATIVE_GLOBAL_NUMBER in range(MESH_NODE.COMPONENTS[component_idx].NUMBER_OF_DERIVATIVES):
                    FIELD_NODE_DERIVATIVE = FIELD_NODE.DERIVATIVES[MESH_NODE_DERIVATIVE_GLOBAL_NUMBER]
                    if FIELD_NODE_DERIVATIVE.NUMBER_OF_VERSIONS > number_of_versions:
                        number_of_versions = FIELD_NODE_DERIVATIVE.NUMBER_OF_VERSIONS
                OUTPUT = OUTPUT + ' The number of versions for nj=%d is [1]:  %d \n' %(component_idx + 1, number_of_versions)

            else:
                number_of_versions = 1
            for FIELD_VERSION_USER_NUMBER in range(1, number_of_versions + 1):
                if number_of_versions > 1:
                    OUTPUT = OUTPUT + ' For version number %d:\n'%(FIELD_VERSION_USER_NUMBER)
                DERIVATIVE_VALUES = []
                for derivative_idx in range(NUMBER_OF_DERIVATIVES):
                    DERIVATIVE_VALUES.append(REGION.FIELDS.FieldParameterSetNodeValueGet(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,FIELD_VERSION_USER_NUMBER,derivative_idx+1,MESH_NODE_USER_NUMBER,FIELD_COMPONENT_USER_NUMBER))
                if NUMBER_OF_FIELD_COMPONENTS == 3:
                    OUTPUT = OUTPUT + " The Xj("+"%d" %(component_idx+1) +") coordinate is [ 0.00000E+00]: "+"%17.16e \n" %(DERIVATIVE_VALUES[0])
                    if (NUMBER_OF_DERIVATIVES == 4 or NUMBER_OF_DERIVATIVES == 8):
                        OUTPUT = OUTPUT + " The derivative wrt direction 1 is [ 0.00000E+00]: "+"%17.16e \n" %(DERIVATIVE_VALUES[1])
                        OUTPUT = OUTPUT + " The derivative wrt direction 2 is [ 0.00000E+00]: "+"%17.16e \n" %(DERIVATIVE_VALUES[2])
                        OUTPUT = OUTPUT + " The derivative wrt directions 1 & 2 is [ 0.00000E+00]: "+"%17.16e \n" %(DERIVATIVE_VALUES[3])
                        if NUMBER_OF_DERIVATIVES == 8:
                            OUTPUT = OUTPUT + " The derivative wrt direction 3 is [ 0.00000E+00]: "+"%17.16e \n" %(DERIVATIVE_VALUES[4])
                            OUTPUT = OUTPUT + " The derivative wrt directions 1 & 3 is [ 0.00000E+00]: "+"%17.16e \n" %(DERIVATIVE_VALUES[5])
                            OUTPUT = OUTPUT + " The derivative wrt directions 2 & 3 is [ 0.00000E+00]: "+"%17.16e \n" %(DERIVATIVE_VALUES[6])
                            OUTPUT = OUTPUT + " The derivative wrt directions 1, 2 & 3 is [ 0.00000E+00]: "+"%17.16e \n" %(DERIVATIVE_VALUES[7])
                elif NUMBER_OF_FIELD_COMPONENTS == 2:
                    OUTPUT = OUTPUT + " The Xj("+"%d" %(component_idx+1) +") coordinate is [ 0.00000E+00]: "+"%17.16e \n" %(DERIVATIVE_VALUES[0])
                    if NUMBER_OF_DERIVATIVES == 4:
                        OUTPUT = OUTPUT + " The derivative wrt direction 1 is [ 0.00000E+00]: "+"%17.16e \n" %(DERIVATIVE_VALUES[1])
                        OUTPUT = OUTPUT + " The derivative wrt direction 2 is [ 0.00000E+00]: "+"%17.16e \n" %(DERIVATIVE_VALUES[2])
                        OUTPUT = OUTPUT + " The derivative wrt directions 1 & 2 is [ 0.00000E+00]: "+"%17.16e \n" %(DERIVATIVE_VALUES[3])
    FILE.write(OUTPUT)
    FILE.close()

def WriteIpBase(FIELD_VARIABLE,OUTPUT_FILENAME):

    # Note that different bases for different field components, while
    # supported in cm, is not support in this export function.

    REGION = FIELD_VARIABLE.REGION
    FIELD_VARIABLE_USER_NUMBER = FIELD_VARIABLE.USER_NUMBER
    FIELD = FIELD_VARIABLE.FIELD
    FIELD_USER_NUMBER = FIELD.USER_NUMBER
    FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(1) #Default to first field component
    MESH_COMPONENT = FIELD_COMPONENT.MESH_COMPONENT
    MESH_ELEMENTS = MESH_COMPONENT.ELEMENTS
    MESH_ELEMENT = MESH_ELEMENTS.ELEMENTS[0]
    BASIS = MESH_ELEMENT.BASIS

    NUMBER_OF_NODES = MESH_COMPONENT.NODES.NUMBER_OF_NODES
    NUMBER_OF_FIELD_COMPONENTS = FIELD_VARIABLE.NUMBER_OF_FIELD_COMPONENTS
    NUMBER_OF_DERIVATIVES = MESH_COMPONENT.NODES.BASIS_MAX_NUMBER_OF_DERIVATIVES
    FILE = open(OUTPUT_FILENAME + ".ipbase", 'w')


    if NUMBER_OF_DERIVATIVES == 1:
        if BASIS.NUMBER_OF_XIC == 2:
            OUTPUT = \
" CMISS Version 2.1  ipbase File Version 2\n\
 Heading:\n\
 \n\
 Enter the number of types of basis function [1]: 1\n\
 \n\
 For basis function type 1 the type of nodal interpolation is [1]:\n\
   (0) Auxiliary basis only\n\
   (1) Lagrange/Hermite tensor prod\n\
   (2) Simplex/Serendipity/Sector\n\
   (3) B-spline tensor product\n\
   (4) Fourier Series/Lagrange/Hermite tensor prod\n\
   (5) Boundary Element Lagrange/Hermite tensor pr.\n\
   (6) Boundary Element Simplex/Serendipity/Sector\n\
   (7) Extended Lagrange (multigrid collocation)\n\
    1\n\
 Enter the number of Xi-coordinates [1]: 2\n\
 \n\
 The interpolant in the Xi(1) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    1\n\
 Enter the number of Gauss points in the Xi(1) direction [2]: 2\n\
 \n\
 The interpolant in the Xi(2) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    1\n\
 Enter the number of Gauss points in the Xi(2) direction [2]: 2\n\
 Enter the node position indices [11211222]: 1 1 2 1 1 2 2 2\n\
 Enter the number of auxiliary element parameters [0]: 0\n"

        elif BASIS.NUMBER_OF_XIC == 3:
            if BASIS.TYPE == '3DQuadraticLagrange':
                OUTPUT = \
" CMISS Version 2.1  ipbase File Version 2\n\
 Heading:\n\
 \n\
 Enter the number of types of basis function [1]: 2\n\
 \n\
 For basis function type 1 the type of nodal interpolation is [1]:\n\
   (0) Auxiliary basis only\n\
   (1) Lagrange/Hermite tensor prod\n\
   (2) Simplex/Serendipity/Sector\n\
   (3) B-spline tensor product\n\
   (4) Fourier Series/Lagrange/Hermite tensor prod\n\
   (5) Boundary Element Lagrange/Hermite tensor pr.\n\
   (6) Boundary Element Simplex/Serendipity/Sector\n\
   (7) Extended Lagrange (multigrid collocation)\n\
    1\n\
 Enter the number of Xi-coordinates [1]: 3\n\
 \n\
 The interpolant in the Xi(1) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    2\n\
 Enter the number of Gauss points in the Xi(1) direction [3]: 3\n\
 \n\
 The interpolant in the Xi(2) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    2\n\
 Enter the number of Gauss points in the Xi(2) direction [3]: 3\n\
 \n\
 The interpolant in the Xi(3) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    2\n\
 Enter the number of Gauss points in the Xi(3) direction [3]: 3\n\
 Enter the node position indices for local node  1 [111]: 1 1 1\n\
 Enter the node position indices for local node  2 [211]: 2 1 1\n\
 Enter the node position indices for local node  3 [311]: 3 1 1\n\
 Enter the node position indices for local node  4 [121]: 1 2 1\n\
 Enter the node position indices for local node  5 [221]: 2 2 1\n\
 Enter the node position indices for local node  6 [321]: 3 2 1\n\
 Enter the node position indices for local node  7 [131]: 1 3 1\n\
 Enter the node position indices for local node  8 [231]: 2 3 1\n\
 Enter the node position indices for local node  9 [331]: 3 3 1\n\
 Enter the node position indices for local node 10 [112]: 1 1 2\n\
 Enter the node position indices for local node 11 [212]: 2 1 2\n\
 Enter the node position indices for local node 12 [312]: 3 1 2\n\
 Enter the node position indices for local node 13 [122]: 1 2 2\n\
 Enter the node position indices for local node 14 [222]: 2 2 2\n\
 Enter the node position indices for local node 15 [322]: 3 2 2\n\
 Enter the node position indices for local node 16 [132]: 1 3 2\n\
 Enter the node position indices for local node 17 [232]: 2 3 2\n\
 Enter the node position indices for local node 18 [332]: 3 3 2\n\
 Enter the node position indices for local node 19 [113]: 1 1 3\n\
 Enter the node position indices for local node 20 [213]: 2 1 3\n\
 Enter the node position indices for local node 21 [313]: 3 1 3\n\
 Enter the node position indices for local node 22 [123]: 1 2 3\n\
 Enter the node position indices for local node 23 [223]: 2 2 3\n\
 Enter the node position indices for local node 24 [323]: 3 2 3\n\
 Enter the node position indices for local node 25 [133]: 1 3 3\n\
 Enter the node position indices for local node 26 [233]: 2 3 3\n\
 Enter the node position indices for local node 27 [333]: 3 3 3\n\
 Enter the number of auxiliary element parameters [0]: 0\n\
 \n\
 For basis function type 2 the type of nodal interpolation is [1]:\n\
   (0) Auxiliary basis only\n\
   (1) Lagrange/Hermite tensor prod\n\
   (2) Simplex/Serendipity/Sector\n\
   (3) B-spline tensor product\n\
   (4) Fourier Series/Lagrange/Hermite tensor prod\n\
   (5) Boundary Element Lagrange/Hermite tensor pr.\n\
   (6) Boundary Element Simplex/Serendipity/Sector\n\
   (7) Extended Lagrange (multigrid collocation)\n\
    1\n\
 Enter the number of Xi-coordinates [1]: 2\n\
 \n\
 The interpolant in the Xi(1) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    2\n\
 Enter the number of Gauss points in the Xi(1) direction [3]: 3\n\
 \n\
 The interpolant in the Xi(2) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    2\n\
 Enter the number of Gauss points in the Xi(2) direction [3]: 3\n\
 Enter the node position indices [112131122232132333]: 1 1 2 1 3 1 1 2 2 2 3 2 1 3 2 3 3 3\n\
 Enter the number of auxiliary element parameters [0]: 0\n"
            else:
                OUTPUT = \
" CMISS Version 1.21 ipbase File Version 2\n\
 \n\
 Enter the number of types of basis function [1]: 2\n\
 \n\
 For basis function type 1 the type of nodal interpolation is [1]:\n\
   (0) Auxiliary basis only\n\
   (1) Lagrange/Hermite tensor prod\n\
   (2) Simplex/Serendipity/Sector\n\
   (3) B-spline tensor product\n\
   (4) Fourier Series/Lagrange/Hermite tensor prod\n\
   (5) Boundary Element Lagrange/Hermite tensor pr.\n\
   (6) Boundary Element Simplex/Serendipity/Sector\n\
   (7) Extended Lagrange (multigrid collocation)\n\
    1\n\
 Enter the number of Xi-coordinates [1]: 3\n\
 \n\
 The interpolant in the Xi(1) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    1\n\
 Enter the number of Gauss points in the Xi(1) direction [2]: 2\n\
 \n\
 The interpolant in the Xi(2) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    1\n\
 Enter the number of Gauss points in the Xi(2) direction [2]: 2\n\
 \n\
 The interpolant in the Xi(3) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    1\n\
 Enter the number of Gauss points in the Xi(3) direction [2]: 2\n\
 Enter the node position indices [111211121221112212122222]: 1 1 1 2 1 1 1 2 1 2 2 1 1 1 2 2 1 2 1 2 2 2 2 2\n\
 Enter the number of auxiliary element parameters [0]: 0\n\
\n\
 For basis function type 2 the type of nodal interpolation is [1]:\n\
   (0) Auxiliary basis only\n\
   (1) Lagrange/Hermite tensor prod\n\
   (2) Simplex/Serendipity/Sector\n\
   (3) B-spline tensor product\n\
   (4) Fourier Series/Lagrange/Hermite tensor prod\n\
   (5) Boundary Element Lagrange/Hermite tensor pr.\n\
   (6) Boundary Element Simplex/Serendipity/Sector\n\
   (7) Extended Lagrange (multigrid collocation)\n\
    1\n\
 Enter the number of Xi-coordinates [1]: 2\n\
 \n\
 The interpolant in the Xi(1) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    1\n\
 Enter the number of Gauss points in the Xi(1) direction [2]: 2\n\
 \n\
 The interpolant in the Xi(2) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    1\n\
 Enter the number of Gauss points in the Xi(2) direction [2]: 2\n\
 Enter the node position indices [11211222]: 1 1 2 1 1 2 2 2\n\
 Enter the number of auxiliary element parameters [0]: 0\n"

        else:
            raise ValueError('Invalid basis number of xi coordinates')

    else:
        if BASIS.scaling_type is 'harmonic':
            scaling = 7
        elif BASIS.scaling_type is 'geometric':
            raise Exception('Geometric field scaling not implemented in cm')
        elif BASIS.scaling_type is 'arithmetic':
            scaling = 6
        else:
            raise Exception('Unknown field scaling used')

        if NUMBER_OF_DERIVATIVES == 4:
            OUTPUT = \
" CMISS Version 1.21 ipbase File Version 2\n\
 Heading: cmgui generated file\n\
\n\
 Enter the number of types of basis function [1]: 1\n\
\n\
 For basis function type 1 the type of nodal interpolation is [1]:\n\
   (0) Auxiliary basis only\n\
   (1) Lagrange/Hermite tensor prod\n\
   (2) Simplex/Serendipity/Sector\n\
   (3) B-spline tensor product\n\
   (4) Fourier Series/Lagrange/Hermite tensor prod\n\
   (5) Boundary Element Lagrange/Hermite tensor pr.\n\
   (6) Boundary Element Simplex/Serendipity/Sector\n\
   (7) Extended Lagrange (multigrid collocation)\n\
    1\n\
 Enter the number of Xi-coordinates [1]: 2\n\
\n\
 The interpolant in the Xi(1) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    5\n\
 Enter the number of Gauss points in the Xi(1) direction [2]: 4\n\
 The interpolant in the Xi(2) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    5\n\
 Enter the number of Gauss points in the Xi(2) direction [2]: 4\n\
 Do you want to set cross derivatives to zero [N]? N\n\
 Enter the node position indices []: 1 1 2 1 1 2 2 2\n\
 Enter the derivative order indices []:  1 1 2 1 1 2 2 2\n\
 Enter the number of auxiliary element parameters [0]:  0\n\
\n\
 For basis function type 1 scale factors are [6]:\n\
   (1) Unit\n\
   (2) Read in - Element based\n\
   (3) Read in - Node based\n\
   (4) Calculated from angle change\n\
   (5) Calculated from arc length\n\
   (6) Calculated from arithmetic mean arc length\n\
   (7) Calculated from harmonic mean arc length\n\
    {0}\n".format(scaling)

        elif NUMBER_OF_DERIVATIVES == 8:

           OUTPUT = \
" CMISS Version 1.21 ipbase File Version 2\n\
 Heading: cmgui generated file\n\
\n\
 Enter the number of types of basis function [1]: 2\n\
\n\
 For basis function type 1 the type of nodal interpolation is [1]:\n\
   (0) Auxiliary basis only\n\
   (1) Lagrange/Hermite tensor prod\n\
   (2) Simplex/Serendipity/Sector\n\
   (3) B-spline tensor product\n\
   (4) Fourier Series/Lagrange/Hermite tensor prod\n\
   (5) Boundary Element Lagrange/Hermite tensor pr.\n\
   (6) Boundary Element Simplex/Serendipity/Sector\n\
   (7) Extended Lagrange (multigrid collocation)\n\
    1\n\
 Enter the number of Xi-coordinates [1]: 3\n\
\n\
 The interpolant in the Xi(1) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    5\n\
 Enter the number of Gauss points in the Xi(1) direction [2]: 4\n\
 The interpolant in the Xi(2) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    5\n\
 Enter the number of Gauss points in the Xi(2) direction [2]: 4\n\
 The interpolant in the Xi(3) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    5\n\
 Enter the number of Gauss points in the Xi(3) direction [2]: 4\n\
 Do you want to set cross derivatives to zero [N]? N\n\
 Enter the node position indices []: 1 1 1 2 1 1 1 2 1 2 2 1 1 1 2 2 1 2 1 2 2 2 2 2\n\
 Enter the derivative order indices []:  1 1 1 2 1 1 1 2 1 2 2 1 1 1 2 2 1 2 1 2 2 2 2 2\n\
 Enter the number of auxiliary element parameters [0]:  0\n\
\n\
 For basis function type 1 scale factors are [6]:\n\
   (1) Unit\n\
   (2) Read in - Element based\n\
   (3) Read in - Node based\n\
   (4) Calculated from angle change\n\
   (5) Calculated from arc length\n\
   (6) Calculated from arithmetic mean arc length\n\
   (7) Calculated from harmonic mean arc length\n\
    7\n\
 For basis function type 2 the type of nodal interpolation is [1]:\n\
   (0) Auxiliary basis only\n\
   (1) Lagrange/Hermite tensor prod\n\
   (2) Simplex/Serendipity/Sector\n\
   (3) B-spline tensor product\n\
   (4) Fourier Series/Lagrange/Hermite tensor prod\n\
   (5) Boundary Element Lagrange/Hermite tensor pr.\n\
   (6) Boundary Element Simplex/Serendipity/Sector\n\
   (7) Extended Lagrange (multigrid collocation)\n\
    1\n\
 Enter the number of Xi-coordinates [1]: 2\n\
\n\
 The interpolant in the Xi(1) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    5\n\
 Enter the number of Gauss points in the Xi(1) direction [2]: 4\n\
 The interpolant in the Xi(2) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    5\n\
 Enter the number of Gauss points in the Xi(2) direction [2]: 4\n\
 Do you want to set cross derivatives to zero [N]? N\n\
 Enter the node position indices []: 1 1 2 1 1 2 2 2\n\
 Enter the derivative order indices []:  1 1 2 1 1 2 2 2\n\
 Enter the number of auxiliary element parameters [0]:  0\n\
\n\
 For basis function type 2 scale factors are [6]:\n\
   (1) Unit\n\
   (2) Read in - Element based\n\
   (3) Read in - Node based\n\
   (4) Calculated from angle change\n\
   (5) Calculated from arc length\n\
   (6) Calculated from arithmetic mean arc length\n\
   (7) Calculated from harmonic mean arc length\n\
    {0}\n".format(scaling)
    FILE.write(OUTPUT)
    FILE.close()


def WriteSingleIpBase(FIELD_VARIABLE,OUTPUT_FILENAME):
    REGION = FIELD_VARIABLE.REGION
    FIELD_VARIABLE_USER_NUMBER = FIELD_VARIABLE.USER_NUMBER
    FIELD = FIELD_VARIABLE.FIELD
    FIELD_USER_NUMBER = FIELD.USER_NUMBER
    FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(1)
    MESH_COMPONENT = FIELD_COMPONENT.MESH_COMPONENT
    NUMBER_OF_NODES = MESH_COMPONENT.NODES.NUMBER_OF_NODES
    NUMBER_OF_FIELD_COMPONENTS = FIELD_VARIABLE.NUMBER_OF_FIELD_COMPONENTS
    NUMBER_OF_DERIVATIVES = MESH_COMPONENT.NODES.BASIS_MAX_NUMBER_OF_DERIVATIVES
    FILE = open(OUTPUT_FILENAME + ".ipbase", 'w')

    if NUMBER_OF_DERIVATIVES == 1:
        OUTPUT = \
" CMISS Version 1.21 ipbase File Version 2\n\
 Heading: 10% uniaxial extension of a unit cube\n\
 \n\
 Enter the number of types of basis function [1]: 1\n\
 \n\
 For basis function type 1 the type of nodal interpolation is [1]:\n\
   (0) Auxiliary basis only\n\
   (1) Lagrange/Hermite tensor prod\n\
   (2) Simplex/Serendipity/Sector\n\
   (3) B-spline tensor product\n\
   (4) Fourier Series/Lagrange/Hermite tensor prod\n\
   (5) Boundary Element Lagrange/Hermite tensor pr.\n\
   (6) Boundary Element Simplex/Serendipity/Sector\n\
   (7) Extended Lagrange (multigrid collocation)\n\
    1\n\
 Enter the number of Xi-coordinates [1]: 3\n\
 \n\
 The interpolant in the Xi(1) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    1\n\
 Enter the number of Gauss points in the Xi(1) direction [2]: 2\n\
 \n\
 The interpolant in the Xi(2) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    1\n\
 Enter the number of Gauss points in the Xi(2) direction [2]: 2\n\
 \n\
 The interpolant in the Xi(3) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    1\n\
 Enter the number of Gauss points in the Xi(3) direction [2]: 2\n\
 Enter the node position indices [111211121221112212122222]: 1 1 1 2 1 1 1 2 1 2 2 1 1 1 2 2 1 2 1 2 2 2 2 2\n\
 Enter the number of auxiliary element parameters [0]: 0\n"

    elif NUMBER_OF_DERIVATIVES == 4:
        OUTPUT = \
" CMISS Version 1.21 ipbase File Version 2\n\
 Heading: cmgui generated file\n\
\n\
 Enter the number of types of basis function [1]: 1\n\
\n\
 For basis function type 1 the type of nodal interpolation is [1]:\n\
   (0) Auxiliary basis only\n\
   (1) Lagrange/Hermite tensor prod\n\
   (2) Simplex/Serendipity/Sector\n\
   (3) B-spline tensor product\n\
   (4) Fourier Series/Lagrange/Hermite tensor prod\n\
   (5) Boundary Element Lagrange/Hermite tensor pr.\n\
   (6) Boundary Element Simplex/Serendipity/Sector\n\
   (7) Extended Lagrange (multigrid collocation)\n\
    1\n\
 Enter the number of Xi-coordinates [1]: 2\n\
\n\
 The interpolant in the Xi(1) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    5\n\
 Enter the number of Gauss points in the Xi(1) direction [2]: 4\n\
 The interpolant in the Xi(2) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    5\n\
 Enter the number of Gauss points in the Xi(2) direction [2]: 4\n\
 Do you want to set cross derivatives to zero [N]? N\n\
 Enter the node position indices []: 1 1 2 1 1 2 2 2\n\
 Enter the derivative order indices []:  1 1 2 1 1 2 2 2\n\
 Enter the number of auxiliary element parameters [0]:  0\n\
\n\
 For basis function type 1 scale factors are [6]:\n\
   (1) Unit\n\
   (2) Read in - Element based\n\
   (3) Read in - Node based\n\
   (4) Calculated from angle change\n\
   (5) Calculated from arc length\n\
   (6) Calculated from arithmetic mean arc length\n\
   (7) Calculated from harmonic mean arc length\n\
    7\n"
    elif NUMBER_OF_DERIVATIVES == 8:

        OUTPUT = \
" CMISS Version 2.0  ipbase File Version 2\n\
 Heading:\n\
\n\
 Enter the number of types of basis function [1]: 1\n\
\n\
 For basis function type 1 the type of nodal interpolation is [1]:\n\
   (0) Auxiliary basis only\n\
   (1) Lagrange/Hermite tensor prod\n\
   (2) Simplex/Serendipity/Sector\n\
   (3) B-spline tensor product\n\
   (4) Fourier Series/Lagrange/Hermite tensor prod\n\
   (5) Boundary Element Lagrange/Hermite tensor pr.\n\
   (6) Boundary Element Simplex/Serendipity/Sector\n\
   (7) Extended Lagrange (multigrid collocation)\n\
    1\n\
 Enter the number of Xi-coordinates [1]: 3\n\
\n\
 The interpolant in the Xi(1) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    5\n\
 Enter the number of Gauss points in the Xi(1) direction [3]: 4\n\
 The interpolant in the Xi(2) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    5\n\
 Enter the number of Gauss points in the Xi(2) direction [3]: 4\n\
 The interpolant in the Xi(3) direction is [1]:\n\
   (1) Linear Lagrange\n\
   (2) Quadratic Lagrange\n\
   (3) Cubic Lagrange\n\
   (4) Quadratic Hermite\n\
   (5) Cubic Hermite\n\
    5\n\
 Enter the number of Gauss points in the Xi(3) direction [3]: 4\n\
 Do you want to set cross derivatives to zero [N]? N\n\
 Enter the node position indices [111211121221112212122222]: 1 1 1 2 1 1 1 2 1 2 2 1 1 1 2 2 1 2 1 2 2 2 2 2\n\
 Enter the derivative order indices [111211121221112212122222]: 1 1 1 2 1 1 1 2 1 2 2 1 1 1 2 2 1 2 1 2 2 2 2 2\n\
 Enter the number of auxiliary element parameters [0]:  0\n\
\n\
 For basis function type 1 scale factors are [6]:\n\
   (1) Unit\n\
   (2) Read in - Element based\n\
   (3) Read in - Node based\n\
   (4) Calculated from angle change\n\
   (5) Calculated from arc length\n\
   (6) Calculated from arithmetic mean arc length\n\
   (7) Calculated from harmonic mean arc length\n\
    7\n"
    FILE.write(OUTPUT)
    FILE.close()

def WriteIpCoor(FIELD_VARIABLE,OUTPUT_FILENAME):
    FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(1)
    MESH_COMPONENT = FIELD_COMPONENT.MESH_COMPONENT
    number_of_field_components = FIELD_VARIABLE.NUMBER_OF_FIELD_COMPONENTS
    file_id = open(OUTPUT_FILENAME + ".ipcoor", 'w')
    file_id.write(' CMISS Version 2.1  ipcoor File Version 1\n')
    file_id.write(' Heading:\n')
    file_id.write(' \n')
    file_id.write(' The global coordinates for region 1 are [1]:\n')
    file_id.write('   (1) rectangular cartesian (x,y,z)\n')
    file_id.write('   (2) cylindrical polar (r,theta,z)\n')
    file_id.write('   (3) spherical polar (r,theta,phi)\n')
    file_id.write('   (4) prolate spheroidal (lambda,mu,theta)\n')
    file_id.write('   (5) oblate  spheroidal (lambda,mu,theta)\n')
    file_id.write('    1\n')
    file_id.write(' Enter the number of global coordinates [{0}]: {1}\n'.format(
        FIELD_VARIABLE.NUMBER_OF_FIELD_COMPONENTS,
        FIELD_VARIABLE.NUMBER_OF_FIELD_COMPONENTS))
    file_id.write(' Do you want to specify another coord. system for dependent variables [N]? N\n')
    if number_of_field_components == 2:
        file_id.write(' The geometry is [1]:\n')
        file_id.write('   (1) unsymmetric\n')
        file_id.write('   (2) cylindrically symmetric about x (or r for cyl.polar)\n')
        file_id.write('   (3) cylindrically symmetric about y (or z for cyl.polar)\n')
        file_id.write('   (4) spherically   symmetric\n')
        file_id.write('   (5) mirror symmetry in x\n')
        file_id.write('   (6) mirror symmetry in y\n')
        file_id.write('   (7) mirror symmetry in x and y\n')
        file_id.write('    1\n')
    file_id.write(' Enter x,y,z origin of coords relative to region 0 [0,0,0]:  0.00000E+00  0.00000E+00  0.00000E+00\n')
    if MESH_COMPONENT.NODES.MULTIPLE_VERSIONS:
        file_id.write(' Are there any non-standard mappings [N]? y\n')
        file_id.write('    in versions to ensure C0 continuity [N]? y\n')
        file_id.write('    in lines [N]? N\n')
        file_id.write('    in degrees of freedom for hanging nodes [N]? N\n')
    else:
        file_id.write(' Are there any non-standard mappings [N]? N\n')
    file_id.close()

def WriteCmCom(FIELD_VARIABLE,OUTPUT_FILENAME):
    FILE = open(OUTPUT_FILENAME + "CMISS.com", 'w')
    output_info = OUTPUT_FILENAME.split("/")
    #print output_info [:-1]
    #print os.sep.join(output_info[:-1])
    #print os.sep.join(output_info[:-1])+ '/para.ippara'
    OUTPUT = \
" \n\
fem def para;r;para\n\
fem def coor;r;%s"%output_info[-1] +"\n\
fem def base;r;%s"%output_info[-1] +"\n\
fem def node;r;%s"%output_info[-1] +"\n\
fem def elem;r;%s"%output_info[-1] +"\n\
fem export node;%s"%output_info[-1] +" as %s"%output_info[-1]+"\n\
fem export elem;%s"%output_info[-1] +" as %s"%output_info[-1]+"\n\
q\n"
    FILE.write(OUTPUT)
    FILE.close()
    print os.sep.join(output_info[:-1])
    FILE = open('./para.ippara', 'w')
    #FILE = open(os.sep.join(output_info[:-1]) + '/para.ippara', 'w')
    OUTPUT = \
" CMISS Version 2.1  ippara File Version 1\n\
 Heading:\n\
 \n\
 Max# auxiliary parameters          (NAM)[1]:         5\n\
 Max# basis functions               (NBM)[1]:        42\n\
 Max# var. types for a  dep. var.   (NCM)[1]:         2\n\
 Max# data points                   (NDM)[1]:      6000\n\
 Max# elements                      (NEM)[1]:     50000\n\
 Max# elements in a region       (NE_R_M)[1]:     50000\n\
 Max# adjacent elements in Xi      (NEIM)[1]:       500\n\
 Max# global face segments          (NFM)[1]:      1461\n\
 Max# faces in a region          (NF_R_M)[1]:      1461\n\
 Max# local Voronoi faces         (NFVCM)[1]:         6\n\
 Max# Gauss points per element      (NGM)[1]:        81\n\
 Max# dependent variables           (NHM)[1]:         6\n\
 Max# local Xi coordinates          (NIM)[1]:         3\n\
 Max# global reference coordinates  (NJM)[1]:         6\n\
 Max# derivatives per variable      (NKM)[1]:         8\n\
 Max# global line segments          (NLM)[1]:      5000\n\
 Max# lines in a region          (NL_R_M)[1]:      5000\n\
 Max# material parameters           (NMM)[1]:        35\n\
 Max# element nodes                 (NNM)[1]:        27\n\
 Max# degrees of freedom            (NOM)[1]:      5000\n\
 Max# global nodes                  (NPM)[1]:     50000\n\
 Max# global nodes in a region   (NP_R_M)[1]:     50000\n\
 Max# global grid points            (NQM)[1]:      4225\n\
 Max# signal sets                  (NSSM)[1]:         1\n\
 Max# grid degrees of freedom      (NYQM)[1]:         1\n\
 Max# regions                       (NRM)[1]:         6\n\
 Max# element dofs per variable     (NSM)[1]:        64\n\
 Max# face dofs per variable       (NSFM)[1]:        16\n\
 Max# eigenvalues                   (NTM)[1]:        20\n\
 Max# time samples                 (NTSM)[1]:       200\n\
 Max# derivatives up to 2nd order   (NUM)[1]:        11\n\
 Max# Voronoi boundary nodes      (NVCBM)[1]:       100\n\
 Max# Voronoi cells                (NVCM)[1]:       200\n\
 Max# versions of a variable        (NVM)[1]:        16\n\
 Max# workstations                  (NWM)[1]:         3\n\
 Max# problem types                 (NXM)[1]:         3\n\
 Max# mesh dofs                     (NYM)[1]:      5000\n\
 Max# mesh dofs in a region      (NY_R_M)[1]:      5000\n\
 Max# dimension of GD           (NZ_GD_M)[1]:   1202500\n\
 Max# dimension of GK           (NZ_GK_M)[1]:   1491840\n\
 Max# dimension of GKK         (NZ_GKK_M)[1]:   1491840\n\
 Max# dimension of GM           (NZ_GM_M)[1]:   1202500\n\
 Max# dimension of GMM         (NZ_GMM_M)[1]:   1202500\n\
 Max# dimension of GQ           (NZ_GQ_M)[1]:   1202500\n\
 Max# dimension of ISC_GD      (NISC_GDM)[1]:   1202500\n\
 Max# dimension of ISR_GD      (NISR_GDM)[1]:      5000\n\
 Max# dimension of ISC_GK      (NISC_GKM)[1]:   1491840\n\
 Max# dimension of ISR_GK      (NISR_GKM)[1]:      5000\n\
 Max# dimension of ISC_GKK    (NISC_GKKM)[1]:   1491840\n\
 Max# dimension of ISR_GKK    (NISR_GKKM)[1]:      5000\n\
 Max# dimension of ISC_GM      (NISC_GMM)[1]:   1202500\n\
 Max# dimension of ISR_GM      (NISR_GMM)[1]:      5000\n\
 Max# dimension of ISC_GMM    (NISC_GMMM)[1]:   1202500\n\
 Max# dimension of ISR_GMM    (NISR_GMMM)[1]:      5000\n\
 Max# dimension of ISC_GQ      (NISC_GQM)[1]:   1202500\n\
 Max# dimension of ISR_GQ      (NISR_GQM)[1]:      5000\n\
 Max# size of Minos arrays    (NZ_MINOSM)[1]:       125\n\
 Max# basis function families      (NBFM)[1]:        13\n\
 Max# nonlin. optim.n constraints  (NCOM)[1]:         0\n\
 Max# data points in one element   (NDEM)[1]:      5000\n\
 Max# dipoles in a region      (NDIPOLEM)[1]:        20\n\
 Max# time points for a dipole (NDIPTIMM)[1]:       500\n\
 Max# elements along a line        (NELM)[1]:        16\n\
 Max# elements a node can be in    (NEPM)[1]:        20\n\
 Max# segments                  (NGRSEGM)[1]:         6\n\
 Max# variables per grid point     (NIQM)[1]:         6\n\
 Max# cell state variables        (NIQSM)[1]:         0\n\
 Max# variables for fibre extens(NIFEXTM)[1]:         8\n\
 Max# variables per mesh dof       (NIYM)[1]:        16\n\
 Max# variables / mesh dof(fix) (NIYFIXM)[1]:         5\n\
 Max# vars. at each gauss point   (NIYGM)[1]:         6\n\
 Max# vars. at face gauss points (NIYGFM)[1]:         0\n\
 Max# linear optimis.n constraints (NLCM)[1]:         1\n\
 Max# auxiliary grid parameters   (NMAQM)[1]:         6\n\
 Max# cell material parameters     (NMQM)[1]:         0\n\
 Max# optimisation variables       (NOPM)[1]:       125\n\
 Max size fractal tree order array (NORM)[1]:        20\n\
 Max# soln dofs for mesh dof       (NOYM)[1]:         1\n\
 Max# domain nodes for BE problems (NPDM)[1]:         1\n\
 Max# grid points per element      (NQEM)[1]:        81\n\
 Max# non-zeros in grid matrix row (NQGM)[1]:        22\n\
 Max# cell integer variables       (NQIM)[1]:         1\n\
 Max# cell real variables          (NQRM)[1]:         1\n\
 Max# spatial var cell int vars  (NQISVM)[1]:         1\n\
 Max# spatial var cell real vars (NQRSVM)[1]:         1\n\
 Max# number of grid schemes      (NQSCM)[1]:         9\n\
 Max# cell variants                (NQVM)[1]:         0\n\
 Max# rows and columns (sb 2)      (NRCM)[1]:         2\n\
 Max# optimisation residuals       (NREM)[1]:       400\n\
 Max# time points          (NTIMEPOINTSM)[1]:         1\n\
 Max# time variables         (NTIMEVARSM)[1]:         1\n\
 Max# mesh dofs for soln dof       (NYOM)[1]:         4\n\
 Max# rows in a problem          (NYROWM)[1]:      5000\n\
 Max image cell array dimension (NIMAGEM)[1]:         1\n\
 Size of transfer matrix  (NY_TRANSFER_M)[1]:       200\n\
 Max# mesh dofs map to 1 mesh dof  (NYYM)[1]:         0\n\
 USE_BEM       (0 or 1)[1]: 1\n\
 USE_CELL      (0 or 1)[1]: 0\n\
 USE_DATA      (0 or 1)[1]: 1\n\
 USE_DIPOLE    (0 or 1)[1]: 1\n\
 USE_GAUSS_PT_MATERIALS  (0 or 1)[0]: 0\n\
 USE_GRAPHICS  (0 or 1)[1]: 1\n\
 USE_GRID      (0 or 1)[1]: 1\n\
 USE_LUNG      (0 or 1)[1]: 1\n\
 USE_MAGNETIC  (0 or 1)[0]: 0\n\
 USE_MAPS      (0 or 1)[0]: 0\n\
 USE_MINOS     (0 or 1)[1]: 0\n\
 USE_NLSTRIPE  (0 or 1)[1]: 1\n\
 USE_NONLIN    (0 or 1)[1]: 1\n\
 USE_NPSOL     (0 or 1)[1]: 1\n\
 USE_SPARSE    (0 or 1)[1]: 1\n\
 USE_TRANSFER  (0 or 1)[1]: 1\n\
 USE_TRIANGLE  (0 or 1)[1]: 0\n\
 USE_VORONOI   (0 or 1)[1]: 0\n\
 USE_TIME      (0 or 1)[1]: 1\n\
\n"
    FILE.write(OUTPUT)
    FILE.close()

def WriteCmguiCom(FIELD_VARIABLE,OUTPUT_FILENAME):
    FILE = open(OUTPUT_FILENAME + "CMGUI.com", 'w')
    output_info = OUTPUT_FILENAME.split("/")
    OUTPUT = \
" \n\
gfx r n %s"%output_info[-1] +".exnode\n\
gfx r e %s"%output_info[-1] +".exelem\n\
\n"
    FILE.write(OUTPUT)
    FILE.close()

def WriteIpData(DATAPOINT_GROUP,OUTPUT_FILENAME,OUTPUT_GROUP_NAME):
    FILE = open(OUTPUT_FILENAME + ".ipdata", 'w')
    output_info = OUTPUT_FILENAME.split("/")
    OUTPUT =OUTPUT_GROUP_NAME+"\n"
    for nd in range(DATAPOINT_GROUP.NUMBER_OF_DATAPOINTS):
        DATAPOINT = DATAPOINT_GROUP.DATAPOINTS[nd]
        COMPONENTS = DATAPOINT.COMPONENTS
        VALUE = []
        for component_idx in range(DATAPOINT.NUMBER_OF_COMPONENTS):
            VALUE.append(COMPONENTS[component_idx].VALUE)
        if DATAPOINT.NUMBER_OF_COMPONENTS == 2:
            OUTPUT = OUTPUT + "%11i  %15.8f  %15.8f  1.0 1.0\n"%(nd+1,VALUE[0],VALUE[1])
        else:
            OUTPUT = OUTPUT + "%11i  %15.8f  %15.8f  %15.8f  1.0 1.0 1.0\n"%(nd+1,VALUE[0],VALUE[1],VALUE[2])
    FILE.write(OUTPUT)
    FILE.close()

#============================================================================

def readexdata(filename):
    readdata = open(filename).read()
    array = re.split(r'[\n\\]', readdata)

    REGION = fem_topology.Region(1)
    REGION.FIELDS.FieldsFieldAdd(1)
    REGION.FIELDS.FieldLabelSet(1,"coordinates")
    REGION.FIELDS.FieldNumberOfFieldComponentsSet(1,3)
    REGION.FIELDS.FieldComponentLabelSet(1,1,"x")
    REGION.FIELDS.FieldComponentLabelSet(1,2,"y")
    REGION.FIELDS.FieldComponentLabelSet(1,3,"z")
    REGION.FIELDS.FieldsFieldAdd(2)
    REGION.FIELDS.FieldLabelSet(2,"groupName")
    REGION.FIELDS.FieldNumberOfFieldComponentsSet(2,1)
    REGION.FIELDS.FieldComponentLabelSet(2,1,"value")
    REGION.FIELDS.FieldsFieldAdd(3)
    REGION.FIELDS.FieldLabelSet(3,"sliceName")
    REGION.FIELDS.FieldNumberOfFieldComponentsSet(3,1)
    REGION.FIELDS.FieldComponentLabelSet(3,1,"value")

    for line in range(len(array)):
        #print array[line][0:6]
        if array[line][0:6] == " Node:":
            temp = array[line].split()
            #print temp[len(temp)-1]
            LOCAL_NODE_NUMBER = int(temp[len(temp)-1])
            GLOBAL_NODE_NUMBER = REGION.NODES.NodesNodeAdd(LOCAL_NODE_NUMBER)
            #print GLOBAL_NODE_NUMBER
            for FIELD_USER_NUMBER in range(1,REGION.FIELDS.NUMBER_OF_FIELDS+1): #Add global node number to each field.
                REGION.FIELDS.FieldGlobalNodeAdd(FIELD_USER_NUMBER)
            REGION.FIELDS.FieldComponentValueAdd(1,1,readvalues(array,line,1,"float"))
            REGION.FIELDS.FieldComponentValueAdd(1,2,readvalues(array,line,2,"float"))
            REGION.FIELDS.FieldComponentValueAdd(1,3,readvalues(array,line,3,"float"))
            REGION.FIELDS.FieldComponentValueAdd(2,1,readvalues(array,line,4,"string"))
            REGION.FIELDS.FieldComponentValueAdd(3,1,readvalues(array,line,5,"string"))
            line = line + 5
    REGION.FIELDS.FieldsFieldValuesCreateFinish()
    return REGION

#============================================================================

def ReadExdata(REGION,DATAPOINT_GROUP_USER_NUMBER,INPUT_FILENAME):
    INPUT = open(INPUT_FILENAME + ".exdata").read()
    INPUT = re.split(r'[\n\\]', INPUT)
    NUMBER_OF_COMPONENTS = 5
    REGION.DATAPOINTS.DatapointGroupCreateStart(DATAPOINT_GROUP_USER_NUMBER)
    REGION.DATAPOINTS.DatapointGroupLabelSet(DATAPOINT_GROUP_USER_NUMBER,"exdata")
    REGION.DATAPOINTS.DatapointGroupNumberOfComponentsSet(DATAPOINT_GROUP_USER_NUMBER,NUMBER_OF_COMPONENTS)
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,1,"x")
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,2,"y")
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,3,"z")
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,4,"groupName")
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,5,"sliceName")
    REGION.DATAPOINTS.DatapointGroupCreateFinish(DATAPOINT_GROUP_USER_NUMBER)
    for line in range(len(INPUT)):
        #print array[line][0:6]
        if INPUT[line][0:6] == " Node:" or INPUT[line][0:5] == "Node:":
            DATAPOINT_USER_NUMBER = int(INPUT[line].split()[-1])
            REGION.DATAPOINTS.DatapointAdd(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER)
            temp = INPUT[line+1].split()
            if len(temp) == 3:
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,1,float(temp[0]))
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,2,float(temp[1]))
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,3,float(temp[2]))
            else:
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,1,float(INPUT[line+1].split()[-1]))
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,2,float(INPUT[line+2].split()[-1]))
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,3,float(INPUT[line+3].split()[-1]))
#                if INPUT[line+4][0:6] != " Node:" and (line+4 < len(INPUT)-1):
                if INPUT[6][0:6] != " Node:" and (line+4 < len(INPUT)-1):
                    REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,4,str(INPUT[line+4].split()[-1]))
                    REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,5,str(INPUT[line+5].split()[-1]))
                    line = line + 5
                else:
                    line = line + 3


#============================================================================

def WriteExdata(REGION,DATAPOINT_GROUP_USER_NUMBER,GROUP_LABEL,NUMBER_OF_OUTPUT_COMPONENTS,OUTPUT_FILENAME):
    OUTPUT = open(OUTPUT_FILENAME + ".exdata", 'w')
    OUTPUT.write(' Group name: '+GROUP_LABEL+'\n')
    if NUMBER_OF_OUTPUT_COMPONENTS == 5:
        OUTPUT.write(' #Fields=3\n')
        OUTPUT.write(' 1) coordinates, coordinate, rectangular cartesian, #Components=3\n')
        OUTPUT.write('  x.  Value index=1, #Derivatives=0, #Versions=1\n')
        OUTPUT.write('  y.  Value index=2, #Derivatives=0, #Versions=1\n')
        OUTPUT.write('  z.  Value index=3, #Derivatives=0, #Versions=1\n')
        OUTPUT.write(' 2) groupName, field, string, #Components=1\n')
        OUTPUT.write('  value.  Value index=4, #Derivatives=0, #Versions=1\n')
        OUTPUT.write(' 3) sliceName, field, string, #Components=1\n')
        OUTPUT.write('  value.  Value index=5, #Derivatives=0, #Versions=1\n')
    elif NUMBER_OF_OUTPUT_COMPONENTS == 3:
        OUTPUT.write(' #Fields=1\n')
        OUTPUT.write(' 1) coordinates, coordinate, rectangular cartesian, #Components=3\n')
        OUTPUT.write('  x.  Value index=1, #Derivatives=0, #Versions=1\n')
        OUTPUT.write('  y.  Value index=2, #Derivatives=0, #Versions=1\n')
        OUTPUT.write('  z.  Value index=3, #Derivatives=0, #Versions=1\n')
    for datapoint in REGION.DATAPOINTS.DatapointsListGet(DATAPOINT_GROUP_USER_NUMBER):
        OUTPUT.write(' Node: %s\n' % datapoint)
        OUTPUT.write('  %.15e\n' % REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,1))
        OUTPUT.write('  %.15e\n' % REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,2))
        OUTPUT.write('  %.15e\n' % REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,3))
        if NUMBER_OF_OUTPUT_COMPONENTS == 5:
            OUTPUT.write(' %s\n' % REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,4))
            OUTPUT.write(' %s\n' % REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,5))
        #OUTPUT.write(' \n')
    OUTPUT.close()

def WriteDataTxt(REGION,DATAPOINT_GROUP_USER_NUMBER,NUMBER_OF_OUTPUT_COMPONENTS,OUTPUT_FILENAME):
    OUTPUT = open(OUTPUT_FILENAME + ".txt", 'w')
    #OUTPUT.write("x coord, y coord, z coord, scalar \n")
    for datapoint in REGION.DATAPOINTS.DatapointsListGet(DATAPOINT_GROUP_USER_NUMBER):
        #OUTPUT.write('%5.15f, %5.15f, %5.15f, 0 \n' % (REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,1),\
        OUTPUT.write('%5.12f, %5.12f, %5.12f \n' % (REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,1),\
        REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,2),\
        REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,3)))
    OUTPUT.close()

#============================================================================

def WriteExdataSelectedGroup(REGION,DATAPOINT_GROUP_USER_NUMBER,GROUP,NUMBER_OF_OUTPUT_COMPONENTS,OUTPUT_FILENAME):
    OUTPUT = open(OUTPUT_FILENAME + ".exdata", 'w')
    OUTPUT.write(' Group name: '+ GROUP +'\n')
    if NUMBER_OF_OUTPUT_COMPONENTS == 5:
        OUTPUT.write(' #Fields=3\n')
        OUTPUT.write(' 1) coordinates, coordinate, rectangular cartesian, #Components=3\n')
        OUTPUT.write('  x.  Value index=1, #Derivatives=0, #Versions=1\n')
        OUTPUT.write('  y.  Value index=2, #Derivatives=0, #Versions=1\n')
        OUTPUT.write('  z.  Value index=3, #Derivatives=0, #Versions=1\n')
        OUTPUT.write(' 2) groupName, field, string, #Components=1\n')
        OUTPUT.write('  value.  Value index=4, #Derivatives=0, #Versions=1\n')
        OUTPUT.write(' 3) sliceName, field, string, #Components=1\n')
        OUTPUT.write('  value.  Value index=5, #Derivatives=0, #Versions=1\n')
    elif NUMBER_OF_OUTPUT_COMPONENTS == 3:
        OUTPUT.write(' #Fields=1\n')
        OUTPUT.write(' 1) coordinates, coordinate, rectangular cartesian, #Components=3\n')
        OUTPUT.write('  x.  Value index=1, #Derivatives=0, #Versions=1\n')
        OUTPUT.write('  y.  Value index=2, #Derivatives=0, #Versions=1\n')
        OUTPUT.write('  z.  Value index=3, #Derivatives=0, #Versions=1\n')
    for datapoint in REGION.DATAPOINTS.DatapointsListGet(DATAPOINT_GROUP_USER_NUMBER):
        try:
            GROUP.index(REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,4))
        except ValueError:
            pass
        else:
            OUTPUT.write(' Node: %s\n' % datapoint)
            OUTPUT.write('  %.15e\n' % REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,1))
            OUTPUT.write('  %.15e\n' % REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,2))
            OUTPUT.write('  %.15e\n' % REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,3))
            if NUMBER_OF_OUTPUT_COMPONENTS == 5:
                OUTPUT.write(' %s\n' % REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,4))
                OUTPUT.write(' %s\n' % REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER,datapoint,5))
            #OUTPUT.write(' \n')
    OUTPUT.close()

#============================================================================

def ReadOpgauss(REGION,DATAPOINT_GROUP_USER_NUMBER,INPUT_FILENAME):
    INPUT = open(INPUT_FILENAME + ".opgaus").read()
    INPUT = re.split(r'[\n\\]', INPUT)
    NUMBER_OF_COMPONENTS = 5
    REGION.DATAPOINTS.DatapointGroupCreateStart(DATAPOINT_GROUP_USER_NUMBER)
    REGION.DATAPOINTS.DatapointGroupLabelSet(DATAPOINT_GROUP_USER_NUMBER,"opgauss")
    REGION.DATAPOINTS.DatapointGroupNumberOfComponentsSet(DATAPOINT_GROUP_USER_NUMBER,NUMBER_OF_COMPONENTS)
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,1,"x")
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,2,"y")
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,3,"z")
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,4,"Element")
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,5,"GaussPoint")
    REGION.DATAPOINTS.DatapointGroupCreateFinish(DATAPOINT_GROUP_USER_NUMBER)
    DATAPOINT_USER_NUMBER = 1
    for line in range(len(INPUT)):
        #print array[line][0:6]
        if INPUT[line][0:8] == " Element":
            ELEMENT_USER_NUMBER = int(INPUT[line].split()[-1])
            #print ELEMENT_USER_NUMBER
        if INPUT[line][0:12] == " Gauss point":
            GAUSS_POINT_USER_NUMBER = int(INPUT[line].split()[-1])
            line = line + 9
            REGION.DATAPOINTS.DatapointAdd(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER)
            REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,1,float(INPUT[line].split()[-3]))
            REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,2,float(INPUT[line].split()[-2]))
            REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,3,float(INPUT[line].split()[-1]))
            REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,4,ELEMENT_USER_NUMBER)
            REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,5,GAUSS_POINT_USER_NUMBER)
            DATAPOINT_USER_NUMBER = DATAPOINT_USER_NUMBER + 1

#============================================================================

def ReadIpxi(REGION,DATAPOINT_GROUP_USER_NUMBER,INPUT_FILENAME):
    INPUT = open(INPUT_FILENAME + ".ipxi").read()
    INPUT = re.split(r'[\n\\]', INPUT)
    NUMBER_OF_COMPONENTS = 4
    REGION.DATAPOINTS.DatapointGroupCreateStart(DATAPOINT_GROUP_USER_NUMBER)
    REGION.DATAPOINTS.DatapointGroupLabelSet(DATAPOINT_GROUP_USER_NUMBER,"GeometricData")
    REGION.DATAPOINTS.DatapointGroupNumberOfComponentsSet(DATAPOINT_GROUP_USER_NUMBER,NUMBER_OF_COMPONENTS)
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,1,"x")
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,2,"y")
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,3,"z")
    REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER,4,"Element")
    REGION.DATAPOINTS.DatapointGroupCreateFinish(DATAPOINT_GROUP_USER_NUMBER)
    startidx = 0
    for nd in range(startidx,len(INPUT)):
        temp = INPUT[nd].split()
        if temp != []:
            REGION.DATAPOINTS.DatapointAdd(DATAPOINT_GROUP_USER_NUMBER,int(temp[0]))
            try:
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,int(temp[0]),1,float(temp[2]))
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,int(temp[0]),2,float(temp[3]))
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,int(temp[0]),3,float(temp[4]))
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,int(temp[0]),4,int(temp[1]))
            except ValueError:
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,int(temp[0]),1,float(0.0))
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,int(temp[0]),2,float(0.0))
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,int(temp[0]),3,float(0.0))
                REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER,int(temp[0]),4,int(0))
            else:
                pass


def ReadIpMesh(REGION,BASIS_USER_NUMBER,MESH_USER_NUMBER,FIELD_USER_NUMBER,IPNODE_INPUT_FILENAME,IPELEM_INPUT_FILENAME):
    DEBUG=False
    IPNODE_FILE = open(IPNODE_INPUT_FILENAME+".ipnode").read()
    IPELEM_FILE = open(IPELEM_INPUT_FILENAME+".ipelem").read()
    IPNODE_LINES = re.split(r'[\n\\]', IPNODE_FILE)
    IPELEM_LINES = re.split(r'[\n\\]', IPELEM_FILE)

    BASIS = REGION.BASES.BasisGlobalGet(BASIS_USER_NUMBER)

    #Create the default node set
    TOTAL_NUMBER_OF_NODES = int(IPNODE_LINES[3].split()[-1]) #Extract last number of line 3
    REGION.NODES.NodesCreateStart(TOTAL_NUMBER_OF_NODES)

    #Create the mesh
    #TOTAL_NUMBER_OF_ELEMENTS = int(IPELEM_LINES[3].split()[-1]) #Extract last number of line 3
    NUMBER_OF_FIELD_COMPONENTS = 1
    REGION.MESHES.MeshesCreateStart(MESH_USER_NUMBER)
    REGION.MESHES.MeshNumberOfDimensionsSet(MESH_USER_NUMBER,BASIS.NUMBER_OF_XIC)
    REGION.MESHES.MeshNumberOfComponentsSet(MESH_USER_NUMBER,NUMBER_OF_FIELD_COMPONENTS)

    #!Create the elements
    #Initialize Mesh Elements
    MESH_COMPONENT_NUMBER = 1
    REGION.MESHES.MeshElementsCreateStart(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,BASIS.USER_NUMBER)

    #Loop through and read element node numbers
    for line in range(len(IPELEM_LINES)):
        
        if IPELEM_LINES[line][0:16] == " Element number ":
            LOCAL_ELEMENT_NUMBER = int(IPELEM_LINES[line].split()[-1])
            ELEMENT_NODES = [int(values) for values in IPELEM_LINES[line+BASIS.NUMBER_OF_XIC+2].split()[8:8+BASIS.NUMBER_OF_NODES]]
            if DEBUG==True: print "Element Number:{0}, element nodes: {1}".format(LOCAL_ELEMENT_NUMBER,ELEMENT_NODES)
            REGION.MESHES.MeshElementsNodesSet(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,LOCAL_ELEMENT_NUMBER,ELEMENT_NODES)
            line = line + 1 + BASIS.NUMBER_OF_XIC+2
            while IPELEM_LINES[line][0:12] == " The version":
                VERSION_NUMBER = int(IPELEM_LINES[line].split()[-1])
                LOCAL_NODE_NUMBER = int(IPELEM_LINES[line].split()[8].rstrip(","))
                occurrence=int(IPELEM_LINES[line].split()[5])
                component=int(IPELEM_LINES[line].split()[9].split('=')[-1])
                element_node_idx = fem_miscellaneous_routines.indexOfNthOccurrence(occurrence, LOCAL_NODE_NUMBER, ELEMENT_NODES)
                for derivative_idx in range(BASIS.NUMBER_OF_PARTIAL_DERIVATIVES):
                    REGION.MESHES.MeshElementsNodeVersionSet(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,LOCAL_ELEMENT_NUMBER,element_node_idx+1,derivative_idx+1,VERSION_NUMBER,component) 
                line +=1
#            line = line + 1 + BASIS.NUMBER_OF_XIC+2
#            VERSION_NUMBER = 1
#            for node_idx in range(BASIS.NUMBER_OF_NODES):
#                for derivative_idx in range(BASIS.NUMBER_OF_PARTIAL_DERIVATIVES):
#                    REGION.MESHES.MeshElementsNodeVersionSet(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,LOCAL_ELEMENT_NUMBER,node_idx+1,derivative_idx+1,VERSION_NUMBER) 
#            while IPELEM_LINES[line][0:12] == " The version":
#                VERSION_NUMBER = int(IPELEM_LINES[line].split()[-1])
#                LOCAL_NODE_NUMBER = int(IPELEM_LINES[line].split()[8].rstrip(","))
#                if DEBUG==True: print "Local Node Number:{0}, version number: {1}".format(LOCAL_NODE_NUMBER,VERSION_NUMBER)
#                node_idx = ELEMENT_NODES.index(LOCAL_NODE_NUMBER)
#                for derivative_idx in range(BASIS.NUMBER_OF_PARTIAL_DERIVATIVES):
#                    REGION.MESHES.MeshElementsNodeVersionSet(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,LOCAL_ELEMENT_NUMBER,node_idx+1,derivative_idx+1,VERSION_NUMBER) 
#                    #GlobalElementNumber,NodeIndex,DerivativeNumber,VersionNumber
#                line = line + 3

    REGION.MESHES.MeshElementsCreateFinish(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER)
    REGION.MESHES.MeshesCreateFinish(MESH_USER_NUMBER)

    #Define Geometric Fields
    REGION.FIELDS.FieldCreateStart(FIELD_USER_NUMBER)
    REGION.FIELDS.FieldTypeSet(FIELD_USER_NUMBER,"FieldGeometricType")
    REGION.FIELDS.FieldMeshSet(FIELD_USER_NUMBER,MESH_USER_NUMBER)
    REGION.FIELDS.FieldNumberOfFieldVariablesSet(FIELD_USER_NUMBER,1)
    REGION.FIELDS.FieldNumberOfFieldComponentsSet(FIELD_USER_NUMBER,1,BASIS.NUMBER_OF_XIC)
    COORDINATE_LABELS = ['x','y','z']
    FIELD_VARIABLE_USER_NUMBER = 1
    for component_idx in range(1,BASIS.NUMBER_OF_XIC+1):
        REGION.FIELDS.FieldComponentLabelSet(FIELD_USER_NUMBER,1,component_idx,COORDINATE_LABELS[component_idx-1])
        REGION.FIELDS.FieldComponentMeshComponentSet(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,component_idx,MESH_COMPONENT_NUMBER) #FieldUserNumber,FieldVariableUserNumber,FieldComponentUserNumber,MeshComponentUserNumber
    REGION.FIELDS.FieldCreateFinish(FIELD_USER_NUMBER)

    NUMBER_OF_COMPONENT_DERIVATIVES = [0]*BASIS.NUMBER_OF_XIC
    COMPONENT_VERSIONS_PRESENT = [False]*BASIS.NUMBER_OF_XIC

    for component_idx in range(BASIS.NUMBER_OF_XIC):
        if BASIS.NUMBER_OF_XIC == 2:
          NUMBER_OF_COMPONENT_DERIVATIVES[component_idx] = int(IPNODE_LINES[component_idx+7].split()[-1]) #Extract last number of line 3
        else:
          NUMBER_OF_COMPONENT_DERIVATIVES[component_idx] = int(IPNODE_LINES[component_idx+8].split()[-1]) #Extract last number of line 3
          if IPNODE_LINES[component_idx+5].split()[-1] == "Y" or IPNODE_LINES[component_idx+5].split()[-1] == "y":
              COMPONENT_VERSIONS_PRESENT[component_idx] = True

    #Loop through and read node derivatives
    if sum(COMPONENT_VERSIONS_PRESENT) > 0:
        for line in range(len(IPNODE_LINES)):
            if IPNODE_LINES[line][0:13] == " Node number ":
                LOCAL_NODE_NUMBER = int(IPNODE_LINES[line].split()[-1])
                if DEBUG==True: print "LOCAL_NODE_NUMBER %s" %LOCAL_NODE_NUMBER
                if sum(COMPONENT_VERSIONS_PRESENT) > 0:
                    line = line + 1
                for component_idx in range(BASIS.NUMBER_OF_XIC):
                    if COMPONENT_VERSIONS_PRESENT[component_idx] == True:
                        NUMBER_OF_VERSIONS = int(IPNODE_LINES[line].split()[-1].rstrip())
                        if NUMBER_OF_VERSIONS > 1:
                            line = line + 1
                    else:
                        NUMBER_OF_VERSIONS = 1
                    line = line + 1
                    if DEBUG==True: print "  component_idx %d" %(component_idx+1)
                    ###################### TEMP
                    #NUMBER_OF_VERSIONS = 1
                    ###################### TEMP
                    for version_idx in range(NUMBER_OF_VERSIONS):
                        if DEBUG==True: print "   version_idx %d" %(version_idx+1)
                        for derivative_idx in range(NUMBER_OF_COMPONENT_DERIVATIVES[component_idx]+1):
                            if DEBUG==True: print "   derivative_idx %d" %(derivative_idx+1)
                            if DEBUG==True: print IPNODE_LINES[line]
                            VALUE = float(IPNODE_LINES[line].split()[-1])
                            REGION.FIELDS.FieldParameterSetUpdateNode(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,version_idx+1,derivative_idx+1,LOCAL_NODE_NUMBER,component_idx+1,VALUE)
                            line = line + 1
                        if (NUMBER_OF_VERSIONS > 1) and (version_idx!=NUMBER_OF_VERSIONS-1):
                            line = line + 1
    else:
        VERSION_NUMBER = 1
        for line in range(len(IPNODE_LINES)):
            if DEBUG==True: print IPNODE_LINES[line]
            if IPNODE_LINES[line][0:13] == " Node number ":
                LOCAL_NODE_NUMBER = int(IPNODE_LINES[line].split()[-1])
                if DEBUG==True: print "LOCAL_NODE_NUMBER %s" %LOCAL_NODE_NUMBER
                line = line + 1
                for component_idx in range(BASIS.NUMBER_OF_XIC):
                    try:
                        FIELD_NODE_EXISTS = REGION.FIELDS.FieldParameterNodeCheckExists(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,LOCAL_NODE_NUMBER,component_idx+1)
                    except:
                        break
                    else:
                        if FIELD_NODE_EXISTS == True:
                            if DEBUG==True: print "  component_idx %d" %(component_idx+1)
                            for derivative_idx in range(NUMBER_OF_COMPONENT_DERIVATIVES[component_idx]+1):
                                if DEBUG==True: print "   derivative_idx %d" %(derivative_idx+1)
                                if DEBUG==True: print IPNODE_LINES[line]
                                VALUE = float(IPNODE_LINES[line].split()[-1])
                                REGION.FIELDS.FieldParameterSetUpdateNode(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,VERSION_NUMBER,derivative_idx+1,LOCAL_NODE_NUMBER,component_idx+1,VALUE)
                                line = line + 1

def WriteIpMap(nodes, derivatives, output_filename):
    number_of_components = 3
    derivative_labels = (
        [' Is the nodal position mapped out [N]? ',
        ' Is the derivative wrt direction 1 is mapped out [N]? ',
        ' Is the derivative wrt direction 2 is mapped out [N]? ',
        ' Is the derivative wrt directions 1 & 2 is mapped out [N]? ',
        ' Is the derivative wrt direction 3 is mapped out [N]? ',
        ' Is the derivative wrt directions 1 & 3 is mapped out [N]? ',
        ' Is the derivative wrt directions 2 & 3 is mapped out [N]? ',
        ' Is the derivative wrt directions 1, 2 & 3 is mapped out [N]? '])
    output = open(output_filename + '.ipmap', 'w')
    output.write(' CMISS Version 2.0  ipmap File Version 1\n')
    output.write(' Heading:\n')
    output.write(' \n')
    output.write(' Define node position mapping [N]? y\n')
    output.write(' The number of nodes with special mappings is [    1]:     {0}\n'.format(len(nodes)))
    output.write('\n')
    for node in nodes:
        output.write(' Node number [ {0}]:     {1}\n'.format(node,node))
        for component in range(1,number_of_components+1):
            output.write(' For the Xj({0}) coordinate:\n'.format(component))
            output.write(' For version number 1:\n')
            output.write(' Is the nodal position mapped out [N]? N\n')
            output.write(' Is the derivative wrt direction 1 is mapped out [N]? N\n')
            output.write(' Is the derivative wrt direction 2 is mapped out [N]? N\n')
            output.write(' Is the derivative wrt directions 1 & 2 is mapped out [N]? N\n')
            output.write(' Is the derivative wrt direction 3 is mapped out [N]? N\n')
            output.write(' Is the derivative wrt directions 1 & 3 is mapped out [N]? N\n')
            output.write(' Is the derivative wrt directions 2 & 3 is mapped out [N]? N\n')
            output.write(' Is the derivative wrt directions 1, 2 & 3 is mapped out [N]? N\n')
            output.write(' For version number 2:\n')

            for derivative_idx, derivative in enumerate(range(1,9)):
                if derivatives[derivative_idx] > 0:
                    mapped = 'y'
                else:
                    mapped = 'n'
                output.write(derivative_labels[derivative_idx] + mapped + '\n')
                if mapped == 'y':
                    output.write(' Enter node, version, direction, derivative numbers to map to [1,1,1,1]: {0} 1 {1} {2}\n'.format(node, component, derivative))
                    output.write(' Enter the mapping coefficient [1]: 0.10000E+01\n')
        output.write('\n')
    output.close()
