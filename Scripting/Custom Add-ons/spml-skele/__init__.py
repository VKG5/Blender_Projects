# To register this as an add-on!
bl_info = {
    'name': 'SMPL Bone Generator',
    'author': 'Varun Kumar Gupta',
    'version': (1, 0, 0),
    'blender': (3, 0, 0),
    'location': "3D Viewport",
    'description': 'A simple to generate an armature given the generic SMPL bone structure',
    'warning': '',
    'wiki_url': '',
    'category': 'Object',
}

import bpy

from . import ParentingBones as mainModule
from . import BoneData as basicFuncs


'''Main Code starts HERE'''
# GLOBAL VARIABLES
# Properties/Inputs for our add-on
# Format : ("Name", The bpy.property relevant to the field - Int, String, Float, etc.)
PROPS = [
    ('filePath', bpy.props.StringProperty(name='File Path')),
]


'''
Functions calls/Dependent Functions
The functions that will be used by the operator class
'''
def clearScene():
    # Calling the delete all function from another script
    basicFuncs.deleteAll()   
    
def callMain():
    # Calling the main generation function
    mainModule.mainParentBones()


'''
Class that actually calls all the necessary code
'''
# Operator Class
class smplSkeleMain(bpy.types.Operator):
    bl_idname = "opr.generate_smpl_skele"
    bl_label = "Generate SMPL Skeleton with 24 Joints"
    
    def execute(self, context):
        # Accessing the values from the UI
        scene = context.scene
        params = (
            scene.filePath
        )
        
        # Sending the input to the actual code
        callMain()
        
        return {'FINISHED'}
    
# Operator Class
class smplSkeleProps(bpy.types.Operator):
    bl_idname = "opr.clear_all"
    bl_label = "Clear the scene"
    
    def execute(self, context):
        # Sending the input to the actual code
        clearScene()
        
        return {'FINISHED'}


'''
Class that generates the UI 
'''            
# UI CLASS
class smplSkeleUI(bpy.types.Panel):
    # Creates a side panel in the 3D Viewport under "Misc"    
    bl_idname = "VIEW3D_PT_SMPL_Skeleton"
    bl_label = "SMPL Skeleton Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    # To draw/create the actual panel
    def draw(self, context):
        
        # Generating the fields that would be visible in the UI Panel
        col = self.layout.column()
        for(prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
        
        # Button to run the generateTrack() script
        col.operator('opr.generate_smpl_skele', text='Generate Skeleton')
        
        # Button to run the generateFillers() script
        col.operator('opr.clear_all', text='CLEAR SCENE')
        

'''
Driver Code
This part includes all the calls and registrations (Without which the add-on won't work!
'''
# To automate the instlalation and uninstallation of multiple scripts/classes!
# Just add the class name in this list
CLASSES = [
    smplSkeleMain,
    smplSkeleProps,
    smplSkeleUI
]

# To install the add-on for the first time
def register():
    # Registering the Properties before the classes
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    ## Debugging
    #print("Registered")
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    
# To delete the add-on upon uninstallation
def unregister():
    # De-Registering the properties
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
        
    ## Debugging
    #print("Unregistered")
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)

# To make this work
if __name__ == "__main__":
    register() 