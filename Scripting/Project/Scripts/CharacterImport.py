import bpy
from math import radians

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

## Driver Code
# Importing the model
def importModel():
    bpy.ops.import_mesh.ply(filepath="F:\Blender\Blender\Scripting\Project\man-in-red-crew-neck-sweatshirt-photography-941693.png_000.ply")

    # Instancing
    ao = bpy.context.active_object
    
    return ao

# Centering the model
def centreModel(model, scene):
    zverts = []

    # get all z coordinates of the vertices
    for face in model.data.polygons:
        verts_in_face = face.vertices[:]
        for vert in verts_in_face:
            local_point = model.data.vertices[vert].co
            world_point = model.matrix_world @ local_point
            zverts.append(world_point[2])
            
    # set the minimum z coordinate as z for cursor location
    scene.cursor.location = (0, 0, min(zverts))
    
    # set the origin to the cursor
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    
    # set the object to (0,0,0)
    model.location = (0,0,0)
    
    # reset the cursor
    scene.cursor.location = (0,0,0)
    
    # Rotating the model
    model.rotation_euler = (radians(-90), radians(0), radians(0))
    
# All the preprocessing
# Centering, Shading Smooth, etc.
def preprocessing(model):
    # Shading smooth the model
    bpy.ops.object.shade_smooth()
    
    # get the scene
    scene = bpy.context.scene
    
    # Resetting the origin
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    
    centreModel(model, scene)
    
    # Resetting the origin again
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    
    # Translation
    model.location = (0, 0, 1.25)
    
    # Converting Tris to Quads
    # Cleaning Topology 
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.tris_convert_to_quads()
    bpy.ops.object.editmode_toggle()

# Calling the functions
clear()
render_quality('CYCLES', 32)
model = importModel()
preprocessing(model)
set_physics(model, 'COLLISION')