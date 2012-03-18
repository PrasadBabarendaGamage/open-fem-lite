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

import fem_generatedMeshRoutines
import fem_quadratureRoutines
import fem_miscellaneous_routines
import fem_ioRoutines


#============================================================================
#General subroutines

def GlobalNumberGet(TYPE,USER_NUMBER):
	try:
		GLOBAL_NUMBER = TYPE.GLOBAL_TO_USER_MAP.index(USER_NUMBER) #invese map
	except ValueError:
		raise ValueError('The specified local number of %d is invalid for the %s.' %(USER_NUMBER,TYPE.IDENTIFIER))
	else:
		return GLOBAL_NUMBER

def femInitialize():
	return Regions()

#============================================================================

class Region():
	def __init__(self,REGION_USER_NUMBER):
		self.REGION_USER_NUMBER = REGION_USER_NUMBER
		self.FIELDS = Fields(self)
		self.NODES = Nodes(self)
		self.BASES = Bases(self)
		self.GENERATED_MESHES = GeneratedMeshes(self)
		self.MESHES = Meshes(self)
		self.DATAPOINTS = DatapointGroups(self)

	def ReadMesh(self,BASIS_USER_NUMBER,MESH_USER_NUMBER,FIELD_USER_NUMBER,FILE_FORMAT,IPNODE_INPUT_FILENAME,IPELEM_INPUT_FILENAME):
		if FILE_FORMAT == "CMISS":
			fem_ioRoutines.ReadIpMesh(self,BASIS_USER_NUMBER,MESH_USER_NUMBER,FIELD_USER_NUMBER,IPNODE_INPUT_FILENAME,IPELEM_INPUT_FILENAME)

	def ReadIpxi(self,DATA_POINT_GROUP_USER_NUMBER,FILE_FORMAT,IPXI_INPUT_FILENAME):
		if FILE_FORMAT == "CMISS":
			fem_ioRoutines.ReadIpxi(self,DATA_POINT_GROUP_USER_NUMBER,IPXI_INPUT_FILENAME)

	def ReadOpgauss(self,DATA_POINT_GROUP_USER_NUMBER,FILE_FORMAT,OPGAUSS_INPUT_FILENAME):
		if FILE_FORMAT == "CMISS":
			fem_ioRoutines.ReadOpgauss(self,DATA_POINT_GROUP_USER_NUMBER,OPGAUSS_INPUT_FILENAME)

	def ReadExdata(self,DATA_POINT_GROUP_USER_NUMBER,FILE_FORMAT,EXDATA_INPUT_FILENAME):
		if FILE_FORMAT == "CMISS":
			fem_ioRoutines.ReadExdata(self,DATA_POINT_GROUP_USER_NUMBER,EXDATA_INPUT_FILENAME)

	def WriteExdata(self,DATA_POINT_GROUP_USER_NUMBER,GROUP_LABEL,NUMBER_OF_OUTPUT_COMPONENTS,FILE_FORMAT,EXDATA_OUTPUT_FILENAME):
		if FILE_FORMAT == "CMISS":
			fem_ioRoutines.WriteExdata(self,DATA_POINT_GROUP_USER_NUMBER,GROUP_LABEL,NUMBER_OF_OUTPUT_COMPONENTS,EXDATA_OUTPUT_FILENAME)
		elif FILE_FORMAT == "TXT":
			fem_ioRoutines.WriteDataTxt(self,DATA_POINT_GROUP_USER_NUMBER,NUMBER_OF_OUTPUT_COMPONENTS,EXDATA_OUTPUT_FILENAME)

	def WriteExdataSelectedGroup(self,DATA_POINT_GROUP_USER_NUMBER,GROUP,NUMBER_OF_OUTPUT_COMPONENTS,FILE_FORMAT,EXDATA_OUTPUT_FILENAME):
		if FILE_FORMAT == "CMISS":
			fem_ioRoutines.WriteExdataSelectedGroup(self,DATA_POINT_GROUP_USER_NUMBER,GROUP,NUMBER_OF_OUTPUT_COMPONENTS,EXDATA_OUTPUT_FILENAME)

	def WriteIpNode(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,OUTPUT_FILENAME):
		FIELD = self.FIELDS.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		fem_ioRoutines.WriteIpNode(FIELD_VARIABLE,OUTPUT_FILENAME)

	def WriteIpElem(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,OUTPUT_FILENAME):
		FIELD = self.FIELDS.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		fem_ioRoutines.WriteIpElem(FIELD_VARIABLE,OUTPUT_FILENAME)

	def WriteIpCoor(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,OUTPUT_FILENAME):
		FIELD = self.FIELDS.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		fem_ioRoutines.WriteIpCoor(FIELD_VARIABLE,OUTPUT_FILENAME)

	def WriteIpBase(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,OUTPUT_FILENAME):
		FIELD = self.FIELDS.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		fem_ioRoutines.WriteIpBase(FIELD_VARIABLE,OUTPUT_FILENAME)

	def WriteCmCom(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,OUTPUT_FILENAME):
		FIELD = self.FIELDS.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		fem_ioRoutines.WriteCmCom(FIELD_VARIABLE,OUTPUT_FILENAME)

	def WriteCmguiCom(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,OUTPUT_FILENAME):
		FIELD = self.FIELDS.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		fem_ioRoutines.WriteCmguiCom(FIELD_VARIABLE,OUTPUT_FILENAME)

	def WriteIpData(self,DATA_POINT_GROUP_USER_NUMBER,OUTPUT_FILENAME,OUTPUT_GROUP_NAME):
		DATAPOINT_GROUP = self.DATAPOINTS.DatapointGroupGlobalGet(DATA_POINT_GROUP_USER_NUMBER)
		fem_ioRoutines.WriteIpData(DATAPOINT_GROUP,OUTPUT_FILENAME,OUTPUT_GROUP_NAME)

class Regions():
	def __init__(self,):
		self.IDENTIFIER = "Region"
		self.NUMBER_OF_REGIONS = 0
		self.GLOBAL_TO_USER_MAP = []
		self.REGIONS = []

	def RegionsCreateStart(self,USER_NUMBER):
		self.RegionsRegionAdd(USER_NUMBER)

	def RegionsRegionAdd(self,USER_NUMBER):
		self.NUMBER_OF_REGIONS = self.NUMBER_OF_REGIONS + 1
		GLOBAL_NUMBER = self.NUMBER_OF_REGIONS
		self.GLOBAL_TO_USER_MAP.append(USER_NUMBER)
		self.REGIONS.append(Region(USER_NUMBER))
		return GLOBAL_NUMBER

	def RegionsRegionGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return self.REGIONS[GLOBAL_NUMBER]

	def RegionsCreateFinish(self,USER_NUMBER):
		pass

#============================================================================

class Quadrature():
	""" !<The type of the quadrature
	"""

	def __init__(self,NUMBER_OF_GAUSS_XI):
		self.IDENTIFIER = "Quadarture"
		self.BASIS = self
		self.NUMBER_OF_GAUSS_XI = NUMBER_OF_GAUSS_XI #!<NUMBER_OF_GAUSS_XI(ni). For standard Gauss schemes the number of Gauss points to be used in the ni'th xi direction.
		self.TYPE = "" #!<The type of the quadrature \see BASIS_ROUTINES_QuadratureTypes
		NUMBER_OF_GAUSS = 1
		for value in NUMBER_OF_GAUSS_XI:
			NUMBER_OF_GAUSS = NUMBER_OF_GAUSS*value
		self.NUMBER_OF_GAUSS = NUMBER_OF_GAUSS  #!<The number of gauss points for the quadrature scheme.
		self.GAUSS_POSITIONS = [] #!<GAUSS_POSITIONS(nic,ng). The positions in the nic'th xi coordinate of Gauss point ng. Old CMISS name XIG(ni,ng,nb).
		self.GAUSS_WEIGHTS = [] #!<GAUSS_WEIGHTS(ng). The weight applied to Gauss point ng. Old CMISS name WG(ng,nb).
		self.GAUSS_BASIS_FNS = [] #!<GAUSS_BASIS_FNS(ns,nu,ng). The value of the basis functions evaluated at Gauss point ng for the nu'th derivative of the basis function associated with the ns'th element parameter. Old CMISS name PG(ns,nu,ng,nb)

#============================================================================


class Basis():
	""" !> Contains all information about a basis .
	"""

	def __init__( self,USER_NUMBER,REGION):
		self.USER_NUMBER = USER_NUMBER #!<The user defined identifier for the basis. The user number must be unique.
		self.REGION = REGION
		self.QUADRATURE = []
		self.NUMBER_OF_XIC = 0
		self.NUMBER_OF_NODES_XIC = []
		self.NUMBER_OF_NODES = 0
		self.NUMBER_OF_PARTIAL_DERIVATIVES = 0
		self.NUMBER_OF_ELEMENT_PARAMETERS = 0

class Bases():
	def __init__(self,REGION):
		self.IDENTIFIER = "Basis"
		self.REGION = REGION
		self.NUMBER_OF_BASES = 0
		self.GLOBAL_TO_USER_MAP = []
		self.BASES = []

	def BasesCreateStart(self,USER_NUMBER):
		self.NUMBER_OF_BASES = self.NUMBER_OF_BASES + 1
		GLOBAL_NUMBER = self.NUMBER_OF_BASES
		self.GLOBAL_TO_USER_MAP.append(USER_NUMBER)
		self.BASES.append(Basis(USER_NUMBER,self.REGION))
		return GLOBAL_NUMBER

	def BasisGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def BasisGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.BasisGlobalNumberGet(USER_NUMBER)
		return self.BASES[GLOBAL_NUMBER]

	def BasisRegionGet(self,USER_NUMBER):
		return self.BASIS.REGION

	def BasesNumberOfGlobalBasesGet(self,):
		return self.NUMBER_OF_BASES

	def BasisTypeSet(self,USER_NUMBER,TYPE):
		BASIS = self.BasisGlobalGet(USER_NUMBER)
		BASIS.TYPE = TYPE

	def BasisNumberOfXiCoordinatesSet(self,USER_NUMBER,NUMBER_OF_XIC):
		BASIS = self.BasisGlobalGet(USER_NUMBER)
		BASIS.NUMBER_OF_XIC = NUMBER_OF_XIC

	def BasisQuadratureNumberOfGaussXiSet(self,USER_NUMBER,NUMBER_OF_GAUSS_XI):
		BASIS = self.BasisGlobalGet(USER_NUMBER)
		BASIS.QUADRATURE = Quadrature(NUMBER_OF_GAUSS_XI)

	def BasesCreateFinish(self,USER_NUMBER):
		BASIS = self.BasisGlobalGet(USER_NUMBER)
		if BASIS.TYPE == "2DLinearLagrange":
			BASIS.NUMBER_OF_NODES = 4 #!<The number of local nodes in the basis.
			BASIS.NUMBER_OF_PARTIAL_DERIVATIVES = 1 #!<The number of paratial derivatives for the basis. Old CMISS name NUT(nbf)
		elif BASIS.TYPE == "3DLinearLagrange":
			BASIS.NUMBER_OF_NODES = 8 #!<The number of local nodes in the basis.
			BASIS.NUMBER_OF_PARTIAL_DERIVATIVES = 1 #!<The number of paratial derivatives for the basis. Old CMISS name NUT(nbf)
		elif BASIS.TYPE == "2DCubicHermite":
			BASIS.NUMBER_OF_NODES = 4 #!<The number of local nodes in the basis.
			BASIS.NUMBER_OF_PARTIAL_DERIVATIVES = 4 #!<The number of paratial derivatives for the basis. Old CMISS name NUT(nbf)
		elif BASIS.TYPE == "3DCubicHermite":
			BASIS.NUMBER_OF_NODES = 8 #!<The number of local nodes in the basis.
			BASIS.NUMBER_OF_PARTIAL_DERIVATIVES = 8 #!<The number of paratial derivatives for the basis. Old CMISS name NUT(nbf)
		else:
			raise ValueError('Basis TYPE of \'%s\' is invalid.' %TYPE)
		BASIS.NUMBER_OF_NODES_XIC = [2]*(BASIS.NUMBER_OF_XIC) # !<NUMBER_OF_XIC(ni). The number of local nodes in the ni'th direction in the basis.
		#!Quadrature
		BASIS.NUMBER_OF_ELEMENT_PARAMETERS = BASIS.NUMBER_OF_NODES*BASIS.NUMBER_OF_XIC #!<The number of element parameters in the basis.
		#Calculate Quadrature Parameters 
		if BASIS.QUADRATURE != []:
			fem_quadratureRoutines.GAUSS1(BASIS)

	def BasisQuadratureNumberOfGaussPositionsGet(self,USER_NUMBER):
		BASIS = self.BasisGlobalGet(USER_NUMBER)
		return BASIS.QUADRATURE.NUMBER_OF_GAUSS

	def BasisQuadratureGaussPositionsGet(self,USER_NUMBER):
		BASIS = self.BasisGlobalGet(USER_NUMBER)
		return BASIS.QUADRATURE.GAUSS_POSITIONS

	def BasisQuadratureGaussWeightsGet(self,USER_NUMBER):
		BASIS = self.BasisGlobalGet(USER_NUMBER)
		return BASIS.QUADRATURE.GAUSS_WEIGHTS

	def BasisEvaluateXi(self,USER_NUMBER,XI):
		BASIS = self.BasisGlobalGet(USER_NUMBER)
		if BASIS.TYPE == "2DLinearLagrange":
			phi = [0.0]*4
			phi[0] = ( 1- XI[0] ) * ( 1- XI[1] )
			phi[1] = XI[0] * ( 1- XI[1] )
			phi[2] = ( 1- XI[0] ) * XI[1]
			phi[3] = XI[0] * XI[1]
		elif BASIS.TYPE == "3DLinearLagrange":
			phi = [0.0]*8
			phi[0] = ( 1- XI[0] ) * ( 1- XI[1] ) * ( 1- XI[2] )
			phi[1] = XI[0] * ( 1- XI[1] ) * ( 1- XI[2] )
			phi[2] = ( 1- XI[0] ) * XI[1] * ( 1- XI[2] )
			phi[3] = XI[0] * XI[1] * ( 1- XI[2] )
			phi[4] = ( 1- XI[0] ) * ( 1- XI[1] ) * XI[2]
			phi[5] = XI[0] * ( 1- XI[1] ) * XI[2]
			phi[6] = ( 1- XI[0] ) * XI[1] * XI[2]
			phi[7] = XI[0] * XI[1] * XI[2]
		return phi

#============================================================================

class FieldInterpolatedPointMetrics():
	""" !> Contains the interpolated point coordinate metrics. Old CMISS name GL,GU,RG.
	"""
	def __init__(self,):
		self.IDENTIFIER = "FieldInterpolatedPointMetrics"
		self.INTERPOLATED_POINT = []
		self.NUMBER_OF_X_DIMENSIONS = 0
		self.NUMBER_OF_XI_DIMENSIONS = 0
		self.GL = [] #!<GL(mi,ni). Covariant metric tensor. Old CMISS name GL.
		self.GU = [] #!<GU(mi,ni). Contravariant metric tensor. Old CMISS name GU.
		self.DX_DXI = [] #!<DX_DXI(nj,ni). Rate of change of the X coordinate system wrt the x coordinate system.
		self.DXI_DX = [] #!<DXI_DX(ni,nj). Rate of change of the Xi coordinate system wrt the x coordinate system. 
		self.JACOBIAN = [] #!<The Jacobian of the Xi to X coordinate system transformation. Old CMISS name RG.

class FieldInterpolatedPoint():
	""" !>Contains the interpolated value (and the derivatives wrt xi) of a field at a point. Old CMISS name XG.
	"""
	def __init__(self,):
		self.IDENTIFIER = "FieldInterpolatedPointMetrics"
		self.INTERPOLATION_PARAMETERS = [] #!<A pointer to the interpolation parameters of the field that is to be interpolated.
		self.MAX_PARTIAL_DERIVATIVE_INDEX #!<The maximum number of partial derivatives that have been allocated for the values component.
		self.PARTIAL_DERIVATIVE_TYPE #!<The type of the partial derivatives that have been interpolated. PARTIAL_DERIVATIVE_TYPE can be either NO_PART_DERIV, FIRST_PART_DERIV or SECOND_PART_DERIV depending on whether just the field value, the field value and all first derivatives (including cross derivatives) or the first value and all first and second derivatives have been interpolated.
		self.VALUES = [] #!<VALUES(component_idx,nu). The interpolated field components and their partial derivatives.

class FieldInterpolationParameters():
	""" !>Contains the parameters required to interpolate a field variable within an element. Old CMISS name XE
	"""
	def __init__(self,):
		self.FIELD = [] #!<A pointer to the field to be interpolated.
		self.FIELD_VARIABLE = [] #!<A pointer to the field VARIABLE to be interpolated.
		self.NUMBER_OF_XI = 0 #!<The number of xi directions for the interpolation parameters.
		self.BASES = [] #!<BASES(component_idx). An array to hold a pointer to the basis (if any) used for interpolating the component_idx'th component of the field variable.
		self.NUMBER_OF_PARAMETERS = [] #!<NUMBER_OF_PARAMETERS(component_idx). The number of interpolation parameters used for interpolating the component_idx'th component of the field variable.
		self.PARAMETERS = [] #!<PARAMETERS(ns,component_idx). The interpolation parameters used for interpolating the component_idx'th component of the field variable.
		self.SCALE_FACTORS = [] #!<SCALE_FACTORS(ns,component_idx). The scale factors used for scaling then component_idx'th component of the field variable. 

class FieldVersion():
	def __init__(self,USER_NUMBER,REGION):
		self.IDENTIFIER = "FieldVersion"
		self.USER_NUMBER = USER_NUMBER #!<The user number of the field version. The user number must be unique.
		self.FIELD_DERIVATIVE_LABEL = ""
		self.REGION = REGION
		self.VALUE = 0

class FieldDerivative():
	def __init__(self,USER_NUMBER,REGION):
		self.IDENTIFIER = "FieldDerivative"
		self.USER_NUMBER = USER_NUMBER #!<The user number of the field derivative. The user number must be unique.
		self.FIELD_DERIVATIVE_LABEL = ""
		self.REGION = REGION
		self.NUMBER_OF_VERSIONS = 0
		self.GLOBAL_TO_USER_MAP = []
		self.VERSIONS = []

	def FieldVersionGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def FieldVersionGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.FieldVersionGlobalNumberGet(USER_NUMBER)
		return self.VERSIONS[GLOBAL_NUMBER]

class FieldNode():
	def __init__(self,USER_NUMBER,REGION):
		self.IDENTIFIER = "FieldNode"
		self.USER_NUMBER = USER_NUMBER #!<The user number of the field node. The user number must be unique.
		self.REGION = REGION
		self.NUMBER_OF_DERIVATIVES = 0
		self.GLOBAL_TO_USER_MAP = []
		self.DERIVATIVES = []
		
	def FieldDerivativeGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def FieldDerivativeGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.FieldDerivativeGlobalNumberGet(USER_NUMBER)
		return self.DERIVATIVES[GLOBAL_NUMBER]


class FieldComponent():
	def __init__(self,USER_NUMBER,REGION):
		self.IDENTIFIER = "FieldComponent"
		self.USER_NUMBER = USER_NUMBER #!<The user number of the field component. The user number must be unique.
		self.FIELD_COMPONENT_LABEL = ""
		self.REGION = REGION
		self.MESH_COMPONENT = []
		self.NUMBER_OF_NODES = 0
		self.GLOBAL_TO_USER_MAP = []
		self.NODES = []

	def FieldNodeGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def FieldNodeGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.FieldNodeGlobalNumberGet(USER_NUMBER)
		return self.NODES[GLOBAL_NUMBER]

class FieldVariable():
	def __init__(self,USER_NUMBER,REGION,FIELD):
		self.IDENTIFIER = "FieldVariable"
		self.USER_NUMBER = USER_NUMBER #!<The user number of the field variable. The user number must be unique.
		self.FIELD_VARIABLE_LABEL = ""
		self.FIELD = FIELD
		self.REGION = REGION
		self.NUMBER_OF_FIELD_COMPONENTS = 0
		self.GLOBAL_TO_USER_MAP = []
		self.COMPONENTS = []

	def FieldComponentGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def FieldComponentGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.FieldComponentGlobalNumberGet(USER_NUMBER)
		return self.COMPONENTS[GLOBAL_NUMBER]

class Field():
	def __init__(self,USER_NUMBER,REGION):
		self.USER_NUMBER = USER_NUMBER
		self.FIELD_LABEL = ""
		self.REGION = REGION
		self.NODES = REGION.NODES
		self.MESH = []
		self.NUMBER_OF_FIELD_VARIABLES = 0
		self.GLOBAL_TO_USER_MAP = []
		self.VARIABLES = []

	def FieldVariableGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def FieldVariableGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.FieldVariableGlobalNumberGet(USER_NUMBER)
		return self.VARIABLES[GLOBAL_NUMBER]

class Fields():
	def __init__(self,REGION):
		self.IDENTIFIER = "Field"
		self.REGION = REGION
		self.NUMBER_OF_FIELDS = 0
		self.GLOBAL_TO_USER_MAP = []
		self.FIELDS = []

	def FieldGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def FieldGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.FieldGlobalNumberGet(USER_NUMBER)
		return self.FIELDS[GLOBAL_NUMBER]

	def FieldCreateStart(self,USER_NUMBER):
		self.FieldsFieldAdd(USER_NUMBER)

	def FieldsFieldAdd(self,USER_NUMBER):
		REGION = self.REGION
		self.NUMBER_OF_FIELDS = self.NUMBER_OF_FIELDS + 1
		GLOBAL_NUMBER = self.NUMBER_OF_FIELDS
		self.GLOBAL_TO_USER_MAP.append(USER_NUMBER)
		self.FIELDS.append(Field(USER_NUMBER,REGION))
		return GLOBAL_NUMBER

	def FieldMeshSet(self,FIELD_USER_NUMBER,MESH_USER_NUMBER):
		REGION = self.REGION
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		MESH = REGION.MESHES.MeshGlobalGet(MESH_USER_NUMBER)
		FIELD.MESH = MESH

	def FieldNumberOfFieldVariablesSet(self,FIELD_USER_NUMBER,NUMBER_OF_FIELD_VARIABLES):
		REGION = self.REGION
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD.NUMBER_OF_FIELD_VARIABLES = NUMBER_OF_FIELD_VARIABLES
		for FIELD_VARIABLE_GLOBAL_NUMBER in range(FIELD.NUMBER_OF_FIELD_VARIABLES):
			FIELD_VARIABLE_USER_NUMBER = FIELD_VARIABLE_GLOBAL_NUMBER + 1
			FIELD.GLOBAL_TO_USER_MAP.append(FIELD_VARIABLE_USER_NUMBER)
			FIELD.VARIABLES.append(FieldVariable(FIELD_VARIABLE_USER_NUMBER,REGION,FIELD))

	def FieldNumberOfFieldComponentsSet(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,NUMBER_OF_FIELD_COMPONENTS):
		REGION = self.REGION
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		FIELD_VARIABLE.NUMBER_OF_FIELD_COMPONENTS = NUMBER_OF_FIELD_COMPONENTS
		for FIELD_COMPONENT_GLOBAL_NUMBER in range(FIELD_VARIABLE.NUMBER_OF_FIELD_COMPONENTS):
			FIELD_COMPONENT_USER_NUMBER = FIELD_COMPONENT_GLOBAL_NUMBER + 1
			FIELD_VARIABLE.GLOBAL_TO_USER_MAP.append(FIELD_COMPONENT_USER_NUMBER)
			FIELD_VARIABLE.COMPONENTS.append(FieldComponent(FIELD_COMPONENT_USER_NUMBER,REGION))

	def FieldComponentMeshComponentSet(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,FIELD_COMPONENT_USER_NUMBER,MESH_COMPONENT_USER_NUMBER):
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		MESH = FIELD.MESH
		MESH_COMPONENT = MESH.MeshTopologyGlobalGet(MESH_COMPONENT_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(FIELD_COMPONENT_USER_NUMBER)
		FIELD_COMPONENT.MESH_COMPONENT = MESH_COMPONENT

	def FieldNumberOfFieldComponentsGet(self,USER_NUMBER):
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		return FIELD.NUMBER_OF_FIELD_COMPONENTS

	def FieldTypeSet(self,USER_NUMBER,TYPE):
		self.FieldLabelSet(USER_NUMBER,TYPE)

	def FieldLabelSet(self,FIELD_USER_NUMBER,LABEL):
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_LABEL = LABEL

	def FieldComponentLabelSet(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,FIELD_COMPONENT_USER_NUMBER,LABEL):
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(FIELD_COMPONENT_USER_NUMBER)
		FIELD_COMPONENT.LABEL = LABEL

	def FieldCreateFinish(self,FIELD_USER_NUMBER):
		REGION = self.REGION
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		for FIELD_VARIABLE_GLOBAL_NUMBER in range(FIELD.NUMBER_OF_FIELD_VARIABLES):
			FIELD_VARIABLE = FIELD.VARIABLES[FIELD_VARIABLE_GLOBAL_NUMBER]
			for FIELD_COMPONENT_GLOBAL_NUMBER in range(FIELD_VARIABLE.NUMBER_OF_FIELD_COMPONENTS):
				FIELD_COMPONENT = FIELD_VARIABLE.COMPONENTS[FIELD_COMPONENT_GLOBAL_NUMBER]
				MESH_COMPONENT = FIELD_COMPONENT.MESH_COMPONENT
				MESH_NODES = MESH_COMPONENT.NODES
				for MESH_NODE_GLOBAL_NUMBER in range(MESH_NODES.NUMBER_OF_NODES):
					MESH_NODE = MESH_NODES.NODES[MESH_NODE_GLOBAL_NUMBER]
					FIELD_NODE_USER_NUMBER = MESH_NODE.USER_NUMBER
					FIELD_COMPONENT.GLOBAL_TO_USER_MAP.append(FIELD_NODE_USER_NUMBER)
					FIELD_COMPONENT.NUMBER_OF_NODES = FIELD_COMPONENT.NUMBER_OF_NODES + 1
					FIELD_COMPONENT.NODES.append(FieldNode(FIELD_NODE_USER_NUMBER,REGION))
					FIELD_NODE = FIELD_COMPONENT.NODES[MESH_NODE_GLOBAL_NUMBER]
					for MESH_NODE_DERIVATIVE_GLOBAL_NUMBER in range(MESH_NODE.NUMBER_OF_DERIVATIVES):
						MESH_NODE_DERIVATIVE = MESH_NODE.DERIVATIVES[MESH_NODE_DERIVATIVE_GLOBAL_NUMBER]
						FIELD_NODE_DERIVATIVE_USER_NUMBER = MESH_NODE_DERIVATIVE.USER_NUMBER
						FIELD_NODE.NUMBER_OF_DERIVATIVES = FIELD_NODE.NUMBER_OF_DERIVATIVES + 1
						FIELD_NODE.GLOBAL_TO_USER_MAP.append(FIELD_NODE_DERIVATIVE_USER_NUMBER)
						FIELD_NODE.DERIVATIVES.append(FieldDerivative(FIELD_NODE_DERIVATIVE_USER_NUMBER,REGION))
						FIELD_NODE_DERIVATIVE = FIELD_NODE.DERIVATIVES[MESH_NODE_DERIVATIVE_GLOBAL_NUMBER]
						for MESH_NODE_DERIVATIVE_VERSION_GLOBAL_NUMBER in range(MESH_NODE_DERIVATIVE.NUMBER_OF_VERSIONS):
							MESH_NODE_DERIVATIVE_VERSION = MESH_NODE_DERIVATIVE.VERSIONS[MESH_NODE_DERIVATIVE_VERSION_GLOBAL_NUMBER]
							FIELD_NODE_DERIVATIVE_VERSION_USER_NUMBER = MESH_NODE_DERIVATIVE_VERSION.USER_NUMBER
							FIELD_NODE_DERIVATIVE.NUMBER_OF_VERSIONS = FIELD_NODE_DERIVATIVE.NUMBER_OF_VERSIONS + 1
							FIELD_NODE_DERIVATIVE.GLOBAL_TO_USER_MAP.append(FIELD_NODE_DERIVATIVE_VERSION_USER_NUMBER)
							FIELD_NODE_DERIVATIVE.VERSIONS.append(FieldVersion(FIELD_NODE_DERIVATIVE_VERSION_USER_NUMBER,REGION))

	def FieldParameterSetUpdateNode(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,FIELD_VERSION_USER_NUMBER,FIELD_DERIVATIVE_USER_NUMBER,FIELD_NODE_USER_NUMBER,FIELD_COMPONENT_USER_NUMBER,VALUE):
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(FIELD_COMPONENT_USER_NUMBER)
		FIELD_NODE = FIELD_COMPONENT.FieldNodeGlobalGet(FIELD_NODE_USER_NUMBER)
		FIELD_DERIVATIVE = FIELD_NODE.FieldDerivativeGlobalGet(FIELD_DERIVATIVE_USER_NUMBER)
		FIELD_VERSION = FIELD_DERIVATIVE.FieldVersionGlobalGet(FIELD_VERSION_USER_NUMBER)
		FIELD_VERSION.VALUE = VALUE

	def FieldParameterNodeCheckExists(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,FIELD_NODE_USER_NUMBER,FIELD_COMPONENT_USER_NUMBER):
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(FIELD_COMPONENT_USER_NUMBER)
		EXISTS = True
		try:
			FIELD_NODE = FIELD_COMPONENT.FieldNodeGlobalGet(FIELD_NODE_USER_NUMBER)
		except ValueError:
			EXISTS = False
		return EXISTS

	def FieldParameterSetNodeValueGet(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,FIELD_VERSION_USER_NUMBER,FIELD_DERIVATIVE_USER_NUMBER,FIELD_NODE_USER_NUMBER,FIELD_COMPONENT_USER_NUMBER):
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(FIELD_COMPONENT_USER_NUMBER)
		FIELD_NODE = FIELD_COMPONENT.FieldNodeGlobalGet(FIELD_NODE_USER_NUMBER)
		FIELD_DERIVATIVE = FIELD_NODE.FieldDerivativeGlobalGet(FIELD_DERIVATIVE_USER_NUMBER)
		FIELD_VERSION = FIELD_DERIVATIVE.FieldVersionGlobalGet(FIELD_VERSION_USER_NUMBER)
		return FIELD_VERSION.VALUE

	def FieldParameterSetNodeValuesGet(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,FIELD_NODE_USER_NUMBER,FIELD_COMPONENT_USER_NUMBER):
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(FIELD_COMPONENT_USER_NUMBER)
		FIELD_NODE = FIELD_COMPONENT.FieldNodeGlobalGet(FIELD_NODE_USER_NUMBER)
		VALUES = []
		for derivative_idx in range(FIELD_NODE.NUMBER_OF_DERIVATIVES):
			FIELD_DERIVATIVE = FIELD_NODE.DERIVATIVES[derivative_idx]
			for version_idx in range(FIELD_DERIVATIVE.NUMBER_OF_VERSIONS):
				FIELD_VERSION = FIELD_DERIVATIVE.VERSIONS[version_idx]
				VALUES.append(FIELD_VERSION.VALUE)
		return VALUES

	def FieldParameterElementValuesGet(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,ELEMENT_USER_NUMBER,FIELD_COMPONENT_USER_NUMBER):
		REGION = self.REGION
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(FIELD_COMPONENT_USER_NUMBER)
		MESH = FIELD.MESH
		MESH_USER_NUMBER=MESH.USER_NUMBER
		MESH_COMPONENT = FIELD_COMPONENT.MESH_COMPONENT
		MESH_COMPONENT_USER_NUMBER=MESH_COMPONENT.USER_NUMBER
		MESH_NODES = MESH_COMPONENT.NODES
		MESH_ELEMENTS = MESH_COMPONENT.ELEMENTS
		MESH_ELEMENT = MESH_ELEMENTS.MeshElementGlobalGet(ELEMENT_USER_NUMBER)
		BASIS = MESH_ELEMENT.BASIS
		MESH_ELEMENT_USER_NODES = REGION.MESHES.MeshElementsNodesGet(MESH_USER_NUMBER,MESH_COMPONENT_USER_NUMBER,ELEMENT_USER_NUMBER)
		ELEMENT_VALUES = fem_miscellaneous_routines.initialize2DList(float(0.0),BASIS.NUMBER_OF_NODES,BASIS.NUMBER_OF_PARTIAL_DERIVATIVES)
		for node_idx in range(BASIS.NUMBER_OF_NODES):
			for derivative_idx in range(BASIS.NUMBER_OF_PARTIAL_DERIVATIVES):
				ELEMENT_NODE_VERSION = REGION.MESHES.MeshElementsNodeVersionGet(MESH_USER_NUMBER,MESH_COMPONENT_USER_NUMBER,ELEMENT_USER_NUMBER,node_idx+1,derivative_idx+1)
				ELEMENT_VALUES[node_idx][derivative_idx] = self.FieldParameterSetNodeValueGet(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,ELEMENT_NODE_VERSION,derivative_idx+1,MESH_ELEMENT_USER_NODES[node_idx],FIELD_COMPONENT_USER_NUMBER)
		return ELEMENT_VALUES

	def FieldInterpolationParametersElementGet(self,FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,ELEMENT_USER_NUMBER):
		REGION = self.REGION
		FIELD = self.FieldGlobalGet(FIELD_USER_NUMBER)
		FIELD_VARIABLE = FIELD.FieldVariableGlobalGet(FIELD_VARIABLE_USER_NUMBER)
		MESH = FIELD.MESH
		MESH_USER_NUMBER=MESH.USER_NUMBER
		for component_idx in range(1,FIELD_VARIABLE.NUMBER_OF_FIELD_COMPONENTS+1):
			FIELD_COMPONENT = FIELD_VARIABLE.FieldComponentGlobalGet(component_idx)
			MESH_COMPONENT = FIELD_COMPONENT.MESH_COMPONENT
			MESH_COMPONENT_USER_NUMBER=MESH_COMPONENT.USER_NUMBER
			MESH_NODES = MESH_COMPONENT.NODES
			MESH_ELEMENTS = MESH_COMPONENT.ELEMENTS
			MESH_ELEMENT = MESH_ELEMENTS.MeshElementGlobalGet(ELEMENT_USER_NUMBER)
			BASIS = MESH_ELEMENT.BASIS
			MESH_ELEMENT_USER_NODES = REGION.MESHES.MeshElementsNodesGet(MESH_USER_NUMBER,MESH_COMPONENT_USER_NUMBER,ELEMENT_USER_NUMBER)
			ELEMENT_VALUES = fem_miscellaneous_routines.initialize2DList(float(0.0),BASIS.NUMBER_OF_NODES,BASIS.NUMBER_OF_PARTIAL_DERIVATIVES)
			for node_idx in range(BASIS.NUMBER_OF_NODES):
				for derivative_idx in range(BASIS.NUMBER_OF_PARTIAL_DERIVATIVES):
					ELEMENT_NODE_VERSION = REGION.MESHES.MeshElementsNodeVersionGet(MESH_USER_NUMBER,MESH_COMPONENT_USER_NUMBER,ELEMENT_USER_NUMBER,node_idx+1,derivative_idx+1)
					ELEMENT_VALUES[node_idx][derivative_idx] = self.FieldParameterSetNodeValueGet(FIELD_USER_NUMBER,FIELD_VARIABLE_USER_NUMBER,ELEMENT_NODE_VERSION,derivative_idx+1,MESH_ELEMENT_USER_NODES[node_idx],FIELD_COMPONENT_USER_NUMBER)
			return ELEMENT_VALUES




#============================================================================

class Node():
	
	def __init__(self,USER_NUMBER,REGION):
		self.USER_NUMBER = USER_NUMBER
		self.REGION = REGION

class Nodes():
	def __init__(self,REGION):
		self.IDENTIFIER = "Node"
		self.REGION = REGION
		self.NUMBER_OF_NODES = 0
		self.GLOBAL_TO_USER_MAP = []
		self.NODES = []

	def NodesNodeAdd(self,USER_NUMBER):
		self.NUMBER_OF_NODES = self.NUMBER_OF_NODES + 1
		GLOBAL_NUMBER = self.NUMBER_OF_NODES
		self.GLOBAL_TO_USER_MAP.append(USER_NUMBER)
		self.NODES.append(Node(USER_NUMBER,self.REGION))
		return GLOBAL_NUMBER

	def NodeGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def NodeLocalNumberGet(self,GLOBAL_NUMBER):
		USER_NUMBER = self.GLOBAL_TO_USER_MAP[GLOBAL_NUMBER] #invese map
		return USER_NUMBER

	def NodesCreateStart(self,TOTAL_NUMBER_OF_NODES):
		self.NUMBER_OF_NODES = TOTAL_NUMBER_OF_NODES
		for USER_NUMBER in range(TOTAL_NUMBER_OF_NODES):
			self.NodesNodeAdd(USER_NUMBER)

	def NodesNumberOfNodesGet(self,):
		return self.NUMBER_OF_NODES

	def NodesCreateFinish(self):
		pass

#	def NodesLocalNodeGet(self,):
#		return self.GLOBAL_TO_USER_MAP[GLOBAL_NUMBER-1]

#============================================================================

class Mesh():
	""" !> Contains all information about a mesh .
	"""

	def __init__( self,USER_NUMBER,REGION):
		self.USER_NUMBER = USER_NUMBER #!<The user number of the mesh. The user number must be unique.
		self.REGION = REGION
		self.NUMBER_OF_COMPONENTS = 0 #!<The number of mesh components in this mesh.
		self.NUMBER_OF_ELEMENTS = 0 #!<The number of elements in the mesh.
		self.NUMBER_OF_DIMENSIONS = 0 #!<The number of dimensions (Xi directions) for this mesh.
		self.IDENTIFIER = "MeshTopology"
		self.TOPOLOGY = []
		self.GLOBAL_TO_USER_MAP = []
		self.FINISHED = False

	def MeshTopologyGlobalComponentNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def MeshTopologyGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.MeshTopologyGlobalComponentNumberGet(USER_NUMBER)
		return self.TOPOLOGY[GLOBAL_NUMBER]

class Meshes():
	def __init__(self,REGION):
		self.IDENTIFIER = "Mesh"
		self.REGION = REGION
		self.NUMBER_OF_MESHES = 0
		self.GLOBAL_TO_USER_MAP = []
		self.MESHES = []

	def MeshGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def MeshGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.MeshGlobalNumberGet(USER_NUMBER)
		return self.MESHES[GLOBAL_NUMBER]

	def MeshesCreateStart(self,USER_NUMBER):
		self.MeshesMeshAdd(USER_NUMBER)

	def MeshesMeshAdd(self,USER_NUMBER):
		self.NUMBER_OF_MESHES = self.NUMBER_OF_MESHES + 1
		GLOBAL_NUMBER = self.NUMBER_OF_MESHES
		self.GLOBAL_TO_USER_MAP.append(USER_NUMBER)
		self.MESHES.append(Mesh(USER_NUMBER,self.REGION))
		return GLOBAL_NUMBER

	def MeshesNumberOfGlobalMeshesGet(self,):
		return self.NUMBER_OF_MESHES

	def MeshNumberOfDimensionsSet(self,USER_NUMBER,NUMBER_OF_DIMENSIONS):
		MESH = self.MeshGlobalGet(USER_NUMBER)
		MESH.NUMBER_OF_COMPONENTS = NUMBER_OF_DIMENSIONS

	def MeshNumberOfComponentsSet(self,USER_NUMBER,NUMBER_OF_COMPONENTS):
		REGION = self.REGION
		MESH = self.MeshGlobalGet(USER_NUMBER)
		MESH.NUMBER_OF_COMPONENTS = NUMBER_OF_COMPONENTS
		for GLOBAL_MESH_COMPONENT_NUMBER in range(MESH.NUMBER_OF_COMPONENTS):
			USER_MESH_COMPONENT_NUMBER = GLOBAL_MESH_COMPONENT_NUMBER + 1
			MESH.TOPOLOGY.append(MeshTopology(USER_MESH_COMPONENT_NUMBER,REGION,MESH))
			MESH.GLOBAL_TO_USER_MAP.append(USER_MESH_COMPONENT_NUMBER)

	#def MeshNumberOfElementsSet(self,USER_NUMBER,NUMBER_OF_ELEMENTS):
	#	MESH = self.MeshGlobalGet(USER_NUMBER)
	#	MESH.NUMBER_OF_ELEMENTS = NUMBER_OF_ELEMENTS

#	def MeshNumberOfElementsGet(self,USER_NUMBER):
#		MESH = self.MeshGlobalGet(USER_NUMBER)
#		return MESH.NUMBER_OF_ELEMENTS

	def MeshElementsCreateStart(self,MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,BASIS_USER_NUMBER):
		self.MeshElementsBasisSet(MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,BASIS_USER_NUMBER)

	def MeshElementsBasisSet(self,MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,BASIS_USER_NUMBER):
		REGION = self.REGION
		MESH = self.MeshGlobalGet(MESH_USER_NUMBER)
		GLOBAL_MESH_COMPONENT_NUMBER = MESH.MeshTopologyGlobalComponentNumberGet(MESH_COMPONENT_NUMBER)
		MESH_COMPONENT = MESH.TOPOLOGY[GLOBAL_MESH_COMPONENT_NUMBER]
		GLOBAL_BASIS_NUMBER = self.REGION.BASES.BasisGlobalNumberGet(BASIS_USER_NUMBER)
		BASIS = self.REGION.BASES.BasisGlobalGet(BASIS_USER_NUMBER)
		MESH_COMPONENT.ELEMENTS.BASIS = BASIS

	def MeshElementsNodesSet(self,MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,ELEMENT_USER_NUMBER,ELEMENT_NODES):
		REGION = self.REGION
		MESH = self.MeshGlobalGet(MESH_USER_NUMBER)
		MESH.NUMBER_OF_ELEMENTS = MESH.NUMBER_OF_ELEMENTS + 1
		GLOBAL_MESH_COMPONENT_NUMBER = MESH.MeshTopologyGlobalComponentNumberGet(MESH_COMPONENT_NUMBER)
		MESH_COMPONENT = MESH.TOPOLOGY[GLOBAL_MESH_COMPONENT_NUMBER]
		MESH_COMPONENT.ELEMENTS.NUMBER_OF_ELEMENTS = MESH_COMPONENT.ELEMENTS.NUMBER_OF_ELEMENTS + 1
		MESH_COMPONENT.ELEMENTS.GLOBAL_TO_USER_MAP.append(ELEMENT_USER_NUMBER) #TODO:: check to see if this element user number has been used elsewhere in the Region
		MESH_COMPONENT.ELEMENTS.ELEMENTS.append(MeshElement(ELEMENT_USER_NUMBER,REGION))
		ELEMENT = MESH_COMPONENT.ELEMENTS.ELEMENTS[-1]
		#Set the basis for the newly created element
		ELEMENT.BASIS = MESH_COMPONENT.ELEMENTS.BASIS
		ELEMENT.USER_ELEMENT_NODES = ELEMENT_NODES
		#Initialize element node versions
		BASIS = ELEMENT.BASIS
		ELEMENT.USER_ELEMENT_NODE_VERSIONS = fem_miscellaneous_routines.initialize2DList(1,BASIS.NUMBER_OF_NODES,BASIS.NUMBER_OF_PARTIAL_DERIVATIVES)

#	def MeshElementNumberUpdate(self,MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,ORIGINAL_ELEMENT_USER_NUMBER,UPDATED_ELEMENT_USER_NUMBER):
#		MESH = self.MeshGlobalGet(MESH_USER_NUMBER)
#		GLOBAL_MESH_COMPONENT_NUMBER = MESH.MeshTopologyGlobalComponentNumberGet(MESH_COMPONENT_NUMBER)
#		MESH_COMPONENT = MESH.TOPOLOGY[GLOBAL_MESH_COMPONENT_NUMBER]
#		ELEMENTS = MESH_COMPONENT.ELEMENTS
#		ELEMENTS.GLOBAL_TO_USER_MAP[ORIGINAL_ELEMENT_USER_NUMBER-1] = UPDATED_ELEMENT_USER_NUMBER
#		ELEMENT = ELEMENTS.ELEMENTS[ORIGINAL_ELEMENT_USER_NUMBER-1]
#		ELEMENT.USER_NUMBER = UPDATED_ELEMENT_USER_NUMBER

	def MeshElementsNodesGet(self,MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,ELEMENT_USER_NUMBER):
		MESH = self.MeshGlobalGet(MESH_USER_NUMBER)
		GLOBAL_MESH_COMPONENT_NUMBER = MESH.MeshTopologyGlobalComponentNumberGet(MESH_COMPONENT_NUMBER)
		MESH_COMPONENT = MESH.TOPOLOGY[GLOBAL_MESH_COMPONENT_NUMBER]
		GLOBAL_ELEMENT_NUMBER = MESH_COMPONENT.ELEMENTS.MeshElementGlobalNumberGet(ELEMENT_USER_NUMBER)
		ELEMENT = MESH_COMPONENT.ELEMENTS.ELEMENTS[GLOBAL_ELEMENT_NUMBER]
		return ELEMENT.USER_ELEMENT_NODES

	def MeshElementsNodeVersionSet(self,MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,ELEMENT_USER_NUMBER,ELEMENT_NODE_NUMBER,DERIVATIVE_NUMBER,VERSION_NUMBER):
		MESH = self.MeshGlobalGet(MESH_USER_NUMBER)
		GLOBAL_MESH_COMPONENT_NUMBER = MESH.MeshTopologyGlobalComponentNumberGet(MESH_COMPONENT_NUMBER)
		MESH_COMPONENT = MESH.TOPOLOGY[GLOBAL_MESH_COMPONENT_NUMBER]
		GLOBAL_ELEMENT_NUMBER = MESH_COMPONENT.ELEMENTS.MeshElementGlobalNumberGet(ELEMENT_USER_NUMBER)
		ELEMENT = MESH_COMPONENT.ELEMENTS.ELEMENTS[GLOBAL_ELEMENT_NUMBER]
		#print ELEMENT.USER_ELEMENT_NODE_VERSIONS
		#print DERIVATIVE_NUMBER
		#print ELEMENT_NODE_NUMBER
		ELEMENT.USER_ELEMENT_NODE_VERSIONS[ELEMENT_NODE_NUMBER-1][DERIVATIVE_NUMBER-1] = VERSION_NUMBER

	def MeshElementsNodeVersionGet(self,MESH_USER_NUMBER,MESH_COMPONENT_NUMBER,ELEMENT_USER_NUMBER,ELEMENT_NODE_NUMBER,DERIVATIVE_NUMBER):
		MESH = self.MeshGlobalGet(MESH_USER_NUMBER)
		GLOBAL_MESH_COMPONENT_NUMBER = MESH.MeshTopologyGlobalComponentNumberGet(MESH_COMPONENT_NUMBER)
		MESH_COMPONENT = MESH.TOPOLOGY[GLOBAL_MESH_COMPONENT_NUMBER]
		GLOBAL_ELEMENT_NUMBER = MESH_COMPONENT.ELEMENTS.MeshElementGlobalNumberGet(ELEMENT_USER_NUMBER)
		ELEMENT = MESH_COMPONENT.ELEMENTS.ELEMENTS[GLOBAL_ELEMENT_NUMBER]
		return ELEMENT.USER_ELEMENT_NODE_VERSIONS[ELEMENT_NODE_NUMBER-1][DERIVATIVE_NUMBER-1]

	def MeshElementsListGet(self,MESH_USER_NUMBER,MESH_COMPONENT_NUMBER):
		MESH = self.MeshGlobalGet(MESH_USER_NUMBER)
		GLOBAL_MESH_COMPONENT_NUMBER = MESH.MeshTopologyGlobalComponentNumberGet(MESH_COMPONENT_NUMBER)
		MESH_COMPONENT = MESH.TOPOLOGY[GLOBAL_MESH_COMPONENT_NUMBER]
		return MESH_COMPONENT.ELEMENTS.GLOBAL_TO_USER_MAP

	def MeshNodesListGet(self,MESH_USER_NUMBER,MESH_COMPONENT_NUMBER):
		MESH = self.MeshGlobalGet(MESH_USER_NUMBER)
		GLOBAL_MESH_COMPONENT_NUMBER = MESH.MeshTopologyGlobalComponentNumberGet(MESH_COMPONENT_NUMBER)
		MESH_COMPONENT = MESH.TOPOLOGY[GLOBAL_MESH_COMPONENT_NUMBER]
		return MESH_COMPONENT.NODES.GLOBAL_TO_USER_MAP

	def MeshTopologyCalculate(self,MESH_USER_NUMBER,MESH_COMPONENT_NUMBER):
		REGION = self.REGION
		MESH = self.MeshGlobalGet(MESH_USER_NUMBER)
		GLOBAL_MESH_COMPONENT_NUMBER = MESH.MeshTopologyGlobalComponentNumberGet(MESH_COMPONENT_NUMBER)
		MESH_COMPONENT = MESH.TOPOLOGY[GLOBAL_MESH_COMPONENT_NUMBER]
		#Loop through elements and list unique nodes in mesh
		NODES_LIST = []
		BASIS_MAX_NUMBER_OF_DERIVATIVES = 1
		for global_element_idx in range(MESH.NUMBER_OF_ELEMENTS):
			[NODES_LIST.append(values) for values in MESH_COMPONENT.ELEMENTS.ELEMENTS[global_element_idx].USER_ELEMENT_NODES]
			if MESH_COMPONENT.ELEMENTS.ELEMENTS[global_element_idx].BASIS.NUMBER_OF_PARTIAL_DERIVATIVES > BASIS_MAX_NUMBER_OF_DERIVATIVES:
				BASIS_MAX_NUMBER_OF_DERIVATIVES = MESH_COMPONENT.ELEMENTS.ELEMENTS[global_element_idx].BASIS.NUMBER_OF_PARTIAL_DERIVATIVES
		NODES = fem_miscellaneous_routines.removeDuplicates(NODES_LIST) 
		MESH_NODES = MESH_COMPONENT.NODES
		MESH_NODES.BASIS_MAX_NUMBER_OF_DERIVATIVES = BASIS_MAX_NUMBER_OF_DERIVATIVES
		#Loop through unique nodes in mesh and assign derivatives 
		for global_mesh_node_idx in range(len(NODES)):
			MESH_NODE_USER_NUMBER = NODES[global_mesh_node_idx]
			MESH_NODES.NUMBER_OF_NODES = MESH_NODES.NUMBER_OF_NODES + 1
			MESH_NODES.NODES.append(MeshNode(MESH_NODE_USER_NUMBER,REGION,MESH_COMPONENT))
			MESH_NODES.GLOBAL_TO_USER_MAP.append(MESH_NODE_USER_NUMBER)
			#Automatically allocate the number of derivatives of the basis to each node
			MESH_NODE = MESH_NODES.NODES[-1]
			for global_derivative_idx in range(BASIS_MAX_NUMBER_OF_DERIVATIVES):
				MESH_NODE_DERIVATIVE_USER_NUMBER = global_derivative_idx+1
				MESH_NODE.NUMBER_OF_DERIVATIVES = MESH_NODE.NUMBER_OF_DERIVATIVES + 1
				MESH_NODE.DERIVATIVES.append(MeshNodeDerivative(MESH_NODE_DERIVATIVE_USER_NUMBER,REGION,MESH_COMPONENT))
				MESH_NODE.GLOBAL_TO_USER_MAP.append(MESH_NODE_DERIVATIVE_USER_NUMBER)

		#Loop through and find and allocate number of versions for each node derivative
		for global_mesh_node_idx in range(MESH_NODES.NUMBER_OF_NODES):
			MESH_NODE = MESH_NODES.NODES[global_mesh_node_idx]
			MESH_NODE_USER_NUMBER = MESH_NODE.USER_NUMBER
			for global_element_idx in range(MESH.NUMBER_OF_ELEMENTS):
				ELEMENT = MESH_COMPONENT.ELEMENTS.ELEMENTS[global_element_idx]
				USER_ELEMENT_NODE_VERSIONS=ELEMENT.USER_ELEMENT_NODE_VERSIONS
				BASIS_NUMBER_OF_ELEMENT_NODES = len(ELEMENT.USER_ELEMENT_NODES)
				for element_node_idx in range(BASIS_NUMBER_OF_ELEMENT_NODES):
					ELEMENT_NODE_USER_NUMBER = ELEMENT.USER_ELEMENT_NODES[element_node_idx]
					if MESH_NODE_USER_NUMBER == ELEMENT_NODE_USER_NUMBER:
						for global_derivative_idx in range(BASIS_MAX_NUMBER_OF_DERIVATIVES):
							MESH_NODE_DERIVATIVE = MESH_NODE.DERIVATIVES[global_derivative_idx]
							MESH_NODE_DERIVATIVE_USER_NUMBER = MESH_NODE_DERIVATIVE.USER_NUMBER
							MESH_NODE_DERIVATIVE_VERSION_USER_NUMBER = USER_ELEMENT_NODE_VERSIONS[element_node_idx][global_derivative_idx]
							try:
								MESH_NODE_DERIVATIVE.GLOBAL_TO_USER_MAP.index(MESH_NODE_DERIVATIVE_VERSION_USER_NUMBER)
							except ValueError:
								MESH_NODE_DERIVATIVE.NUMBER_OF_VERSIONS = MESH_NODE_DERIVATIVE.NUMBER_OF_VERSIONS + 1
								MESH_NODE_DERIVATIVE.VERSIONS.append(MeshNodeDerivativeVersion(MESH_NODE_DERIVATIVE_VERSION_USER_NUMBER,REGION,MESH_COMPONENT))
								MESH_NODE_DERIVATIVE.GLOBAL_TO_USER_MAP.append(MESH_NODE_DERIVATIVE_VERSION_USER_NUMBER)
								if MESH_NODE_DERIVATIVE.NUMBER_OF_VERSIONS>1:
									MESH_NODE.MULTIPLE_VERSIONS = True
			if MESH_NODE.MULTIPLE_VERSIONS==True:
				MESH_NODES.MULTIPLE_VERSIONS = True
		MESH.FINISHED = True
					
	def MeshElementsCreateFinish(self,MESH_USER_NUMBER,MESH_COMPONENT_NUMBER):
		pass


	#Go through and find mesh nodes in the specified mesh's elements 
	def MeshesCreateFinish(self,MESH_USER_NUMBER):
		REGION = self.REGION
		MESH = self.MeshGlobalGet(MESH_USER_NUMBER)
		for mesh_component_global_idx in range(MESH.NUMBER_OF_COMPONENTS):
			MESH_COMPONENT_USER_NUMBER = MESH.TOPOLOGY[mesh_component_global_idx].USER_NUMBER
			self.MeshTopologyCalculate(MESH_USER_NUMBER,MESH_COMPONENT_USER_NUMBER)

 #============================================================================

class MeshTopology():
	""" !> Contains all information about a mesh topolgy.
	"""

	def __init__( self,USER_NUMBER,REGION,MESH):
		self.USER_NUMBER = USER_NUMBER #!<The user number of the mesh topology. The user number must be unique.
		self.REGION = REGION
		self.MESH = MESH
		self.ELEMENTS = MeshElements(REGION,MESH,self)
		self.NODES = MeshNodes(REGION,MESH,self)

class MeshElement():
	def __init__(self,USER_NUMBER,REGION):
		self.USER_NUMBER = USER_NUMBER #!<The user number of a mesh element. The user number must be unique.
		self.REGION = REGION
		self.BASIS = []
		self.USER_ELEMENT_NODES = []
		self.USER_ELEMENT_NODE_VERSIONS = []

class MeshElements():
	def __init__(self,REGION,MESH,TOPOLOGY):
		self.IDENTIFIER = "MeshElement"
		self.REGION = REGION
		self.MESH = MESH
		self.BASIS = []
		self.TOPOLOGY = TOPOLOGY
		self.NUMBER_OF_ELEMENTS = 0
		self.GLOBAL_TO_USER_MAP = []
		self.ELEMENTS = []

	def MeshElementGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def MeshElementGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.MeshElementGlobalNumberGet(USER_NUMBER)
		return self.ELEMENTS[GLOBAL_NUMBER]

class MeshNodeDerivativeVersion():
	def __init__(self,USER_NUMBER,REGION,TOPOLOGY):
		self.USER_NUMBER = USER_NUMBER #!<The user number of a mesh node. The user number must be unique.
		self.REGION = REGION
		self.TOPOLOGY = TOPOLOGY

class MeshNodeDerivative():
	def __init__(self,USER_NUMBER,REGION,TOPOLOGY):
		self.USER_NUMBER = USER_NUMBER #!<The user number of a mesh node. The user number must be unique.
		self.REGION = REGION
		self.TOPOLOGY = TOPOLOGY
		self.NUMBER_OF_VERSIONS = 0
		self.GLOBAL_TO_USER_MAP = []
		self.VERSIONS = []

class MeshNode():
	def __init__(self,USER_NUMBER,REGION,TOPOLOGY):
		self.USER_NUMBER = USER_NUMBER #!<The user number of a mesh node. The user number must be unique.
		self.REGION = REGION
		self.TOPOLOGY = TOPOLOGY
		self.NUMBER_OF_DERIVATIVES = 0
		self.GLOBAL_TO_USER_MAP = []
		self.DERIVATIVES = []
		self.MULTIPLE_VERSIONS = False

class MeshNodes():
	def __init__(self,REGION,MESH,TOPOLOGY):
		self.IDENTIFIER = "MeshNode"
		self.REGION = REGION
		self.MESH = MESH
		self.TOPOLOGY = TOPOLOGY
		self.NUMBER_OF_NODES = 0
		self.GLOBAL_TO_USER_MAP = []
		self.NODES = []
		self.BASIS_MAX_NUMBER_OF_DERIVATIVES = 0
		self.MULTIPLE_VERSIONS = False

	def MeshNodeGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

#============================================================================

class GeneratedMesh():
	""" !> Contains all information about a generated mesh .
	"""

	def __init__( self,USER_NUMBER):
		self.USER_NUMBER = USER_NUMBER #!<The user defined identifier for the generated mesh. The user number must be unique.
		self.MESH_USER_NUMBER = 0
		self.ORIGIN = []#!<ORIGIN(nj). The position of the origin (first) corner of the regular mesh
		self.MAXIMUM_EXTENT = [] #!<MAXIMUM_EXTENT(nj). The extent/size in each nj'th direction of the regular mesh.
		self.MESH_DIMENSION = [] #!<The dimension/number of Xi directions of the regular mesh.
		self.NUMBER_OF_ELEMENTS_XIC = [] #!<NUMBER_OF_ELEMENTS_XIC(ni). The number of elements in the ni'th Xi direction for the mesh.
		self.BASIS = [] #!<The pointer to the basis used in the regular mesh.
		self.REGION = []
		self.FIELD = []
		self.MESH = []
		self.TOTAL_NUMBER_OF_NODES_XIC = []
		self.TOTAL_NUMBER_OF_ELEMENTS_XIC = []
		self.TOTAL_NUMBER_OF_NODES = 0
		self.TOTAL_NUMBER_OF_ELEMENTS = 0

class GeneratedMeshes():
	def __init__(self,REGION):
		self.IDENTIFIER = "GeneratedMesh"
		self.NUMBER_OF_GENERATED_MESHES = 0
		self.GENERATED_MESHES = []
		self.REGION = REGION
		self.GLOBAL_TO_USER_MAP = []

	def GeneratedMeshesCreateStart(self,USER_NUMBER):
		self.GeneratedMeshesGeneratedMeshAdd(USER_NUMBER)

	def GeneratedMeshesGeneratedMeshAdd(self,USER_NUMBER):
		self.NUMBER_OF_GENERATED_MESHES = self.NUMBER_OF_GENERATED_MESHES + 1
		GLOBAL_NUMBER = self.NUMBER_OF_GENERATED_MESHES
		self.GLOBAL_TO_USER_MAP.append(USER_NUMBER)
		self.GENERATED_MESHES.append(GeneratedMesh(USER_NUMBER))
		return GLOBAL_NUMBER

	def GeneratedMeshGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def GeneratedMeshesNumberOfGlobalGeneratedMeshesGet(self,):
		return self.NUMBER_OF_GENERATED_MESHES

	def GeneratedMeshBasisSet(self,USER_NUMBER,BASIS_USER_NUMBER):
		GLOBAL_NUMBER = self.GeneratedMeshGlobalNumberGet(USER_NUMBER)
		GENERATED_MESH = self.GENERATED_MESHES[GLOBAL_NUMBER]
		GLOBAL_BASIS_NUMBER = self.REGION.BASES.BasisGlobalNumberGet(BASIS_USER_NUMBER)
		BASIS = self.REGION.BASES.BASES[GLOBAL_BASIS_NUMBER]
		GENERATED_MESH.BASIS = BASIS
		GENERATED_MESH.MESH_DIMENSION = GENERATED_MESH.BASIS.NUMBER_OF_XIC

	def GeneratedMeshMeshUserNumberSet(self,USER_NUMBER,MESH_USER_NUMBER):
		GLOBAL_NUMBER = self.GeneratedMeshGlobalNumberGet(USER_NUMBER)
		self.GENERATED_MESHES[GLOBAL_NUMBER].MESH_USER_NUMBER = MESH_USER_NUMBER

	def GeneratedMeshOriginSet(self,USER_NUMBER,ORIGIN):
		GLOBAL_NUMBER = self.GeneratedMeshGlobalNumberGet(USER_NUMBER)
		self.GENERATED_MESHES[GLOBAL_NUMBER].ORIGIN = ORIGIN

	def GeneratedMeshMaximumExtentSet(self,USER_NUMBER,MAXIMUM_EXTENT):
		GLOBAL_NUMBER = self.GeneratedMeshGlobalNumberGet(USER_NUMBER)
		self.GENERATED_MESHES[GLOBAL_NUMBER].MAXIMUM_EXTENT = MAXIMUM_EXTENT

	def GeneratedMeshNumberOfElementsSet(self,USER_NUMBER,NUMBER_OF_ELEMENTS_XIC):
		GLOBAL_NUMBER = self.GeneratedMeshGlobalNumberGet(USER_NUMBER)
		[self.GENERATED_MESHES[GLOBAL_NUMBER].NUMBER_OF_ELEMENTS_XIC.append(value) for value in NUMBER_OF_ELEMENTS_XIC]

	def GeneratedMeshesCreateFinish(self,USER_NUMBER):
		GLOBAL_NUMBER = self.GeneratedMeshGlobalNumberGet(USER_NUMBER)
		GENERATED_MESH = self.GENERATED_MESHES[GLOBAL_NUMBER]
		GENERATED_MESH.REGION = self.REGION
		fem_generatedMeshRoutines.GENERATED_MESH_REGULAR_CREATE(GENERATED_MESH)

	#Attaches a field to the generated  and calculates generated mesh geometric parameters
	def GeneratedMeshGeometricParametersCalculate(self,FIELD_USER_NUMBER,GENERATED_MESH_USER_NUMBER):
		GENERATED_MESH_GLOBAL_NUMBER = self.GeneratedMeshGlobalNumberGet(GENERATED_MESH_USER_NUMBER)
		GENERATED_MESH = self.GENERATED_MESHES[GENERATED_MESH_GLOBAL_NUMBER]
		REGION = self.REGION
		FIELD_GLOBAL_NUMBER = REGION.FIELDS.FieldGlobalNumberGet(FIELD_USER_NUMBER)
		GENERATED_MESH.FIELD =  REGION.FIELDS.FIELDS[FIELD_GLOBAL_NUMBER]
		fem_generatedMeshRoutines.GENERATED_MESH_GEOMETRIC_PARAMETERS_CALCULATE(GENERATED_MESH)

#============================================================================

class DatapointComponent():
	def __init__(self,USER_NUMBER,REGION):
		self.USER_NUMBER = USER_NUMBER
		self.LABEL = ""
		self.REGION = REGION
		self.VALUE = 0

class Datapoint():
	def __init__(self,REGION,USER_NUMBER):
		self.USER_NUMBER = USER_NUMBER
		self.IDENTIFIER = "DatapointComponent"
		self.REGION = REGION
		self.NUMBER_OF_COMPONENTS = 0
		self.GLOBAL_TO_USER_MAP = []
		self.COMPONENTS = []

	def DatapointComponentGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def DatapointComponentGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.DatapointComponentGlobalNumberGet(USER_NUMBER)
		return self.COMPONENTS[GLOBAL_NUMBER]

class Datapoints():
	def __init__(self,USER_NUMBER,REGION):
		self.USER_NUMBER = USER_NUMBER
		self.LABEL = ""
		self.IDENTIFIER = "DatapointGroup"
		self.REGION = REGION
		self.NUMBER_OF_COMPONENTS = 0
		self.COMPONENT_LABELS = []
		self.NUMBER_OF_DATAPOINTS = 0
		self.GLOBAL_TO_USER_MAP = []
		self.DATAPOINTS = []

	def DatapointGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def DatapointGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.DatapointGlobalNumberGet(USER_NUMBER)
		return self.DATAPOINTS[GLOBAL_NUMBER]

class DatapointGroups():
	def __init__(self,REGION):
		self.IDENTIFIER = "Datapoint"
		self.REGION = REGION
		self.NUMBER_OF_DATAPOINT_GROUPS = 0
		self.GLOBAL_TO_USER_MAP = []
		self.DATAPOINT_GROUPS = []

	def DatapointGroupGlobalNumberGet(self,USER_NUMBER):
		GLOBAL_NUMBER = GlobalNumberGet(self,USER_NUMBER)
		return GLOBAL_NUMBER

	def DatapointGroupGlobalGet(self,USER_NUMBER):
		GLOBAL_NUMBER = self.DatapointGroupGlobalNumberGet(USER_NUMBER)
		return self.DATAPOINT_GROUPS[GLOBAL_NUMBER]

	def DatapointGroupAdd(self,USER_NUMBER):
		REGION = self.REGION
		self.NUMBER_OF_DATAPOINT_GROUPS = self.NUMBER_OF_DATAPOINT_GROUPS + 1
		self.GLOBAL_TO_USER_MAP.append(USER_NUMBER)
		self.DATAPOINT_GROUPS.append(Datapoints(USER_NUMBER,REGION))

	def DatapointGroupCreateStart(self,DATAPOINT_GROUP_USER_NUMBER):
		self.DatapointGroupAdd(DATAPOINT_GROUP_USER_NUMBER)
#		for GLOBAL_DATAPOINT_NUMBER in range(TOTAL_NUMBER_OF_DATAPOINTS):
#			DATAPOINT_USER_NUMBER = GLOBAL_DATAPOINT_NUMBER + 1
#			self.DatapointAdd(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER)

	def DatapointGroupLabelSet(self,DATAPOINT_GROUP_USER_NUMBER,LABEL):
		DATAPOINT_GROUP = self.DatapointGroupGlobalGet(DATAPOINT_GROUP_USER_NUMBER)
		DATAPOINT_GROUP.LABEL = LABEL

	def DatapointGroupNumberOfComponentsSet(self,DATAPOINT_GROUP_USER_NUMBER,NUMBER_OF_COMPONENTS):
		DATAPOINT_GROUP = self.DatapointGroupGlobalGet(DATAPOINT_GROUP_USER_NUMBER)
		DATAPOINT_GROUP.NUMBER_OF_COMPONENTS = NUMBER_OF_COMPONENTS
		DATAPOINT_GROUP.COMPONENT_LABELS = [""]*NUMBER_OF_COMPONENTS
#		DATAPOINT_GROUP = self.DatapointGroupGlobalGet(DATAPOINT_GROUP_USER_NUMBER)
#		for GLOBAL_DATAPOINT_NUMBER in range(DATAPOINT_GROUP.NUMBER_OF_DATAPOINTS):
#			DATAPOINT_USER_NUMBER = GLOBAL_DATAPOINT_NUMBER + 1
#			for DATAPOINT_COMPONENT_GLOBAL_NUMBER in range(NUMBER_OF_COMPONENTS):
#				DATAPOINT_COMPONENT_USER_NUMBER = DATAPOINT_COMPONENT_GLOBAL_NUMBER + 1
#				self.DatapointComponentAdd(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,DATAPOINT_COMPONENT_USER_NUMBER)

	def DatapointGroupComponentLabelSet(self,DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_GROUP_COMPONENT_USER_NUMBER,LABEL):
		DATAPOINT_GROUP = self.DatapointGroupGlobalGet(DATAPOINT_GROUP_USER_NUMBER)
		DATAPOINT_GROUP.COMPONENT_LABELS[DATAPOINT_GROUP_COMPONENT_USER_NUMBER-1] = LABEL

	def DatapointComponentAdd(self,DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,DATAPOINT_COMPONENT_USER_NUMBER):
		REGION = self.REGION
		DATAPOINT_GROUP = self.DatapointGroupGlobalGet(DATAPOINT_GROUP_USER_NUMBER)
		DATAPOINT = DATAPOINT_GROUP.DatapointGlobalGet(DATAPOINT_USER_NUMBER)
		DATAPOINT.NUMBER_OF_COMPONENTS = DATAPOINT.NUMBER_OF_COMPONENTS + 1
		DATAPOINT.GLOBAL_TO_USER_MAP.append(DATAPOINT_COMPONENT_USER_NUMBER)
		DATAPOINT.COMPONENTS.append(DatapointComponent(DATAPOINT_COMPONENT_USER_NUMBER,REGION))

	def DatapointAdd(self,DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER):
		REGION = self.REGION
		DATAPOINT_GROUP = self.DatapointGroupGlobalGet(DATAPOINT_GROUP_USER_NUMBER)
		DATAPOINT_GROUP.NUMBER_OF_DATAPOINTS = DATAPOINT_GROUP.NUMBER_OF_DATAPOINTS + 1
		DATAPOINT_GROUP.GLOBAL_TO_USER_MAP.append(DATAPOINT_USER_NUMBER)
		DATAPOINT_GROUP.DATAPOINTS.append(Datapoint(REGION,DATAPOINT_USER_NUMBER))
		for component_idx in range(1,DATAPOINT_GROUP.NUMBER_OF_COMPONENTS+1):
			self.DatapointComponentAdd(DATAPOINT_GROUP_USER_NUMBER,DATAPOINT_USER_NUMBER,component_idx)

	def DatapointComponentValueSet(self,DATAPOINT_GROUP_USER_NUMBER,DATA_POINT_USER_NUMBER,DATAPOINT_GROUP_COMPONENT_USER_NUMBER,VALUE):
		DATAPOINT_GROUP = self.DatapointGroupGlobalGet(DATAPOINT_GROUP_USER_NUMBER)
		DATAPOINT = DATAPOINT_GROUP.DatapointGlobalGet(DATA_POINT_USER_NUMBER)
		DATAPOINT_GROUP_COMPONENT = DATAPOINT.DatapointComponentGlobalGet(DATAPOINT_GROUP_COMPONENT_USER_NUMBER)
		DATAPOINT_GROUP_COMPONENT.VALUE = VALUE

	def DatapointComponentValueGet(self,DATAPOINT_GROUP_USER_NUMBER,DATA_POINT_USER_NUMBER,DATAPOINT_GROUP_COMPONENT_USER_NUMBER):
		DATAPOINT_GROUP = self.DatapointGroupGlobalGet(DATAPOINT_GROUP_USER_NUMBER)
		DATAPOINT = DATAPOINT_GROUP.DatapointGlobalGet(DATA_POINT_USER_NUMBER)
		DATAPOINT_GROUP_COMPONENT = DATAPOINT.DatapointComponentGlobalGet(DATAPOINT_GROUP_COMPONENT_USER_NUMBER)
		return DATAPOINT_GROUP_COMPONENT.VALUE

	def DatapointsListGet(self,DATAPOINT_GROUP_USER_NUMBER):
		DATAPOINT_GROUP = self.DatapointGroupGlobalGet(DATAPOINT_GROUP_USER_NUMBER)
		DATAPOINT_LIST = []
		[DATAPOINT_LIST.append(value) for value in DATAPOINT_GROUP.GLOBAL_TO_USER_MAP]
		return DATAPOINT_LIST

	def DatapointGroupCreateFinish(self,USER_NUMBER):
		pass

#============================================================================
