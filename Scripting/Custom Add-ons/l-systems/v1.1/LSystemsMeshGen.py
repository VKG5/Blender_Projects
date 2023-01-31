import bpy
import math
       
def generateMesh(str, length, rads):
    ## Setting the correct mode
    if(bpy.context.mode != 'OBJECT'):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
    obj = bpy.context.active_object

    # Selecting object
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Toggling Edit Mode
    bpy.ops.object.mode_set(mode = 'EDIT')

    # Selecting all
    bpy.ops.mesh.select_all(action = 'SELECT')

    # Merging at center for further processing
    bpy.ops.mesh.merge(type = 'CENTER')
    
    ## Variable for storing the current angle
    currA = 0
    
    try:
        #print("\nThis list is:\n")
        for i in range(len(str)):
            ## Special Characters cases
            if(str[i]=='+'):
                currA += rads
                
            elif(str[i]=='-'):
                currA -= rads
                
            ## Consonants        
            else:
                x = round( math.cos( math.radians(currA) ), 3 ) * length
                y = round( math.sin( math.radians(currA) ), 3 ) * length
                z = 0
                
                ## TODO : DETERMINE AXIS
                #bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(x, y, z), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False)})
                bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(x, y, z)})
                
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Removing close points/doubles
        bpy.ops.mesh.remove_doubles()
            
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        print("Successfully Generated the Pattern!")
        
    except:
        print("Failed to generate the pattern!")