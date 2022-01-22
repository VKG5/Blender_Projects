import bpy
from math import radians
import os

# Macros
C = bpy.context
D = bpy.data
O = bpy.ops

''' 
This is just some general code to set properties/modifiers to the objects that 
Will be used later on in the process 
'''
## Boilerplate Code
# Deleting every object from the scene
def clear():
    ## Just for security
    #bpy.data.texts['summon.py'].use_fake_user = True
    
    O.object.select_all(action='SELECT')
    
    O.object.delete()
    
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
        '''
        
# Import Code
def importModel(filePath, name):
    # Debugging code
    #print(dir)
    #print(dir+"\\Models\\{}".format(fileName))
    
    ## Importing the PCD (Point Cloud Distribution)
    O.import_scene.import_pcd(filepath=filePath)
    
    # Renaming the object
    C.object.name = name
    
# Centering the model
def centreModel(model, scene):
    # set the object to (0,0,0)
    model.location = (0,0,1)
    
    # reset the cursor
    scene.cursor.location = (0,0,0)
    
    # Rotating the model
    model.rotation_euler = (radians(-90), radians(0), radians(0))
    

'''
This section has all the preprocessing, for example, smoothing the model, optimizing it,
Linking the armature to the mesh and adding/running cloth sims
'''
# All the preprocessing
# Centering, Shading Smooth, etc.
def preprocessing(model):
    # Shading smooth the model
    O.object.shade_smooth()
    
    # get the scene
    scene = C.scene
    
    # Resetting the origin
    O.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    
    centreModel(model, scene)
    
    # Applying the transforms
    O.object.transform_apply(location=False, rotation=True, scale=True)


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
    
