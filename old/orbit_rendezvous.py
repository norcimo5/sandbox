#!/usr/bin/env python2.7

from visual import *
from visual.graph import *

#################################################################################
# I made this game for you.  You should play with it.  By play with it,         #
# I mean that you should change around some of the things and run it.  You      #
# will have a blast.  I hav tried to fully document pieces of the code          #
# so you know what you can change and what you might want to leave alone.       #
# If you don't have the visual model, you can get it at http://www.vpython.org  #
#################################################################################



# scene2 just labels the display window.  I made it bigger than the default
scene2=display(width=800,height=800, x=0, y=0, title='Orbit')

# Ignore the following two lines for now.  I was going include a bar graph
## gscene=display(x=800,y=0, width=480, height=360, title='Graph')
## f1=gvbars(color=color.red, display=gscene)

# This makes the Earth.  Notice distance units are in Earth radii 
Earth=sphere(pos=vector(0,0,0), radius=1, material=materials.earth)

# These are the starting parameters for the space craft
R=2.75
# GM is the constant I found from the game Space Agency
GM=1.47
# v is the theoretical speed for a circular orbit
v=sqrt(GM/R)

# the other object is just something else oribting the Earth
other=sphere(pos=vector(1.5*R,0,0), radius=0.1, color=color.red, make_trail=True)

# the mass doesn't really matter - but you can change it if you like
other.m=1
# the initial momentum.  The velocity is in the negative y direction with a speed
# to give it a circular orbit
other.p=vector(0,-sqrt(GM/(1.5*R)),0)
               
# L is the length of the space craft
L=.2
# sc stands for space craft.  It's a cone so you can tell which way it points
# remember for a cone, the pos is the vector location of the flat end of the cone
# axis is a vector from the position of the cone to the pointy part
sc=cone(pos=vector(R,0,0), axis=(0,L,0), radius=.1, color=color.cyan,
        make_trail=True, retain=1300)


# I need the mass and initial momentum for the space craft
sc.m=1
sc.p=vector(0,-v,0)*sc.m

# ff is the strength of the thruster force.
#### YOU CAN CHANGE THIS
ff=0.25

# dt is the time interval step.  You can change this if it makes you happy.
dt=0.01

# time isn't usually used, but here it is
t=0

# dtheta is the amount the space turns when you click an arrow
dtheta=10*pi/180

# so the space craft automatically turns in the orbit.  If you didn't do anything
# it would keep turning so that it points in the direciton of motion
# dangle is the amount the space deviates from this direction
dangle=0

# This is just the Force - Since I am adding things to it, I want it to already exist
F=vector(0,0,0)

# exhaust is supposed to be an arrow that represents the rockets firing
# for some reason, it doesn't work exactly correct
# the idea is to make it see through when the rockets AREN't on
exhaust=arrow(pos=sc.pos, axis=-sc.axis, color=color.yellow, opacity=0)


# this is the main loop that runs the stuff
while True:

    # rate tells vpython how fast to run.  This should be 1/dt
    rate(100)

    # at the begining of each loop, I recent the exhaust to be invisible
    exhaust.opacity=0

    # reset the force to be zero (in case the rockets are off)
    F=vector(0,0,0)

    # here I look to see if a key is pressed for navigation
    if scene2.kb.keys:
        # this just gets the key stroke and calls it k
        k= scene2.kb.getkey()

        # if you push the up arrow, add a thrust to the total force
        if k =='up':
            #the thrust is in the same direction as the cone
            # norm(sc.axis) is a unit vector of the axis vector
            F=F+ff*norm(sc.axis)

            # make the exhaust opacity visible at 1
            exhaust.opacity=1


        # do the same thing if the down arrow is pushed except use a minus sign 
        if k=='down':
            F=F-ff*norm(sc.axis)
            
            exhaust.opacity=1

        # if you push left arrow, the space craft will turn to the left with
        # respect to its orbital motion direction
        if k=='left':
            # really, I just increase the daangle and then rotate the spacecraft later
            dangle=dangle+dtheta
        if k=='right':
            #sc.rotate(angle=-dtheta, axis=vector(0,0,1), origin=sc.pos)
            dangle=dangle-dtheta
    

    # here I rotate the space craft.  There are two rotations.  The first is a rotation
    # due to the motion around the planet.  The visual rotate function takes an angle and an
    # axis of rotation.  In this case, I first set the orientation of the spacecraft to point
    # away from the planet (that is where I set sc.axis).
    # next, I rotate pi/2 radians to the right.  Next, I rotate an amount of dangle
    # note that this rotation is different than in the game.  In the Space Agency game
    # you have thrusters to rotate.  I did it this way just because it was easier to play
    
    sc.axis=norm(sc.pos)*.2
    sc.rotate(angle=(-pi/2+dangle), axis=vector(0,0,1), origin=sc.pos)

    # Now for the physics.  This next line is the sum of the rocket thrust force (if any)
    # and the gravitational force.
    # To calculate the gravitational force, it is just 1/r^2 type of gravity.
    # If you wanted to play around, this is something you could change.  You could change
    # the gravitational constant (GM) to change the strength of the force or you could
    # change the model - maybe make it a constant gravitational force or something like that
    Ft=-GM*norm(sc.pos)*sc.m/mag(sc.pos)**2+F

    # Once I have the net force, I can use the momentum principle.  This says that the
    # new momentum is the old momentum plus F*dt
    sc.p=sc.p+Ft*dt

    # Now I can determine the new position of the spacecraft.
    # New position = old position * v*dt (where v = p/m)
    sc.pos=sc.pos+sc.p*dt/sc.m

    # This does the same thing for the other orbiting object.  There is no thrust.
    other.p=other.p-dt*GM*norm(other.pos)/mag(other.pos)**2
    other.pos=other.pos+other.p*dt/other.m
    
    # This updates the position and direction of the thrust arrow
    exhaust.pos=sc.pos
    exhaust.axis=-sc.axis

    # update time
    t=t+dt


# if you wanted to make a bar graph, you would use the line below.  Needs some work though.
##    f1.plot(pos=(1,mag(sc.p)))
    

            
