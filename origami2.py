import math

# copy of tmPoint.h, TreeMaker 5.x,

#C++ code that I don't know what it does

########
#ifndef _TMPOINT_H_
#define _TMPOINT_H_

# // Standard libraries
#include <cmath>
#include <vector>

#//Common TreeMaker header
#include "tmHeader.h"

#//Utility routines for min and max of a par

#template <class T>
#T& min_val(T& t1, T& t2 {return t1 < t2 ? t1 : t2;};
#template <class T>
#T min_val(const T& t1....
#template <class T>
#T&...
#template <class T>
#T max_val......

##########

#real code now

"""
Constants
"""

Pi=3.1415926535897932385
TwoPi = 6.2831853071795864769
Radian = 57.95779513082321
Degrees = 0.017453292519943296

class Point:
    '''Creates a point class based on floats'''
    def __init__(self,x=0,y=0):
        #Creates a new point that can be accessed for it's information, with default values of (0,0)
        '''Create a new point at the origin'''
        #not sure if this is what I want, since I am just copying it from
        #Interactive Python, but I'm pretty sure that I do need a constructor of some sort.
        self.x = x
        self.y = x

        #what the hell
        #template <class Tx, class Ty>
        #tmPoint(const Tx& ax, const Ty@ ay) : x(tmFloat(ax)), y(tmFloat(ay)) {};

        #in tmPoin.h the constants are tmPoint& and fp
        def add(self, point)
            self.x += point.x
            self.y += point.y
            return #self?
        def sub(self, point)
            self.x -= point.x
            self.y -= point.y
        def mult(self,point)
            self.x *= point.x
            self.y *= point.y
        def div(self, point)
            self.x /= point.x
            self.y /= point.y

            #probably some other stuff going on... with the operator() function
            # whether stuff gets returned or not

            #are these supposed to be modifying?

            #I think these are totally wrong

        def addConstant(self,constant)
            self.x + constant
            self.y + constant
        def subConstant (self, constant)
            self.x - constant
            self.y - constant
        def multConstant (self, constant)
            self.x 

        #magnitude

        def mag(self)
            math.sqrt(self.x**2 + self.y**2) #do I need a return?

        #"Normalize in place" (what is that?)
        def normalize(self)
            r

        #bla bla bla bla point class, here are the rest of the functions
        #More arithmetic stuff with scalars
        #another magnitude function
        #magnitude squared function
        #inner product of two points
        #normalize a point
        #rotate 90 degrees ccw, cw
        #arbitrary rotations
        #find the intersection of two lines, each defined by a point + direction
        #centroid of triangle
        #Bisector intersection of triangle
        #angle
        #rotational orientation of three points
        #Unit vector at a given angle
        #two points (p1 and p2) lie on same line segment...
        #strict parallelity
        #strict equality
        #strict inequality
        #projection between two line segments
        #clip line to rectangle
        #polygon encloses a point

        #endthingy---
            #endif // _TMPOINT_H_
