'''
To call this file, load it into the Blender text editor and the use the following command/code

my_module = bpy.data.texts[<nameOfModule>"Basic_Funcs.py"].as_module()

Then use my_module to access the function offered!
'''


import bpy
from math import radians
import os

'''
Starting Code
Global Variables, paths, boilerplate code
'''
# Macros
C = bpy.context
D = bpy.data
O = bpy.ops

# Getting path
dir = os.path.dirname(D.filepath)


''' 
This is just some general code to set properties/modifiers to the objects that 
Will be used later on in the process 
'''
## Boilerplate Code
# Deleting every object from the scene
def clear():
    ## Just for security
    #D.texts['summon.py'].use_fake_user = True
    
    O.object.select_all(action='SELECT')
    
    O.object.delete()

# For clearing the outliner
def removeCollections():
    # Deleting all collections
    for coll in bpy.data.collections: 
        ## Debugging
        #print(coll.name)
        
        # If it is a valid collection, then remove it
        if(coll):
            bpy.data.collections.remove(coll)

# Clearing the scene
def deleteAll():
    # Checking if scene is already empty
    if(len(D.scenes['Scene'].objects) > 0):
        # Setting mode to OBJECT in case we are in any other mode
        O.object.mode_set(mode='OBJECT')
        
        # Deleting everything that was present 
        O.object.select_all(action='SELECT')
        O.object.delete()
        
        print("Successfully deleted the objects!")
    
    else:
        print("Nothing to delete! Scene already empty.")
    
    # Clearing the project (Purging)
    O.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    
    
# Set the render parameters
def render_quality(engine, samples):
    # Set the render engine "BLENDER_EEVEE" or "CYCLES"
    C.scene.render.engine = engine
        
    if(engine=='CYCLES'):
        D.scenes['Scene'].cycles.samples = samples
    
    else:
        # Viewport Quality
        D.scenes['Scene'].eevee.taa_samples = 32
        
        # Render Quality
        D.scenes['Scene'].eevee.taa_render_samples = samples
        
        # Enabling some options
        D.scenes['Scene'].eevee.use_bloom = True
        D.scenes['Scene'].eevee.use_gtao = True
        D.scenes['Scene'].eevee.use_ssr = True
        
        
        ''' 
        Only enable this section when required
        '''
        # Setting the quality
        ## Shadows
        D.scenes['Scene'].eevee.shadow_cube_size = '1024'
        D.scenes['Scene'].eevee.shadow_cascade_size = '1024'
        D.scenes['Scene'].eevee.use_shadow_high_bitdepth = True
        
        ## Performance
        D.scenes['Scene'].render.use_high_quality_normals = True
        
        ## Indirect Lighting***** IMPORTANT FOR GOOD QUALITY
        # Freeing the light bake if already performed
        O.scene.light_cache_free()
        
        # Only bake once
        D.scenes['Scene'].eevee.gi_diffuse_bounces = 5
        D.scenes['Scene'].eevee.gi_cubemap_resolution = '1024'
        D.scenes['Scene'].eevee.gi_visibility_resolution = '16'
        
        # Baking the light, this will take a lot of time depending on the parameters above
        O.scene.light_cache_bake()
        
        
## Physics properties
# Setting rigidbody contraints 
def set_rigidbody_constraints(obj, rtype):
    # Getting the active object's name
    name = obj.name
    #print(name)
    
    # Adding the rigidbody property
    O.rigidbody.object_add(type = rtype)
    
# Setting Physics properties   
def set_physics(obj, type):
    obj.modifiers.new(obj.name+type, type)
    
# Adding a camera
def add_camera(loc, rot, translate_loc):
    O.object.camera_add(location=camera_loc, rotation=camera_rot)
    
    # Translating the object
    O.transform.translate(value=translate_loc)
    
    # Instancing the active object
    ao = C.active_object




'''
This part includes the driver code
Starting from importing the models to translating them in space to their proper location
And correcting their origin points
'''
## Driver Code
# Importing the model
def importModel(fileName, name):
    O.import_scene.import_pcd(filepath=dir+"\\{}".format(fileName))
    
    # Renaming the object
    C.object.name = name     

# Importing the Armature
def importArmature(path, name):
    O.import_scene.fbx(filepath=dir+"\\"+path)
    
    # Renaming the armature
    if(path=="Walking_Trial.fbx" or path=="Walking.fbx" or path=="WalkingInPlace.fbx"):
        C.object.name = "armature"
    
    else:
        C.object.name = "metarig"
    
# Installing the add-on
def installAddOn(name):
    O.preferences.addon_install(filepath=dir+"\\"+name+".zip")
    O.preferences.addon_enable(module=name)
    
    # Debugging
    print("Successfully Installed the add-on:", name)


'''
To bake/apply the various transforms and modifiers applied
'''
def bake_data():
    for scene in D.scenes:
        for object in scene.objects:
            for modifier in object.modifiers:
                if modifier.type == 'FLUID':
                    if modifier.fluid_type == 'DOMAIN':
                        print("Baking fluid")
                        object.select_set(True)
                        C.view_layer.objects.active = object
                        O.fluid.bake_data()
                elif modifier.type == 'CLOTH':
                    print("Baking cloth")
                    override = {'scene': scene, 'active_object': object, 'point_cache': modifier.point_cache}
                    O.ptcache.free_bake(override)
                    O.ptcache.bake(override, bake=True)
                elif modifier.type == 'PARTICLE_SYSTEM':
                    print("Baking particles")
                    override = {'scene': scene, 'active_object': object, 'point_cache': modifier.particle_system.point_cache}
                    O.ptcache.free_bake(override)
                    O.ptcache.bake(override, bake=True)

# To apply all the modifiers on an object
def apply_modifiers():
    for scene in D.scenes:
        for object in scene.objects:
            #print(object.name)
            object.select_set(True)
            C.view_layer.objects.active = object
            for modifiers in object.modifiers:
                # We don't need to bake the armature, since we will animate the model using this later
                if(modifiers.name=='Armature'):
                    continue
                
                else:
                    O.object.modifier_apply(modifier=modifiers.name)

# To save the file        
def save_file(name):
    # Save the file
    O.wm.save_as_mainfile(filepath=dir+name, filter_blender=False)