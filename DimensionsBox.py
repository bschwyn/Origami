import Tkinter as Tk

class DimSubmissionBox(object):
    
    def __init__(self,parent):
        
        #create toplevel
        top = self.top = Tk.Toplevel(parent)
        top.wm_title("Initalize Model")

        #make new frame that above the background frame
        dialog = Tk.Frame(self.top)
        dialog.grid()
        
        #create a title
        self.l_name = Tk.Label(dialog)
        self.l_name["text"] = "Name:"
        self.l_name.grid(row = 0, column = 0)
        
        self.e_name = Tk.Entry(dialog)
        self.e_name.grid(row = 0, column = 1)
        
        #height and width labels
        self.l_height = Tk.Label(dialog)
        self.l_height["text"] = "Height:"
        self.l_width = Tk.Label(dialog)
        self.l_width["text"] = "Width:"
            
        self.l_height.grid(row = 1)
        self.l_width.grid(row = 2)
        
        #height and width entry boxes
        self.e_height = Tk.Entry(dialog)
        self.e_width = Tk.Entry(dialog)
        self.e_height.grid(row = 1, column = 1)
        self.e_width.grid(row =2, column = 1)
        
        #submits data
        self.b_submit = Tk.Button(dialog)
        self.b_submit["text"] = "Submit"
        self.b_submit["command"] = lambda: self.submit_data()
        self.b_submit.grid(row =3, columnspan = 2)

        #cancel button    
        self.b_cancel = Tk.Button(dialog)
        self.b_cancel["text"] = "Cancel"
        self.b_cancel["command"] = self.top.destroy
        self.b_cancel.grid(row = 4,columnspan = 2)
                        
    def submit_data(self):
        height_data = self.e_height.get()
        width_data = self.e_width.get()        
        
        data = (width_data, height_data)
        
        name = self.e_name.get()
        
        if data:
            self.entered_dimensions = data
            self.name = name
            self.top.destroy()
