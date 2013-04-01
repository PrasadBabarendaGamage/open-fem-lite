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

import fem_topology as CMISSLite

def main():


    # Initialize and Create Regions.
    CMISSLite_WorldRegion = CMISSLite.femInitialize()
    CMISSLite_region_user_number = 1
    CMISSLite_WorldRegion.RegionsCreateStart(CMISSLite_region_user_number)
    CMISSLite_WorldRegion.RegionsCreateFinish(CMISSLite_region_user_number)
    CMISSLite_Mesh = (
        CMISSLite_WorldRegion.RegionsRegionGet(CMISSLite_region_user_number))

    input_folder = 'input/'
    input_filename = 'cmNodeGroups.txt'
    CMISSLite_Mesh.NODEGROUPS.extract_node_groups(input_folder+input_filename)
    input_filename = ('BC_Backward.ipinit')
    CMISSLite_Mesh.NODEGROUPS.extract_boundary_conditions(input_folder+
                                                          input_filename)

    # Display node groups
    CMISSLite_Mesh.NODEGROUPS.display_node_groups(listNodes=True,
                                                  listDerivatives=True)

    # Loop over all node groups
    for user_number in CMISSLite_Mesh.NODEGROUPS.globalToUserMap:
        node_group = CMISSLite_Mesh.NODEGROUPS.node_group_global_get(
            user_number)
        print 'Node group label: {0}'.format(node_group.label)
        # List the boundary conditions prescribed for each node group (
        # similar to what the display_node_groups achieves, above).  
        for component, component_derivatives in enumerate(
                node_group.bc.derivatives):
            print '  Component number: {0}'.format(component+1)
            for derivative in component_derivatives:
                print '    Derivative {0:>3} assigned'.format(derivative)

if __name__ == '__main__':
    main()
    print 'Program successfully completed.'
