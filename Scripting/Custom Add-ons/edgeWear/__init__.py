# To register script as an add-on
bl_info = {
    'name' :'Edge Wear Generator',
    'author' : 'Varun Kumar Gupta',
    'version' : (1,0,0),
    'blender' : (3,2,0),
    'location' : '3D Viewport',
    'description' : 'A simple add-on that generated Edge Wear in a completely Procedural manner',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'Node',
}

import bpy

from . import basicFuncs as basicFuncs
#basicFuncs = bpy.data.texts["basicFuncs.py"].as_module()
from . import addEdgeWear as edgeWear
#edgeWear = bpy.data.texts["addEdgeWear.py"].as_module()

'''
Main Code
'''
# GLOBAL VARIABLES
# Properties/Inputs for our add-on
# Format : ("Name", bpy.props.<propertyName> (Int, String, Enum, Float, etc.)
PROPS = [
    ## Remesh Options
    ("remeshMode", bpy.props.EnumProperty(name = 'Remesh Mode',
                                          description = 'Pick the Remesh mode you want to use',
                                          items = [
                                            ('BLOCKS', 'Blocks', ''),
                                            ('SMOOTH', 'Smooth', ''),
                                            ('SHARP', 'Sharp', ''),
                                            ('VOXEL', 'Voxel', '')
                                            ])),
                                            
    ("remeshDetail", bpy.props.IntProperty(name = 'Mesh Quality',
                                           description = 'Higher Values mean finer mesh and more geometry',
                                           default = 3, min = 0, max = 10)),
                                           
    ("remeshScale", bpy.props.FloatProperty(name = 'Remesh Scale',
                                            description = 'Higher Values mean more details in the mesh',
                                            default = 0.9, min = 0, max = 0.990)),                               
                                           
    ("remeshSharpness", bpy.props.FloatProperty(name = 'Remesh Sharpness',
                                                description = 'Higher Values mean closer to input mesh, lower values will produce noise',
                                                default = 1.0, min = 0.25, max = 2.0)),
                                                
    ("remeshShading", bpy.props.BoolProperty(name = 'Smooth Shading',
                                           description = 'Output faces with smooth shading rather than flat',
                                           default = False)),
]

PROPS2 = [
    ## Actual Edge Wear Options
    ("subDiv", bpy.props.IntProperty(name = 'SubDiv Levels',
                                     description = 'Higher Values mean finer mesh and more geometry',
                                     default = 3, min = 0, max = 10)),
                                     
    ("wearAmt", bpy.props.FloatProperty(name = 'Wear Amount',
                                        description = 'Higher Values mean more edge wear',
                                        default = 0.9, min = 0, max = 1)),
                                        
    ("noiseRando", bpy.props.FloatProperty(name = 'Wear Randomness',
                                           description = 'Higher Values mean more noise',
                                           default = 0.5)),
                                           
    ("noiseScale", bpy.props.FloatProperty(name = 'Wear Scale',
                                           description = 'Higher Values mean finer noise',
                                           default = 3.0)),
                                           
    ("noiseDetail", bpy.props.FloatProperty(name = 'Wear Detail',
                                            description = 'Higher Values mean finer noise',
                                            default = 2.0, min = 0, max = 15)),
                                          
    ("noiseDist", bpy.props.FloatProperty(name = 'Wear Distortion',
                                          description = 'Higher Values mean more distorted noise',
                                          default = 0)),
    
    ("wearFac", bpy.props.FloatProperty(name = 'Wear Factor',
                                            description = 'Higher Values mean more weathering/wear',
                                            default = 6, min = 0, max = 9)),
]            

## Function that calls the change param from edgeWear script
def callEdgeWearChange(context, params):
    edgeWear.changeEdgeParams(context.selected_objects, params[0], params[1], params[2],
                              params[3], params[4], params[5], params[6],
                              params[7], params[8], params[9], params[10], params[11])
                              
                              
'''
Class that calls code
'''
# Operator Class
class clearScene(bpy.types.Operator):
    bl_idname = "opr.used_to_clear_scene"
    bl_label = "Clear Scene"
    
    def execute(self, context):
        ## Debugging
        #print(params)
        
        basicFuncs.deleteAll()
        
        return {'FINISHED'}
    
# Operator Class
class applySelectedModifiers(bpy.types.Operator):
    bl_idname = "opr.apply_selected_modifiers"
    bl_label = "Apply Selcted Modifiers"
    
    def execute(self, context):
        
        basicFuncs.apply_modifiers()
        
        return {'FINISHED'}
    
# Operator Class
class addEdgeWearOnSelected(bpy.types.Operator):
    bl_idname = "opr.add_edgewear"
    bl_label = "Add Edge Wear"
    
    def execute(self, context):
        
        edgeWear.addEdgeWear()
        
        return {'FINISHED'}
    
# Operator Class
class changeEdgeWearParameters(bpy.types.Operator):
    bl_idname = "opr.change_edgewear_params"
    bl_label = "Recalculate Edge Wear"
    
    def execute(self, context):
        # Accessing the values from the UI
        scene = context.scene
        
        params = (
            scene.wearAmt,
            scene.subDiv,
            scene.noiseRando,
            scene.noiseScale,
            scene.noiseDetail,
            scene.noiseDist,
            scene.wearFac,
            scene.remeshMode,
            scene.remeshDetail,
            scene.remeshScale,
            scene.remeshSharpness,
            scene.remeshShading
        )
        
        callEdgeWearChange(context, params)
        
        return {'FINISHED'}
    
# Operator Class
class deleteModifiers(bpy.types.Operator):
    bl_idname = "opr.delete_selected_modifiers"
    bl_label = "Delete Modifiers"
    
    def execute(self, context):
        
        bpy.ops.object.delete_all_modifiers()
        
        return {'FINISHED'}
    
# Operator Class
class getOriginal(bpy.types.Operator):
    bl_idname = "opr.get_original_object"
    bl_label = "Recover Original Object"
    
    def execute(self, context):
        
        basicFuncs.getOriginalObject()
        
        return {'FINISHED'}
    

''' 
Class that generates the U
'''
# UI Class
class demoUI(bpy.types.Panel):
    # Creates side panel in the 3D Viewport under Misc
    bl_idname = "VIEW3D_PT_Demo_UI"
    bl_label = "Edge Wear Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    # To draw/create the actual panels
    def draw(self, context):
        self.layout.label(text="Mesh Properties : ")
        
        # Generating fields that will be visible in the Panel
        col = self.layout.column()
        
        for(prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
            
        self.layout.label(text="Edge Wear Properties : ")
        # To add space in the UI
        col = self.layout.column()
        
        col.scale_y = 3
        # Button to add Edge Wear to selected objects in the scene
        col.operator("opr.add_edgewear", text="Add Edge Wear")
        
        # To add space in the UI
        col = self.layout.column()
        # To add space in the UI
        col = self.layout.column()
        
        # Generating fields that will be visible in the Panel
        col = self.layout.column()
        
        for(prop_name, _) in PROPS2:
            row = col.row()
            row.prop(context.scene, prop_name)
            
        # To add space in the UI
        col = self.layout.column()
        col = self.layout.column()
        
        # Button to recalculate edge wear on objects in the scene
        col.operator("opr.change_edgewear_params", text="Recalculate Edge Wear")
        
        col = self.layout.column()
        # Button to Get a copy of Original objects in the scene
        col.operator("opr.get_original_object", text="Recover")
        
        self.layout.label(text="General Functions : ")
        col = self.layout.column()
        
        # Button to run the basicFuncs() Script
        col.operator("opr.used_to_clear_scene", text="Clear Scene")
        
        # Button to Get a copy of Original objects in the scene
        col.operator("opr.apply_selected_modifiers", text="Apply Modifiers")
        
        # Button to Get a copy of Original objects in the scene
        col.operator("opr.delete_selected_modifiers", text="Delete Modifiers")

'''
Driver Code
This part registers the classes with Blender and makes the add-on actually work!
Don't skip this part!!
'''

# To auomate the installation and uninstallation of multiple scripts/classes
# Just add the class names in this list
CLASSES = [
    clearScene,
    applySelectedModifiers,
    addEdgeWearOnSelected,
    changeEdgeWearParameters,
    deleteModifiers,
    getOriginal,
    demoUI
]    

# To register all the classes
def register():
    # Registering the Properties before the classes
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
        
    for (prop_name, prop_value) in PROPS2:
        setattr(bpy.types.Scene, prop_name, prop_value)
        
    for cls in CLASSES:
        bpy.utils.register_class(cls)
        
# To unregister all the classes
def unregister():
    # Un-registering the Properties before the classes
    for(prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
        
    for(prop_name, _) in PROPS2:
        delattr(bpy.types.Scene, prop_name)
        
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)
        
# Calling the register or constructor
if __name__ == "__main__":
    register()