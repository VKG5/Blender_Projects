'''
To call this file, load it into the Blender text editor and the use the following command/code

my_module = bpy.data.texts[<nameOfModule>"Basic_Funcs.py"].as_module()

Then use my_module to access the function offered!
'''


import bpy
from math import radians
import os

# Getting path
#dir = os.path.dirname(bpy.data.filepath)
dir = os.path.dirname(os.path.realpath(__file__))


''' 
This is just some general code to set properties/modifiers to the objects that 
Will be used later on in the process 
'''             
# To get the original object
def getOriginalObject():
    # Getting a list of selected objects
    objList = bpy.context.selected_objects
            
    ## Debugging
    #print(objList)
    
    # Deselecting all objects
    bpy.ops.object.select_all(action="DESELECT")
        
    for obj in objList:    
        # Making sure the object is selected
        obj.select_set(True)
        
        bpy.context.view_layer.objects.active = obj
        
        # Duplicating the object
        bpy.ops.object.duplicate_move()
        
        obj.select_set(False)
        
        newObj = bpy.context.active_object
        newObj.select_set(True)
        
        bpy.context.view_layer.objects.active = newObj
        
        # Removing the modifiers to get the original object
        bpy.ops.object.delete_all_modifiers()
        
        newObj.name = obj.name + "_Orig"
        
        # Deselecting the newly created object
        bpy.ops.object.select_all(action="DESELECT")