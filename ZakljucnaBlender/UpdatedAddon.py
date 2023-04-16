bl_info = {
    "name": "Render Add-on",
    "description": "",
    "author": "Tilen Sketa",
    "version": (0, 3, 0),
    "blender": (3, 0, 1),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

import bpy
import math
import os
import random
import sys

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(PropertyGroup):
        
    int_around_angles: IntProperty(
        name = "Around Angles",
        description="Number of object rotations",
        default = 4,
        min = 1,
        max = 32
        )
        
    int_number_of_positions: IntProperty(
        name = "Number Of Positions",
        description="Number of object positions",
        default = 1,
        min = 1,
        max = 10
        )
        
    int_max_offset: IntProperty(
        name = "Max Offset",
        description="Max offset for position",
        default = 0,
        min = 0,
        max = 10
        )
        
    string_path: StringProperty(
        name = "Output",
        description="Choose a directory:",
        default="",
        subtype='FILE_PATH'
        )
        
    the_chosen_object : PointerProperty(
        name="Object",
        description="Choose object",
        type=bpy.types.Object
        )
        

# ------------------------------------------------------------------------
#    Functions
# ------------------------------------------------------------------------

def setupEnvironment(black_white, part):
    
    # Get scene reference
    scene = bpy.context.scene

    # Reference shadow catcher
    shadowCatcher = scene.objects["ShadowCatcher"]
    
    # If black and white image is selected
    if black_white == True:
        # Turn off shadow catcher
        shadowCatcher.hide_render = True
        # Change rendere engine to eevee
        scene.render.engine = "BLENDER_EEVEE"
        # Set background image to false
        scene.render.film_transparent = False
        # Make world black
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0
        # Reference emmision material
        emmision_mat = bpy.data.materials["Emmision"]
        # Delete materials
        part.data.materials.clear()
        # Set object material to emmision
        part.data.materials.append(emmision_mat)

    # If black and white mode is not selected
    else:
        # Turn on shadow catcher
        shadowCatcher.hide_render = False
        # Change rendere engine to cycles
        scene.render.engine = 'CYCLES'
        # Set background image to false
        scene.render.film_transparent = True
        # Make world not black
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.5
        # Delete materials
        part.data.materials.clear()
        # Set object material to Part Material
        part.data.materials.append(bpy.data.materials["Part Material"])


def renderScene(numberOfPositions, maxOffset, around, output_dir, part):
    
    # Get scene reference
    scene = bpy.context.scene
    
    step = 0
    
    # For every position
    for pos in range(0, numberOfPositions):
        # Set object location
        x = random.uniform(-maxOffset, maxOffset)
        y = random.uniform(-maxOffset, maxOffset)
        part.location = x,y,part.location.z
        
        # Set object rotation
        rx = math.radians(90)
        rz = math.radians(random.randint(0, 359))
        part.rotation_euler = rx,0,rz
        
        # For every angle in around
        for i in range(around):
            # Calculate angle in radians
            angle = math.radians(360 / around)
            # Set part z rotation
            part.rotation_euler[2] += angle
            # Change black/white to normal mode
            for j in range(2):
                if j == 0:
                    setupEnvironment(False, part)
                else:
                    setupEnvironment(True, part)
                
                # Configure output path
                output_file_pattern_string = 'render%d.jpg'
                
                # Render image and save it
                scene.render.filepath = os.path.join(output_dir, (output_file_pattern_string % step))
                bpy.ops.render.render(write_still = True)
                    
                step += 1
    
    # Set normal color mode
    setupEnvironment(False, part)
    scene.render.engine = "BLENDER_EEVEE"
    
def setupBackground():

    # general settings
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.use_nodes = True
    compositor = bpy.context.scene.node_tree

    #get background image struct
    active_cam = bpy.context.scene.camera.name
    bg_images = bpy.data.objects[active_cam].data.background_images.items()

    # get background image data, if it exists in struct
    try:
        image = bg_images[0][1].image
        image_scale = bg_images[0][1].scale
    except:
        sys.exit("No Background Found")


    # create new compositor node, if it not already exists
    node_names = {"bg_image_node":"CompositorNodeImage", "alpha_over_node":"CompositorNodeAlphaOver", "frame_method_node":"CompositorNodeScale", "scale_node":"CompositorNodeScale"}
    current_nodes = compositor.nodes.keys()

    for name,type in node_names.items():
        if name not in current_nodes:
            node = compositor.nodes.new(type=type)
            node.name = name
            

    #edit compositor nodes  
    bg_image_node = compositor.nodes["bg_image_node"]
    bg_image_node.image = image

    alpha_over_node = compositor.nodes["alpha_over_node"]
    alpha_over_node.location[0] = 600

    frame_method_node = compositor.nodes["frame_method_node"]
    frame_method_node.space = "RENDER_SIZE"
    frame_method_node.location[0] = 200

    scale_node = compositor.nodes["scale_node"]
    scale_node.inputs[1].default_value = image_scale
    scale_node.inputs[2].default_value = image_scale
    scale_node.location[0] = 400


    #link compositor nodes
    compositor.links.new(compositor.nodes["Render Layers"].outputs[0], alpha_over_node.inputs[2])
    compositor.links.new(bg_image_node.outputs[0], frame_method_node.inputs[0])
    compositor.links.new(frame_method_node.outputs[0], scale_node.inputs[0])
    compositor.links.new(scale_node.outputs[0], alpha_over_node.inputs[1])
    compositor.links.new(alpha_over_node.outputs[0], compositor.nodes["Composite"].inputs[0])

def setupBasics():
    
    # Get reference to scene
    scene = bpy.context.scene
    
    # Remove all materials that are not Part Material
    for material in bpy.data.materials:
        if material.name != "Part Material":
            material.user_clear()
            bpy.data.materials.remove(material)
    
    # Create emmision material
    emmision_mat = bpy.data.materials.new(name="Emmision")
    emmision_mat.use_nodes = True
    emmision_mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = (1, 1, 1, 1)
    
    # Deselect all objects
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    
    # Select camera and light
    for o in scene.objects:
        if o.name == "Camera" and o.type == "CAMERA":
            o.select_set(True)
        if o.name == "Light":
            o.hide_render = True
            o.hide_set(True)
    
    # Delete camera     
    bpy.ops.object.delete()
    
    # Get reference to shadowCatcher
    catcher = bpy.context.scene.objects.get("ShadowCatcher")
    # If there is no catcher make one
    if not catcher:
        plane = bpy.ops.mesh.primitive_plane_add(
            size=10, 
            enter_editmode=False, 
            align='WORLD', 
            location=(0, 0, 0), 
            scale=(1, 1, 1))
        # Make planes name ShadowCatcher
        bpy.context.object.name = "ShadowCatcher"
        # Set scene visibility
        bpy.context.object.hide_set(True)
        # Switch to cycles, turn shadow_catcher on, switch back to eevee
        scene.render.engine = 'CYCLES'
        bpy.context.object.is_shadow_catcher = True
        scene.render.engine = "BLENDER_EEVEE"
    
    # If catcher exists
    else:
        # Set scene visibility
        catcher.hide_set(True)
        # Switch to cycles, turn shadow_catcher on, switch back to eevee
        scene.render.engine = 'CYCLES'
        catcher.is_shadow_catcher = True
        scene.render.engine = "BLENDER_EEVEE"

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class WM_OT_ExecuteButton(Operator):
    bl_label = "Execute"
    bl_idname = "wm.execute_button"

    # On click
    def execute(self, context):
        # Get scene and mytool reference
        scene = context.scene
        mytool = scene.my_tool
        
        setupBasics()
        setupBackground()
        # Do renderScene function
        renderScene(
            mytool.int_number_of_positions,
            mytool.int_max_offset,
            mytool.int_around_angles,
            mytool.string_path,
            mytool.the_chosen_object)
        
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_label = "My Panel"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_context = "objectmode"

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        rd = context.scene.render

        layout.prop(rd, "resolution_x", text="Resolution X")
        layout.prop(rd, "resolution_y", text="Resolution Y")
        layout.prop(rd, "resolution_percentage", text="%")
        layout.prop(mytool, "int_around_angles")
        layout.prop(mytool, "int_number_of_positions")
        layout.prop(mytool, "int_max_offset")
        layout.prop(mytool, "the_chosen_object")
        layout.prop(mytool, "string_path")
        layout.operator("wm.execute_button")

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    WM_OT_ExecuteButton,
    OBJECT_PT_CustomPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()
