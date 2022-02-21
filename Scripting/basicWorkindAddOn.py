# To register this as an add-on!
bl_info = {
    # Required
    'name': 'Example Addon',
    'description': 'A basic addon',
    'blender': (3, 0, 0),
    'category': 'Object',
    # Optional
    'location': 'View3D',
    'version': (1, 0, 0),
    'author': 'Varun Kumar Gupta',
    'wiki_url': 'https://boxcutter-manual.readthedocs.io/'
}

import bpy

# Macros
D = bpy.data
C = bpy.context
O = bpy.ops

'''Main Code starts HERE'''
# GLOBAL VARIABLES
# Properties/Inputs for our add-on
# Format : ("Name", The bpy.property relevant to the field - Int, String, Float, etc.)
PROPS = [
    ('sectors', bpy.props.IntProperty(name='Sectors', default=1, min=1, max=3)),
    ('apiLink', bpy.props.StringProperty(name='API Link')),
    ('dropList', bpy.props.EnumProperty(
                                name='Track Type',
                                description = 'Selection a track preset',
                                items = [
                                    ('Track001', 'Melbourne', ''),
                                    ('Track002', 'Texas', '')
                                ] ) )
]

'''
Functions calls/Dependent Functions
The functions that will be used by the operator class
'''
def trial_func(params):
    ## Debugging
    #print("Types of the parameters : %s, %s" % (type(params[0]), type(params[1])))

    ## Debugging
    #print(type(C.scene.dropList))
    pass


'''
Class that actually calls all the necessary code
'''
# Operator Class
class f1TrackProps(bpy.types.Operator):
    bl_idname = "opr.generate_f1_track"
    bl_label = "Generate F1 Track"
    
    def execute(self, context):
        # Accessing the values from the UI
        scene = context.scene
        params = (
            scene.sectors,
            scene.apiLink
        )
        
        ## Debugging
        #print("Hey!")
        
        trial_func(params)
        
        return {'FINISHED'}


'''
Class that generates the UI 
'''            
# UI CLASS
class f1TrackDemoUI(bpy.types.Panel):
    # Creates a side panel in the 3D Viewport under "Misc"    
    bl_idname = "VIEW3D_PT_F1_Track_Generator"
    bl_label = "F1 Track Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    # To draw/create the actual panel
    def draw(self, context):
        
        # Generating the fields that would be visible in the UI Panel
        col = self.layout.column()
        for(prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
        
        col.operator('opr.generate_f1_track', text='Generate')
        

'''
Driver Code
This part includes all the calls and registrations (Without which the add-on won't work!
'''
# To automate the instlalation and uninstallation of multiple scripts/classes!
# Just add the class name in this list
CLASSES = [
    f1TrackProps,
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