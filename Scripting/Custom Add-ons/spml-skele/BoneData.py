# Contains the data for processing the bones/armature in further steps
import bpy
import csv
import os

'''
Data required for processing
'''
def definePreData():
    # Defining a list set for appropriate naming
    boneNames = [(0, 'Pelvis'), (1, 'L_Hip'), (2, 'R_Hip'), (3, 'Spine1'), (4, 'L_Knee'), (5, 'R_Knee'), (6, 'Spine2'), 
                 (7, 'L_Ankle'), (8, 'R_Ankle'), (9, 'Spine3'), (10, 'L_Foot'), (11, 'R_Foot'), (12, 'Neck'), (13, 'L_Collar'), 
                 (14, 'R_Collar'), (15, 'Head'), (16, 'L_Shoulder'), (17, 'R_Shoulder'), (18, 'L_Elbow'), (19, 'R_Elbow'), 
                 (20, 'L_Wrist'), (21, 'R_Wrist'), (22, 'L_Hand'), (23, 'R_Hand')]

    # Defining the parenting heirarchy
    parentingHeirarchy = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 6), (4, 7), 
                          (5, 8), (6, 9), (7, 10), (8, 11), (9, 12), (9, 13), 
                          (9, 14), (12, 15), (13, 16), (14, 17), (16, 18), (17, 19), 
                          (18, 20), (19, 21), (20, 22), (21, 23)]
    
    return boneNames, parentingHeirarchy

# Last three entries 15, 22, 23 are proxies until we generate better data


'''
Preprocessing Functions
'''
# Clearing the scene
def deleteAll():
    # Checking if scene is already empty
    if(len(bpy.data.scenes['Scene'].objects) > 0):
        # Setting mode to OBJECT in case we are in any other mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Deleting everything that was present 
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        print("Deleted all the objects!")
             
    else:
        print("Nothing to delete! Scene already empty.")
    
    ## Removing unused collections to clear the outliner
    for coll in bpy.data.collections:
        print("Deleting collection : %s" % coll.name)
        if(coll):
            bpy.data.collections.remove(coll)
                
    ## Purging the unused data       
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
            
# Since we don't have data for 3 points, we'll be modifying the data imported from the CSV 
def modifyRows(rows, boneNames, parentingHeirarchy):
    # We will add 3 proxy points for the Head and Hands respectively
    # Head Proxy Point
    boneNames += [(24, 'HeadProxy'), (25, 'L_HandProxy'), (26, 'R_HandProxy')]
    parentingHeirarchy += [(15, 24), (22, 25), (23, 26)]
    
    # Head Proxy Point
    index = 24
    
    #Appending proxies
    rows.append([0,0,0])
    
    temp = [-0.003932, -0.921002, -0.091091]
    for i in range(3): 
        rows[index][i] = temp[i]
    
    # L Hand Proxy Point
    index += 1
    
    #Appending proxies
    rows.append([0,0,0])
    
    temp = [0.197403, -0.34503, -0.482663]
    for i in range(3): 
        rows[index][i] = temp[i]
    
    # R Hand Proxy Point
    index += 1
    
    #Appending proxies
    rows.append([0,0,0])
    
    temp = [-0.222678, -0.516357, -0.47337]
    for i in range(3):
        rows[index][i] = temp[i]
        
    return rows, boneNames, parentingHeirarchy

# Importing the CSV
def importCSV(path):
    file = open(path)
    
    ## Debugging
    #print(type(file))
    
    # Calling the pre data function to initialize lists
    boneNames, parentingHeirarchy = definePreData()
     
    csvreader = csv.reader(file)     
    
    # Getting the labels
    header = []
    header = next(csvreader)
    
    ## Debugging
    #print(header)
    
    # Getting the data
    rows = []
    for row in csvreader:
        rows.append(row)
    
    ## Debugging
    #print("Before modifying : %s" % len(rows))
        
    ## Adding the proxies
    rows, boneNames, parentingHeirarchy = modifyRows(rows, boneNames, parentingHeirarchy)
    
    ## Debugging
    #print("After modifying : %s" % len(rows))
    
    file.close()
    
    print("\nCSV imported and data stored successfully!\n")
    
    return header, rows, boneNames, parentingHeirarchy