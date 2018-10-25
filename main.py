
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


#emu example
run_simple_examples = False
if run_simple_examples:
    print "Emu"
    emu = model.Model(1.0,1.0)
    emu.add_node_to(source = None, x = 0.5, y = 0.5,) #creates node 1
    emu.add_node_to(1,.25,.75) #creates node 2 attached to node1
    emu.add_node_to(1,.5,.25) #creates node 3 attached to node 2
    emu.add_node_to(1,.75,.75)
    big_thing = emu.scale_optimization()
    print big_thing
    #print big_thing.message
    # big_thing.x
    print "\n\nCrane"
    crane = model.Model(1.0, 1.0)
    crane.add_node_to(source = None, x = 0.5, y = 0.5)
    crane.add_node_to(1,0.1,0.1)
    crane.add_node_to(1,0.1, 0.9)
    crane.add_node_to(1,0.9,0.1)
    crane.add_node_to(1,0.9,0.9)
    opto = crane.scale_optimization()
    print opto 
    
run_complex_examples = False
if run_complex_examples:
    print "pentagon"
    pentagon = model.Model(1.0, 1.0)
    pentagon.add_node_to(source = None, x = 0.5, y = 0.5)
    pentagon.add_node_to(1, .1, .1)
    pentagon.add_node_to(1, .9,.1)
    pentagon.add_node_to(1, .9, .9)
    pentagon.add_node_to(1, .1, .9)
    pentagon.add_node_to(1,.5, .9)
    popto = pentagon.scale_optimization()
    print popto
    
    
    print "\n\nMuller-Lyer"
    muller = model.Model(1.0,1.0)
    muller.add_node_to(source= None,x = .38, y = .63)
    muller.add_node_to(1,.66,.82)
    muller.add_node_to(1,.1, .8)
    muller.add_node_to(1,.45,.3)
    muller.add_node_to(4,.85,.1)
    muller.add_node_to(4,.1, .05)
    mullerization = muller.scale_optimization()
    print mullerization
    
    
   



#'''
rungui= True
if rungui:
    root = Tk.Tk()
    gui = app.Application(master = root)
    root.mainloop()
    root.destroy()    
