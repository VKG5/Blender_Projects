import bpy
import bpy
import math
       
from . import GetVertices as getVertices
#getVertices = bpy.data.texts["getVertices.py"].as_module()

def cpop(ls):
    try:
        return ls.pop(), True
        
    except IndexError:
        return [], False

## For generating the actual mesh
def generateMesh(str, length, rads):
    ## Setting the correct mode
    getVertices.setMode(bpy.context.active_object, 'OBJECT')

    # Selecting object        
    obj = getVertices.getCurrObj()

    # Toggling Edit Mode
    getVertices.setMode(obj, 'EDIT')

    # Selecting all
    bpy.ops.mesh.select_all(action = 'SELECT')

    # Merging at center for further processing
    bpy.ops.mesh.merge(type = 'CENTER')
    
    # Resetting the vertex selection to origin
    getVertices.selectVertexIndex(obj, 0)
    
    ## Variable for storing the current angle
    currA = 0
    
    ## List for storing indices
    indexLs = []
    index = 0
    
    try:
        ## Debugging
        #print("\nSTEPS:\n")
        
        for i in range(len(str)):
            ## Special Characters cases
            if(str[i]=='+'):
                currA += rads
                ## Debugging
                #print("Adding Angle")
                
            elif(str[i]=='-'):
                currA -= rads
                ## Debugging
                #print("Subtracting Angle")
                
            elif(str[i]=='['):
                # Pushing the value into a list
                indexLs.append((getVertices.getCurrVert(obj), currA))
                
            elif(str[i]==']'):
                # Removing the last element (First inserted index and angle)
                vert, flag = cpop(indexLs)
                
                if(flag):
                    ## Selecting the required vertex
                    getVertices.selectVertexIndex(obj, vert[0])
                    currA = vert[1]
                        
            elif(str[i]=='X'):
                continue
                
            ## Consonants for moving forward   
            else:
                x = round( math.cos( math.radians(currA) ), 3 ) * length
                y = round( math.sin( math.radians(currA) ), 3 ) * length
                z = 0
                
                ## TODO : DETERMINE AXIS
                bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(x, y, z)})
                
                # Incrementing the index
                index += 1
                
        bpy.ops.mesh.select_all(action = 'SELECT')
        
        ## Removing close points/doubles
        bpy.ops.mesh.remove_doubles()
            
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        print("Successfully Generated the Pattern!")
        
    except Exception as inst:
        print("Failed to generate the pattern!", type(inst))