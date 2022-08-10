import bpy
import os

# Getting path
#dir = os.path.dirname(bpy.data.filepath)
dir = os.path.dirname(os.path.realpath(__file__))

from . import importFiles as importFiles
#importFiles = bpy.data.texts["importFiles.py"].as_module()

def setType(name):
    match name:
        case 'blank':
            # Checking if the required world exists or not
            if(bpy.data.worlds['WorldW']):
                bpy.context.scene.world = bpy.data.worlds['WorldW']
            
            return 
        
        case 'black':
            # Checking if the required world exists or not
            if(bpy.data.worlds['BlackW']):
                bpy.context.scene.world = bpy.data.worlds['BlackW']
            
            return
                
        case 'white':
            # Checking if the required world exists or not
            if(bpy.data.worlds['WhiteW']):
                bpy.context.scene.world = bpy.data.worlds['WhiteW']
            
            return
         
        case 'grey':
            # Checking if the required world exists or not
            if(bpy.data.worlds['MidW']):
                bpy.context.scene.world = bpy.data.worlds['MidW']
                
            return
        
        case 'normal':
            # Checking if the required world exists or not
            if(bpy.data.worlds['NormalW']):
                bpy.context.scene.world = bpy.data.worlds['NormalW']
                
            return
        
        case default:
            print("Not valid world!")
            return 
        
def setWorld(name):
    importFiles.import_world()
    
    # If there is a world present
    if(len(bpy.data.worlds) > 0):    
        setType(name)
        
    else:
        bpy.ops.world.new()
        setType(name)