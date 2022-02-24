'''
To call this file, load it into the Blender text editor and the use the following command/code

my_module = bpy.data.texts[<nameOfModule>"Basic_Funcs.py"].as_module()

Then use my_module to access the function offered!
'''


import bpy
from math import radians
import os


# Getting path
dir = os.getcwd()


''' 
This is just some general code to set properties/modifiers to the objects that 
Will be used later on in the process 
'''
## Boilerplate Code     
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
        # Selecting all objects in case nothing is selected
        bpy.ops.object.select_all(action='SELECT')
        # Setting mode to OBJECT in case we are in any other mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Deleting everything that was present 
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        print("Successfully deleted the objects!")
    
    else:
        print("Nothing to delete! Scene already empty.")
        
    # Removing the collections
    removeCollections()
    
    # Clearing the project (Purging)
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

def printNames(trackN, apiN):
    print(trackN, apiN)