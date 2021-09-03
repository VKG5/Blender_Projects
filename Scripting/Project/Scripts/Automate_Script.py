import bpy
from math import radians

# Deleting every object from the scene
def clear():
    ## Just for security
    #bpy.data.texts['summon.py'].use_fake_user = True
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
## Set the render parameters
def render_quality(engine, samples):
    # Set the render engine "BLENDER_EEVEE" or "CYCLES"
    bpy.context.scene.render.engine = engine
    bpy.data.scenes['Scene'].cycles.samples = samples
    
### Setting rigidbody contraints 
def set_rigidbody_constraints(obj, rtype):
    # Getting the active object's name
    name = obj.name
    #print(name)
    
    # Adding the rigidbody property
    bpy.ops.rigidbody.object_add(type = rtype)

### Subsurf modifier
def subsurf(obj, levels):
    index = obj.name+'Subdivision'
    obj.modifiers.new(name = index, type='SUBSURF')
    obj.modifiers[index].subdivision_type = 'SIMPLE'
    # ViewPort samples
    obj.modifiers[index].levels = levels 
    obj.modifiers[index].render_levels = levels
    
    # Smoothing
    mesh = obj.data
    for face in mesh.polygons:
        face.use_smooth = True
     
### Setting Physics properties   
def set_physics(obj, type):
    obj.modifiers.new(obj.name+type, type)

### Adding the cube   
def add_cube(loc, size, tranalste_loc):
    ## Adding an object
    bpy.ops.mesh.primitive_cube_add(location=loc, scale=size)

    # Translating the object
    bpy.ops.transform.translate(value=translate_loc)
    
    # Instancing the active object
    ao = bpy.context.active_object
        
    # Rigidbody properties
    set_physics(ao, 'COLLISION')
    
    return ao
    
### Adding the plane
def add_plane(loc, scaling_factor, sub_surf_levels):
    bpy.ops.mesh.primitive_plane_add(location=loc, size=scaling_factor)
    
    ao = bpy.context.active_object
    
    # Rigidbody properties
    subsurf(ao, sub_surf_levels)
    set_physics(ao, 'CLOTH')
    
    return ao

### Adding a camera
def add_camera(loc, rot, translate_loc):
    bpy.ops.object.camera_add(location=camera_loc, rotation=camera_rot)
    
    # Translating the object
    bpy.ops.transform.translate(value=translate_loc)
    
    # Instancing the active object
    ao = bpy.context.active_object
    
    return ao

def bake_data():
    for scene in bpy.data.scenes:
        for object in scene.objects:
            for modifier in object.modifiers:
                if modifier.type == 'FLUID':
                    if modifier.fluid_type == 'DOMAIN':
                        print("Baking fluid")
                        object.select_set(True)
                        bpy.context.view_layer.objects.active = object
                        bpy.ops.fluid.bake_data()
                elif modifier.type == 'CLOTH':
                    print("Baking cloth")
                    override = {'scene': scene, 'active_object': object, 'point_cache': modifier.point_cache}
                    bpy.ops.ptcache.free_bake(override)
                    bpy.ops.ptcache.bake(override, bake=True)
                elif modifier.type == 'PARTICLE_SYSTEM':
                    print("Baking particles")
                    override = {'scene': scene, 'active_object': object, 'point_cache': modifier.particle_system.point_cache}
                    bpy.ops.ptcache.free_bake(override)
                    bpy.ops.ptcache.bake(override, bake=True)
    
    # Save the file
    bpy.ops.wm.save_as_mainfile(filepath="F:\Blender\Blender\Scripting\Simul.blend")

# To apply all the modifiers on an object
def apply_modifiers():
    for scene in bpy.data.scenes:
        for object in scene.objects:
            #print(object.name)
            object.select_set(True)
            bpy.context.view_layer.objects.active = object
            for modifiers in object.modifiers:
                #print(modifiers.name)
                bpy.ops.object.modifier_apply(modifier=modifiers.name)
                
# Parameters (x,y,z)
loc_c = (0,0,0)
loc_p = (0,0,5)
camera_loc = (0,0,0)
camera_rot = (radians(90),radians(0),radians(0))
camera_trans = (0,-15,0)
size = (1,1,1)    
translate_loc = (0,0,0)
scaling_factor = 7
sub_surf_levels = 5

# Calling the functions (Creating instances)
clear()
render_quality('CYCLES', 16)
cube = add_cube(loc_c, size, translate_loc)
plane = add_plane(loc_p, scaling_factor, sub_surf_levels)
camera = add_camera(camera_loc, camera_rot, camera_trans)

## To bake the data for faster playback
bake_data()

## **Optional**, if you want to apply the modifiers
# apply_modifiers()

    
## Trial Rotation + Access
#cube.rotation_euler[2] += radians(45)
#plane.rotation_euler[2] += radians(45)
