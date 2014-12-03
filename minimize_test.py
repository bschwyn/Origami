from scipy.optimize import minimize
import math
#test of minimizing a tetrad graph

#....._____________
#....\...O......O..\
#....\....\..../...\
#....\.....\./.....\
#....\......O......\
#....\......\......\
#....\......O......\
#....\_____________\

#....._____________
#....\............O\
#....\.............\
#....\O............\
#....\.......O.....\
#....\.............\
#....\.............\
#....\________O____\

#u_1=(.25,.75)
#u_2 doesn't matter
#u_3 = (.5.25)
#u_4 = (.75,.75)
#m=1

#x =(u1x,u1y,u3x,u3y,u4x,u4y,m)

#expected (.26795,1)(0,0), (1,.26795) m = .5176, use eps .1, maxiter 50

#emu

x0 = (.25,.75,.5,.25,.75,.75,1)

bnds = ((0,1.0),(0,1.0),(0,1.0),(0,1.0),(0,1.0),(0,1.0),(0,1.0))
  
f = lambda x: -x[-1]

def dist(x1,x2,y1,y2):
    dist = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    return dist

cons1 = lambda x: -x[6]*2 + dist(x[0],x[2],x[1],x[3])
cons2 = lambda x: -x[6]*2 + dist(x[0],x[4],x[1],x[5])
cons3 = lambda x: -x[6]*2 + dist(x[2],x[4],x[3],x[5])

cons_emu = [{"type": "ineq", "fun": cons1}, {"type": "ineq", "fun": cons2}, {"type": "ineq", "fun": cons3}]
print "____emu____"
print minimize(f, x0, method = 'SLSQP', bounds = bnds, constraints = cons_emu, options = { "eps":.1, "maxiter":50, "ftol":.0001})




#crane

x1 = (.25,.25,.25,.75,.75,.25,.75,.75,1)

#expected (0,0) (1,0) (0,1), (1,1), m = .5
g = lambda x: -x[-1]

bndsc = ((0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1))

cons1c = lambda x: -x[8]*2 + dist(x[0],x[2],x[1],x[3])
cons2c = lambda x: -x[8]*2 + dist(x[0],x[4],x[1],x[5])
cons3c = lambda x: -x[8]*2 + dist(x[0],x[6],x[1],x[7])
cons4c = lambda x: -x[8]*2 + dist(x[2],x[4],x[3],x[5])
cons5c = lambda x: -x[8]*2 + dist(x[2],x[6],x[3],x[7])
cons6c = lambda x: -x[8]*2 + dist(x[4],x[6],x[5],x[7])



cons_crane = [{"type": "ineq", "fun": cons1c}, {"type": "ineq", "fun": cons2c}, {"type": "ineq", "fun": cons3c},{"type": "ineq", "fun": cons4c},{"type": "ineq", "fun": cons5c},{"type": "ineq", "fun": cons6c}]
print "\n\n"
print "____crane____"
print minimize(g, x1, method = 'SLSQP', bounds = bndsc, constraints = cons_crane)




#pentagon ------gets close to the correct answer, and finds a minimum, but not the global minimum
# finds global minimum w/ version 2 of x0 coordinates

pentagon_x0 = (.1,.1,.2,.9,.8,.1, .9, .9,.2,.5, 1) #my original x cooridnates
pentagon_x0_v2 = (.45, .95, .95, .65, .9, .9, .35, 0.1, 0.05, .5,1) #coordinates close to global optimum
pentagon_bnds = ((0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1))
h = lambda x: -x[-1]

pcons23 = lambda x: -x[-1]*2 + dist(x[0],x[2],x[1],x[3])
pcons24 = lambda x: -x[-1]*2 + dist(x[0],x[4], x[1],x[5])
pcons25 = lambda x: -x[-1]*2 + dist(x[0],x[6], x[1],x[7])
pcons26= lambda x: -x[-1]*2 +  dist(x[0],x[8], x[1],x[9])
pcons34= lambda x: -x[-1]*2 +  dist(x[2],x[4], x[3],x[5])
pcons35= lambda x: -x[-1]*2 + dist(x[2], x[6], x[3],x[7])
pcons36= lambda x: -x[-1]*2 + dist(x[2],x[8], x[3],x[9])
pcons45= lambda x: -x[-1]*2 + dist(x[4],x[6], x[5],x[7])
pcons46= lambda x: -x[-1]*2 + dist(x[4],x[8], x[5],x[9])
pcons56= lambda x: -x[-1]*2 + dist(x[6],x[8], x[7],x[9])

cons_pentagon = [{"type": "ineq", "fun": pcons23}, {"type": "ineq", "fun": pcons24}, {"type": "ineq", "fun": pcons25},{"type": "ineq", "fun": pcons26},{"type": "ineq", "fun": pcons34},{"type": "ineq", "fun": pcons35},{"type": "ineq", "fun": pcons36},{"type": "ineq", "fun": pcons45},{"type": "ineq", "fun": pcons46},{"type": "ineq", "fun": pcons56}]

print "\n\npentagon"
print minimize(h,pentagon_x0_v2,method = "SLSQP",bounds = pentagon_bnds,constraints = cons_pentagon)



# muller, 2-1-2
m_x0 = (.3, .95, .9, .9, .8, .1, .15, .1,1)
i = lambda x: -x[-1]
m_bnds = ((0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1))

mcons23 = lambda x: -x[-1]*2 + dist(x[0],x[2],x[1],x[3])
mcons25 = lambda x: -x[-1]*3 + dist(x[0],x[4],x[1],x[5])
mcons26 = lambda x: -x[-1]*3 + dist(x[0],x[6],x[1],x[7])
mcons35 = lambda x: -x[-1]*3 + dist(x[2],x[4],x[3],x[5])
mcons36 = lambda x: -x[-1]*3 + dist(x[2],x[6],x[3], x[7])
mcons56 = lambda x: -x[-1]*2 + dist(x[4],x[6],x[5], x[7])


cons_muller = [{"type": "ineq", "fun": mcons23}, {"type": "ineq", "fun": mcons25}, {"type": "ineq", "fun": mcons26},{"type": "ineq", "fun": mcons35},{"type": "ineq", "fun": mcons36},{"type": "ineq", "fun": mcons56}]
print "\n\nmuller"
print minimize(i,m_x0,method = "SLSQP",bounds = m_bnds, constraints = cons_muller)
