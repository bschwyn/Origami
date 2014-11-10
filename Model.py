import networkx as nx
from scipy.optimize import minimize
import math
import matplotlib.pyplot as plt
import itertools
import numpy as np
import Application as app
import AddNodeCommand as addnodec


class Model:
    #initialize the properties of the medium (paper) that the origami model will use.
    def __init__(self, application, width = 1.0, height = 1.0):
        self.width = width
        self.height = height
        self.scale = 1.0
        self.node_counter = 1
        self.G = nx.Graph()
        self.app = application
        self.undo_stack = []
        #self.edges = {}
        #self.vertices = {}
        #self.vertex-node_indices = {}
        #self.edge_indices = {}
        #self.nodes = {}
        #self.paths = {}
        #self.leaf_vertices
        
    #add node information to the model. Can be passed information through NodeBox or directly
    def add_node_to(self, source, x, y, length = 1.0, strain = 0.0):
        self.undo_stack.append(addnodec.AddNodeCommand(self, source, x, y, length, strain))
    
    def add_node_undo(self, app):
        self.undo_stack.pop().undo(app)
    
    #returns a list of nodes
    def getAllNodes(self):
        return self.G.nodes()
        
    #get node attribute (such as coordinates)
    def getNodeAttribute(self,node,attribute):
        return self.G.node[node][attribute]
        
        
    def getEdgeAttribute(self,node1,node2,attribute):
        return self.G[node1][node2][attribute]
        
    def getNodeCounter(self):
        return self.node_counter
        
   #change edge attributes with the networkx change_attributes function
   #change coordinates through the same change_coordinates function


  
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


    #determines whether node is a leaf node (1 edge only)
    def is_leaf_node(self,node):
        leaf_nodes = self.all_leaf_nodes()
        return node in leaf_nodes

# leaf nodes are nodes with only one edge         
    def all_leaf_nodes(self):
        leaf_nodes = []
        for node in self.G:
            if self.G.degree(node) == 1:
                leaf_nodes.append(node)
        return leaf_nodes
    
     
    #returns a list of the shortest paths
    def all_shortest_paths(self):
        return all_pairs_shortest_path(self.G)

    #returns a list of all edges connected to a leaf vertext
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
            edge_length = graph.edge[node1][node2]['length']
            edge_strain = graph.edge[node1][node2]['strain']
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
            edge_length = graph.edge[node1][node2]['length']      
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
# creates a list of inequalities in the correct format for scipy.optimize.minimize
    def _scale_construct_constraints(self):
        leaf_nodes = self.all_leaf_nodes()
        constraints = []
        #all possible paths between two leaf nodes
        for combo in itertools.combinations(leaf_nodes, 2):
            source = combo[0]
            target = combo[1]
            sum_of_strained_lengths = self.sum_of_strained_lengths(source,target)
            
            source_index = leaf_nodes.index(source)
            target_index = leaf_nodes.index(target)
            
            #create a corresponding x and y index for each source and target index
            src_x = source_index * 2
            trg_x = (target_index) * 2
            src_y = (source_index * 2) + 1
            trg_y = (target_index * 2) + 1
            
            def make_lambda(x1,x2,y1,y2):
                return lambda x: -x[-1] * sum_of_strained_lengths + self.dist(x[x1], x[x2], x[y1], x[y2])
            
            constraints.append({"type": "ineq", "fun": make_lambda(src_x,trg_x,src_y,trg_y)})
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
        optimize = minimize(fun,s_vector0,method='SLSQP', bounds=bnds, constraints=cons, options={ "eps":.1, "maxiter":50, "ftol":.0001})
        
        return optimize
    
    #this determines whether or not a graph can be scale optimized
    def scale_optimization_ready(self):
        #this is a dummy return value
        #the smallest graph has 4 nodes / 3 leaf nodes, but there may be more complex structure required
        
        if len(self.all_leaf_nodes()) >= 3: #for fun
            print "scale_optimization_ready"
            return True
        else:
            return False
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

