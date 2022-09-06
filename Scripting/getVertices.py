##==== x SCRIPT USED FOR GETTING THE VERTICES OF ANY OBJECT x ====##
# BMesh for Edit Mode
import bpy, bmesh

## Function for setting the correct context
def setMode(obj, smode):
    if obj.mode != smode:
        bpy.ops.object.mode_set(mode = smode)
        return
    
    # If already in required mode
    return
    
## Selecting and setting current object active
def getCurrObj():
    obj = bpy.context.active_object
    
    obj.select_set(True)
    
    return obj

def selectVertex(obj, index):
    # Edit Mode
    if(obj.mode == 'EDIT'):
        ## How to select vertices in Edit Mode
        bpy.ops.mesh.select_all(action = 'DESELECT')
        
        # bmesh pointer to manipulate vertices
        bm = bmesh.from_edit_mesh(obj.data)
        
        bm.verts[index].select_set(True)
        
        bm.select_mode |= {'VERT'}
        
        bm.select_flush_mode()
        
        bmesh.update_edit_mesh(obj.data)
        
        return
    
    elif(obj.mode == 'OBJECT'):
        # Set the proper mode
        setMode(obj, 'EDIT')
        
        bpy.ops.mesh.select_mode(type = 'VERT')
        
        bpy.ops.mesh.select_all(action = 'DESELECT')
        
        # Set the proper mode
        setMode(obj, 'OBJECT')
        
        obj.data.vertices[index].select = True
        
        # Set the proper mode
        setMode(obj, 'EDIT')
        
        return
    
    else:
        ## Debugging
        #print("Not Valid Mode")
        return
    
def getVertices(obj, mode):
    verts = {}
    
    ## Uses bmesh, EDIT MODE
    if(mode == 'EDIT'):
        # Set the proper mode
        setMode(obj, 'EDIT')
            
        ## Getting a bmesh pointer
        bm = bmesh.from_edit_mesh(obj.data)

        # This works only in edit mode
        ## For getting a list of vertices
        for i, v in enumerate(bm.verts):
            ## Coordinates as tuples and index
            verts[i] = v.co.to_tuple()
    
    ## Uses bpy, OBJECT MODE
    elif(mode == 'OBJECT'):
        # Set he proper mode
        setMode(obj, 'OBJECT')
        
        obj.select_set(True)
            
        # This works only in object mode
        ## For getting a list of vertices
        for i, v in enumerate(obj.data.vertices):
            ## Coordinates as tuples and index
            verts[i] = v.co.to_tuple()
        
    else:
        # Returning empty list if not valid mode
        return []
            
    return verts

def main():
    obj = getCurrObj()
    mode = 'OBJECT'
    
    # Dictionary that maps, vertex index and coordinates
    verts = {}
    
    ## Getting the vertices
    if(getVertices(obj, mode)):
        verts = getVertices(obj, mode)
        
    ## Debugging
    #for i in verts:
    #    print(i, verts[i])
    
    ## Selecting the vertex
    selectVertex(obj, 2)
    
    # Processing the verts
    
main()