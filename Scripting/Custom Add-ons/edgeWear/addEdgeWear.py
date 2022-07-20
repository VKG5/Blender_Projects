import bpy
import os

# Getting path
#dir = os.path.dirname(bpy.data.filepath)
dir = os.path.dirname(os.path.realpath(__file__))

# Global Variables
nodesModifName = 'edgeNODES'
remeshModifName = 'edgeREMESH'

# Appending files from the baseNodes.blend file
def appendFile():
    ## Debugging
    #print(dir)
    
    # Defining variables
    filePath = dir+"\\baseNodes.blend"
    fileType = "NodeTree"
    fileName = "chippedEdges"
    
    # Checking if the node network is already present
    for nodes in bpy.data.node_groups:
        if(nodes.name == fileName):
            print("Node network already added!")
            break
            
    bpy.ops.wm.append(
        filepath = os.path.join(filePath, fileType, fileName),
        directory = os.path.join(filePath, fileType),
        filename = fileName
    )
    
    print("Successfully added the node network {}".format(fileName))
    
# For adding modifiers to selected object
def addModifier(obj, name):
    modifName = "edge" + name
    
    # Adding the Remsh modifier
    obj.modifiers.new(modifName, name)
    
    print("Successfully added the {} modifier as {}".format(name,modifName))
    
'''
We can access the Geometry Nodes Inputs using 
bpy.context.object.modifier[<nodeSystemName>]['Input_<inputPosition>'] = value

2 = Wear Amount
3 = SubDiv Levl
4 = Noise Randomness
5 = Noise Scale
6 = Noise Detail
7 = Distortion
8 = Wear Factor

***NEED TO USE THE
bpy.context.object.update_tag() function after every change!!
'''
# Exposed parameters to update the edge wear
def changeEdgeParams(objList, wear=0.0, subDiv = 0, noiseRando = 0.0, noiseScale = 0.0, noiseDetail = 0.0, dist = 0.0, wearFac = 0.0, remeshMode = 'SHARP', remeshDetail = 0, remeshScale = 0.0, remeshSharpness = 0.0, remeshShade = False):
    # Deselecting all objects
    bpy.ops.object.select_all(action="DESELECT")
    
    # Iterating over the selected objects
    for obj in objList:
        # Checking if the selected object is a mesh
        if(obj.type == 'MESH'):
            # Setting context
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj 
            
            # Checking if the modifiers are already present or not
            if(obj.modifiers):
                flag1, flag2 = True, True
                
                # Checking if the Nodes Modifier is present
                if(obj.modifiers[nodesModifName]):
                    # change the Geo Nodes Params
                    obj.modifiers[nodesModifName]['Input_2'] = subDiv
                    obj.modifiers[nodesModifName]['Input_3'] = wear
                    obj.modifiers[nodesModifName]['Input_4'] = noiseRando
                    obj.modifiers[nodesModifName]['Input_5'] = noiseScale
                    obj.modifiers[nodesModifName]['Input_6'] = noiseDetail
                    obj.modifiers[nodesModifName]['Input_7'] = dist
                    obj.modifiers[nodesModifName]['Input_8'] = wearFac
                    
                    flag1 = False
                    
                # Checking if the Remesh Modifier is present
                if(obj.modifiers[remeshModifName]):
                    # Changing the Remesh Modifier options
                    obj.modifiers[remeshModifName].mode = remeshMode
                    obj.modifiers[remeshModifName].octree_depth = remeshDetail
                    obj.modifiers[remeshModifName].scale = remeshScale
                    obj.modifiers[remeshModifName].sharpness = remeshSharpness
                    obj.modifiers[remeshModifName].use_smooth_shade = remeshShade
                    
                    flag2 = False
                    
                # Applying the changes even if one was present
                if(flag1 or flag2):
                    # To update the changes in the viewport
                    obj.update_tag()
                    print("Successfully applied the changes to : {}".format(obj.name))
                    
            else:
                print("NO RELEVANT MODIFIERS FOUND! PLEASE RE-CHECK")
                        
        else:
            print("Selected object was not a mesh : {}".format(obj.name))
            
        # Deselecting all objects
        bpy.ops.object.select_all(action="DESELECT") 
        
# Automating the Edge Wear process - Adding modifiers and adjusting their parameters
def addEdgeWear():
    # Getting a list of selected objects
    objList = bpy.context.selected_objects
            
    ## Debugging
    #print(objList)
    
    # Deselecting all objects
    bpy.ops.object.select_all(action="DESELECT")
    
    # Iterating over the selected objects
    for obj in objList:
        # Checking if the object is valid
        if(obj.type == 'MESH'):
            # Importing the file
            appendFile()
            
            # Cleaning the modifer stack
            # Checking if the modifiers are already there
            for modif in obj.modifiers:
                # Checking if there is already a Nodes modifiers
                if modif.name == nodesModifName or modif.name == remeshModifName:
                    obj.modifiers.remove(modif)
                    
            obj.select_set(True)
            
            # Making sure it's in Object mode
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Setting the selected object as active object
            bpy.context.view_layer.objects.active = obj
            
            # If we want to add the Remesh Modifier
            #if(name=='REMESH'):
            addModifier(obj, 'REMESH')
            
            # Adding the Edge Wear setup
            addModifier(obj, 'NODES')
            
            # Our procedural wear node is named chippedEdges
            group = bpy.data.node_groups['chippedEdges']
            
            obj.modifiers[nodesModifName].node_group = group
            
            # Turning off show in Edit Mode Wireframe option
            obj.modifiers[nodesModifName].show_in_editmode = False
            
    changeEdgeParams(objList, 1.0, 3, 0.5, 3.0, 2.0, 0.0, 6.0, 'SHARP', 3, 0.9, 1.0, False)
            
    print("Successfully added Edge Wear on selected object(s)!")