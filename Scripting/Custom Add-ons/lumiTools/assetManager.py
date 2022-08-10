## The use of this file/feature is to mark the selected objects as assets. 
## TODO : You can also mark materials as assets using this.

import bpy
import os

# To add a new asset library
def addAssetLib(dir, filename, extension):
    ## Debugging
    #print(dir, filename)
    
    try:
        bpy.ops.preferences.asset_library_add(directory = dir)
        
        ## Debugging
        print("Successfully added the {} asset library!".format(filename))
    
    except:
        print("Failed to add the {} asset libray".format(filename))

# Marking selected objects as assets
def clearAssets():
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
        
        # Checking if the selected asset is an asset
        if(obj.asset_data):
            # Marking as asset
            obj.asset_clear()
        
        # Deselecting all objects
        bpy.ops.object.select_all(action="DESELECT")
        
    # Clearing the project (Purging)
    # bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

# Clearing already marked assets
def markAssets():
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
        
        ## Checking if the object isn't already an asset
        if(not obj.asset_data):
            # Generating the preview for Mesh type objects
            if(obj.type == 'MESH'):
                # Generating a preview for the asset
                obj.asset_generate_preview()
            
            # Marking as asset
            obj.asset_mark()
        
        # Deselecting all objects
        bpy.ops.object.select_all(action="DESELECT")

## TODO
def createSubLib(name):
    pass