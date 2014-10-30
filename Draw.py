

class DrawCommand:
    def __init__(self,application, current_node, source, x, y, length, strain):
        self.current = current_node
        self.source = source
        self.x = x
        self.y = y
        self.length = length
        self.strain = strain
        self.draw_node(application, self.current, self.source, self.x, self.y, self.length, self.strain)
    

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
        application.frame.delete(circle)
        application.frame.delete(dot)
        application.frame.delete(edge_label)
        application.frame.delete(node_label)
        application.frame.delete(new_line)
     
