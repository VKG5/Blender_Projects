# Converting the added bones into one armature and parenting them accordingly
import bpy
import csv
import os
import re

# Getting the directory
dir = os.path.dirname(os.path.realpath(__file__))

# Setting up references for ease of use
from . import BoneAdd as boneAdd


'''
Main Functions
'''
def clearOutliner():
    # Selecting all the active objects and putting them into one collection after importing
    bpy.ops.object.select_all(action='SELECT')

    nameColl = "armatureColl"
    bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name=nameColl)

    ## Debugging
    #print("Successfully cleaned the outliner")

    # Joining the different bones into one object
    bpy.ops.object.join()

    nameArmature = "boneStruct"

    # Renaming the object to something
    # Getting the active Object
    active_obj = bpy.context.object

    # Changing the Object name (For ease of debugging
    active_obj.name = nameArmature

    ## Purging the unused data       
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

    ## Debugging
    print("Successfully cleaned the outliner")
    
    return active_obj

def parentBones(activeObj, boneNamesRef, boneParentingHeirarchy):
    # Setting the object to EDIT mode to manipulate the bones
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Getting the parenting heirarchy
    ## Don't need the last 3 entries since they're proxies
    print(len(boneParentingHeirarchy))
    for boneIndex in range(len(boneParentingHeirarchy)-3):
        # Parent Bone
        boneNameP = boneNamesRef[boneParentingHeirarchy[boneIndex][0]][1]
        
        # Child Bone
        boneNameC = boneNamesRef[boneParentingHeirarchy[boneIndex][1]][1]
        
        ## Debugging
        #print("Parent : %s, Child : %s" % (boneNameP, boneNameC))
        
        # TODO Get proper dataset
        ## Ignoring the Feet due to data limitations for now
        if(boneNameC != 'L_Foot' and boneNameC != 'R_Foot'):
            ## Debugging
            # Parenting the bone
            activeObj.data.edit_bones[boneNameC].parent = activeObj.data.edit_bones[boneNameP]
    
    print("Parenting completed!")
    print("Removing unnecessary bones")
    
    # Deleting duplicates/un-wanted bones
    pattern = '.*00[12]$'
    for bone in activeObj.data.edit_bones:
        if(re.search(pattern, bone.name)):
            ## Debugging
            print("Removing bone : %s" % bone.name)
            activeObj.data.edit_bones.remove(bone)
            
    ## Debugging
    #print(bpy.data.armatures[armName].bones['Head'])


'''
Driver Code
'''
def mainParentBones():
    print("Parenting the bones")
    
    # Calling Functions
    # Parenting the bones
    boneNames, parentingHeirarchy = boneAdd.boneAddMain()
    
    # Calling clear outliner
    activeObj = clearOutliner()
     
    # Flag 
    flag = False
       
    # Iterating through available armatures
    for arm in bpy.data.armatures:  
        # Checking if the armature has more than 1 bones
        if(len(arm.bones)>1):
            # Linking those bones
            parentBones(activeObj, boneNames, parentingHeirarchy)
            flag = True   
    
    # For troubleshooting
    if not flag:
        print("No valid armatures in the scene")
                     
    bpy.ops.object.mode_set(mode='OBJECT')
    
    ## Optional
    # Parent the bones (CONNECTED Type)
    #bpy.ops.armature.parent_set(type='CONNECTED')
    
    # Paren the bones (OFFSET Type)
    #bpy.ops.armature.parent_set(type='OFFSET')