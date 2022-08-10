import bpy
import os

# Getting path
#dir = os.path.dirname(bpy.data.filepath)
dir = os.path.dirname(os.path.realpath(__file__))

from . import importFiles as importFiles
#importFiles = bpy.data.texts["importFiles.py"].as_module()

# Global Variables
nodesModifName = "visualizationNodes"

# For adding modifiers to selected object
def addModifier(obj, name):
    modifName = nodesModifName
    
    # Adding the Remsh modifier
    obj.modifiers.new(modifName, name)
    
    ## Debugging
    #print("Successfully added the {} modifier as {}".format(name,modifName))
    
def setType(name):
    match name:
        case 'ao':
            return bpy.data.materials['AO']
        
        case 'depth':
            return bpy.data.materials['Depth']
        
        case 'direction':
            return bpy.data.materials['Direction']
        
        case 'flow':
            return bpy.data.materials['Flow']
        
        case 'normal':
            return bpy.data.materials['NormalMap']
               
        case 'opactiy':
            return bpy.data.materials['Opacity']
        
        case 'randomColor':
            return bpy.data.materials['RandomColor']
        
        case 'randomID':
            return bpy.data.materials['RandomID']
        
        case 'root':
            return bpy.data.materials['Root']
        
        case default:
            return None
        
def setValue(name):
    match name:
        case 'ao':
            bpy.data.materials['AO'].node_tree.nodes['Group'].inputs['Distance'].default_value = bpy.context.scene.aoDist
            
            bpy.data.materials['AO'].node_tree.nodes['Group'].inputs['Inside?'].default_value = bpy.context.scene.aoInside
        
        case 'depth':
            bpy.data.materials['Depth'].node_tree.nodes['Group'].inputs['Depth'].default_value = bpy.context.scene.depthDepth
            
            bpy.data.materials['Depth'].node_tree.nodes['Group'].inputs['Invert?'].default_value = bpy.context.scene.depthInvert
        
        case 'direction':
            bpy.data.materials['Direction'].node_tree.nodes['Group.001'].inputs['FlipBlue?'].default_value = bpy.context.scene.dirBlue
            
            bpy.data.materials['Direction'].node_tree.nodes['Group.001'].inputs['FlipGreen?'].default_value = bpy.context.scene.dirGreen
            
            bpy.data.materials['Direction'].node_tree.nodes['Group.001'].inputs['FlipRed?'].default_value = bpy.context.scene.dirRed
        
        case 'flow':
            bpy.data.materials['Flow'].node_tree.nodes['Group.001'].inputs['FlipGreen?'].default_value = bpy.context.scene.flowGreen
            
            bpy.data.materials['Flow'].node_tree.nodes['Group.001'].inputs['FlipRed?'].default_value = bpy.context.scene.flowRed
        
        case 'normal':
            bpy.data.materials['NormalMap'].node_tree.nodes['Group'].inputs['FlipRed?'].default_value = bpy.context.scene.normalRed
               
        case 'opactiy':
            bpy.data.materials['Opacity'].node_tree.nodes['Group'].inputs['Cut'].default_value = bpy.context.scene.opaCut
            
            bpy.data.materials['Opacity'].node_tree.nodes['Group'].inputs['Contrast'].default_value = bpy.context.scene.opaContrast
            
            bpy.data.materials['Opacity'].node_tree.nodes['Group'].inputs['Frequency'].default_value = bpy.context.scene.opaFrequency
            
            bpy.data.materials['Opacity'].node_tree.nodes['Group'].inputs['Seed'].default_value = bpy.context.scene.opaSeed
        
        case 'randomColor':
            bpy.data.materials['RandomColor'].node_tree.nodes['Group'].inputs['Contrast'].default_value = bpy.context.scene.randoContrast
            
            bpy.data.materials['RandomColor'].node_tree.nodes['Group'].inputs['Seed'].default_value = bpy.context.scene.randoSeed
        
        case 'randomID':
            bpy.data.materials['RandomID'].node_tree.nodes['Group.002'].inputs['Contrast'].default_value = bpy.context.scene.randIDContrast
        
        case 'root':
            bpy.data.materials['Root'].node_tree.nodes['Group.001'].inputs['Contrast'].default_value = bpy.context.scene.rootContrast
            
            bpy.data.materials['Root'].node_tree.nodes['Group.001'].inputs['Root'].default_value = bpy.context.scene.rootRoot
            
            bpy.data.materials['Root'].node_tree.nodes['Group.001'].inputs['Tip'].default_value = bpy.context.scene.rootTip
        
        case default:
            return None
    
def checkModif(obj):
    for modif in obj.modifiers:
        # Checking if there is already a vizNodes Modifier
        if(modif.name == nodesModifName):
            return True, modif
        
    return False, None
        
def setMat(obj, name):
    importFiles.import_mats()
    
    # Checking if the object is a valid object (MESH)
    if(obj.type == 'MESH'):
        check, modif = checkModif(obj)
        # Checking if the modifier is already present or not
        if(not check):
            ## Adding the Geo Nodes network 
            # Arguments : Object reference, Node type
            addModifier(obj, 'NODES')
        
        # If present, then let it be
        # Our procedural wear node is named GetParentData
        group = bpy.data.node_groups['GetParentData']
        
        obj.modifiers[nodesModifName].node_group = group
        
        # Turning off show in Edit Mode Wireframe option
        obj.modifiers[nodesModifName].show_in_editmode = False
        
        obj.modifiers[nodesModifName]['Input_7'] = setType(name)
        
        ## Checking if context is valid
        if(bpy.context.scene):
            setValue(name)
        
def removeNode(obj):
    # Checking if the object is a valid object (MESH)
    if(obj.type == 'MESH'):
        check, modif = checkModif(obj)
        # Checking if the modifier is already present or not
        if(check):
            obj.modifiers.remove(modif)