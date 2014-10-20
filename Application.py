import Tkinter as Tk
import DimensionsBox as dbox
import NodeBox as nbox
import Model as model


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
        
        self.bv2 = Tk.Button(self)
        self.bv2['text'] = "New Model"
        self.bv2['command'] = self.submission_box
        self.bv2.pack()
        
    #create a dialog box, wait until the box is closed before acessing it's properties
    def submission_box(self):
        inputDialog = dbox.DimSubmissionBox(self) #not sure whether this should be self or root that goes to dbox as the parent
        self.wait_window(inputDialog.top)
        dimensions = inputDialog.entered_dimensions
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
        border = self.frame_width/10
        frame_width = self.frame_width
        frame_height = self.frame_height
        paper_height = dimensions[1]
        paper_width = dimensions[0]
       
        
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
        radius = .5 #some number
        bounds = 2**.5 * radius
        #bounding box = 1.414*radius
        model = self.model
        if source is None:
            origin = self.frame.create_circle(x - bounds, y - bounds, x + bounds, x + bounds)
        else:
            model
            new_node = self.frame.create_circle(x-bounds, y-bounds, x + bounds, x + bounds)
            source_x = model.getNodeAttributes(source,"x")
            source_y = model.getNodeAttributes(source, "y")
            new_line = self.frame.create_line(source_x,source_y, x ,y)
        
            #draw circle at coordinates w/ radius
        #else
        #draw circle at coordinates
        #draw line from coordinates of source_node to new coordinates
        #remove circle at source node, replace with dot
        
        
        #create a new set of widgets explicitely for adding and deleting new nodes, and accessing that information.
    
    def say_hi(self):
        print "hello!"
