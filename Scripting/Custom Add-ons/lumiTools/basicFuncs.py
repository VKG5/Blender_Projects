'''
To call this file, load it into the Blender text editor and the use the following command/code

my_module = bpy.data.texts[<nameOfModule>"Basic_Funcs.py"].as_module()

Then use my_module to access the function offered!
'''

import bpy
from math import radians
import os
import addon_utils
import re

# Getting path
#dir = os.path.dirname(bpy.data.filepath)
dir = os.path.dirname(os.path.realpath(__file__))

from . import worldSettings as worldSettings
#worldSettings = bpy.data.texts["worldSettings.py"].as_module()

from . import setMaterials as setMaterials
#setMaterials = bpy.data.texts["setMaterials.py"].as_module()

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
    if(len(bpy.context.scene.objects) > 0):
        if('EDIT' in bpy.context.mode.upper()):
            # Setting mode to OBJECT in case we are in any other mode
            bpy.ops.object.mode_set(mode='OBJECT')
            
         # Selecting everything in case nothing was selected
        bpy.ops.object.select_all(action='SELECT')
        
        # Setting active
        bpy.context.view_layer.objects.active = bpy.context.scene.objects[0]
        
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
        
# Enabling the add-on
def enableAddOn(addon_module_name):
    # Getting the state of the add-on
    loaded_default, loaded_state = addon_utils.check(addon_module_name)
    
    # Checking if already enabled
    if not loaded_state:
        addon_utils.enable(addon_module_name)
        
# Removing speical characters from name
def removeSpecial(string):
    arr = [ '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '=', '+', 
            '[', ']', '{', '}', '\\', '/', '|', ':', ';', '\'', '\"', '?', '.', 
            ',', '<', '>', " " ]
        
    for symbol in arr:
        string = string.replace(symbol, "")
        
    return string

# Remove numericals from name
def removeNumericals(string):
    for number in "0987654321":
        string.replace(number, "")
        
    return string

def convertToID(module):
    # Convert module type to string
    s = str(module)
    
    # Extracting the module name given string
    result = re.search('<module (.*) from ', s)
    
    # Removing the single quotes
    result = (result.group(1)).replace("\'", "")
    
    return result

# Installing the add-on
def installAddOn(dir, filename, extension):
    ## Debugging
    #print(dir+"\\"+filename+extension) 
    
    bpy.ops.preferences.addon_install(filepath=dir+"\\"+filename+extension)
    
    # Addons that are enabled by default
    default_addons = ["io_scene_3ds",
                  "io_scene_fbx",
                  "io_anim_bvh",
                  "io_mesh_ply",
                  "io_scene_obj",
                  "io_scene_x3d",
                  "io_mesh_stl",
                  "io_mesh_uv_layout",
                  "io_curve_svg",
                  "cycles"]
    
    # Current active add-ons
    activeAddons = []
    
    allAddons = {}
    
    # Getting the active add-ons
    for mod in bpy.context.preferences.addons:
        # Storing the active add-on names
        activeAddons.append(removeSpecial(mod.module).lower())
        
    # Getting a list of all add-ons
    for mod in addon_utils.modules():
        # Getting the module name
        key = removeSpecial(mod.bl_info['name']).lower()
        value = convertToID(mod)
        
        allAddons[key] = value
        
#    ## Debugging
#    print("\nActive Addons: ")
#    for add in activeAddons:
#        print(add)
#        
#    print("\nAll Addons: ")
#    for add in allAddons:
#        print(add, allAddons[add])

    flag = False
    
    installMod = removeSpecial(filename).lower()    
    
    print("Trying to install Mod : {}\n".format(installMod))
    
    # Getting the list of add-ons that are inactive
    for main in allAddons:
        # Iterating over add-ons that are not activated
        ## Debugging
        print("Mod name :", main)        
        for comp in activeAddons:
            if(main is not comp):
                if(main[:len(main)//2] in installMod):
                    ## Debugging
                    print("Activating : {}".format(allAddons[main]))
                    
                    enableAddOn(allAddons[main])
                    
                    # Success message
                    print("Successfully Installed the add-on:", filename)
                    flag = True
                    break
                
        if(flag):
            break
        
    ## In case the add-on fails to install
    print("Failed to install add-on {}\nPlease check if the add-on is valid".format(filename))
    
def setWorld(value, gvalue, mat):
    bpy.context.scene.render.film_transparent = value
    bpy.context.scene.cycles.film_transparent_glass = gvalue
    
    # If nothing is selected, then leave the world settings
    if(mat=='none'):
        pass
    
    # Make changes according to selection
    else:
        worldSettings.setWorld(mat)
            
def setMaterial(mat):
    # Getting a list of selected objects
    objList = bpy.context.selected_objects
    
    # Deselecting all objects
    bpy.ops.object.select_all(action="DESELECT")
    
    for obj in objList:
        # If nothing is selected, then leave the world settings
        if(mat=='none'):
            continue
        
        # Make changes according to selection
        else:
            setMaterials.setMat(obj, mat)
            
def removeVizNode():
    # Getting a list of selected objects
    objList = bpy.context.selected_objects
    
    # Deselecting all objects
    bpy.ops.object.select_all(action="DESELECT")
    
    for obj in objList:
        setMaterials.removeNode(obj)