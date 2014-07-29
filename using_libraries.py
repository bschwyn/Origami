import networkx as nx
import numpy as np
from scipy.optimize import minimize
import math

import matplotlib.pyplot as plt
import unittest
import itertools

class Node:
    def __init__(self,key,x,y):
        self.id = key
        self.x = x
        self.y = y

#class rectangle:
#   def __init__(self,width,height):
#        self.width = width
#        self.height = height

class Model:
    #initialize the piece of paper, dimensions, and additional properties
    def __init__(self,width = 1.0, height = 1.0):
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
    
    
    
    def add_node_to(self, source_node = None, x = .5, y = self.height/2, length = 1.0, strain = 1.0):
        #This makes it so that there is not needed a source node for the first time. If there is a source node for the first node, it should be ignored.
        if len(self.G)==0:
            self.G.add_node(self.node_counter)
            self.node_counter +=1
        else:
            
        #when there is already an existing node
            new_node = self.node_counter
            self.G.add_node(new_node)
            self.G.add_edge(new_node,source_node,length = length, strain = strain)
            self.node_counter +=1
            #check if leaf node
            
    def delete_node(self, node):
        if self.node_counter == 2:
            self.G.delete_node(1)
        elif self.is_leaf_node(node):
            self.G.remove_node(node)
        else:
            raise "Error: cannot delete connected node"
                
    def draw(self):
        nx.draw(self.G)
        plt.show()
         
    def all_leaf_nodes(self):
        leaf_nodes = set()
        for node in self.G:
            if self.G.degree(node) == 1:
                leaf_nodes.add(node)
        return leaf_nodes
    
    def is_leaf_node(self,node):
        leaf_nodes = self.all_leaf_nodes()
        return node in leaf_nodes
    
    def all_shortest_paths(self):
        return all_pairs_shortest_path(self.G)
        
        
    def all_leaf_paths(self):
        leaf_nodes = all_leaf_nodes(self.G)
        all_paths = all_pairs_shortest_path(self.G) #returns {source : {target1 : [path1] , ... , targetn:[pathn]}, ... }
        #filter dictionary for all sources that are 
        leaf_paths = {leaf_node: all_paths[leaf_node] for node in leaf_nodes}
        return leaf_paths  
        
        
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
    
    def objective_function():
        return -m
    
    def construct_bounds(self):
        bnd1 = (0,self.width)
        bnd2 = (0,self.height)
        bnds = ()
        leaf_nodes = self.all_leaf_nodes()
        for vertex in leaf_nodes:
            bnds += bnd1
            bnds += bnd2
        return bnds
        
    def construct_constraints(self):
        leaf_nodes = self.all_leaf_nodes()
        constraints = []
        for combo in itertools.combinations(leaf_nodes,2):
            source = combo[0]
            target = combo[1]
            A = self.sum_of_strained_lengths(source,target)
            B = math.sqrt((source.x-target.x)**2 +(source.y - target.y)**2)
            C = B/A
            fun = self.scale - C
            constraints.append(fun)
        constraints2 = []
        for constraint in constraints:
            constraint_dict = {"type": "ineq", "fun": constraint}
            constraints2.append(constraint_dict)
        return constraints2
            
    def scale_optimization(self):
        leaf_nodes = self.all_leaf_nodes(self.G)
        
        fun = self.objective_function()
        x0 = [] #array of vertex coordinates
        bounds = self.calculate_bounds()
        constraints = self.calculate_contraints()
        
        scipy.optmize.minimize(fun,x0,args=(),method=SLSQP,jac=None,hess=None,hessp=None,bounds=None,constraints=(),tol=None,callback=None,options=None)
        
class TestOrigami(unittest.TestCase):
    #run these tests by placing "unittest.main()" in my file
    
    def setUp(self): #create EMU graph
        self.emu = Model (1.0,1.0)
        self.emu.add_node_to() #creates node 1
        self.emu.add_node_to(1) #creates node 2 attached to node1
        self.emu.add_node_to(2) #creates node 3 attached to node 2
        self.emu.add_node_to(2) #creates node 4 attached to node 2
    
    def test_add_delete(self):
        self.emu.add_node_to(3)
        self.emu.delete_node(4)
    
    #def test_draw(self):
    #    self.emu.draw()
        
    def test_all_leaf_nodes(self):
        leaf_nodes = self.emu.all_leaf_nodes()
        self.assertEqual(leaf_nodes,set([1,3,4]))       
        
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
        return None
    
    def test_objective_function(self):
        return None
    
    def test_construct_constraints(self):
        return None
    
    def test_construct_bounds(self):
        return None
    
    def test_scale_optimization(self):
        return None
    
if __name__ == '__main__':
    unittest.main()        
       
emu = Model (1.0,1.0)
emu.draw()
emu.add_node() #creates node 1
emu.draw()
emu.add_node(1) #creates node 2 attached to node1
emu.draw()
emu.add_node(2) #creates node 3 attached to node 2
emu.draw()
emu.add_node(2)
emu.draw()     

       
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
#correct connections?
#nx.draw(six)
#plt.show()

#def find_leaf_vertices(graph):
    #for each node in the graph
    #test if the number of edges is == 1
    #if edge ==1
    #put that node into an array
    #return the array of all leaf vertices
    
def find_leaf_vertices(graph):
    leaf_nodes = []
    for node in graph:
        if graph.degree(node) == 1:
            leaf_nodes.append(node)
    return leaf_nodes
    
shortest_path = nx.shortest_path(six,6,4)


def sum_of_strained_lengths(graph,source, target):
    shortest_path = nx.shortest_path(graph,source, target)
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
    
test = sum_of_strained_lengths(six,6,4)
print "sum_of_strained_lengts"
print test
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
#main class---create a new origami figure

#make a pallate/square

#create graph

#def leaf_vertices(G):

#add node
#def add_node(G):
  # G.add_node


#def scale_optimization(rectangle,leaf_vertices):



#class TestOrigamiGraph(unittest.TestCase):
