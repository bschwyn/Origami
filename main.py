
# *** libraries***
#import networkx as nx
#import numpy as np
#from scipy.optimize import minimize
#import math
#import matplotlib.pyplot as plt
#import unittest
#import itertools
import Tkinter as Tk
import re

import Model as model
import Application as app
import NodeBox
import DimensionsBox
import Test


run_emu_example = True           
if run_emu_example:
    
    emu = model.Model(1.0,1.0)
    emu.draw()
    emu.add_node_to(source_node = None, x = 0.5, y = 0.5,) #creates node 1
    emu.draw()
    emu.add_node_to(1,.25,.75) #creates node 2 attached to node1
    emu.draw()
    emu.add_node_to(1,.5,.25) #creates node 3 attached to node 2
    emu.draw()
    emu.add_node_to(1,.75,.75)
    emu.draw()
    print "objective function:"
    print "-x[-1]"
    print "initial guess"
    print emu._scale_initial_guess()

    big_thing = emu.scale_optimization()
    print big_thing
    print big_thing.message


#'''
rungui=False
if rungui:
    root = Tk.Tk()
    gui = app.Application(master = root)
    root.mainloop()
    root.destroy()    
