# If the example path is not set, default to current directory
if (!defined $example) {
    $example = "./";
}
# Drop off the trailing / in the example path
$chopped = chop $example;
if ($chopped ne "/") {
    $example .= $chopped;
}
#**************************************************************
#
# allocate memory for program arrays etc.
fem def para;r;memory;../ProblemSetup/
#**************************************************************
#
# Set up beam geometry
fem def coor 3,1
fem def base;r;TriCubicHerm;../Mesh/ #basis function for interpolation of 3d coords
fem def;add base;r;BiCubicHerm;../Mesh/ #for interpolation of coords on 2D surfaces
fem def;add base;r;TriLinearPress;../Mesh/ #interpolates hydrostatic pressure
fem def;add base;r;BiLinear;../Mesh/
#The geometry being subjected to gravity load is a cuboid 60mm long,(x-direction) 40X40 mm in y,z directions

fem def node;r;beam;../Mesh/
fem def elem;r;beam;../Mesh/
fem def fibre;d;bla
fem def elem;d;bla fibre

fem export node;Output/beamInitial as beamInitial
fem export elem;Output/beamInitial as beamInitial

#group nodes that are against the wall for cantilever setup. Certain degrees of freedom for these nodes will be fixed in the ipinit file
#to simulate the cantilever setup

fem group elem all_elements external s1=0 as BACKELEMENTS
fem group node xi1=0 external element BACKELEMENTS as BACKNODES
fem list node groups
fem def equa;r;mechanics;../ProblemSetup/ #use 3D finite elasticity to simulate the deformation
#
#apart from the neo_hookean parameter, you need to give the density of the body..
#units for this model
#
# Density in gram per millimeter cubed 
# gravity m/(sec squared). 
# This means force is in mN. Therefore stress will be in kPa (kN/squared m)or (mN/squared mm)
# so neo-Hookean param is in kPa
fem def mate;r;neo_hookean 
#
#The gravity vector is set in the ipinit file. 
fem def init;r;gravity;../ProblemSetup/
#
#Define the nonlinear equations solution algorithm to be used
#I have chosen modified newton with LU factorisation. The LU factorisation
# can be slow, but with modified newton, the total time taken can actually be reduced
fem def solv;r;modif_newton;../ProblemSetup/
#**************************************************************
#
# solve the problem
fem solv inc 0.5 iter 100
fem solv inc 0.5 iter 100
#**************************************************************
#

fem export node;Output/beam field as beam
fem export elem;Output/beam field as beam
q
q

