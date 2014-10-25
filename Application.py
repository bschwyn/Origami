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
            self.model.scale_optimization()
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
        self.model = model.Model(width, height)
        
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
        
        if paper_height > paper_width:
            paper_shorter_edge_pixels = paper_width/paper_height * paper_long_edge_pixels
            self.frame.create_rectangle(border_p,border_p,border_p + paper_shorter_edge_pixels, border_p + paper_long_edge_pixels, fill = "white")
        else:
            paper_shorter_edge_pixels = paper_height / paper_width * paper_long_edge_pixels
            self.frame.create_rectangle(border_p, border_p, border_p + paper_long_edge_pixels, border_p + paper_shorter_edge_pixels, fill = "white")
            
       #draw hash marks / paper size
       
        #create hash marker untl the end
        #x axis
        """
        marker_dist = 0
        while marker_dist < paper_height:
            marker_incr = .25
            marker_incr_pixels = 
            self.frame.create_line(border_p + 
            
            
            marker_dist += marker_incr
            self.frame.create_line(border_p + marker_dist, border_p - 10, border_p + marker_dist, border_p - 10)
            marker_dist + (frame_pixels - border_p)*float(paper_width)/float(paper_height)
        """   
       
        #for distance in range(b_p, paper_height, marker):
        #   self.frame.create(b_p- 10, b_p, b_p -3, b_p)
        
        #self.frame.create_line(b_p - 10, b_p, b_p-3, b_p)
        #self.frame.create_line(b_p, b_p - 10, b_p, b_p - 3)  
        
        #self.frame.create_line(frame_width, b_p, b_p - 10, b_p, b_p - 1)     
        
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
        paper_long_edge = self.frame_pixels - 2 * self.border_pixels
        radius = self.frame_pixels/10 #some number
        #bounds = 2**.5 * radius
        #bounding box = 1.414*radius
        
        paper_width = self.getDimensions()[0]
        paper_height = self.getDimensions()[1]
        
        scaled_width = paper_long_edge/float(paper_width)
        scaled_height = paper_long_edge/float(paper_height)
        
        x_coord = x * scaled_width
        y_coord = y * scaled_height
        
        x_corner_dist = self.border_pixels + x_coord
        y_corner_dist = self.border_pixels + y_coord
        
        #size of rectangle at node location
        dot = 2.5
        
        
        
        
        if x > paper_width or y > paper_height:
            return "Error: coordinate not in bounds"
        
        new_node = self.frame.create_oval(x_corner_dist - radius ,y_corner_dist - radius, x_corner_dist + radius, y_corner_dist + radius)   
        self.frame.create_text(x_corner_dist + 10, y_corner_dist, text = "node" + str(current_node) + "\n" + "(" + str(x) + "," + str(y) + ")")  
        
        #only draw a circle
        if source is None:
            #origin_circle = self.frame.create_oval(x - bounds, y - bounds, x + bounds, x + bounds)
            b = self.border_pixels
            
            self.frame.create_rectangle(x_corner_dist - dot, y_corner_dist - dot, x_corner_dist + dot, y_corner_dist + dot, fill = "red")
            
        #draw a circle and a line
        else:
            #circle
            #new_node = self.frame.create_oval(x_corner_dist - radius, y_corner_dist - radius, x_corner_dist + radius, y_corner_dist + radius)
            
            self.frame.create_rectangle(x_corner_dist - dot, y_corner_dist - dot, x_corner_dist + dot, y_corner_dist + dot, fill = "black")
           
            source_x = self.model.getNodeAttribute(source,"x")
            source_y = self.model.getNodeAttribute(source, "y")
            
            x_s_corner_dist = self.border_pixels + source_x * scaled_width
            y_s_corner_dist = self.border_pixels + source_y * scaled_height
            
            new_line = self.frame.create_line(x_s_corner_dist, y_s_corner_dist, x_corner_dist, y_corner_dist)
        
        
        #create a new set of widgets explicitely for adding and deleting new nodes, and accessing that information.
               
    def say_hi(self):
        print "hello!"
