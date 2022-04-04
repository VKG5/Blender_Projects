# Adding the bones in proper orientation and renaming them accordingly
import bpy
import csv
import os

# Getting the directory
dir = os.path.dirname(os.path.realpath(__file__))

# Setting up references for ease of use
from . import BoneData as boneData


''' 
Main Functions
'''
# Adding bones based on CSV data
def addBones(vertX, vertY, vertZ, name):
    ## Adding a single bone
    bpy.ops.object.armature_add()

    ## Debugging
    #print(active_obj)
    
    # Getting the active Object
    active_obj = bpy.context.object
    
    # Changing the Object name (For ease of debugging
    active_obj.name = name
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Changing the name of the bone rather than the armature as a whole
    bpy.context.active_bone.name = name
    
    # Transforming the bones
    for bone in active_obj.data.edit_bones:
        # We are getting strings from the CSV
        # Hence, explicit conversion to float
        bone.head.z = float(vertZ[0])
        bone.tail.z = float(vertZ[1])
        
        bone.head.x = float(vertX[0])
        bone.tail.x = float(vertX[1])
        
        bone.head.y = float(vertY[0])
        bone.tail.y = float(vertY[1])

    bpy.ops.object.mode_set(mode='OBJECT')
    
    ## Debugging
    #print("Added bone %s" % (name))

# For adding normal bones which have 2 points specified
def addBonesParams(r1, r2, rows, name):
    xBone1, yBone1, zBone1 = rows[r1]
    xBone2, yBone2, zBone2 = rows[r2]

    vertX = [xBone1, xBone2]
    vertY = [yBone1, yBone2]
    vertZ = [zBone1, zBone2]
    
    addBones(vertX, vertY, vertZ, name)


'''
Driver Code
'''
## Function calls
def boneAddMain():
    # Clear the scene
    boneData.deleteAll()

    # CSV File location/path
    csvPath = dir + "\\Data\\020_24joints.csv"
    # Importing the CSV
    header, rows, boneNames, parentingHeirarchy = boneData.importCSV(csvPath)
    
    ## Debugging
    #for i in boneData.boneNames:
        #print(rows[i[0]])
    
    ## Debugging
    #print(header,"\n",rows)
    #print(len(boneNames), len(parentingHeirarchy))

    ## Adding the bones
    for i in parentingHeirarchy:
        ## Debugging
        #print(i[0], i[1])
        
        # Pelvis condition
        if(i[0]==0 and i[1]!=3):
            continue
        
        elif(i[0]==0 and i[1]==3):
            addBonesParams(0, 3, rows, boneNames[i[0]][1])
        
        else:
            addBonesParams(i[0], i[1], rows, boneNames[i[0]][1])

    print("Added all bones successfully!")
    
    return boneNames, parentingHeirarchy
     
     