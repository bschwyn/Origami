#Understanding my origami project:

#input: connections in a graph and data attached to that
#lengths and connections go on to an optimization program

#perhaps I can put the data in the form

#example is going to be a human stick figure

#adjacency List representation

#A space-efficient way to implement a sparsely connected graph is with an adjacency list.
class Point:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y

#class Edge:
 #   def __init__(self, length, strain = 0):
 #       self.id = #the two vertices?

class Vertex:
    def __init__(self, key, x=0,y=0): #the constructor! give key on initialization
        self.id = key #ask what id is, get key
        self.connectedTo = {} #a dictionary which starts out as empty
        data = Point(x,y)

    def addNeighbor(self,nbr,length = 0,strain = 0): #weight is length
        self.conntectedTo[nbr] = data

    def __str__(self): #this gives a verbal description of the connection ('key1' is connected to...'key2')
        return str(self.id) + ' connectedTo: ' +str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys() #this gives a list of the keys in the dict.
    #nbr's are keys, so are listed

    def getID(self):
        return self.id
    
    def getLength(self,nbr):
        return self.connectedTo[nbr]

    #advanced functions
    #def GetLoc(self):
    #    return self.##############
    #?#?#?#?#?#
    #def GetTreeNode(self):
     #   #?#?#?#?#?#
    #ignoring symmetry for now

"""Define U to be the set of all vector-valued vertex coordinates u_i,
i in I^n, where I^n is a set of vertex indices: I^n = {1..n_n} Each vertex
u_i has coordinate variables u_i,x, and u_i,y.

Define E to be the set of all edges e_i, i in I^e, where I^e is a set of
edge indices I^e = {1..n_e}. Each edge contains exactly two nodes n_i,
n_j, in e_k. Eache edge e_i has a length l_i and a fractional distortion,
called *strain*, sigma_i.

Each vertex u_i, corresponds one-to-one with the node n_i.

Define U^t to be the set of leaf vertices, which are those vertices that
correspond to a node connected to exactly one edge. Define I^tn to be the
set of leaf node indices. Clearly, U^t is a subset of U and I^tn is a
subset of I^n.

Define P to be the set of all paths, p_ij
"""
    ##
    #Constructor
    #tmVertex(tmTree* aTree);
    #tmVertex(tmTree* aTree, tmVertexOwner* aVertexOwner, tmPoint aLoc,
    #tmFloat aElevation, bool aIsBorderVertex, tmNode* aTreeNode = 0);
    #why are there two tmVertex thingies?

    #other functions (from tmVertex.cpp and .h
    #IsMajorVertex
    #IsMinorVertex
    ###????
    #"Register with tmTree"
        #mTree->mVertices.push_back(this)
        #mIndex = mTree->mVertices.size()
    #"initialize member data"
        #mLoc = tmPoint(0.,0.)
        #mElevation = 0.
        #mIsBorderVertex = false
        #mTreeNode = 0
        #mLeftPseudohingeMate = 0
        #mRightPseudoingeMate = 0
        #mDepth = DEPTH_NOT_SET;
        #mDiscreteDepth = size_t(-1)
    
            #owner???
        #mVerteOwner = 0

    #things that happen in addition
    #constructor---more stuff is constructed... owner???
    #more things initialized (aLoc, aElevation, aIsBorderVertex, mTreeNode=aTreenNode???

        #??owner thingies
        #reutrn owner
        #get owerner as path

     #GenNumMajorCreases
    #GetNumHingeCreases
    #IsAxialVertex
    #IsAxialOrGussetVertex
    #IsHingeVertex
    #GetDegree
    #Return first incident hinge crease
    #GetAxialOrGussetCreases
    #GetHingeCreases
    #SwapLinks
    #ClearCleanupData
    #VerticesSameLoc
    #Putv5Self, Getv5Self
    
    
    
    
    

#the graph class also has a dictionary----of vertices.
#while each vertex keeps track of it's neighbors
#they can't keep track of them *as vertices* so you need to go one level of abstraction higher
    
class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices+1
        newVertex = Vertex(key)#calls Vertex class
        self.vertList[key] = newVertex #the item added to the dictionary is newVertex-the actual vertex from the Vertex class
        return newVertex #why return it?
    
    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n): #why do some functions have __f__
        return n in self.vertList

    def addEdge(self,f,t,edgelength = 0,edgestrain = 0): #should length of an edge be given a different name as opposed to length between vertices? (cost vs. weight)
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t],edgelength=0, edgestrain=0)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values()) #I don't know what this does


#perhaps I should have a NODE class where you add nw
