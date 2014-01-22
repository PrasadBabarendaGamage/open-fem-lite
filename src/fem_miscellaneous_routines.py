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

import copy

def remove_from_list(list_, remove):
    new_list = copy.deepcopy(list_)
    for item in remove:
        try:
            new_list.remove(item)
        except:
            pass
    return new_list

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

def initialize1DList(VALUE,A):
    return [VALUE for i in range(A)]

def initialize2DList(VALUE,A,B):
    return [[VALUE for i in range(B)] for j in range(A)]
    #return [ [VALUE]*A for i in range(B) ]

def initialize3DList(VALUE,A,B,C):
    return [[[VALUE for i in range(C)] for j in range(B)] for k in range(A)]

def initialize4DList(VALUE,A,B,C,D):
    return [[[[VALUE for i in range(D)] for j in range(C)] for k in range(B)] for l in range(A)]

def CMISS_intStringToArray(String):
	StringArray = String.split(',')
	Data = []
	for value in StringArray:
		if value.find('..')>-1:
			temp = value.split('..')
			temp2 = range(int(temp[0]),int(temp[1])+1)
			[Data.append(point) for point in temp2]
		else:
			Data.append(int(value))
	return Data

def indexOfNthOccurrence(N, element, stream):
    """for N>0, returns index or None"""
    seen = 0
    for i,x in enumerate(stream):
        if x==element:
            seen += 1
            if seen==N:
                return i
