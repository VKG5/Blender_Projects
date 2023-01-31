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

## Getting the last currently selected vertex
def getCurrVert(obj):
    setMode(obj, 'EDIT')
    
    # bmesh pointer to manipulate vertices
    bm = bmesh.from_edit_mesh(obj.data)
    
    for index, vert in enumerate(bm.verts):
        ## Debugging
        #print(vert.co.to_tuple(), index)
        
        # Checking if the current vertex is selected
        if(vert.select):
            return index
        
    # In case no vertex is active/selected
    return None

## Selecting a particular vertex
def selectVertexIndex(obj, index):
    bpy.ops.mesh.select_mode(type = 'VERT')
    
    bpy.ops.mesh.select_all(action = 'DESELECT')
    
    # Set the proper mode
    setMode(obj, 'OBJECT')
    
    obj.data.vertices[index].select = True
    
    # Set the proper mode
    setMode(obj, 'EDIT')
    
    ## Debugging
    #print("Selected vertex")
    
    return