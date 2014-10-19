import Tkinter as Tk
import re

class NodeBox(object):

    #the initial nodebox should have a frame and add-node
    
    def __init__(self, parent, application):
        top = self.top = Tk.Toplevel(parent)
        dialog = Tk.Frame(self.top)
        dialog.grid()
        self.add_node_widgets(dialog)
        self.app = application
    
    #provides interface for adding node information
    def add_node_widgets(self,dialog):
        self.l_source_node = Tk.Label(dialog)
        self.l_source_node["text"] = "Source Node"
        
        self.l_xy = Tk.Label(dialog)
        self.l_xy["text"] = "Coordinates (format = 'x,y')"
        
        self.e_source_node = Tk.Entry(dialog)
        self.e_xy = Tk.Entry(dialog)
        
        self.l_source_node.grid(row = 0,column = 0)
        self.e_source_node.grid(row = 0, column = 1)
        self.l_xy.grid(row = 1, column = 0)
        self.e_xy.grid(row = 1, column = 1)
        
        self.b_addnode = Tk.Button(dialog)
        self.b_addnode['text'] = "Add Node"
        self.b_addnode['command'] = lambda: self.add_node_info(self.app)
        self.b_addnode.grid(row = 2, columnspan = 2)
        
    #def 

    #this creates a block of information on a node
    #the info block contiains
    #name of node
    #coordinates
    #neighbors
    #
    
    
    def add_node_info(self, application):
        source_node = self.e_source_node.get()
        x_coordinate = self.coordinate_parse()[0]
        y_coordinate = self.coordinate_parse()[1]
        application.add_node_to_model(source_node,x_coordinate,y_coordinate)
        
        
    #takes input string of the coordinates, returns a touple
    def coordinate_parse(self):
        coord_string = self.e_xy.get()
        int_or_float= re.compile("\d+\.?\d*")
        xy = re.findall(int_or_float, coord_string)
        if len(xy)!=2:
            print "ERROR: coordinates must have x and y"
        x = float(xy[0])
        y = float(xy[1])
        return (x,y)
