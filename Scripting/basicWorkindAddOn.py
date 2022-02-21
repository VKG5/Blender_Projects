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
    'author': 'Varun Kumar Gupta',
    'wiki_url': 'https://boxcutter-manual.readthedocs.io/'
}

import bpy

'''Main Code starts HERE'''
# GLOBAL VARIABLES
# Properties/Inputs for our add-on
# Format : ("Name", The bpy.property relevant to the field - Int, String, Float, etc.)
PROPS = [
    ('Sectors', bpy.props.IntProperty(name='Sectors', default=1, min=1, max=3)),
    ('API Link', bpy.props.StringProperty(name='apiLink'))
]

# Operator Class
#class f1TrackProps(bpy.types.Operator):

# UI CLASS
class f1TrackDemoUI(bpy.types.Panel):
    # Creates a side panel in the 3D Viewport under "Misc"    
    bl_idname = "VIEW3D_PT_F1_Track_Generator"
    bl_label = "F1 Track Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    # To draw/create the actual panel
    def draw(self, context):
        col = self.layout.column()
        for(prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)

# To automate the instlalation and uninstallation of multiple scripts/classes!
# Just add the class name in this list
CLASSES = [
#    f1TrackProps,
    f1TrackDemoUI
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