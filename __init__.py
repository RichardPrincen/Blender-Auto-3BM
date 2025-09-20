bl_info = {
    "author": "Amir Hossein Mafi <amir77mafi@gmail.com>, Richard Princen <princenrichard@gmail.com>",
    "version": (2, 0),
    "blender": (4, 0, 0),
    "description": 'Automatically enables "Emulate 3 Button Mouse" when entering certain modes',
    "category": "3D View",
}

import bpy
from bpy.app.handlers import persistent

def callback_mode_change(object, data):
    if bpy.context.mode == "SCULPT" or bpy.context.mode == "PAINT_WEIGHT" or bpy.context.mode == "PAINT_VERTEX_COLOR" or bpy.context.mode == "PAINT_TEXTURE" or bpy.context.mode == "VERTEX_PAINT" or bpy.context.mode == "PARTICLE":  
        bpy.context.preferences.inputs.use_mouse_emulate_3_button=True
    else:
        bpy.context.preferences.inputs.use_mouse_emulate_3_button=False

owner = object()

def subscribe_mode_change():
    subscribe_to = (bpy.types.Object, "mode")

    bpy.msgbus.subscribe_rna(
        key=subscribe_to,
        owner=owner,
        args=(owner,"mode",),
        notify=callback_mode_change,
    )

def unsubscribe_mode_change():
    bpy.msgbus.clear_by_owner(owner)

@persistent
def load_handler(dummy):
    subscribe_mode_change()

def register():
    print("register")
    bpy.app.handlers.load_post.append(load_handler)
    
    # subscribe for the first time use, so we don't need to restart the blend file
    subscribe_mode_change()

def unregister():
    bpy.app.handlers.load_post.remove(load_handler)

    # unsubscribe after unregister, so we don't need to restart the blend file
    unsubscribe_mode_change()
