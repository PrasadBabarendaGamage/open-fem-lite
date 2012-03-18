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


DEBUG=False
A = 1
#>Start to create the regular generated mesh type
def GENERATED_MESH_REGULAR_CREATE(GENERATED_MESH):
    REGION = GENERATED_MESH.REGION
    BASIS = GENERATED_MESH.BASIS
    BASIS_NUMBER_OF_NODES = BASIS.NUMBER_OF_NODES

    NUMBER_OF_XIC = BASIS.NUMBER_OF_XIC
    NUMBER_OF_ELEMENTS_XIC = GENERATED_MESH.NUMBER_OF_ELEMENTS_XIC
    NUMBER_OF_ELEMENTS_XIC.insert(0,0)
    NUMBER_OF_NODES_XIC = BASIS.NUMBER_OF_NODES_XIC
    NUMBER_OF_NODES_XIC.insert(0,0)
    TOTAL_NUMBER_OF_NODES_XIC = [0]*(3+A)
    TOTAL_NUMBER_OF_ELEMENTS_XIC = [0]*(3+A)

    #Calculate sizes
    TOTAL_NUMBER_OF_NODES=1
    TOTAL_NUMBER_OF_ELEMENTS=1
    for xic_idx in range(1,NUMBER_OF_XIC+A):
        TOTAL_NUMBER_OF_NODES_XIC[xic_idx]=(BASIS.NUMBER_OF_NODES_XIC[xic_idx]-2)*NUMBER_OF_ELEMENTS_XIC[xic_idx]+NUMBER_OF_ELEMENTS_XIC[xic_idx]+1
        TOTAL_NUMBER_OF_ELEMENTS_XIC[xic_idx]=NUMBER_OF_ELEMENTS_XIC[xic_idx]
        TOTAL_NUMBER_OF_NODES=TOTAL_NUMBER_OF_NODES*TOTAL_NUMBER_OF_NODES_XIC[xic_idx]
        TOTAL_NUMBER_OF_ELEMENTS=TOTAL_NUMBER_OF_ELEMENTS*TOTAL_NUMBER_OF_ELEMENTS_XIC[xic_idx]

    GENERATED_MESH.TOTAL_NUMBER_OF_NODES_XIC = TOTAL_NUMBER_OF_NODES_XIC
    GENERATED_MESH.TOTAL_NUMBER_OF_ELEMENTS_XIC = TOTAL_NUMBER_OF_ELEMENTS_XIC
    GENERATED_MESH.TOTAL_NUMBER_OF_NODES = TOTAL_NUMBER_OF_NODES
    GENERATED_MESH.TOTAL_NUMBER_OF_ELEMENTS = TOTAL_NUMBER_OF_ELEMENTS

    if DEBUG:
        print TOTAL_NUMBER_OF_NODES_XIC
        print TOTAL_NUMBER_OF_ELEMENTS_XIC
        print TOTAL_NUMBER_OF_NODES
        print TOTAL_NUMBER_OF_ELEMENTS

    #Create the default node set
    REGION.NODES.NodesCreateStart(TOTAL_NUMBER_OF_NODES)

    #Create the mesh
    MESH_USER_NUMBER = GENERATED_MESH.MESH_USER_NUMBER
    NUMBER_OF_COMPONENTS = 1
    REGION.MESHES.MeshesCreateStart(MESH_USER_NUMBER)
    REGION.MESHES.MeshNumberOfDimensionsSet(MESH_USER_NUMBER,BASIS.NUMBER_OF_XIC)
    REGION.MESHES.MeshNumberOfComponentsSet(MESH_USER_NUMBER,NUMBER_OF_COMPONENTS)

    #!Create the elements
    #Initialize Mesh Elements
    REGION.MESHES.MeshElementsCreateStart(MESH_USER_NUMBER,1,BASIS.USER_NUMBER)
    MESH_COMPONENT_NUMBER = 1

    #!Set the elements for the regular mesh
    ELEMENT_NODES = [0]*(BASIS_NUMBER_OF_NODES+A)
    #Step in the xi[3)direction
    for ne3 in range(A,TOTAL_NUMBER_OF_ELEMENTS_XIC[3]+1+A):
        for ne2 in range(A,TOTAL_NUMBER_OF_ELEMENTS_XIC[2]+1+A):
            for ne1 in range(A,TOTAL_NUMBER_OF_ELEMENTS_XIC[1]+1+A):
                if((NUMBER_OF_XIC<3) or (ne3 <=TOTAL_NUMBER_OF_ELEMENTS_XIC[3])):
                    if(NUMBER_OF_XIC<2 or ne2<=TOTAL_NUMBER_OF_ELEMENTS_XIC[2]):
                        if(ne1<=TOTAL_NUMBER_OF_ELEMENTS_XIC[1]):
                            ne=ne1
                            np=1+(ne1-1)*(NUMBER_OF_NODES_XIC[1]-1)
                            if(NUMBER_OF_XIC>1):
                                ne=ne+(ne2-1)*TOTAL_NUMBER_OF_ELEMENTS_XIC[1]
                                np=np+(ne2-1)*TOTAL_NUMBER_OF_NODES_XIC[1]*(NUMBER_OF_NODES_XIC[2]-1)
                                if(NUMBER_OF_XIC>2):
                                    ne=ne+(ne3-1)*TOTAL_NUMBER_OF_ELEMENTS_XIC[1]*TOTAL_NUMBER_OF_ELEMENTS_XIC[2]
                                    np=np+(ne3-1)*TOTAL_NUMBER_OF_NODES_XIC[1]*TOTAL_NUMBER_OF_NODES_XIC[2]*(NUMBER_OF_NODES_XIC[3]-1)
                            nn=0
                            for nn1 in range(A,NUMBER_OF_NODES_XIC[1]+A):
                                nn=nn+1
                                ELEMENT_NODES[nn]=np+(nn1-1)
                            if(NUMBER_OF_XIC>1):
                                for nn2 in range(A+1,NUMBER_OF_NODES_XIC[2]+A):
                                    for nn1 in range(A,NUMBER_OF_NODES_XIC[1]+A):
                                        nn=nn+1
                                        ELEMENT_NODES[nn]=np+(nn1-1)+(nn2-1)*TOTAL_NUMBER_OF_NODES_XIC[1]
                                if(NUMBER_OF_XIC>2):
                                    for nn3 in range(A+1,NUMBER_OF_NODES_XIC[3]+A):
                                        for nn2 in range(A,NUMBER_OF_NODES_XIC[2]+A):
                                            for nn1 in range(A,NUMBER_OF_NODES_XIC[1]+A):
                                                nn=nn+1
                                                ELEMENT_NODES[nn]=np+(nn1-1)+(nn2-1)*TOTAL_NUMBER_OF_NODES_XIC[1]+(nn3-1)*TOTAL_NUMBER_OF_NODES_XIC[1]*TOTAL_NUMBER_OF_NODES_XIC[2]
                            #print ELEMENT_NODES[1:len(ELEMENT_NODES)]
                            REGION.MESHES.MeshElementsNodesSet(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,ne,ELEMENT_NODES[1:len(ELEMENT_NODES)])
    REGION.MESHES.MeshElementsCreateFinish(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER)
    REGION.MESHES.MeshesCreateFinish(MESH_USER_NUMBER)
    GENERATED_MESH.MESH = REGION.MESHES.MeshGlobalGet(MESH_USER_NUMBER)

def GENERATED_MESH_GEOMETRIC_PARAMETERS_CALCULATE(GENERATED_MESH):
    REGION = GENERATED_MESH.REGION
    BASIS = GENERATED_MESH.BASIS
    MESH = GENERATED_MESH.MESH
    FIELD = GENERATED_MESH.FIELD
    FIELD_USER_NUMBER = FIELD.USER_NUMBER

    #Default to first field variable of the field and thier first NUMBER_OF_XIC'th number of components
    FIELD_VARIABLE = FIELD.VARIABLES[0]
    FIELD_VARIABLE_USER_NUMBER = FIELD_VARIABLE.USER_NUMBER
    MAXIMUM_EXTENT = GENERATED_MESH.MAXIMUM_EXTENT
    FIELD_NODE_USER_NUMBER = 0
    if BASIS.NUMBER_OF_XIC == 3:
        VALUE = [0]*(3)
        for Z_COUNTER in range(GENERATED_MESH.TOTAL_NUMBER_OF_NODES_XIC[3]):
            for Y_COUNTER in range(GENERATED_MESH.TOTAL_NUMBER_OF_NODES_XIC[2]):
                for X_COUNTER in range(GENERATED_MESH.TOTAL_NUMBER_OF_NODES_XIC[1]):
                    FIELD_NODE_USER_NUMBER = FIELD_NODE_USER_NUMBER + 1
                    for XIC_COORDINATE in range(BASIS.NUMBER_OF_XIC):
                        FIELD_COMPONENT_USER_NUMBER = XIC_COORDINATE + 1
                        REGION.FIELDS.FieldParameterSetUpdateNode(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,1,1,FIELD_NODE_USER_NUMBER,FIELD_COMPONENT_USER_NUMBER,VALUE[XIC_COORDINATE])
                    VALUE[0] = VALUE[0] + (MAXIMUM_EXTENT[0]/(GENERATED_MESH.TOTAL_NUMBER_OF_NODES_XIC[1]-1))
                VALUE[1] = VALUE[1] + (MAXIMUM_EXTENT[1]/(GENERATED_MESH.TOTAL_NUMBER_OF_NODES_XIC[2]-1))
                VALUE[0] = 0
            VALUE[2] = MAXIMUM_EXTENT[2]/(GENERATED_MESH.TOTAL_NUMBER_OF_NODES_XIC[3]-1)
            VALUE[1] = 0
    elif BASIS.NUMBER_OF_XIC == 2:
        VALUE = [0]*(2)
        for Y_COUNTER in range(GENERATED_MESH.TOTAL_NUMBER_OF_NODES_XIC[2]):
            for X_COUNTER in range(GENERATED_MESH.TOTAL_NUMBER_OF_NODES_XIC[1]):
                FIELD_NODE_USER_NUMBER = FIELD_NODE_USER_NUMBER + 1
                for XIC_COORDINATE in range(BASIS.NUMBER_OF_XIC):
                    FIELD_COMPONENT_USER_NUMBER = XIC_COORDINATE + 1
                    REGION.FIELDS.FieldParameterSetUpdateNode(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,1,1,FIELD_NODE_USER_NUMBER,FIELD_COMPONENT_USER_NUMBER,VALUE[XIC_COORDINATE])
                VALUE[0] = VALUE[0] + (MAXIMUM_EXTENT[0]/(GENERATED_MESH.TOTAL_NUMBER_OF_NODES_XIC[1]-1))
            VALUE[1] = MAXIMUM_EXTENT[1]/(GENERATED_MESH.TOTAL_NUMBER_OF_NODES_XIC[2]-1)
            VALUE[0] = 0

