#Origami program
#inspired by Robert J. Lang's TreeMaker program
#used algorithms from Origami Design Secrets: http://www.langorigami.com/books/ODS1e_Algorithms.pdf

#9;11

# *** libraries***
import networkx as nx
import numpy as np
from scipy.optimize import minimize
import math
import matplotlib.pyplot as plt
import unittest
import itertools
import Tkinter as Tk
import re

# useless?

class Node:
    def __init__(self,key,x,y):
        self.id = key
        self.x = x
        self.y = y

#unecessecary

class Rectangle:
   def __init__(self,width,height):
        self.width = width
        self.height = height

#contains data structure for origami model, modifying its structure, properties of the medium (paper size) that affects the design

class Model:
    #initialize the properties of the medium (paper) that the origami model will use.
    def __init__(self, width = 1.0, height = 1.0):
        self.width = width
        self.height = height
        self.scale = 1.0
        self.node_counter = 1
        self.G = nx.Graph()
        #self.edges = {}
        #self.vertices = {}
        #self.vertex-node_indices = {}
        #self.edge_indices = {}
        #self.nodes = {}
        #self.paths = {}
        #self.leaf_vertices


#addes a node to the graph structure representing the origami model
    
    def add_node_to(self, source_node = None, x = 0.0, y = 0.0, length = 1.0, strain = 0.0):

        #if this is the first node
        if len(self.G)==0 and source_node == None:
            self.G.add_node(self.node_counter,x = x, y = y)
            self.node_counter +=1  
                   
        #adding attional nodes 
        elif source_node in self.G.nodes(): 
            new_node = self.node_counter
            self.G.add_node(new_node,x=x,y=y)
            self.G.add_edge(new_node,source_node,length = length, strain = strain)
            self.node_counter +=1            
        else:
            print "error"

#deletes a  node and any related edges from the graph structure
            
    def delete_node(self, node):
        
        if len(self.G)==1:
            self.G.delete_node(1)            
        elif self.is_leaf_node(node):
            self.G.remove_node(node)            
        else:
            raise "Error: cannot delete connected node"

#draws graph using matplotlib
                
    def draw(self):
        nx.draw(self.G)
        plt.show()

#*** helper functions ***

# leaf nodes are nodes with only one edge         
    def all_leaf_nodes(self):
        leaf_nodes = []
        for node in self.G:
            if self.G.degree(node) == 1:
                leaf_nodes.append(node)
        return leaf_nodes
    
    def is_leaf_node(self,node):
        leaf_nodes = self.all_leaf_nodes()
        return node in leaf_nodes
        
    def all_shortest_paths(self):
        return all_pairs_shortest_path(self.G)

    def all_leaf_edges(self):
        leaf_edges = []
        for node in self.G:
            if self.G.degree(node) == 1:
                leaf_edge = G.edges(node)[0]
                leaf_edges.append(leaf_edge)
        return leaf_edges
    

#pythagorean theorem to find distance between two points
    def dist(self, x1, x2, y1, y2):
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist 
        
#full of errors
#returns array of dictionaries that are all paths between different leaf nodes        
    def all_leaf_paths(self):
        leaf_nodes = all_leaf_nodes(self.G)
        all_paths = all_pairs_shortest_path(self.G) #returns {source : {target1 : [path1] , ... , targetn:[pathn]}, ... }
        #filter dictionary for all sources that are 
        #leaf_paths = {leaf_node: all_paths[leaf_node] for leaf_node in leaf_nodes}
        leaf_paths = {}
        for source in all_paths:
            if source in leaf_nodes:
                leaf_paths[source] = all_paths[source]
            target = getthetarget
            if target in leaf_nodes:
                leaf_paths[target] = thepath
        return leaf_paths  

# ***sub fucntions for optimization***

#returns strained length of a path  
#every edge has associated strain and length    
#= Sum(1+strain_k)*length_k for all edges k in path
    def sum_of_strained_lengths(self,source, target):
        graph = self.G
        shortest_path = nx.shortest_path(graph ,source, target)
        i = 0
        sum_of_strained_length = 0
        while i < len(shortest_path)-1:
            node1 = shortest_path[i]
            node2 = shortest_path[i+1]
            edge_length = graph[node1][node2]['length']
            edge_strain = graph[node1][node2]['strain']
            strained_length = (1+edge_strain) * edge_length        
            sum_of_strained_length += strained_length
            i+=1
        return sum_of_strained_length

#=sum(length_k) for all edges k in a path
    def sum_of_lengths(self,source, target):
        graph = self.G
        shortest_path = nx.shortest_path(graph ,source, target)
        i = 0
        sum_of_length = 0
        while i < len(shortest_path)-1:
            node1 = shortest_path[i]
            node2 = shortest_path[i+1]
            edge_length = graph[node1][node2]['length']      
            sum_of_length += edge_length
            i+=1
        return sum_of_length

# ***functions for scalar optimization***
# http://www.langorigami.com/books/ODS1e_Algorithms.pdf
# Section A.3. Scalar Optimization


#s_vector is a vector of the variables [node1_x, node1_y, node2_x, node2_y....noden_x, noden_y, scale]
#returns scale note negative
    def _scale_objective_function(self,s_vector):
        return -s_vector[-1]

#constrains all leaf node x and y coordinates to stay within the paper boundaries.
    def _scale_construct_bounds(self):
        x_bnd = (0,self.width)
        y_bnd = (0,self.height)
        bnds = []
        leaf_nodes = self.all_leaf_nodes()
        #create list of bounds
        for vertex in leaf_nodes:
            bnds.append(x_bnd)
            bnds.append(y_bnd)
        #scale represents the length of a flap of width 1.0 on the actual paper.
        #create boundaries for possible scale size
        theoretical_max_scale = min(self.width, self.height)
        scale_bnd = (0,theoretical_max_scale)
        bnds.append(scale_bnd)
        return bnds
        

# {scale * Sum[(1+strain_k)*length_k] for edge in all leaf paths - euclidian distance between nodes <= 0 } for all leaf paths
# creates a list of inequalities in the correct format for numpy.optimize.minimize
    def _scale_construct_constraints(self):
        leaf_nodes = self.all_leaf_nodes()
        constraints = []
        #all possible paths between two leaf nodes
        for combo in itertools.combinations(leaf_nodes,2):
            source = combo[0]
            target = combo[1]
            sum_of_strained_lengths = self.sum_of_strained_lengths(source,target)
            
            source_index = leaf_nodes.index(source)
            target_index = leaf_nodes.index(target)
            
            #create a corresponding x and y index for each source and target index
            src_x = source_index * 2
            src_y = (source_index + 1) * 2
            trg_x = target_index * 2
            trg_y = (target_index + 1) * 2
            
            #constraint function in form where cons >=0
            def cons(s_vector):
                coord_distance = self.dist(s_vector[src_x], s_vector[src_y], s_vector[trg_x], s_vector[trg_y])
                
                return -s_vector[-1] + coord_distance/sum_of_strained_lengths

            constraints.append({"type": "ineq", "fun": cons})
        return constraints
        
#returns a 2d array of the coordinates of all of the leaf vertices

#currently retarded----unnecessary to make an array from an array        
#s_vector =(u1x,u1y,u3x,u3y,u4x,u4y,m) format
    def _scale_initial_guess(self):
        leaf_nodes = self.all_leaf_nodes()
        pre_array = []
        for node in leaf_nodes:
            pre_array.append(self.G.node[node]['x'])
            pre_array.append(self.G.node[node]['y'])
        pre_array.append(self.scale)            
        
        s_vector0 = np.array(pre_array)
        return s_vector0 #array of vertex coordinates
                

#finds the x,y coordinates of nodes such that scale is minimized
    def scale_optimization(self):
        fun = self._scale_objective_function
        s_vector0 = self._scale_initial_guess()
        bnds = self._scale_construct_bounds()
        cons = self._scale_construct_constraints()
        
        return minimize(fun,s_vector0,method='SLSQP', bounds=bnds, constraints=cons, options={ "eps":.0001})
    
# ***functions for edge optimization***
# http://www.langorigami.com/books/ODS1e_Algorithms.pdf
# Section A.4. Edge Optimization
   
    
#returns strain    
    def _edge_objective_function(self,e_vector):
        return -e_vector[-1]
    
#create array of node coordinates and strain factor
#e_vector =(u1x,u1y,u3x,u3y,u4x,u4y,strain) format
    def _edge_initial_guess(self):
        leaf_nodes = self.all_leaf_nodes()
        pre_array = []
        strain_factor = 1.0
        for node in leaf_nodes:
            pre_array.append(self.G.node[node]['x'])
            pre_array.append(self.G.node[node]['y'])
        pre_array.append(strain_factor)
        
        e_vector0 = np.array(pre_array)
        return e_vector0
    
# create inequality for each leaf path to adjust selected edges according to a variable strain factor
# see Lang for details

    def _edge_constraints(self,selected_edges):
        leaf_nodes = self.all_leaf_nodes()
        constraints = []
        scale = self.scale
        #for all leaf paths
        for combo in itertools.combinations(leaf_nodes,2):
            source = combo[0]
            target = combo[1]
            
            #modification of sum_of_strained_lengths
            
            
            graph = self.G
            shortest_path = nx.shortest_path(graph, source, target)
            i = 0
            sum_of_strained_length = 0
            #for all edges in a leaf path
            while i < len(shortest_path)-1:
                node1 = shortest_path[i]
                node2 = shortest_path[i+1]
                edge_length = graph[node1][node2]['length']
                edge_strain = graph[node1][node2]['strain']
                
                edge = (node1, node2)
                #compute two different sums
                if edge in selected_edges:
                    selected_edge_length += edge_length
                else:
                    strained_length = (1+edge_strain) * edge_length        
                    sum_of_strained_length += strained_length
                i+=1
            
           
            source_index = leaf_nodes.index(source)
            target_index = leaf_nodes.index(target)
            
            #create a corresponding x and y index for each source and target index
            
            src_x = source_index * 2
            src_y = (source_index + 1) * 2
            trg_x = target_index * 2
            trg_y = (target_index + 1) * 2
            
            #constraint function in form where cons >=0
            def cons(e_vector):
                coord_distance = self.dist(e_vector[src_x],e_vector[src_y],e_vector[trg_x],e_vector[trg_y])
                return -e_vector[-1] + (coord_distance - fixed_strained_edge_length)/selected_edge_lengths

            constraints.append({"type": "ineq", "fun": cons})
        return  constraints   
            
            
    
    
    def edge_optimization(self):
        fun  = self._edge_objective_function
        e_vector0 = self._edge_initial_guess()
        bnds = self._edge_construct_bounds() #same bounds as scale optimize
        cons = self._edge_constraints()
        return minimize(fun,e_vector0,method= 'SLSQP', bounds = bnds,
        constrains = cons, options = {"eps":0001})



    
#import Tkinter as Tk
#from Tkinter import *

class Application(Tk.Frame):
    
#initialze frame    
    def __init__(self, master = None):
        Tk.Frame.__init__(self,master)
        self.pack()
        
        self.dimensions = None
        self.create_frame()
        self.first_widgets()
    
    def get_dimensions(self):
        return self.dimensions      
    #makes basic frame size
    def create_frame(self):
        pixel_scale = 500
        self.frame_width = pixel_scale
        self.frame_height = pixel_scale
        self.frame = Tk.Canvas(self, width = self.frame_width, height = self.frame_height)
        self.frame.pack()
        
        #image = cool_image_from_file
        #image.place location
    
    #creates the basic widgets for starting a new model, quit    
    def first_widgets(self):
        #quits the program
        self.QUIT = Tk.Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit
  
        self.QUIT.pack()
        #test: says hello
        self.hi_there = Tk.Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi
        
        self.hi_there.pack()
        
        self.bv2 = Tk.Button(root)
        self.bv2['text'] = "New Model"
        self.bv2['command'] = self.submission_box
        self.bv2.pack()
        
    #create a dialog box, wait until the box is closed before acessing it's properties
    def submission_box(self):
        inputDialog = DimSubmissionBox(root)
        self.wait_window(inputDialog.top)
        self.dimensions = inputDialog.dimensions
        self.draw_paper()
        self.add_node_box()
        
    #create origami model object
    def initialize_model(self):
    
        width = self.get_dimensions()[0]
        height = self.get_dimensions()[1]
        self.model = Model(width, height)
        
    #draws a square representing the paper
    def draw_paper(self):
        border = self.frame_width/10
        frame_width = self.frame_width
        frame_height = self.frame_height
        paper_height = self.get_dimensions()[1]
        paper_width = self.get_dimensions()[0]
       
        
        if paper_height > paper_width:
            self.frame.create_rectangle(border,border,(frame_width - border)*float(paper_width)/float(paper_height), frame_height - border, fill = "white")
        else:
            self.frame.create_rectangle(border, border, frame_width - border, (frame_width - border)*float(paper_height)/float(paper_width), fill = "white")
        
    def add_node_box(self):
        
        nodebox = NodeBox(root,self)
        self.wait_window(nodebox.top)
        #self.wait_window(inputDialog.top)
        #self.dimensions = inputDialog.dimensions
        
        
    def model_widgets(self):
        self.new_node_l = Tk.Label(root, self)
        self.new_node_l['text'] = 'new node information'
        
        self.node_entry = Tk.Entry(self)
        self.node_entry["command"]
        
        self.node_button = Tk.Button(self)
        self.node_button["text"] = 'enter new info'     
      
        
        #create a new set of widgets explicitely for adding and deleting new nodes, and accessing that information.
    
    def say_hi(self):
        print "hello!"

#Nodebox is an object which has all the information for nodes and edges. It has the capabilities to add nodes to the model, and keep track of all the information, and update that info.

class NodeBox(object):

    #the initial nodebox should have a frame and add-node
    
    def __init__(self, parent, application):
        top = self.top = Tk.Toplevel(parent)
        info = Tk.Frame(self.top)
        info.grid()
        self.add_node_stuff(info)
        self.app = application
    
    #provides interface for adding node information
    def add_node_stuff(self,info):
        self.l_source_node = Tk.Label(info)
        self.l_source_node["text"] = "Source Node"
        
        self.l_xy = Tk.Label(info)
        self.l_xy["text"] = "Coordinates (format = 'x,y')"
        
        self.e_source_node = Tk.Entry(info)
        self.e_xy = Tk.Entry(info)
        
        self.l_source_node.grid(row = 0,column = 0)
        self.e_source_node.grid(row = 0, column = 1)
        self.l_xy.grid(row = 1, column = 0)
        self.e_xy.grid(row = 1, column = 1)
        
        self.b_addnode = Tk.Button(info)
        self.b_addnode['text'] = "Add Node"
        self.b_addnode['command'] = lambda: self.add_node_info(self.app)
        self.b_addnode.grid(row = 2, columnspan = 2)
        
    #def 

    #this creates a block of information on a node
    #the info block contiains
    #name of node
    #coordinates
    #neighbors
    #
    
    
    def add_node_info(self, application):
        source_node = self.e_source_node.get()
        x_coordinate = self.coordinate_parse()[0]
        y_coordinate = self.coordinate_parse()[1]
        
        node_data = (source_node, x_coordinate, y_coordinate)
        
        #labels and shit
        #add the node with the info to Model
        
        #create widgets that represent the info
        
        pass
        
    #takes input string of the coordinates, returns a touple
    def coordinate_parse(self):
        coord_string = self.e_xy.get()
        int_or_float= re.compile("\d+\.?\d*")
        xy = re.findall(int_or_float, coord_string)
        if len(xy)!=2:
            print "ERROR: coordinates must have x and y"
        x = float(xy[0])
        y = float(xy[1])
        return (x,y)
        
class DimSubmissionBox(object):
    
    def __init__(self,parent):
        
        top = self.top = Tk.Toplevel(parent)

        
        dialog = Tk.Frame(self.top)
        dialog.grid()
        
        #height and width labels
        self.l_height = Tk.Label(dialog)
        self.l_height["text"] = "Height:"
        self.l_width = Tk.Label(dialog)
        self.l_width["text"] = "Width:"
            
        self.l_height.grid(row = 0)
        self.l_width.grid(row = 1)
        
        #height and width entry boxes
        self.e_height = Tk.Entry(dialog)
        self.e_width = Tk.Entry(dialog)
        self.e_height.grid(row = 0, column = 1)
        self.e_width.grid(row = 1, column = 1)
        
        #submits data
        self.b_submit = Tk.Button(dialog)
        self.b_submit["text"] = "Submit"
        self.b_submit["command"] = lambda: self.submit_data()
        self.b_submit.grid(row =2, columnspan = 2)

        #cancel button    
        self.b_cancel = Tk.Button(dialog)
        self.b_cancel["text"] = "Cancel"
        self.b_cancel["command"] = self.top.destroy
        self.b_cancel.grid(row = 3,columnspan = 2)
                        
    def submit_data(self):
        height_data = self.e_height.get()
        width_data = self.e_width.get()
        data = (width_data, height_data)
        if data:
            self.dimensions = data
            self.top.destroy()
            


# ***///***/// TESTING ***///***///***        
        
        
        
class TestOrigami(unittest.TestCase):
    #run these tests by placing "unittest.main()" in my file
    
    def setUp(self): #create EMU graph
        self.emu = Model(1.0,1.0)
        self.emu.add_node_to(source_node = None, x = 0.5, y = 0.25) #creates node 1
        self.emu.add_node_to(1,.5,.5) #creates node 2 attached to node1
        self.emu.add_node_to(2,.75,.75) #creates node 3 attached to node 2
        self.emu.add_node_to(2,.25,.75) #creates node 4 attached to node 2
    
    def test_add_delete(self):
        self.emu.add_node_to(3)
        self.emu.delete_node(4)
    
    def test_draw(self):
        self.emu.draw()
    
    def test_dist(self):
        hyp = self.emu.dist(3,0,4,0)
        self.assertEqual(hyp,5.0)
        
    def test_all_leaf_nodes(self):
        leaf_nodes = self.emu.all_leaf_nodes()
        self.assertEqual(leaf_nodes,[1,3,4])       
        
    def test_is_leaf_node(self):
        self.assertEqual(self.emu.is_leaf_node(1),True)
        self.assertEqual(self.emu.is_leaf_node(2),False)
        self.assertEqual(self.emu.is_leaf_node(3),True)
        self.assertEqual(self.emu.is_leaf_node(4),True)
    
    def test_all_shortest_paths(self):
        
        return None
    
    def test_all_leaf_paths(self):
        return None
    
    def test_sum_of_strained_lengths(self):
        self.assertEqual(self.emu.sum_of_strained_lengths(1,3),2.0)
        self.assertEqual(self.emu.sum_of_strained_lengths(4,2),1.0)
            
    def test_objective_function(self):
        return None
        
    def test_constraints_function_index(self):
        ln = [1,2,3]
        ln2 = [1,2,8]
        ln3 = [1,2,4,6,7,8,9,10,15,18,19,20,21,29]
        ln4 = [4,5,6]
        ln5 = [4,9,10]
    
     
    def test_initial_guess(self):
        x0 = self.emu._scale_initial_guess()
        truth_value = np.array_equal(x0,[.5,.25,.75,.75,.25,.75,1.0])   
        self.assertTrue(truth_value)
            
    
    def test_construct_constraints(self):
        self.emu._scale_construct_constraints()
    
    
    def test_construct_bounds(self):
        bnds = self.emu._scale_construct_bounds()
        x0 = self.emu._scale_initial_guess()
        self.assertEqual(len(bnds),len(x0))
        for i in range(0,len(bnds)-1,2):
            self.assertEqual(bnds[i][1],self.emu.width)
            self.assertEqual(bnds[i+1][1],self.emu.height)
        self.assertEqual(bnds[-1][0],0)
        self.assertEqual(bnds[-1][1],min(self.emu.width,self.emu.height))
    
    def test_scale_optimization(self):
        self.emu.scale_optimization()
   
    
        
# RUN TESTS        
        
    
#if __name__ == '__main__':
#    unittest.main()
    

# everything below this is mostly crap----aka one time tests to try and figure stuff out.
  
run_emu_example = False            
if run_emu_example:
    
    emu = Model(1.0,1.0)
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
rungui=True
if rungui:
    root = Tk.Tk()
    gui = Application(master = root)
    root.mainloop()
    root.destroy()    
#'''        

#there are 4 posible sets of coordinates that are correct
#(x = .7321, y = 0, x = 0, y = .7321, x = 1, y = 1, scale = .5176)


"""       
G = nx.Graph()

G.add_node(1)
G.add_node(2)
G.add_edge(1,2)

G.add_node(3)
G.add_edge(2,3)

G.add_node(4)
G.add_edge(2,4)

G.add_node(5)
G.add_edge(1,5)
G.add_node(6)
G.add_edge(1,6)

G[1][6]['color'] = 'blue'
print( G[1][6]['color'])

#crane

crane = nx.Graph()
crane.add_nodes_from([1,2,3,4,5])
crane.add_edges_from([(1,2),(1,3),(1,4),(1,5)])

crane2 = nx.Graph()
center = Node(1,.5,.5)
ll = Node(2,0.0,0.0)
lr = Node(3,1.0,0.0)
ur = Node(4,1.0,1.0)
ul = Node(5,0.0,1.0)
crane2.add_edges_from([(center,ll),(center,lr),(center,ur),(center,ul)])


six = nx.Graph()
six.add_nodes_from([1,2,3,4,5,6,7,8])
six.add_edges_from([(1,2),(2,3),(2,4),(2,5),(1,6),(1,7),(1,8)], length = 1.0,strain = 1.0)

six.node[1]['x']=.51
six.node[1]['y'] = .7
six.node[2]['x'] = .52
six.node[2]['y'] = .3

six.node[3]['x'] = .55
six.node[3]['y'] = .2
six.node[4]['x'] = .23
six.node[4]['y'] = .25
six.node[5]['x'] = .81
six.node[5]['y'] = .22

six.node[6]['x'] = .45
six.node[6]['y'] = .89
six.node[7]['x'] = .78
six.node[7]['y'] = .76
six.node[8]['x'] = .23
six.node[8]['y'] = .8


print(six[2][4]['length'])

x =six.degree(3)
print x
"""
#correct connections?
#nx.draw(six)
#plt.show()


'''
def scale_optimization(graph,width,height):

    scipy.optimize.minimize_scalar(-scale, 
'''
    #minimize (-scale) over {all vertices && scale } s.t.

    #for every path in the graph from vertex i to vertex j
    #

    #constraints
    #vertices = graph.nodes
    #from robert's program
    #leaf_nodes = get_leaf_nodes(????)
    #set up state vector??????
    #number of variables = 1+2*number_of_leaf_nodes
    #set lower bound 0, upper bound paper size for each variable.
    #(or two bounds) (Robert has info stored as vector thing)
    #note
'''    
    for node in leaf_nodes:
        graph[node]['x'] <= width ###########
        graph[node]['y'] <= height ##############
        
        for node2 in leaf_nodees:
            G = graph
            source = node
            target = node2
            sigma = sum_of_strained_lengths(graph,source,target)
            
            distance = np.sqrt((G[source]['x']-G[target]['x'])**2 + (G[source]['y']-G[target]['y'])**2)
            
            scale * sigma - distance <= 0###########
'''

'''
def edge_opimization(graph):
    #selectively lengthen flaps by the same relative amount to fill out a crease pattern.
    #keep scale m fixed.
    #subset of edges subjected to variable strain sigma
    #subset of leaf vertices allowed to move.
    
    #minimize -sigma over { sigma, all vertices} s.t.
    
    for nodde in graph:
        graph[node]['x'] <= width ###########
        graph[node]['y'] <= height ##############
    sigma * scale
'''
     
   
