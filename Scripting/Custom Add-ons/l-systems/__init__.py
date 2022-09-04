# To register script as an add-on
bl_info = {
    'name' :'L-System Generator',
    'author' : 'Varun Kumar Gupta',
    'version' : (1,1,0),
    'blender' : (3,2,0),
    'location' : '3D Viewport',
    'description' : 'L-System Generator based on Axioms and Strings',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'UI',
}

import bpy
import os
from bpy.props import *

#from . import LSystems as lsystems
lsystems = bpy.data.texts["l-systems.py"].as_module()

'''
Main Code
'''
# GLOBAL VARIABLES
# Properties/Inputs for our add-on
# Format : ("Name", bpy.props.<propertyName> (Int, String, Enum, Float, etc.)
PROPS = [
    ## Presets
    ("presetVal", bpy.props.EnumProperty( name = 'Presets ',
                                      description = 'Some presets for you to play around with',
                                      items = [
                                        ('custom', 'None', 'Custom Pattern'),
                                        ('kochSnow', 'Koch Snowflake', 'A variant of the Koch curve to create a snowflake'),
                                        ('koch', 'Koch Curve', 'A variant of the Koch curve which uses only right angles'),
                                        ('sierpinski', 'Sierpinski Triangle', 'The Sierpinski triangle'),
                                        ('sierpinskiCurve', 'Sierpinski Arrowhead Curve', 'Sierpiński arrowhead curve'),
                                        ('dragon', 'Dragon Curve', 'The dragon curve')
                                        ])),
              
    ("axiom", bpy.props.StringProperty( name = 'Axiom',
                                        description = 'The starting point of our L-System',
                                        default = "A" )),
                                        
    ("generations", bpy.props.IntProperty( name = 'Generations',
                                           description = 'Iterations/Generations : How many times to run the loop',
                                           default = 3, min = 1, max = 100)),
    
    ("numRules", bpy.props.IntProperty( name = 'Number of Rules',
                                        description = 'The number of rules in your L-System',
                                        default = 2, min = 1, max = 5)),
                                        
    ("angle", bpy.props.FloatProperty( name = 'Angle',
                                        description = 'Angle by which each segment will rotate (Degrees)',
                                        default = 60, min = 0, max = 360)),
                                        
    ("length", bpy.props.FloatProperty( name = 'Length',
                                        description = 'The length of each generated segment',
                                        default = 1, min = 0.05, max = 10)),
    
    ("rule1", bpy.props.StringProperty( name = 'Rule 1',
                                        description = 'First rule for you L-System',
                                        default = 'A:AB' )),
    
    ("rule2", bpy.props.StringProperty( name = 'Rule 2',
                                        description = 'Second rule for you L-System',
                                        default = 'B:A' )),
    
    ("rule3", bpy.props.StringProperty( name = 'Rule 3',
                                        description = 'Third rule for you L-System',
                                        default = 'C:B' )),
                                        
    ("rule4", bpy.props.StringProperty( name = 'Rule 4',
                                        description = 'Fourth rule for you L-System',
                                        default = 'D:BA' )),
    
    ("rule5", bpy.props.StringProperty( name = 'Rule 5',
                                        description = 'Fifth rule for you L-System',
                                        default = 'E:CD' )),                                     
]

## Class for pre-setting values
def presetClass(preset):
    match preset:
        case 'kochSnow':
            bpy.context.scene.axiom = 'F--F--F'
            bpy.context.scene.generations = 5
            bpy.context.scene.numRules = 1
            bpy.context.scene.angle = 60
            bpy.context.scene.length = 1.0
            bpy.context.scene.rule1 = 'F:F+F--F+F'
            return
        
        case 'koch':
            bpy.context.scene.axiom = 'F'
            bpy.context.scene.generations = 3
            bpy.context.scene.numRules = 1
            bpy.context.scene.angle = 90
            bpy.context.scene.length = 1.0
            bpy.context.scene.rule1 = 'F:F+F-F-F+F'
            return
            
        case 'sierpinski':
            bpy.context.scene.axiom = 'F-G-G'
            bpy.context.scene.generations = 4
            bpy.context.scene.numRules = 2
            bpy.context.scene.angle = 120
            bpy.context.scene.length = 1.0
            bpy.context.scene.rule1 = 'F:F-G+F+G-F'
            bpy.context.scene.rule2 = 'G:GG'
            return
            
        case 'sierpinskiCurve':
            bpy.context.scene.axiom = 'A'
            bpy.context.scene.generations = 4
            bpy.context.scene.numRules = 2
            bpy.context.scene.angle = 60
            bpy.context.scene.length = 1.0
            bpy.context.scene.rule1 = 'A:B-A-B'
            bpy.context.scene.rule2 = 'B:A+B+A'
            return
        
        case 'dragon':
            bpy.context.scene.axiom = 'F'
            bpy.context.scene.generations = 10
            bpy.context.scene.numRules = 2
            bpy.context.scene.angle = 90
            bpy.context.scene.length = 1.0
            bpy.context.scene.rule1 = 'F:F+G'
            bpy.context.scene.rule2 = 'G:F-G'
            return
        
        case default:
            return
        
## Cases for passing the selected rules
def passRulesNum(num):
    match num:
        case 1:
            return [bpy.context.scene.rule1]
        
        case 2:
            return [bpy.context.scene.rule1, 
                    bpy.context.scene.rule2]
        
        case 3:
            return [bpy.context.scene.rule1, 
                    bpy.context.scene.rule2,
                    bpy.context.scene.rule3]
        
        case 4:
            return [bpy.context.scene.rule1, 
                    bpy.context.scene.rule2,
                    bpy.context.scene.rule3, 
                    bpy.context.scene.rule4]
        
        case 5:
            return [bpy.context.scene.rule1, 
                    bpy.context.scene.rule2,
                    bpy.context.scene.rule3, 
                    bpy.context.scene.rule4, 
                    bpy.context.scene.rule5]
                    
                            
'''
Class that calls code
'''
# Operator Class
class generateLSystems(bpy.types.Operator):
    bl_idname = "opr.generate_l_system"
    bl_label = "Clear Scene"
    bl_description = "Completely wipe the scene; including collections, nodes and everything present"
    
    def execute(self, context):
        ## Debugging
        #print(params)
        
        # Pre-setting the values
        presetClass(context.scene.presetVal)
        
        passRules = passRulesNum( bpy.context.scene.numRules )    
        
        lsystems.generateLSystem( bpy.context.scene.axiom, 
                                  bpy.context.scene.generations, 
                                  bpy.context.scene.numRules, 
                                  bpy.context.scene.angle, 
                                  bpy.context.scene.length, 
                                  passRules )
        
        return {'FINISHED'}


''' 
Class that generates the UI
'''
# UI Class
class demoUI(bpy.types.Panel):
    # Creates side panel in the 3D Viewport under Misc
    bl_idname = "VIEW3D_PT_L_Systems"
    bl_label = "L-Systems"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Lumi_Tools" 
    
    # To draw/create the actual panels
    def draw(self, context):
        # Generating fields that will be visible in the Panel
        layout = self.layout
        col = layout.column(align = True)
        
        layout.label(text="L-Systems Parameters: ")
        col = layout.column(align = True)
              
        for(prop_name, _) in PROPS[:6]:
            row = col.row(align = True)
            row.prop(context.scene, prop_name)    
        
        layout.label(text="L-System Rules: ", icon = 'ERROR')
        layout.label(text="Enter the rules in format 'A(Rule Variable):AB(Actual Rule)'")
        
        col = layout.column(align = True)
        
        col.scale_y = 1.5
        ## Debugging
        #print(bpy.context.scene.numRules)
        for(prop_name, _) in PROPS[6 : 6+(bpy.context.scene.numRules)]:
            row = col.row(align = True)
            row.prop(context.scene, prop_name)
        
        col = layout.column(align = True)
        col.scale_y = 2
        col.operator("opr.generate_l_system", text="Generate System", icon = 'DISCLOSURE_TRI_RIGHT')
        
        
'''
Driver Code
This part registers the classes with Blender and makes the add-on actually work!
Don't skip this part!!
'''

# To auomate the installation and uninstallation of multiple scripts/classes
# Just add the class names in this list
CLASSES = [
    generateLSystems,
    demoUI
]    

# To register all the classes
def register():
    # Registering the Properties before the classes
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
        
    for cls in CLASSES:
        bpy.utils.register_class(cls)
        
# To unregister all the classes
def unregister():
    # Un-registering the Properties before the classes
    for(prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
        
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)
        
# Calling the register or constructor
if __name__ == "__main__":
    register()