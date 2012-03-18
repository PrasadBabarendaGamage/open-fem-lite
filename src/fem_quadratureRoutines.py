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

from math import *
import fem_miscellaneous_routines

def GAUSS1(BASIS):

    D = []
    D.append([0.0]*7)
    D.append([-0.2886751345948130, 0.2886751345948130]+[0.0]*5)
    D.append([-0.3872983346207410, 0.0               , 0.3872983346207410]+[0.0]*4)
    D.append([-0.4305681557970260,-0.1699905217924280, 0.1699905217924280, 0.4305681557970260]+[0.0]*3)
    D.append([-0.4530899229693320,-0.2692346550528410, 0.0               , 0.2692346550528410, 0.4530899229693320]+[0.0]*2)
    D.append([-0.4662347571015760,-0.3306046932331330,-0.1193095930415990, 0.1193095930415990, 0.3306046932331330, 0.4662347571015760]+[0.0]*1)
    D.append([-0.4745539561713800,-0.3707655927996970,-0.2029225756886990, 0.0               , 0.2029225756886990, 0.3707655927996970,0.4745539561713800])

    

    W = []
    W.append([1.0]+[0.0]*6)
    W.append([0.50,0.50]+[0.0]*5)
    W.append([0.2777777777777780, 0.4444444444444440, 0.2777777777777780]+[0.0]*4)
    W.append([0.1739274225687270, 0.3260725774312730, 0.3260725774312730, 0.1739274225687270]+[0.0]*3)
    W.append([0.1184634425280940, 0.2393143352496830, 0.2844444444444440, 0.2393143352496830, 0.1184634425280940]+[0.0]*2)
    W.append([0.0856622461895850, 0.1803807865240700, 0.2339569672863460, 0.2339569672863460, 0.1803807865240700, 0.0856622461895850]+[0.0]*1)
    W.append([0.0647424830844350, 0.1398526957446390, 0.1909150252525600, 0.2089795918367350, 0.1909150252525600, 0.1398526957446390, 0.064742483084435])
    NGAP = BASIS.QUADRATURE.NUMBER_OF_GAUSS_XI

    NIT = BASIS.NUMBER_OF_XIC
    XI = fem_miscellaneous_routines.initialize1DList(0.0,NIT)    
    WG = fem_miscellaneous_routines.initialize1DList(0.0,BASIS.QUADRATURE.NUMBER_OF_GAUSS)
    XIG = fem_miscellaneous_routines.initialize2DList(0.0,BASIS.QUADRATURE.NUMBER_OF_GAUSS,NIT)
    XIGG = fem_miscellaneous_routines.initialize4DList(0.0,NGAP[0],NGAP[1],NGAP[2],3)
    ng1=NGAP[0]-1
    ng2=0
    ng3=0
    ng2=NGAP[1]-1
    ng3=NGAP[2]-1
    ng =0

    for k in range (ng3+1):
        for j in range(ng2+1):
            for i in range(ng1+1):
                XIGG[i][j][k][0]=0.5+D[ng1][i]
                XIGG[i][j][k][1]=0.5+D[ng2][j]
                XIGG[i][j][k][2]=0.5+D[ng3][k]
                WG[ng]=W[ng1][i]*W[ng2][j]*W[ng3][k]
                for ni in range(NIT):
                    XI[ni]=XIGG[i][j][k][ni]
                    XIG[ng][ni]=XI[ni]
                ng=ng+1

    BASIS.QUADRATURE.GAUSS_POSITIONS = XIG
    BASIS.QUADRATURE.GAUSS_WEIGHTS  = WG


def GAUSS1_MATERIAL_POINTS(BASIS):
    D = []
    D.append([0.0]*9)
    D.append([-0.5,0.0,0.5]+[0.0]*6)
    D.append([-0.5,-0.2886751345948130, 0.2886751345948130,0.5]+[0.0]*5)
    D.append([-0.5,-0.3872983346207410, 0.0               , 0.3872983346207410,0.5]+[0.0]*4)
    D.append([-0.5,-0.4305681557970260,-0.1699905217924280, 0.1699905217924280, 0.4305681557970260,0.5]+[0.0]*3)
    D.append([-0.5,-0.4530899229693320,-0.2692346550528410, 0.0               , 0.2692346550528410, 0.4530899229693320,0.5]+[0.0]*2)
    D.append([-0.5,-0.4662347571015760,-0.3306046932331330,-0.1193095930415990, 0.1193095930415990, 0.3306046932331330, 0.4662347571015760,0.5]+[0.0]*1)
    D.append([-0.5,-0.4745539561713800,-0.3707655927996970,-0.2029225756886990, 0.0               , 0.2029225756886990, 0.3707655927996970,0.4745539561713800,0.5])

    

    #W = []
    #W.append([1.0]+[0.0]*6)
    #W.append([0.50,0.50]+[0.0]*5)
    #W.append([0.2777777777777780, 0.4444444444444440, 0.2777777777777780]+[0.0]*4)
    #W.append([0.1739274225687270, 0.3260725774312730, 0.3260725774312730, 0.1739274225687270]+[0.0]*3)
    #W.append([0.1184634425280940, 0.2393143352496830, 0.2844444444444440, 0.2393143352496830, 0.1184634425280940]+[0.0]*2)
    #W.append([0.0856622461895850, 0.1803807865240700, 0.2339569672863460, 0.2339569672863460, 0.1803807865240700, 0.0856622461895850]+[0.0]*1)
    #W.append([0.0647424830844350, 0.1398526957446390, 0.1909150252525600, 0.2089795918367350, 0.1909150252525600, 0.1398526957446390, 0.064742483084435])
    NGAP = BASIS.QUADRATURE.NUMBER_OF_GAUSS_XI

    NIT = BASIS.NUMBER_OF_XIC
    XI = fem_miscellaneous_routines.initialize1DList(0.0,NIT)    
    XIG = fem_miscellaneous_routines.initialize2DList(0.0,(NGAP[0]+2)*(NGAP[1]+2)*(NGAP[2]+2),NIT)
    XIGG = fem_miscellaneous_routines.initialize4DList(0.0,NGAP[0]+2,NGAP[1]+2,NGAP[2]+2,3)
    ng1=NGAP[0]
    ng2=0
    ng3=0
    ng2=NGAP[1]
    ng3=NGAP[2]
    ng =0

    for k in range (ng3+2):
        for j in range(ng2+2):
            for i in range(ng1+2):
                XIGG[i][j][k][0]=0.5+D[ng1][i]
                XIGG[i][j][k][1]=0.5+D[ng2][j]
                XIGG[i][j][k][2]=0.5+D[ng3][k]
                for ni in range(NIT):
                    XI[ni]=XIGG[i][j][k][ni]
                    XIG[ng][ni]=XI[ni]
                ng=ng+1

    BASIS.QUADRATURE.GAUSS_POSITIONS = XIG

