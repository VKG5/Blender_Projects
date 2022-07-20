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
# For clearing the outliner
def removeCollections():
    # Deleting all collections
    for coll in bpy.data.collections: 
        ## Debugging
        #print(coll.name)
        
        # If it is a valid collection, then remove it
        if(coll):
            bpy.data.collections.remove(coll)

# Clearing the scene
def deleteAll():
    # Checking if scene is already empty
    if(len(bpy.data.scenes['Scene'].objects) > 0):
         # Selecting everything in case nothing was selected
        bpy.ops.object.select_all(action='SELECT')
            
        # Setting mode to OBJECT in case we are in any other mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Deleting everything that was present 
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        ## Logging
        print("Successfully deleted the objects!")
            
    else:
        print("Nothing to delete! Scene already empty.")
    
    # Removing the collections
    removeCollections()
    
    # Clearing the project (Purging)
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

# To apply all the modifiers on an object
def apply_modifiers():
    # Getting a list of selected objects
    objList = bpy.context.selected_objects
            
    ## Debugging
    #print(objList)
    
    # Deselecting all objects
    bpy.ops.object.select_all(action="DESELECT")
    
    # Iterating over the selected objects
    for obj in objList:
        obj.select_set(True)
        
        # Setting the selected object as active obj
        bpy.context.view_layer.objects.active = obj
        
        for modifiers in obj.modifiers:
            # We don't bake/apply the armature
            if(modifiers.name == 'Armature'):
                continue
                
            else:
                bpy.ops.object.modifier_apply(modifier = modifiers.name)
            
        # Deselecting all objects
        bpy.ops.object.select_all(action="DESELECT")
                    
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