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

class Model:
    #initialize the piece of paper, dimensions, and additional properties
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
    
#add_node_to
#if there are no nodes in the graph, adds a new node w/ coordinates.
#if there are nodes in the graph, a source_node must be specified, and data is added to the new node and the new edge.
#must throw errors if: graph would not be a tree, source_node doesn't exist    
    
    def add_node_to(self, source_node = None, x = 0.0, y = 0.0, length = 1.0, strain = 0.0):
        #This makes it so that there is not needed a source node for the first time. If there is a source node for the first node, it should be ignored.
        #empty graph doing the "and source_node == None increased the speed by .001 to .008
        if len(self.G)==0 and source_node == None:
            self.G.add_node(self.node_counter,x = x, y = y)
            self.node_counter +=1         
        #adding to existing graph   
        elif source_node in self.G.nodes(): 
            new_node = self.node_counter
            self.G.add_node(new_node,x=x,y=y)
            self.G.add_edge(new_node,source_node,length = length, strain = strain)
            self.node_counter +=1            
        else:
            print "error"

#deletes a specified node and edge
            
    def delete_node(self, node):
        if len(self.G)==1:
            self.G.delete_node(1)            
        elif self.is_leaf_node(node):
            self.G.remove_node(node)            
        else:
            raise "Error: cannot delete connected node"

#draws graph
                
    def draw(self):
        nx.draw(self.G)
        plt.show()

#*** helper functions ***
         
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

    def dist(x1,x2,y1,y2):
        dist = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
        return dist
        
#possibly full of errors        
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
#x is a vector of the variables [node1_x, node1_y, node2_x, node2_y....noden_x, noden_y, scale]
    def objective_function(self,x):
        return -x[-1]

#constrains all leaf node x and y coordinates to stay within the paper boundaries.
    def construct_bounds(self):
        x_bnd = (0,self.width)
        y_bnd = (0,self.height)
        bnds = []
        leaf_nodes = self.all_leaf_nodes()
        for vertex in leaf_nodes:
            bnds.append(x_bnd)
            bnds.append(y_bnd)
        #scale represents the length of a flap of width 1.0 on the actual paper.
        theoretical_max_scale = min(self.width, self.height)
        scale_bnd = (0,theoretical_max_scale)
        bnds.append(scale_bnd)
        return bnds
        

        
    def construct_constraints(self):
        leaf_nodes = self.all_leaf_nodes()
        constraints = []
        for combo in itertools.combinations(leaf_nodes,2):
            source = combo[0]
            target = combo[1]
            sum_of_strained_lengths = self.sum_of_strained_lengths(source,target)
            #converting node # in combination to array index in x
            
            source_index = leaf_nodes.index(source)
            target_index = leaf_nodes.index(target)
            
            src_x = source_index * 2
            src_y = (source_index + 1) * 2
            trg_x = target_index * 2
            trg_y = (target_index + 1) * 2
            
            def cons(x):
                coord_distance = self.dist(x[src_x],x[src_y],x[trg_x],x[trg_y])
                
                return -x[-1] + coord_distance/sum_of_strained_lengths

            constraints.append({"type": "ineq", "fun": cons})
        return constraints
        
#returns a 2d array of the coordinates of all of the leaf vertices

#currently retarded----unnecessary to make an array from an array        
    def initial_guess(self):
        leaf_nodes = self.all_leaf_nodes()
        pre_array = []
        for node in leaf_nodes:
            pre_array.append(self.G.node[node]['x'])
            pre_array.append(self.G.node[node]['y'])
        pre_array.append(self.scale)            
        
        x0 = np.array(pre_array)
        return x0 #array of vertex coordinates
                
# ***scale optimization***
            
    def scale_optimization(self):
        #fun_old = self.objective_function
        fun = self.objective_function
        x0 = self.initial_guess()
        bnds = self.construct_bounds()
        cons = self.construct_constraints()
        
        return minimize(fun,x0,method='SLSQP', bounds=bnds, constraints=cons, options={ "eps":.0001})
    
    def all_leaf_edges(self):
        leaf_edges = []
        for node in self.G:
            if self.G.degree(node) == 1:
                leaf_edge = G.edges(node)[0]
                leaf_edges.append(leaf_edge)
        return leaf_edges
        
    def edge_function(self,x):
        return -x[-1]
    
    def edge_initial_guess(self):
        leaf_nodes = self.all_leaf_nodes()
        pre_array = []
        strain_factor = 1.0 #strain factor is just given a number
        for node in leaf_nodes:
            pre_array.append(self.G.node[node]['x'])
            pre_array.append(self.G.node[node]['y'])
        pre_array.append(strain_factor)
        
        x0 = np.array(pre_array)
        return x0
    
    
    def edge_constraints(self,selected_edges):
        leaf_nodes = self.all_leaf_nodes()
        constraints = []
        m = self.scale
        for combo in itertools.combinations(leaf_nodes,2):
            source = combo[0]
            target = combo[1]
            
            #modification of sum_of_strained_lengths
            graph = self.G
            shortest_path = nx.shortest_path(graph, source, target)
            i = 0
            sum_of_strained_length = 0
            while i < len(shortest_path)-1:
                node1 = shortest_path[i]
                node2 = shortest_path[i+1]
                edge_length = graph[node1][node2]['length']
                edge_strain = graph[node1][node2]['strain']
                if (node1,node2) in selected_edges:
                    selected_edge_length += edge_length
                else:
                    strained_length = (1+edge_strain) * edge_length        
                    sum_of_strained_length += strained_length
                i+=1
            
            
            
            source_index = leaf_nodes.index(source)
            target_index = leaf_nodes.index(target)
            
            src_x = source_index * 2
            src_y = (source_index + 1) * 2
            trg_x = target_index * 2
            trg_y = (target_index + 1) * 2
            
            def cons(x):
                coord_distance = self.dist(x[src_x],x[src_y],x[trg_x],x[trg_y])
                return -x[-1] + (coord_distance - fixed_strained_edge_length)/selected_edge_lengths

            constraints.append({"type": "ineq", "fun": cons})
        return  constraints   
            
            
    
    
    def edge_optimization(self):
        fun  = self.edge_function
        x0 = self.edge_initial_guess()
        bnds = self.construct_bounds() #same bounds as scale optimize
        cons = self.edge_constraints()
        return minimize(fun,x0,method= 'SLSQP', bounds = bnds,
        constrains = cons, options = {"eps":0001})
    
        
        

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
    
    #def test_draw(self):
     #   self.emu.draw()
        
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
        x0 = self.emu.initial_guess()
        truth_value = np.array_equal(x0,[.5,.25,.75,.75,.25,.75,1.0])   
        self.assertTrue(truth_value)
            
    
    def test_construct_constraints(self):
        self.emu.construct_constraints()
    
    
    def test_construct_bounds(self):
        bnds = self.emu.construct_bounds()
        x0 = self.emu.initial_guess()
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
            
      
emu = Model (1.0,1.0)
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
print emu.initial_guess()

big_thing = emu.scale_optimization()
print big_thing
print big_thing.message

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
