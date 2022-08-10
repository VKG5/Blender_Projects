# To register script as an add-on
bl_info = {
    'name' :'Lumi Tools',
    'author' : 'Varun Kumar Gupta',
    'version' : (1,0,0),
    'blender' : (3,2,0),
    'location' : '3D Viewport>Side Panel',
    'description' : 'A set of custom tools/features that I find useful',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'UI',
}

import bpy
import os
from bpy.props import *
from bpy_extras.io_utils import ImportHelper

from . import basicFuncs as basicFuncs
#basicFuncs = bpy.data.texts["basicFuncs.py"].as_module()
from . import assetManager as assetManager
#assetManager = bpy.data.texts["assetManager.py"].as_module()

'''
Main Code
'''
# GLOBAL VARIABLES
# Properties/Inputs for our add-on
# Format : ("Name", bpy.props.<propertyName> (Int, String, Enum, Float, etc.)
PROPS = [
    ## Visualization Options
    ("vizNode", bpy.props.EnumProperty( name = 'Viz Nodes ',
                                      description = 'Pick the visualization mode you want to see',
                                      items = [
                                        ('none', 'None', 'Keep the current material'),
                                        ('ao', 'Ambient Occlusion', 'Quick Ambient Occlusion'),
                                        ('depth', 'Depth', 'Depth of an object (Range 0-1 on Z)'),
                                        ('direction', 'Direction', 'Direction for particles/curves'),
                                        ('flow', 'Flow', 'The flow for particles/curves'),
                                        ## ('hairDiff', 'Hair Diffuse', 'Diffuse Shader for particles using curves (Specifically hair)'),
                                        ('normal', 'Normal Map', 'Quick Normal Map'),
                                        ('opactiy', 'Opacity Map', 'Quick alpha map'),
                                        ('randomColor', 'Random Color', 'Gives a random color to the object or random color per strand'),
                                        ('randomID', 'Random ID', 'Gives a differnt value b/w 0 to 1 (B-W) to each face/strand'),
                                        ('root', 'Root', 'Gives the root for any particle/curve system')
                                        ])),
]

# Global list that changes depending on input
PROPS2 = [
        ## Ambient Occlusion Map - 3
        ("aoDist", bpy.props.FloatProperty(name = 'AO Distance',
                                    description = 'The distance for the AO node',
                                    default = 0, min = 0, max = 1000)),
        ("aoInside", bpy.props.FloatProperty(name = 'Inside', 
                                    description = 'Invert AO calculation based on the factor',
                                    default = 0, min = 0, max = 1)),
        ("aoNormals", bpy.props.StringProperty(name = 'Normal Map',
                                    description = 'Please open the shader editor',
                                    default = 'Please visit the shader editor to include a normal map')),
                                    
        ## Depth - 2
        ("depthDepth", bpy.props.FloatProperty(name = 'Depth',
                                    description = 'The depth of object from Z=0',
                                    default = 0.5, min = 0)),
        ("depthInvert", bpy.props.FloatProperty(name = 'Invert', 
                                    description = 'Invert depth',
                                    default = 0, min = 0, max = 1)),
                                    
        ## Direction - 3
        ("dirRed", bpy.props.FloatProperty(name = 'Flip Red',
                                    description = 'Invert Red channel',
                                    default = 0, min = 0, max = 1)),
        ("dirGreen", bpy.props.FloatProperty(name = 'Flip Green', 
                                    description = 'Invert Green channel',
                                    default = 0, min = 0, max = 1)),
        ("dirBlue", bpy.props.FloatProperty(name = 'Flip Blue',
                                    description = 'Invert Blue channel',
                                    default = 0, min = 0, max = 1)),
                                    
        ## Flow - 2
        ("flowRed", bpy.props.FloatProperty(name = 'Flip Red',
                                    description = 'Invert Red channel',
                                    default = 0, min = 0, max = 1)),
        ("flowGreen", bpy.props.FloatProperty(name = 'Flip Green', 
                                    description = 'Invert Green channel',
                                    default = 0, min = 0, max = 1)),
                                    
        ## Normal Map - 1
        ("normalRed", bpy.props.FloatProperty(name = 'Flip Red',
                                    description = 'Invert Red channel',
                                    default = 0, min = 0, max = 1)),
                                    
        ## Opacity - 4
        ("opaCut", bpy.props.FloatProperty(name = 'Cut',
                                    description = 'Cut from the root of the emitter',
                                    default = 0.01, min = 0.01, max = 1)),
        ("opaContrast", bpy.props.FloatProperty(name = 'Contrast', 
                                    description = 'Overall contrast',
                                    default = 0.01, min = 0.01, max = 10)),
        ("opaFrequency", bpy.props.FloatProperty(name = 'Frequency',
                                    description = 'Change the root points with some noise',
                                    default = 0, min = 0, max = 10)),
        ("opaSeed", bpy.props.FloatProperty(name = 'Seed',
                                    description = 'Seed for the frequency',
                                    default = 0, min = -1, max = 1)),
        
        ## Random Color - 2
        ("randoContrast", bpy.props.FloatProperty(name = 'Contrast', 
                                    description = 'Range of colors',
                                    default = 0, min = 0, max = 1)),
        ("randoSeed", bpy.props.FloatProperty(name = 'Seed',
                                    description = 'Seed for the colors',
                                    default = 0)),
                                    
        ## Random IDs - 1
        ("randIDContrast", bpy.props.FloatProperty(name = 'Contrast', 
                                    description = 'Range of colors',
                                    default = 0, min = 0, max = 1)),
                                    
        ## Root Map - 3
        ("rootContrast", bpy.props.FloatProperty(name = 'Contrast', 
                                    description = 'Overall contrast',
                                    default = 0, min = 0, max = 1)),
        ("rootRoot", bpy.props.FloatProperty(name = 'Root',
                                    description = 'Root starting point from actual root',
                                    default = 0, min = 0, max = 1)),
        ("rootTip", bpy.props.FloatProperty(name = 'Tip',
                                    description = 'Positioning of the Tip from the Root',
                                    default = 0, min = 0, max = 1)),
                                          
]

# World Inputs
PROPSWorld = [
        ## Visualization Options
        ("worldNode", bpy.props.EnumProperty( name = 'World Nodes ',
                                          description = 'Pick the visualization mode you want to see',
                                          items = [
                                            ('none', 'None', 'Keep the current BG'),
                                            ('blank', 'Blank', 'Default World'),
                                            ('black', 'Black', 'Black background'),
                                            ('grey', 'Grey', 'Grey background'),
                                            ('white', 'White', 'White background'),
                                            ('normal', 'Normal', 'Blank normal background') ])),
                                            
        ('worldTransparent', bpy.props.BoolProperty( name = ' Transparent Background ',
                                            description = "Whether the world background should be transparent or not",
                                            default = False)),
                                            
        ('worldGlassTrans', bpy.props.BoolProperty( name = ' Transparent Glass ',
                                            description = "Whether the glass materials should be transparent or not",
                                            default = False)),
]

def toRegister(value):
    match value:
        case 'ao':
            return PROPS2[:2]
        
        case 'depth':
            return PROPS2[3:5]
        
        case 'direction':
            return PROPS2[5:8]
        
        case 'flow':
            return PROPS2[8:10]
        
        case 'normal':
            return PROPS2[10:11]
               
        case 'opactiy':
            return PROPS2[11:15]
        
        case 'randomColor':
            return PROPS2[15:17]
        
        case 'randomID':
            return PROPS2[17:18]
        
        case 'root':
            return PROPS2[18:21]
        
        case default:
            return []
            
                                                 
'''
Class that calls code
'''
# Operator Class
class clearScene(bpy.types.Operator):
    bl_idname = "opr.used_to_clear_scene"
    bl_label = "Clear Scene"
    bl_description = "Completely wipe the scene; including collections, nodes and everything present"
    
    def execute(self, context):
        ## Debugging
        #print(params)
        
        basicFuncs.deleteAll()
        
        return {'FINISHED'}
    
# Operator Class
class applySelectedModifiers(bpy.types.Operator):
    bl_idname = "opr.apply_selected_modifiers"
    bl_label = "Apply Selcted Modifiers"
    bl_description = "Apply all modifiers to selected objects (Except Armature)"
    
    def execute(self, context):
        
        basicFuncs.apply_modifiers()
        
        return {'FINISHED'}
    
# Operator Class
class deleteModifiers(bpy.types.Operator):
    bl_idname = "opr.delete_selected_modifiers"
    bl_label = "Delete Modifiers"
    bl_description = "Delete all modifiers from the selected objects"
    
    def execute(self, context):
        
        bpy.ops.object.delete_all_modifiers()
        
        return {'FINISHED'}
    
# Opens a file select dialog and starts scanning the selected file.
# Operator Class
class ScanFileOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "opr.scan_file"
    bl_label = "Install the selected add-on"
    bl_description = "Install any add-on without going to Edit>Preferences>Add-ons (Experimental)"
    
    # Filtering visible files
    filter_glob: StringProperty(
        # Files that will be visible
        default='*.zip;*.py',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        ## Debugging
        # self.filepath - Note that this is a regular StringProperty 
        # inside ImportHelper that we inherited when we subclassed it.
        
        #print(self.filepath)
        # Splitting the filename and extension
        
        filepath, extension = os.path.splitext(self.filepath)
        filename = os.path.basename(filepath)
        dir = os.path.dirname(filepath)
        
        # Passing the arguments to install add-on
        basicFuncs.installAddOn(dir, filename, extension)
        return {'FINISHED'}
 
    # Invoking the actual window
    def invoke(self, context, event):
        # Calling self Operator (Class) upon execution
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Opens a file select dialog and starts scanning the selected file.
# Operator Class
class getAssetPath(bpy.types.Operator, ImportHelper):
    bl_idname = "opr.add_asset_library"
    bl_label = "Add asset library into path/project"
    bl_description = "Install any add-on without going to Edit>Preferences>File Paths"
    
    # Filtering visible files
    filter_glob: StringProperty(
        default='*.blend*',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        filepath, extension = os.path.splitext(self.filepath)
        filename = os.path.basename(filepath)
        dir = os.path.dirname(filepath)
        
        # Passing the arguments to install add-on
        assetManager.addAssetLib(dir, filename, extension)
        return {'FINISHED'}
 
    # Invoking the actual window
    def invoke(self, context, event):
        # Calling self Operator (Class) upon execution
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class markAsset(bpy.types.Operator):
    bl_idname = "opr.mark_as_asset"
    bl_label = "Mark selected objects as assets"
    bl_description = "Mark all the selected objects as assets (Preview generated only for Mesh objects)"
    
    def execute(self, context):
        
        assetManager.markAssets()
        
        return {'FINISHED'}
    
class clearAsset(bpy.types.Operator):
    bl_idname = "opr.clear_the_asset"
    bl_label = "Clear selected objects as assets"
    bl_description = "Clear all the selected objects from assets"
    
    def execute(self, context):
        
        assetManager.clearAssets()
        
        return {'FINISHED'}

class worldSettings(bpy.types.Operator):
    bl_idname = "opr.set_transparent"
    bl_label = "Set the background as transparent"
    bl_description = "World background is transparent, for compositing over other backgrounds"
    
    def execute(self, context):
        # Setting the world properties
        basicFuncs.setWorld(context.scene.worldTransparent, context.scene.worldGlassTrans, context.scene.worldNode)

        return {'FINISHED'}
    
class vizMaterialSettings(bpy.types.Operator):
    bl_idname = "opr.set_mat_geo"
    bl_label = "Apply the visualization nodes"
    bl_description = "Sets the visualization node material in Geo nodes, rather than the object itself (Group should be at the bottom of the modif stack)"
    
    def execute(self, context):
        basicFuncs.setMaterial(context.scene.vizNode)
        
        return {'FINISHED'}
    
class vizRemove(bpy.types.Operator):
    bl_idname = "opr.remove_viz_nodes"
    bl_label = "Remove the visualization nodes"
    bl_description = "Remove visualization nodes from selected objects"
    
    def execute(self, context):
        basicFuncs.removeVizNode()
        
        return {'FINISHED'}
        
''' 
Class that generates the UI
'''
# UI Class
class demoUI(bpy.types.Panel):
    # Creates side panel in the 3D Viewport under Misc
    bl_idname = "VIEW3D_PT_Lumi_Tools"
    bl_label = "Lumi Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Lumi_Tools" 
    
    # To draw/create the actual panels
    def draw(self, context):
        # Generating fields that will be visible in the Panel
        col = self.layout.column()
                
#        for(prop_name, _) in PROPS:
#            row = col.row()
#            row.prop(context.scene, prop_name)
        
        self.layout.label(text="General Functions : ")
        col = self.layout.column()
        
        col.scale_y = 1.5
        # Button to run the basicFuncs() Script
        col.operator("opr.used_to_clear_scene", text="Clear Scene (Deep Clean)")
        
        col = self.layout.column()
        col = self.layout.column()
        # Button to Get a copy of Original objects in the scene
        col.operator("opr.apply_selected_modifiers", text="Apply Modifiers")
        
        # Button to Get a copy of Original objects in the scene
        col.operator("opr.delete_selected_modifiers", text="Delete Modifiers")
        
        # Get the asset libray
        col = self.layout.column()
        col = self.layout.column()
        col.operator("opr.add_asset_library", text="Add Asset Library", icon = 'ASSET_MANAGER')
        
        # Get the add-on file path
        col.operator("opr.scan_file", text="Install Addon", icon = 'ERROR')
        
        # Get the add-on file path
        col = self.layout.column()
        col = self.layout.column()
        col.operator("opr.mark_as_asset", text="Mark Asset(s)", icon = 'ADD')
        
        # Get the add-on file path
        col.operator("opr.clear_the_asset", text="Clear Asset(s)", icon = 'DOT')
        
# UI Class
class vizUI(bpy.types.Panel):
    # Creates side panel in the 3D Viewport under Misc
    bl_idname = "VIEW3D_PT_Viz_Tools"
    bl_label = "Visualization Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Lumi_Tools" 
    
    # To draw/create the actual panels
    def draw(self, context):
        # Generating fields that will be visible in the Panel
        col = self.layout.column()
                
        # Registering the drop-down that contains a list of nodes available
        for(prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
        
        registerPROPS = toRegister(context.scene.vizNode)
        
        ## Adding a space
        col = self.layout.column()
        
        ## Debugging
        #print("After Registering : \n{}".format(registerPROPS))
        
        for(prop_name, _) in registerPROPS:
            row = col.row()
            row.prop(context.scene, prop_name)   
        
        # A message for Ambient Occlusion node
        if(context.scene.vizNode == 'ao'):
            self.layout.label(text="Normal Map:")
            self.layout.label(text="Please visit the shader editor for this.")
            
        ## Adding a space
        col = self.layout.column()
        
        ## World Settings
        # Registering the world options
        for(prop_name, _) in PROPSWorld[:2]:
            row = col.row()
            row.prop(context.scene, prop_name)
            row = col.row()
        
        if(context.scene.worldTransparent):
            row = col.row()
            row.prop(context.scene, PROPSWorld[2][0])
            
        ## Adding a space
        col = self.layout.column()
        
        ## Transparent
        col.operator("opr.set_transparent", text = "Apply World Settings")
        
        col.operator("opr.set_mat_geo", text = "Set Material(s)", icon = 'ERROR')
        
        col.operator("opr.remove_viz_nodes", text = "Remove Viz Nodes")
            

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
    deleteModifiers,
    ScanFileOperator,
    getAssetPath,
    markAsset,
    clearAsset,
    worldSettings,
    vizMaterialSettings,
    vizRemove,
    demoUI,
    vizUI
]    

# To register all the classes
def register():
    # Registering the Properties before the classes
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    # Registering the global list properties
    for (prop_name, prop_value) in PROPS2:
        setattr(bpy.types.Scene, prop_name, prop_value)
        
    # Registering the world properties
    for (prop_name, prop_value) in PROPSWorld:
        setattr(bpy.types.Scene, prop_name, prop_value)
        
    for cls in CLASSES:
        bpy.utils.register_class(cls)
        
# To unregister all the classes
def unregister():
    # Un-registering the Properties before the classes
    for(prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
        
    # Un-registering the global list properties before the classes
    for(prop_name, _) in PROPS2:
        delattr(bpy.types.Scene, prop_name)
    
    # Registering the world properties
    for(prop_name, _) in PROPSWorld:
        delattr(bpy.types.Scene, prop_name)
        
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)
        
# Calling the register or constructor
if __name__ == "__main__":
    register()