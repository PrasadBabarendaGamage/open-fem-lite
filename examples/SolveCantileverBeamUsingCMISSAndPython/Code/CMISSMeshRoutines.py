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

def ExtractNodalParameters(REGION):
    parameters = []

    #User Numbers
    MeshUserNumber = 1
    GeometricFieldUserNumber = 1
    GeometricFieldNumberOfComponents = 3
    MeshComponent = 1
    FieldVariable = 1
    VersionNumber = 1
    for meshNodeNumber in REGION.MESHES.MeshNodesListGet(MeshUserNumber,MeshComponent):
        for fieldComponentNumber in range(1,GeometricFieldNumberOfComponents+1):
            for derivativeNumber in range(1,9):
                parameters.append(REGION.FIELDS.FieldParameterSetNodeValueGet(GeometricFieldUserNumber,FieldVariable,VersionNumber,derivativeNumber,meshNodeNumber,fieldComponentNumber))

    return parameters

def ReadInMesh(filename):
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
    REGION.ReadMesh(BasisUserNumber,MeshUserNumber,GeometricFieldUserNumber,"CMISS",filename,filename)
    
    return REGION
