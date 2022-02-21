# To register this as an add-on!
bl_info = {
    # required
    'name': 'Example Addon',
    'description': 'A basic addon',
    'blender': (3, 0, 0),
    'category': 'Object',
    # optional
    'location': 'View3D',
    'version': (1, 0, 0),
    'author': 'Varun Kumar Gupta, Nazzal Naseer',
    'wiki_url': 'https://boxcutter-manual.readthedocs.io/'
}

import bpy

'''Main Code starts HERE'''
    
# UI CLASS
class f1TrackDemoUI(bpy.types.Panel):
    '''Creates a Panel in the scene context of the properties editor'''
#    bl_label = "F1 Track Generator"
#    bl_idname = "f1TrackGen"
#    bl_space_type = "PROPERTIES"
#    bl_region_type = "WINDOW"
#    cl_context = "scene"
    
    bl_idname = "VIEW3D_PT_Example Panel"
    bl_label = "Example Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    # To draw/create the actual panel
    def draw(self, context):
        layout = self.layout
        
        scene = context.scene
        
        # Create a simple row.
        layout.label(text="Hello World")

# To automate the instlalation and uninstallation of multiple scripts/classes!
# Just add the class name in this list
classes = [
    f1TrackDemoUI
]
        
# To install the add-on for the first time
def register():
    ## Debugging
    print("Registered")
    for cls in classes:
        bpy.utils.register_class(cls)
    
# To delete the add-on upon uninstallation
def unregister():
    print("Unregistered")
    for cls in classes:
        bpy.utils.unregister_class(cls)

# To make this work
if __name__ == "__main__":
    register() 