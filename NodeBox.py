import Tkinter as Tk
import re
import sys

class NodeBox(object):

    #the initial nodebox should have a frame and add-node
    
    def __init__(self, parent, application):
        top = self.top = Tk.Toplevel(parent)
        top.config(background = "#CCFFCC")
        top.wm_title("add nodes")
        source_frame = Tk.Frame(self.top)
        source_frame.grid(row = 0,column= 0)
        
        #self.wm_title("Title")
        entry_frame = Tk.Frame(self.top)
        entry_frame.grid(row = 1, column = 0, padx = 10, pady = 10)
        
        self.app = application
        self.add_node_widgets(entry_frame, source_frame)
        
        self.radiobuttonstack = []
        #this is the storage variable for the radio_buttons
        self.rb_var = Tk.IntVar()
    
    #provides interface for adding node information
    def add_node_widgets(self,entry_frame,source_frame):
        
        self.l_source_node = Tk.Label(source_frame)
        self.l_source_node["text"] = "Source Node:"
        self.l_source_node.grid(row = 0,column = 0)
        
        self.l_xy = Tk.Label(entry_frame)
        self.l_xy["text"] = "Coordinates:"
        self.l_xy.grid(row = 1, column = 0)
        
        
        self.e_xy = Tk.Entry(entry_frame)
        self.e_xy.grid(row = 1, column = 1)
        
        self.l_length = Tk.Label(entry_frame)
        self.l_length["text"] = "Length:"
        self.l_length.grid(row = 2, column = 0)
        
        self.e_length = Tk.Entry(entry_frame)
        self.e_length.grid(row = 2, column = 1)
         
        self.l_strain = Tk.Label(entry_frame)
        self.l_strain["text"] = "Strain:"
        self.l_strain.grid(row = 3, column = 0)
        
        self.e_strain = Tk.Entry(entry_frame)
        self.e_strain.grid(row = 3, column = 1)
        
        
        self.b_addnode = Tk.Button(entry_frame)
        self.b_addnode['text'] = "Add Node"
        self.b_addnode['command'] = lambda: self.add_node_info(self.app, source_frame)
        self.b_addnode.grid(columnspan = 2)
        
        self.b_undo = Tk.Button(entry_frame)
        self.b_undo['text'] = "Undo"
        self.b_undo['command'] = lambda: self.undo_add_node(self.app)
        self.b_undo.grid(columnspan = 2)

        print("Formatting: 'float, float' for coordinates, length and strain can be int or float, default to 1", sys.stderr)

        
  

    #this creates a block of information on a node
    #the info block contiains
    #name of node
    #coordinates
    #neighbors
    #after entry boxes are filled:

    
    #pass the node information from the user input box to the application (and from there to model)
    def add_node_info(self, application, frame):

        #get source node from radiobutton 
        #if there is noghting added to the model yet
        if self.rb_var.get() == 0 and len(application.model.getAllNodes()) == 0:
           source = None
        #get the node number from the radio button
        elif self.rb_var.get() != 0:
            source = self.rb_var.get()
        else:
            print("Error: node must have source", sys.stderr)

        #parse coordinate entry into x and y
        x_coordinate = self.xy_entry_to_float()[0]
        y_coordinate = self.xy_entry_to_float()[1]
        
        #get length and strain entries
        if self.e_length.get() is "":
            length = 1.0
        else:
            length = float(self.e_length.get())
            
        if self.e_strain.get() is "":
            strain = 0.0
        else:
            strain = float(self.e_strain.get())
        
        
        #user input errors possible
        application.move_node_info_from_app_to_model(source, x_coordinate, y_coordinate, length, strain)
        
        #bad form possibly, but an easy hack
        node_list = application.model.getAllNodes()
        current_node = list(node_list)[-1]
        
        button = Tk.Radiobutton(frame, text = "node" + str(current_node), variable = self.rb_var, value = current_node)
        button.grid( columnspan = 2)
        self.radiobuttonstack.append(button)
    
    def undo_add_node(self,application):
        application.add_node_undo()
        rb = self.radiobuttonstack.pop()
        rb.destroy()
        #undo add radio button
        
    #takes input string of the coordinates, returns a touple
    def xy_entry_to_float(self):
        coord_string = self.e_xy.get()
        int_or_float= re.compile("\d+\.?\d*") #really want \d+\.?\d* OR \d*\.?\d+ first covers (1 and 1.0), second covers (.2, 1.0). \d*\.\d* would cover all of these and individual periods, which seems reasonable, but may also caputre periods by themselves need to test.
        xy = re.findall(int_or_float, coord_string)
        if len(xy)!=2:
            print("ERROR: coordinates must have x and y", sys.stderr)
        x = float(xy[0])
        y = float(xy[1])
        return (x,y)
        
