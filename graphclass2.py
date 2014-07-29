import heapq

class Vertex:
    def __init__(self,key,x,y, distance=0, pi = None): #how would I initialize a field elsewhere?
        self.id = key
        self.connectedTo = {}
        self.location = Point(x,y)
        self.distance = distance
        self.pi = None#predecessor

    def addNeighbor(self,nbr,weight = 0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id + ' connected to' + str([x.id for x in self.connectedTo]))

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key,x=0,y=0):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key,x,y)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None
   
    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,cost = 0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t],cost)
        self.vertList[t].addNeighbor(self.vertList[f],cost) #this makes all edges bidirectional

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

    def printEdges(self):
        for v in self:
            for w in v.getConnections():
                # see string formmating
                # %s means string
                #print("( %s , %s )" % (v.getId(),w.getId()))
                print ' ( {} , {} )'.format( v.getId(), w.getId() )

    def initializeSingleSource(self,sourceId):
        for v in self:
            vertex = v
            vertex.distance = float('inf')
            vertex.pi = None
        source = self.vertList[sourceId]
        source.distance = 0


    def shortestPath(self,start,end):
        
        self.initializeSingleSource(start)

        #set
        visited_vertices = {}

        #priority queue
        pq = []
        for v in self:
            vertex = v
            heapq.heappush(pq,(vertex.distance,vertex.id))
            
        while pq: #??#??#??# no sure what exactly this is doing.
           minimum = heapq.heappop(pq)[1] #extracting the nearest vertex (minimum)
           #do I really need this visited vertie thingy?

           u = self.getVertex(minimum)
        
           #relax
           for v in u.getConnections():
               if v.distance >= u.distance + u.getWeight(v):
                   v.distance = u.distance + u.getWeight(v)
                   v.pi = u
        return getVer
           
        
        
class Point:

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        


#test
#with cycles, similar to pg 659
#no coordinates
graph = Graph()
graph.addEdge("s","t",10)
graph.addEdge("t","x",1)
graph.addEdge("s","y",5)
graph.addEdge("s","z",7)
graph.addEdge("y","z",2)
graph.addEdge("y","x",9)
graph.addEdge("x","z",4)
graph.addEdge("t","y",3)
#getVertex
print graph.getVertex("s")
print graph.getVertex("not a vertex")

#get

#I don't understand the __str__ function


