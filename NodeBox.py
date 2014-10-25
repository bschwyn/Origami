import Tkinter as Tk
import re

class NodeBox(object):

    #the initial nodebox should have a frame and add-node
    
    def __init__(self, parent, application):
        top = self.top = Tk.Toplevel(parent)
        dialog = Tk.Frame(self.top)
        dialog.grid()
        self.app = application
        self.add_node_widgets(dialog)
    
    #provides interface for adding node information
    def add_node_widgets(self,dialog):
        #self.cb_source_node = Tk.Radiobutton(master,
        #radio button
        
        self.l_source_node = Tk.Label(dialog)
        self.l_source_node["text"] = "Source Node:"
        self.l_source_node.grid(row = 0,column = 0)
        
        
        self.e_source_node = Tk.Entry(dialog)
        self.e_source_node.grid(row = 0, column = 1)
        
        self.l_xy = Tk.Label(dialog)
        self.l_xy["text"] = "Coordinates:"
        self.l_xy.grid(row = 1, column = 0)
        
        
        self.e_xy = Tk.Entry(dialog)
        self.e_xy.grid(row = 1, column = 1)
        
        self.l_length = Tk.Label(dialog)
        self.l_length["text"] = "Length:"
        self.l_length.grid(row = 2, column = 0)
        
        self.e_length = Tk.Entry(dialog)
        self.e_length.grid(row = 2, column = 1)
         
        self.l_strain = Tk.Label(dialog)
        self.l_strain["text"] = "Strain:"
        self.l_strain.grid(row = 3, column = 0)
        
        self.e_strain = Tk.Entry(dialog)
        self.e_strain.grid(row = 3, column = 1)
        
        
        self.b_addnode = Tk.Button(dialog)
        self.b_addnode['text'] = "Add Node"
        self.b_addnode['command'] = lambda: self.add_node_info(self.app, dialog)
        self.b_addnode.grid(columnspan = 2)
        
        """
        #making a single radiobutton that goes
        v = Tk.IntVar()
        node_list = self.app.model.getNodes()
        
        
        if len(node_list) == 1:
            print "node lsit is 1"
            self.rb_test = Tk.Radiobutton(dialog, text = "source", variable = v, value = 0).grid()
        else:
            print "node list not 1"
        """
    
        #when "Add Node" is pressed, the new node is added to the model, it is drawn, and a new radio button should appear representing that node as a possible source.
        #add radio button needs to get it's information for the name of the source from somewhere. it can either keep track here, or keep track with the same source as the names of the nodes: Model.
        #after getting the node number from application
        
        #the number of radio buttons should be dependent on the model, as opposed ot anything within add_node_info. add_node_info should get info from the radio buttons, add information to the model, which radiobutton looks at to figure out how many radio buttons to draw.
        
    def radiobutton(self, dialog):
        
        v = Tk.IntVar()
        
        #access the model through the application
        node_list = self.app.model.getNodes()
        print node_list
        
        if len(node_list) >= 1:
            button = Tk.Radiobutton(dialog, text = "source 1", variable = v, value = 1)
            button.grid()
        #else:
            #print "something else"
        
        node
            
        if len(node_list) >=1:
            
            for node in node_list:
                node_str = str(node)
                button = Tk.Radiobutton(dialog, text = "node" + node_str, variable = v, value = node)
                button.grid()
            
       # else:
       #     for node in node_list:
       #         node_str = str(node)
        #        Radiobutton(dialog, text = "node" + node_str, variable = v, value = node, command = lambda:self.setSource(node)).grid()
                #for every node in the model, create a radio button
                #get integer from node name
                #the text should be node and the related integer, variable = v, value is the integer
        #return source
    #def 

    #this creates a block of information on a node
    #the info block contiains
    #name of node
    #coordinates
    #neighbors
    #
    
    #after entry boxes are filled:
    

    
    #pass the node information to the application where the model is stored
    def add_node_info(self, application, dialog):
    
    #Something which gets information from the radiobutton goes here.
    #####
        #have default source be none ---no button
        #otherwise have source be from radiobutton
    
        if self.e_source_node.get() is "":
            source = None
        else:
            source = int(self.e_source_node.get())
    ####        
        x_coordinate = self.xy_entry_to_float()[0]
        y_coordinate = self.xy_entry_to_float()[1]
        
        if self.e_length.get() is "":
            length = 1.0
        else:
            length = float(self.e_length.get())
            
        if self.e_strain.get() is "":
            strain = 0.0
        else:
            strain = float(self.e_strain.get())
        
        
        #user input errors possible
        application.add_node_to_model(source, x_coordinate, y_coordinate, length, strain)
        application.draw_node(source, x_coordinate, y_coordinate, length, strain)
        self.radiobutton(dialog,source = None)
        
        
    #takes input string of the coordinates, returns a touple
    def xy_entry_to_float(self):
        coord_string = self.e_xy.get()
        int_or_float= re.compile("\d+\.?\d*") #really want \d+\.?\d* OR \d*\.?\d+ first covers (1 and 1.0), second covers (.2, 1.0). \d*\.\d* would cover all of these and individual periods, which seems reasonable, but may also caputre periods by themselves need to test.
        xy = re.findall(int_or_float, coord_string)
        if len(xy)!=2:
            print "ERROR: coordinates must have x and y"
        x = float(xy[0])
        y = float(xy[1])
        return (x,y)
