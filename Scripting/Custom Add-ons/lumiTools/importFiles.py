import bpy
import os

# Getting path
#dir = os.path.dirname(bpy.data.filepath)
dir = os.path.dirname(os.path.realpath(__file__))

# Global variable for checking if already imported
# flagAll = False
flagW = False
flagM = False

# Importing collections/files from other projects
def appendFiles(path, type, files):
    filePath = path
    fileType = type
    
    for fileName in files:
        ## Debugging
        #print("FilePath : {}\nDirectory : {}\n FileName : {}".format(os.path.join(filePath, fileType, fileName), os.path.join(filePath, fileType), fileName))
    
        try:
            if(bpy.ops.wm.append(
                filepath = os.path.join(filePath, fileType, fileName),
                directory = os.path.join(filePath, fileType),
                filename = fileName,
                ## To prevent duplicates
                do_reuse_local_id = True,
                set_fake=True
            )):
                ## Debugging
                #print("Successfully imported the {} : {}!".format(fileType, fileName))
                continue
                
            else:
                print("{} : {} missing".format(fileType, fileName))
                
        except:
            print("Failed to import {}".format(fileName)) 
            
# Importing shaders
def importMaterials():
    ## Takes these three inputs : path, type, files
    # Path = The path of the file from which teh file will be imported
    # Type = The type of node tree/sub structure the files belongs to
    # Files = A list containing the name of the files that will be imported
    
    baseFile = "baseFile.blend"
    
    path = dir + "\\" + baseFile
    type = "Material"
    files = ['AO', 'Depth', 'Direction', 'Flow', 'NormalMap', 'Opacity', 'RandomColor', 'RandomID', 'Root']
    
    appendFiles(path, type, files)
    
# Importing world materials
def importWorldMats():
    baseFile = "baseFile.blend"
    
    path = dir + "\\" + baseFile
    type = "World"
    files = ['WorldW', 'BlackW', 'MidW', 'WhiteW', 'NormalW']
    
    appendFiles(path, type, files)
    
# Importing Nodes networks
def importGeoNodes():
    baseFile = "baseFile.blend"
    
    path = dir + "\\" + baseFile
    type = "NodeTree"
    files = ['GetParentData']
    
    appendFiles(path, type, files)    

'''
In case we need it later
def importAll():
    global flagAll
    
    if(not flagAll):
        importMaterials()
        importWorldMats()
        importGeoNodes()
        
        flagAll = True
        
    else:
        print("Already imported")
'''
    
def import_world():
    global flagW
    
    if(not flagW):
        importWorldMats()
        
        flagW = True
        
    else:
        print("Already imported World Mats")
        
def import_mats():
    global flagM
    
    if(not flagM):
        importMaterials()
        importGeoNodes()
        
        flagM = True
        
    else:
        print("Already imported required Materials")