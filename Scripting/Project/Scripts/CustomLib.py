## Boilerplate Code
# Deleting every object from the scene
def clear():
    ## Just for security
    #bpy.data.texts['summon.py'].use_fake_user = True
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
# Set the render parameters
def render_quality(engine, samples):
    # Set the render engine "BLENDER_EEVEE" or "CYCLES"
    bpy.context.scene.render.engine = engine
    bpy.data.scenes['Scene'].cycles.samples = samples
    
## Physics properties
# Setting rigidbody contraints 
def set_rigidbody_constraints(obj, rtype):
    # Getting the active object's name
    name = obj.name
    #print(name)
    
    # Adding the rigidbody property
    bpy.ops.rigidbody.object_add(type = rtype)
    
# Setting Physics properties   
def set_physics(obj, type):
    obj.modifiers.new(obj.name+type, type)
    
# Adding a camera
def add_camera(loc, rot, translate_loc):
    bpy.ops.object.camera_add(location=camera_loc, rotation=camera_rot)
    
    # Translating the object
    bpy.ops.transform.translate(value=translate_loc)
    
    # Instancing the active object
    ao = bpy.context.active_object