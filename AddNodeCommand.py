import Application as app

class AddNodeCommand:
    def __init__(self, model, source, x, y, length, strain):
        self.source = source
        self.x = x
        self.y = y
        self.length = length
        self.strain = strain
        self.add_node_to(model, self.source, self.x, self.y, self.length, self.strain)
        
    def add_node_to(self, model, source_node = None, x = 0.0, y = 0.0, length = 1.0, strain = 0.0):
        
        if x > model.width or y > model.height or x<0 or y <0:
            print "Error: coordinates not in scope"
        elif length < 0 or strain < 0:
            print "Error: length and strian must be positive"
             
        #if this is the first node
        elif len(model.G)==0 and source_node == None:
            model.G.add_node(model.node_counter, x = x, y = y)
            app.DrawCommand(model.app, model.node_counter, source_node, x, y, length, strain)
            model.node_counter +=1
        #adding attional nodes 
        elif source_node in model.G.nodes(): 
            new_node = model.node_counter
            model.G.add_node(new_node,x=x,y=y)
            model.G.add_edge(new_node,source_node,length = length, strain = strain)        
            app.DrawCommand(model.app, model.node_counter, source_node, x, y, length, strain)
            model.node_counter +=1
        else:
            print "Error: source not found"
    
    def undo(self):
       # remove_node()
       delete_node()
