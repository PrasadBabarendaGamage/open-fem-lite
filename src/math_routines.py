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

# v and w are tuples representing 3d vectors
import random
from time import *
import cProfile
import math
def cross(v, w):
    x = float(v[1])*float(w[2]) - float(v[2])*float(w[1])
    y = float(v[2])*float(w[0]) - float(v[0])*float(w[2])
    z = float(v[0])*float(w[1]) - float(v[1])*float(w[0])
 
    return (x, y, z)

# v is a tuple representing a 3d vector
def normalize(v):
    len = length(v);
    return (float(v[0]) / len, float(v[1]) / len, float(v[2]) / len)

# v is a tuple representing a 3d vector
def length(v):
    return (float(v[0])*float(v[0]) + float(v[1])*float(v[1]) + float(v[2])*float(v[2])) ** 0.5

# v and w are tuples representing 3d vectors
def dot(v, w):
    return float(v[0])*float(w[0]) + float(v[1])*float(w[1]) + float(v[2])*float(w[2])

#===============================================================================================
#Below is from http://www.syntagmatic.net/matrix-multiplication-in-python/

def zero(m,n):
    # Create zero matrix
    new_matrix = [[0 for row in range(n)] for col in range(m)]
    return new_matrix
 
def rand(m,n):
    # Create random matrix
    new_matrix = [[random.random() for row in range(n)] for col in range(m)]
    return new_matrix
 
def show(matrix):
    # Print out matrix
    for col in matrix:
        print col 
 
def mult(matrix1,matrix2):
    # Matrix multiplication
    if len(matrix1[0]) != len(matrix2):
        # Check matrix dimensions
        print 'Matrices must be m*n and n*p to multiply!'
    else:
        # Multiply if correct dimensions
        new_matrix = zero(len(matrix1),len(matrix2[0]))
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):
                    new_matrix[i][j] += matrix1[i][k]*matrix2[k][j]
        return new_matrix
 
def time_mult(matrix1,matrix2):
    # Clock the time matrix multiplication takes
    start = clock()
    new_matrix = mult(matrix1,matrix2)
    end = clock()
    print 'Multiplication took ',end-start,' seconds'
 
def profile_mult(matrix1,matrix2):
    # A more detailed timing with process information
    # Arguments must be strings for this function
    # eg. profile_mult('a','b')
    cProfile.run('matrix.mult(' + matrix1 + ',' + matrix2 + ')')

#===============================================================================================

def transpose2Dlist(IN):
	return [[r[col] for r in IN] for col in range(len(IN[0]))]

def TransformationMatrix(xn):
	for value in range(3):
		xn[value] = xn[value]*math.pi/float(180)
	ZROT = transpose2Dlist([[math.cos(xn[0]),math.sin(xn[0]),0,0], [-math.sin(xn[0]),math.cos(xn[0]),0,0], [0,0,1,0], [0,0,0,1]])
	YROT = transpose2Dlist([[math.cos(xn[1]),0,-math.sin(xn[1]),0], [0,1,0,0], [math.sin(xn[1]),0,math.cos(xn[1]),0], [0,0,0,1]])
	XROT = transpose2Dlist([[1,0,0,0], [0,math.cos(xn[2]),math.sin(xn[2]),0], [0,-math.sin(xn[2]),math.cos(xn[2]),0], [0,0,0,1]])
	TRANS = transpose2Dlist([[1,0,0,0], [0,1,0,0], [0,0,1,0], [xn[3],xn[4],xn[5],1]])
	SCALE = transpose2Dlist([[xn[6],0,0,0], [0,xn[7],0,0], [0,0,xn[8],0], [0,0,0,1]])
	R = mult(ZROT,mult(YROT,mult(XROT,mult(TRANS,SCALE))))
	return R

def ApplyTransform(R,IN_DATA):
	OUT_DATA = []
	temp = []
	for value in range(len(IN_DATA)):
		temp = IN_DATA[value][:]
		temp.append(1)
		temp2 = []
		for value2 in range(len(temp)):
			temp2.append([temp[value2]])
		temp3 = mult(R,temp2)[0:3]
		temp4=[]
		for value3 in range(len(temp3)):
			temp4.append(temp3[value3][0])
		OUT_DATA.append(temp4)
	return OUT_DATA
