import Tkinter as Tk
import DimensionsBox as dbox
import NodeBox as nbox
import Model as model


class Application(Tk.Frame):
    
#initialze frame    
    def __init__(self, master = None):
        button_frame = Tk.Frame.__init__(self,master)
        self.pack()
        self.model = None
        self.dimensions = None
        self.create_canvas_frame()
        self.widgets()
    
    def getDimensions(self):
        return self.dimensions
         
    #makes basic frame size
    def create_canvas_frame(self):
        self.frame_pixels = 500
        self.frame = Tk.Canvas(self, width = self.frame_pixels, height = self.frame_pixels)
        self.frame.pack()
        
        #image = cool_image_from_file
        #image.place location
    
    #creates the basic widgets for starting a new model, quit    
    def widgets(self):
        #quits the program
        self.b_QUIT = Tk.Button(self)
        self.b_QUIT["text"] = "QUIT"
        self.b_QUIT["fg"] = "red"
        self.b_QUIT["command"] = self.quit
  
        self.b_QUIT.pack()
        
        #test: says hello
        self.hi_there = Tk.Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi
        
        self.hi_there.pack()
        
        self.b_newmodel = Tk.Button(self)
        self.b_newmodel['text'] = "New Model"
        self.b_newmodel['command'] = self.new_model
        self.b_newmodel.pack()
        
        #does scale optimization when ready
        self.b_optimize = Tk.Button(self)
        self.b_optimize["text"] = "scale optimization"
        self.b_optimize["command"] = self.scale_optimization_and_check
        self.b_optimize.pack()
 
    #calls optimization if ready
    def scale_optimization_and_check(self):
        if self.model == None:
            print "Error: model not initialized yet"
            
        elif self.model.scale_optimization_ready():
            print "calling scale optimization"
            optimization = self.model.scale_optimization()
            #draw new scale
        else:
            print "Error: model not ready for scale optimization yet"
            
        
    #create a dialog box, wait until the box is closed before acessing it's properties
    def new_model(self):
        #destory old windows currently running
        inputDialog = dbox.DimSubmissionBox(self) #not sure whether this should be self or root that goes to dbox as the parent
        self.wait_window(inputDialog.top)
        dimensions = inputDialog.entered_dimensions
        self.dimension = dimensions
        self.initialize_model(dimensions)
        self.draw_new_paper(dimensions)
        self.new_node_dialog_box()
        
    #create origami model object
    def initialize_model(self,paper_size):
    
        width = paper_size[0]
        height = paper_size[1]
        self.model = model.Model(self, width, height)
        
    #draws a square representing the paper
    def draw_new_paper(self,dimensions):
        #if a node submission box exists already, destroy it
        #1) check if box exists
        #2) destroy
        #another possibility
        #destroy all toplevel objects
        #if self.nodebox:
        #    self.nodebox.destroy()
        
        #p means pixels
        border_p =  self.border_pixels = self.frame_pixels/10
        frame_pixels = self.frame_pixels
        paper_height = float(dimensions[1])
        paper_width = float(dimensions[0])
        self.dimensions = dimensions
        
        paper_long_edge_pixels = frame_pixels - 2*border_p
       
        self.frame.delete("all")
        
        #draw a hamburger/hotdog rectangle of the same shape as the paper dimensions
        if paper_height > paper_width:
            paper_height_pixels = paper_long_edge_pixels
            paper_width_pixels = paper_shorter_edge_pixels = paper_width/paper_height * paper_long_edge_pixels
            self.frame.create_rectangle(border_p,border_p,border_p + paper_shorter_edge_pixels, border_p + paper_long_edge_pixels, fill = "white")
        else:
            paper_width_pixels = paper_long_edge_pixels
            paper_height_pixels = paper_shorter_edge_pixels = paper_height / paper_width * paper_long_edge_pixels
            self.frame.create_rectangle(border_p, border_p, border_p + paper_long_edge_pixels, border_p + paper_shorter_edge_pixels, fill = "white")
            
       #draw hash marks / paper size
       
        #hash markers every .25 size increments
        #width marks
        x_marker_dist = 0
        while x_marker_dist <= paper_width:
            marker_incr_p = paper_width_pixels * x_marker_dist / paper_width
            self.frame.create_line(border_p + marker_incr_p, border_p - 10, border_p + marker_incr_p, border_p - 3)
            self.frame.create_text(border_p + marker_incr_p, border_p - 17, text = str(x_marker_dist))
            x_marker_dist += .25
        
        #height marks
        y_marker_dist = 0
        while y_marker_dist <= paper_height:
            marker_incr_p = paper_height_pixels * y_marker_dist / paper_height
            self.frame.create_line(border_p - 10, border_p + marker_incr_p, border_p -3,  border_p +  marker_incr_p)
            self.frame.create_text(border_p - 23, border_p + marker_incr_p, text = str(y_marker_dist))
            y_marker_dist += .25
            
    
    
    def new_node_dialog_box(self):
        
        nodebox = nbox.NodeBox(self,self)
        #self.wait_window(inputDialog.top)
        #self.dimensions = inputDialog.dimensions ###not ture anymore
    
    
    #adds the information about the node recieved from the nodebox the model
    def add_node_to_model(self,source,x,y,length=1.0,strain=1.0):
        self.model.add_node_to(source,x,y,length,strain)  
        
        
    #I'm pretty sure this needs to be discarded    
    def model_widgets(self):
        self.new_node_l = Tk.Label(root, self)
        self.new_node_l['text'] = 'new node information'
        
        self.node_entry = Tk.Entry(self)
        self.node_entry["command"]
        
        self.node_button = Tk.Button(self)
        self.node_button["text"] = 'enter new info'     

    
#makes a visual representation of the node and it's connections
    def draw_node(self, current_node, source, x, y, length, strain):
    
        #width of square in pixels
        paper_long_edge_pixels = self.frame_pixels - 2 * self.border_pixels
        radius = self.frame_pixels/10 #some number    
            
        #get paper size
        paper_width = float(self.getDimensions()[0])
        paper_height = float(self.getDimensions()[1])
        
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
        x_corner_dist = self.border_pixels + x_pixels
        y_corner_dist = self.border_pixels + y_pixels
        
        #size of rectangle at node location
        dot = 2.5
        
          
        
        if x > paper_width or y > paper_height:
            return "Error: coordinate not in bounds"
        
        
        #draw a circle
        rad = length * radius
        new_node = self.frame.create_oval(x_corner_dist - rad ,y_corner_dist - rad, x_corner_dist + rad, y_corner_dist + rad) 
        
        #node number and coordinates label 
        self.frame.create_text(x_corner_dist + 10, y_corner_dist, text = "node" + str(current_node) + "\n" + "(" + str(x) + "," + str(y) + ")")  
        
        
        if source is None:
            #origin_circle = self.frame.create_oval(x - bounds, y - bounds, x + bounds, x + bounds)
            b = self.border_pixels
            
            self.frame.create_rectangle(x_corner_dist - dot, y_corner_dist - dot, x_corner_dist + dot, y_corner_dist + dot, fill = "red")
            
        #draw a circle and a line
        else:
            #draw rectangle dot at node location
            self.frame.create_rectangle(x_corner_dist - dot, y_corner_dist - dot, x_corner_dist + dot, y_corner_dist + dot, fill = "black")
           
            #draw line between nodes
            source_x = self.model.getNodeAttribute(source,"x")
            source_y = self.model.getNodeAttribute(source, "y")
            
            x_s_corner_dist = self.border_pixels + source_x * paper_width_pixels / paper_width
            y_s_corner_dist = self.border_pixels + source_y * paper_height_pixels / paper_height
            
            new_line = self.frame.create_line(x_s_corner_dist, y_s_corner_dist, x_corner_dist, y_corner_dist)
            
            
            #draw label halfway for length and strain
            x_halfway = self.border_pixels + (source_x + x) / 2 * paper_width_pixels / paper_width
            y_halfway = self.border_pixels + (source_y + y) / 2 * paper_height_pixels / paper_height
            
            self.frame.create_text(x_halfway, y_halfway, text = "Length = " + str(length) + "\n"+"Strain = " + str(strain))
            
            
        
        
        #create a new set of widgets explicitely for adding and deleting new nodes, and accessing that information.
               
    def say_hi(self):
        print "hello!"
        
    def draw_scaled_model(self, optimize_return_object):
        new_x_vector = optimize_return_objects.x
        new_scale = new_x_vector[-1]

class Draw(Application):
    def __init__(self,application, current_node, source, x, y, length, strain):
        self.current = current_node
        self.source = source
        self.x = x
        self.y = y
        self.length = length
        self.strain = strain
        self.draw_node(self.current, self.source, self.x, self.y, self.length, self.strain)
    

    def draw_node(self, current_node, source, x, y, length, strain):
    
        #width of square in pixels
        paper_long_edge_pixels = application.frame_pixels - 2 * application.border_pixels
        radius = self.frame_pixels/10 #some number
        
            
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
        x_corner_dist = self.border_pixels + x_pixels
        y_corner_dist = self.border_pixels + y_pixels
        
        #size of rectangle at node location
        dot = 2.5
        
          
        
        if x > paper_width or y > paper_height:
            return "Error: coordinate not in bounds"
        
        
        #draw a circle
        rad = length * radius
        self.circle = self.frame.create_oval(x_corner_dist - rad ,y_corner_dist - rad, x_corner_dist + rad, y_corner_dist + rad) 
        
        #node number and coordinates label 
        self.node_label = self.frame.create_text(x_corner_dist + 10, y_corner_dist, text = "node" + str(current_node) + "\n" + "(" + str(x) + "," + str(y) + ")")  
        
        
        if source is None:
            #origin_circle = self.frame.create_oval(x - bounds, y - bounds, x + bounds, x + bounds)
            b = self.border_pixels
            
            self.dot = self.frame.create_rectangle(x_corner_dist - dot, y_corner_dist - dot, x_corner_dist + dot, y_corner_dist + dot, fill = "red")
            
        #draw a  line
        else:
            #draw rectangle dot at node location
            self.dot = self.frame.create_rectangle(x_corner_dist - dot, y_corner_dist - dot, x_corner_dist + dot, y_corner_dist + dot, fill = "black")
           
            #draw line between nodes
            source_x = self.model.getNodeAttribute(source,"x")
            source_y = self.model.getNodeAttribute(source, "y")
            
            x_s_corner_dist = self.border_pixels + source_x * paper_width_pixels / paper_width
            y_s_corner_dist = self.border_pixels + source_y * paper_height_pixels / paper_height
            
            self.new_line = self.frame.create_line(x_s_corner_dist, y_s_corner_dist, x_corner_dist, y_corner_dist)
            
            
            #draw label halfway for length and strain
            x_halfway = self.border_pixels + (source_x + x) / 2 * paper_width_pixels / paper_width
            y_halfway = self.border_pixels + (source_y + y) / 2 * paper_height_pixels / paper_height
            
            self.edge_label = self.frame.create_text(x_halfway, y_halfway, text = "Length = " + str(length) + "\n"+"Strain = " + str(strain))

    def undo(self):
        self.delete(circle)
        self.delete(dot)
        self.delete(edge_label)
        self.delete(node_label)
        self.delete(new_line)
            

