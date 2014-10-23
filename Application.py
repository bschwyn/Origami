import Tkinter as Tk
import DimensionsBox as dbox
import NodeBox as nbox
import Model as model


class Application(Tk.Frame):
    
#initialze frame    
    def __init__(self, master = None):
        Tk.Frame.__init__(self,master)
        self.pack()
        self.model = None
        self.dimensions = None
        self.create_frame()
        self.widgets()
    
    def getDimensions(self):
        return self.dimensions      
    #makes basic frame size
    def create_frame(self):
        self.pixel_width = 500
        self.frame = Tk.Canvas(self, width = self.pixel_width, height = self.pixel_width)
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
        self.b_newmodel['command'] = self.submission_box
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
            self.model.scale_optimization()
        else:
            print "Error: model not ready for scale optimization yet"
            
        
    #create a dialog box, wait until the box is closed before acessing it's properties
    def submission_box(self):
        inputDialog = dbox.DimSubmissionBox(self) #not sure whether this should be self or root that goes to dbox as the parent
        self.wait_window(inputDialog.top)
        dimensions = inputDialog.entered_dimensions
        self.dimension = dimensions
        self.initialize_model(dimensions)
        self.draw_paper(dimensions)
        self.node_dialog_box()
        
    #create origami model object
    def initialize_model(self,paper_size):
    
        width = paper_size[0]
        height = paper_size[1]
        self.model = model.Model(width, height)
        
    #draws a square representing the paper
    def draw_paper(self,dimensions):
        border = self.border = self.pixel_width/10
        frame_width = self.pixel_width
        frame_height = self.pixel_width
        paper_height = dimensions[1]
        paper_width = dimensions[0]
        self.dimensions = dimensions
       
        
        if paper_height > paper_width:
            self.frame.create_rectangle(border,border,(frame_width - border)*float(paper_width)/float(paper_height), frame_height - border, fill = "white")
        else:
            self.frame.create_rectangle(border, border, frame_width - border, (frame_width - border)*float(paper_height)/float(paper_width), fill = "white")
        
    def node_dialog_box(self):
        
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

    def draw_node(self, source, x, y, length, strain):
        paper_edge_length = self.pixel_width - 2 * self.border
        radius = self.pixel_width/10 #some number
        #bounds = 2**.5 * radius
        #bounding box = 1.414*radius
        
        paper_width = self.getDimensions()[0]
        paper_height = self.getDimensions()[1]
        
        scaled_width = paper_edge_length/float(paper_width)
        scaled_height = paper_edge_length/float(paper_height)
        
        x_coord = x * scaled_width
        y_coord = y * scaled_height
        
        x_corner_dist = self.border + x_coord
        y_corner_dist = self.border + y_coord
        
        if x > paper_width or y > paper_height:
            return "Error: coordinate not in bounds"
        
        
        if source is None:
            #origin_circle = self.frame.create_oval(x - bounds, y - bounds, x + bounds, x + bounds)
            b = self.border
            self.frame.create_oval(x_corner_dist - radius ,y_corner_dist - radius, x_corner_dist + radius, y_corner_dist + radius)
        else:
            
            new_node = self.frame.create_oval(x_corner_dist - radius, y_corner_dist - radius, x_corner_dist + radius, y_corner_dist + radius)
           
            source_x = self.model.getNodeAttribute(source,"x")
            source_y = self.model.getNodeAttribute(source, "y")
            
            x_s_corner_dist = self.border + source_x * scaled_width
            y_s_corner_dist = self.border + source_y * scaled_height
            
            new_line = self.frame.create_line(x_s_corner_dist, y_s_corner_dist, x_corner_dist, y_corner_dist)
        
            #draw circle at coordinates w/ radius
        #else
        #draw circle at coordinates
        #draw line from coordinates of source_node to new coordinates
        #aremove circle at source node, replace with dot
        
        
        #create a new set of widgets explicitely for adding and deleting new nodes, and accessing that information.
    
            
            
    def say_hi(self):
        print "hello!"
