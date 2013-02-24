import fem_topology
import math_routines
import fem_miscellaneous_routines
import os

WORLD_REGION = fem_topology.femInitialize()
#=================================================================================================================================

RegionUserNumber = 1
WORLD_REGION.RegionsCreateStart(RegionUserNumber)
WORLD_REGION.RegionsCreateFinish(RegionUserNumber)
REGION = WORLD_REGION.RegionsRegionGet(RegionUserNumber)

DATAPOINT_GROUP_USER_NUMBER1 = 1
DATAPOINT_GROUP_USER_NUMBER2 = 2
DATAPOINT_GROUP_USER_NUMBER3 = 3


REGION.ReadExdata(DATAPOINT_GROUP_USER_NUMBER1,"CMISS",'./input/testexdataio')
muscleDatapointList = REGION.DATAPOINTS.DatapointsListGet(DATAPOINT_GROUP_USER_NUMBER1)

NUMBER_OF_COMPONENTS = 5
REGION.DATAPOINTS.DatapointGroupCreateStart(DATAPOINT_GROUP_USER_NUMBER3)
REGION.DATAPOINTS.DatapointGroupLabelSet(DATAPOINT_GROUP_USER_NUMBER3,"exdata")
REGION.DATAPOINTS.DatapointGroupNumberOfComponentsSet(DATAPOINT_GROUP_USER_NUMBER3,NUMBER_OF_COMPONENTS)
REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER3,1,"x")
REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER3,2,"y")
REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER3,3,"z")
REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER3,4,"groupName")
REGION.DATAPOINTS.DatapointGroupComponentLabelSet(DATAPOINT_GROUP_USER_NUMBER3,5,"sliceName")
REGION.DATAPOINTS.DatapointGroupCreateFinish(DATAPOINT_GROUP_USER_NUMBER3)

for datapoint in muscleDatapointList:
	COORDINATES = []
	COORDINATES.append(REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER1,datapoint,1))
	COORDINATES.append(REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER1,datapoint,2))
	COORDINATES.append(REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER1,datapoint,3))
	groupName = REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER1,datapoint,4)
	sliceName = REGION.DATAPOINTS.DatapointComponentValueGet(DATAPOINT_GROUP_USER_NUMBER1,datapoint,5)
	REGION.DATAPOINTS.DatapointAdd(DATAPOINT_GROUP_USER_NUMBER3,datapoint)
	REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER3,datapoint,1,COORDINATES[0])
	REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER3,datapoint,2,COORDINATES[1])
	REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER3,datapoint,3,COORDINATES[2])
	REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER3,datapoint,4,groupName)
	REGION.DATAPOINTS.DatapointComponentValueSet(DATAPOINT_GROUP_USER_NUMBER3,datapoint,5,sliceName)

REGION.WriteExdataSelectedGroup(DATAPOINT_GROUP_USER_NUMBER3,"SKIN",NUMBER_OF_COMPONENTS,"CMISS",'./output/skin')

