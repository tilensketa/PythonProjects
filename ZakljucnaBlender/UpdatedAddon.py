bl_info = {
    "name": "Render Add-on",
    "description": "",
    "author": "Tilen Sketa",
    "version": (1, 0, 0),
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
from mathutils import Color
import colorsys

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

def update_environment_strength(self, context):
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = self.float_environment_strength

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(PropertyGroup):
    
    float_environment_strength: FloatProperty(
        name = "Environment Light Strength",
        description="Strength of environment texture",
        default = 1,
        min = 0,
        max = 2,
        update = update_environment_strength,
        step = 1
        )
        
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
        
    the_chosen_collection : PointerProperty(
        name="Collection",
        description="Choose collection",
        type=bpy.types.Collection
        )
        

# ------------------------------------------------------------------------
#    Functions
# ------------------------------------------------------------------------

def prepare_environment(shadow_catcher_bool: bool, renderer: str, background_image_bool: bool, environment_strength: float):
    """Enable/disable shadow catcher and background image, set render engine and environment strength, append material"""
    # Get refrences
    scene = bpy.context.scene
    shadow_catcher = scene.objects["ShadowCatcher"]
    # Turn on/off shadow catcher, change render engine, background image on/off
    shadow_catcher.hide_render = shadow_catcher_bool
    scene.render.engine = renderer
    scene.render.film_transparent = background_image_bool
    # Set environment texture strength
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = environment_strength

def prepare_object(part: bpy.types.Object, material_name: str):
    """Clear object materials and append material"""
    part.data.materials.clear()
    part.data.materials.append(bpy.data.materials[material_name])

def render_scene(number_of_positions: int, max_offset: int, around: int, output_dir: str, collection: bpy.types.Collection, environment_strength: float):
    """Position, rotate object and make render"""
    # Get scene reference
    scene = bpy.context.scene
    
    step = 0
    
    # For every position
    for pos in range(number_of_positions):
        # Set object location
        angles = []
        angle = random.uniform(0, math.radians(360))
        for obj in bpy.data.collections[collection.name].all_objects:
            angle += math.radians(360/len(bpy.data.collections[collection.name].all_objects))
            angles.append(angle)
        for obj in bpy.data.collections[collection.name].all_objects:
            r = random.uniform(max_offset/2, max_offset)
            ang = angles[random.randint(0, len(angles) - 1)]
            angles.remove(ang)
            x = r * math.cos(ang)
            y = r * math.sin(ang)
            obj.location = x,y,obj.location.z
        
        # Set object rotation
        for obj in bpy.data.collections[collection.name].all_objects:
            rz = math.radians(random.randint(0, 359))
            obj.rotation_euler[2] = rz
        
        # For every angle in around
        for i in range(around):
            # Calculate angle in radians
            angle = math.radians(360 / around)
            # Set object's z rotation
            for obj in bpy.data.collections[collection.name].all_objects:
                obj.rotation_euler[2] += angle
            # Change black/white to normal mode
            for j in range(2):
                if j == 0:
                    prepare_environment(False, "CYCLES", True, environment_strength)
                    for i, obj in enumerate(bpy.data.collections[collection.name].all_objects):
                        prepare_object(obj, "Part Material " + str(i))
                else:
                    prepare_environment(True, "BLENDER_EEVEE", False, 0)
                    for i, obj in enumerate(bpy.data.collections[collection.name].all_objects):
                        prepare_object(obj, "Emmision " + str(i))
                
                # Configure output path
                output_file_pattern_string = 'render%d.jpg'
                
                # Render image and save it
                scene.render.filepath = os.path.join(output_dir, (output_file_pattern_string % step))
                bpy.ops.render.render(write_still = True)
                step += 1
    
    # Set normal color mode
    prepare_environment(False, "BLENDER_EEVEE", True, environment_strength)
    for i, obj in enumerate(bpy.data.collections[collection.name].all_objects):
        prepare_object(obj, "Part Material " + str(i))
    
def setup_background():
    """Make background image on render"""

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

def setup_basics(collection: bpy.types.Collection):
    """Delete all materials except Part Materials, create Emmision materials, delete camera and light and create shadow catcher"""
    # Get reference to scene
    scene = bpy.context.scene
    
    # Remove all materials that are not Part Material
    materials = []
    number_of_objects = len(bpy.data.collections[collection.name].all_objects)
    for i in range(number_of_objects):
        materials.append("Part Material " + str(i))

    for material in bpy.data.materials:
        if material.name not in materials:
            material.user_clear()
            bpy.data.materials.remove(material)
    
    # Create emmision materials
    if number_of_objects > 1:
        for i, obj in enumerate(bpy.data.collections[collection.name].all_objects):
            emmision_mat = bpy.data.materials.new(name="Emmision "+ str(i))
            emmision_mat.use_nodes = True
            h = (1 / number_of_objects) * i
            hsv_color = colorsys.hsv_to_rgb(h, 1, 1)
            rgb_color = (hsv_color[0], hsv_color[1], hsv_color[2], 1)
            emmision_mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = rgb_color
    else:
        for i, obj in enumerate(bpy.data.collections[collection.name].all_objects):
            emmision_mat = bpy.data.materials.new(name="Emmision "+ str(i))
            emmision_mat.use_nodes = True
            hsv_color = colorsys.hsv_to_rgb(1, 0, 1)
            rgb_color = (hsv_color[0], hsv_color[1], hsv_color[2], 1)
            emmision_mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = rgb_color
    
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

        setup_basics(mytool.the_chosen_collection)
        setup_background()
        render_scene(
            mytool.int_number_of_positions,
            mytool.int_max_offset,
            mytool.int_around_angles,
            mytool.string_path,
            mytool.the_chosen_collection,
            mytool.float_environment_strength)
        
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
        layout.prop(rd.image_settings, "file_format")
        layout.prop(rd.image_settings, "color_depth")
        layout.prop(mytool,  "float_environment_strength")
        layout.prop(mytool, "int_around_angles")
        layout.prop(mytool, "int_number_of_positions")
        layout.prop(mytool, "int_max_offset")
        layout.prop(mytool, "the_chosen_collection")
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
