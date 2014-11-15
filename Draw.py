

class DrawCommand:
    def __init__(self,application):
        self.draw_model(application)
    
    def draw_model(self, application):
    
        #clear everything
        application.frame.delete("all")
        
        #redraw
        application.draw_new_paper()
        
        #do all the scale stuff
        paper_long_edge_pixels = application.frame_pixels - 2 * application.border_pixels
        radius = application.frame_pixels/10 # some number
        
        paper_width = float(application.getDimensions()[0])
        paper_height = float(application.getDimensions()[1])
        
        if paper_height > paper_width:
            paper_height_pixels = paper_long_edge_pixels
            paper_width_pixels = paper_shorter_edge_pixels = paper_width/paper_height * paper_long_edge_pixels
        else:
            paper_width_pixels = paper_long_edge_pixels
            paper_height_pixels = paper_shorter_edge_pixels = paper_height / paper_width * paper_long_edge_pixels
        
        #draw a dot w/ all the nodes
        for node in application.model.getAllNodes():
            #x = node["x"]
            #y = node["y"]
            #or....?
            
            x = application.model.getNodeAttribute(node,"x")
            y = application.model.getNodeAttribute(node,"y")
            #distance in pixels from corner of "paper square" to node
            x_pixels = paper_width_pixels * x / paper_width
            y_pixels = paper_height_pixels * y / paper_height
        
            #distance in pixels from corner of frame to node
            x_corner_dist = application.border_pixels + x_pixels
            y_corner_dist = application.border_pixels + y_pixels
            
            #draw dot
            dot = 2.5
            application.frame.create_rectangle(x_corner_dist - dot, y_corner_dist - dot, x_corner_dist + dot, y_corner_dist + dot, fill = "red")
            #draw label
            application.frame.create_text(x_corner_dist + 10, y_corner_dist, text = "node" + str(node) + "\n" + "(" + str(x) + "," + str(y) + ")") 
        
        #for all nodes:
        #draw a dot w/ coordinates
        
        #for all leaf nodes
        #draw a circle
        for node in application.model.all_leaf_nodes():
        
            neighbor = application.model.G.neighbors(node)[0]
            
            length = application.model.getEdgeAttribute(node, neighbor,"length")
            strain = application.model.getEdgeAttribute(node, neighbor, "strain")
            
            #coordinates of node in paper scale
            x = application.model.getNodeAttribute(node,"x")
            y = application.model.getNodeAttribute(node,"y")
            #distance in pixels from corner of "paper square" to node
            x_pixels = paper_width_pixels * x / paper_width
            y_pixels = paper_height_pixels * y / paper_height
        
            #distance in pixels from corner of frame to node
            x_corner_dist = application.border_pixels + x_pixels
            y_corner_dist = application.border_pixels + y_pixels
            
            #draw a circle
            
            
            if application.model.scale == 1.0:
                rad = length * radius
                application.frame.create_oval(x_corner_dist - rad ,y_corner_dist - rad, x_corner_dist + rad, y_corner_dist + rad)
            #after optimization
            else:
                
                rad = paper_long_edge_pixels * application.model.scale * length
                application.frame.create_oval(x_corner_dist - rad ,y_corner_dist - rad, x_corner_dist + rad, y_corner_dist + rad)
           
                
        for edge in application.model.all_edges():
        
            
            source = edge[0]
            target = edge[1]
            
            
            x = application.model.getNodeAttribute(target,"x")
            y = application.model.getNodeAttribute(target,"y")
            
            length = application.model.getEdgeAttribute(edge[0], edge[1], "length")
            strain = application.model.getEdgeAttribute(edge[0], edge[1], "strain")
                
            #draw line between nodes
            source_x = application.model.getNodeAttribute(source,"x")
            source_y = application.model.getNodeAttribute(source, "y")
            
            x_s_corner_dist = application.border_pixels + source_x * paper_width_pixels / paper_width
            y_s_corner_dist = application.border_pixels + source_y * paper_height_pixels / paper_height
            
            #distance in pixels from corner of "paper square" to node
            x_pixels = paper_width_pixels * x / paper_width
            y_pixels = paper_height_pixels * y / paper_height   
        
            #distance in pixels from corner of frame to node
            x_corner_dist = application.border_pixels + x_pixels
            y_corner_dist = application.border_pixels + y_pixels
        
            
            application.frame.create_line(x_s_corner_dist, y_s_corner_dist, x_corner_dist, y_corner_dist)
            
            
            #draw label halfway for length and strain
            x_halfway = application.border_pixels + (source_x + x) / 2 * paper_width_pixels / paper_width
            y_halfway = application.border_pixels + (source_y + y) / 2 * paper_height_pixels / paper_height
            
            application.frame.create_text(x_halfway, y_halfway, text = "Length = " + str(length) + "\n"+"Strain = " + str(strain))
        
        
            
        #for all edges
        #draw a line w/ some labels

#makes a visual representation of the node and it's connections
    def draw_node(self, application, current_node, source, x, y, length, strain):
    
        #width of square in pixels
        paper_long_edge_pixels = application.frame_pixels - 2 * application.border_pixels
        radius = application.frame_pixels/10 #some number
        
            
        #get paper size
        paper_width = float(application.getDimensions()[0])
        paper_height = float(application.getDimensions()[1])
        
        #
        if paper_height > paper_width:
            paper_height_pixels = paper_long_edge_pixels
            paper_width_pixels = paper_shorter_edge_pixels = paper_width/paper_height * paper_long_edge_pixels
        else:
            paper_width_pixels = paper_long_edge_pixels
            paper_height_pixels = paper_shorter_edge_pixels = paper_height / paper_width * paper_long_edge_pixels
        
        #distance in pixels from corner of "paper square" to node
        x_pixels = paper_width_pixels * x / paper_width
        y_pixels = paper_height_pixels * y / paper_height   
        
        #distance in pixels from corner of frame to node
        x_corner_dist = application.border_pixels + x_pixels
        y_corner_dist = application.border_pixels + y_pixels
        
        #size of rectangle at node location
        dot = 2.5
        
          
        
        if x > paper_width or y > paper_height:
            return "Error: coordinate not in bounds"
        
        
        #draw a circle
        rad = length * radius
        self.circle = application.frame.create_oval(x_corner_dist - rad ,y_corner_dist - rad, x_corner_dist + rad, y_corner_dist + rad) 
        
        #node number and coordinates label 
        self.node_label = application.frame.create_text(x_corner_dist + 10, y_corner_dist, text = "node" + str(current_node) + "\n" + "(" + str(x) + "," + str(y) + ")")  
        
        
        if source is None:
            #origin_circle = self.frame.create_oval(x - bounds, y - bounds, x + bounds, x + bounds)
            b = application.border_pixels
            
            self.dot = application.frame.create_rectangle(x_corner_dist - dot, y_corner_dist - dot, x_corner_dist + dot, y_corner_dist + dot, fill = "red")
            
        #draw a  line
        else:
            #draw rectangle dot at node location
            self.dot = application.frame.create_rectangle(x_corner_dist - dot, y_corner_dist - dot, x_corner_dist + dot, y_corner_dist + dot, fill = "black")
           
            #draw line between nodes
            source_x = application.model.getNodeAttribute(source,"x")
            source_y = application.model.getNodeAttribute(source, "y")
            
            x_s_corner_dist = application.border_pixels + source_x * paper_width_pixels / paper_width
            y_s_corner_dist = application.border_pixels + source_y * paper_height_pixels / paper_height
            
            self.new_line = application.frame.create_line(x_s_corner_dist, y_s_corner_dist, x_corner_dist, y_corner_dist)
            
            
            #draw label halfway for length and strain
            x_halfway = application.border_pixels + (source_x + x) / 2 * paper_width_pixels / paper_width
            y_halfway = application.border_pixels + (source_y + y) / 2 * paper_height_pixels / paper_height
            
            self.edge_label = application.frame.create_text(x_halfway, y_halfway, text = "Length = " + str(length) + "\n"+"Strain = " + str(strain))

    def undo(self, application):
        pass
