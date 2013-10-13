# -*- coding: utf-8 -*-
from __future__ import print_function, division 
from ui_utils import TreeFrame, TextFrame
import ui_utils
try:
    import tkinter as tk
    from tkinter import ttk
    import tkinter.font as tk_font
except ImportError:
    import Tkinter as tk
    import ttk 
    import tkFont as tk_font


class MemoryFrame(TreeFrame):
    def __init__(self, master, columns):
        TreeFrame.__init__(self, master, columns)
    
    def stop_debugging(self):
        self._clear_tree()
        
    def change_font_size(self, delta):
        pass
    
        
class VariablesFrame(MemoryFrame):
    def __init__(self, master):
        MemoryFrame.__init__(self, master, ('name', 'id', 'value'))
    
        self.tree.column('name', width=90, anchor=tk.W, stretch=False)
        self.tree.column('id', width=55, anchor=tk.W, stretch=False)
        self.tree.column('value', width=150, anchor=tk.W, stretch=True)
        
        self.tree.heading('name', text='Nimi', anchor=tk.W) # TODO:
        self.tree.heading('id', text='Id', anchor=tk.W)
        self.tree.heading('value', text='Väärtus', anchor=tk.W) # TODO:
        
        self.tree.configure(displaycolumns=("name", "value"))
        #self.tree.tag_configure("item", font=ui_utils.TREE_FONT)

    def update_variables(self, variables):
        self._clear_tree()
        
        if variables:
            for name in sorted(variables.keys()):
                
                if not name.startswith("__"): # TODO: consult prefs
                    node_id = self.tree.insert("", "end", tags="item")
                    self.tree.set(node_id, "name", name)
                    self.tree.set(node_id, "id", variables[name].id)
                    self.tree.set(node_id, "value", variables[name].short_repr)
            
        
class GlobalsFrame(VariablesFrame):
    def __init__(self, master):
        VariablesFrame.__init__(self, master)

    def handle_vm_message(self, event):
        if hasattr(event, "globals"):
            # TODO: handle other modules as well
            self.update_variables(event.globals["__main__"])
    
    def show_module(self, module_name, frame_id=None):
        "TODO:"
    

class LocalsFrame(VariablesFrame):   
    def handle_vm_message(self, event):
        pass

    def show_frame(self, frame):
        "TODO:"
    

class HeapFrame(MemoryFrame):
    def __init__(self, master):
        MemoryFrame.__init__(self, master, ("id", "value"))
        
        self.tree.column('id', width=55, anchor=tk.W, stretch=False)
        self.tree.column('value', width=150, anchor=tk.W, stretch=True)
        
        self.tree.heading('id', text='Id', anchor=tk.W)
        self.tree.heading('value', text='Väärtus', anchor=tk.W) # TODO:

    def _update_data(self, data):
        self._clear_tree()
        for value_id in sorted(data.keys()):
            node_id = self.tree.insert("", "end")
            self.tree.set(node_id, "id", value_id)
            self.tree.set(node_id, "value", data[value_id])
            

    def handle_vm_message(self, event):
        if hasattr(event, "heap"):
            self._update_data(event.heap)
    
        
class ObjectInfoFrame(TextFrame):
    def __init__(self, master):
        self.font = tk_font.nametofont("TkTextFont")
        TextFrame.__init__(self, master, self.font)
        
        self.text.insert("1.0", """len(...)
    len(object) -> integer
    
    Return the number of items of a sequence or mapping.""")


