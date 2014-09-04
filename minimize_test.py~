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

x0 = (.25,.75,.5,.25,.75,.75,1)

bnds = ((0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1))
  
f = lambda x: -x[6]

def dist(x1,x2,y1,y2):
    dist = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    return dist

cons1 = lambda x: -x[6]*2 + dist(x[0],x[2],x[1],x[3])
cons2 = lambda x: -x[6]*2 + dist(x[0],x[4],x[1],x[5])
cons3 = lambda x: -x[6]*2 + dist(x[2],x[4],x[3],x[5])

cons = [{"type": "ineq", "fun": cons1}, {"type": "ineq", "fun": cons2}, {"type": "ineq", "fun": cons3}]

#print minimize(f, x0, method = 'SLSQP', bounds = bnds, constraints = cons,options = { "eps":.1})

x1 = (.25,.25,.25,.75,.75,.25,.75,.75,1)


bndsc = ((0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1))
cons1c = lambda x: -x[8]*2 + dist(x[0],x[2],x[1],x[3])
cons2c = lambda x: -x[8]*2 + dist(x[0],x[4],x[1],x[5])
cons3c = lambda x: -x[8]*2 + dist(x[0],x[6],x[1],x[7])
cons4c = lambda x: -x[8]*2 + dist(x[2],x[4],x[3],x[5])
cons5c = lambda x: -x[8]*2 + dist(x[2],x[6],x[3],x[7])
cons6c = lambda x: -x[8]*2 + dist(x[4],x[6],x[5],x[7])



cons_crane = [{"type": "ineq", "fun": cons1c}, {"type": "ineq", "fun": cons2c}, {"type": "ineq", "fun": cons3c},{"type": "ineq", "fun": cons4c},{"type": "ineq", "fun": cons5c},{"type": "ineq", "fun": cons6c}]

print minimize(f, x1, method = 'SLSQP', bounds = bndsc, constraints = cons_crane, options = {"eps":.0001})
