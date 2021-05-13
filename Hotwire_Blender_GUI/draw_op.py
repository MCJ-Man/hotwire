bl_info = {
    "name" : "Line Strips",
    "authro" : "jayanam",
    "desription" : "",
    "blender" : (2,80,0),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy
import sys
sys.path.append('C:\\Users\\JMCrosair\\Documents\\20-Studiwerkstatt\\01 Robotik\\10_Blender')
import draw_op

import bpy

import bgl

import gpu

from gpu_extras.batch import batch_for_shader

from bpy.types import Operator

class OT_draw_operator(Operator):
    bl_idname = "object.draw_op"
    bl_label = "Draw operator"
    bl_description = "Operator for drawing"
    bl_options ={'REGISTER'}
    v = [(1,3,3), (0,4,4), (0,6,2), (0,0,1)]
    
    def __init__(self):
        self.draw_handle = None
        self.draw_event = None
        
        self.widgets = []
        
    def invoke(self, context, event):
        
        self.create_batch()
        
        args = (self, context)
        self.register_handlers(args, context)
        
        context.window_manager.modal_handler_add(self)
        return{"RUNNING_MODAL"}
    
    def register_handlers(self, args, context):
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_px, args, "WINDOW", "POST_VIEW")
        
        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)
        
    def unregister_handlers(self, context):
        
        context.window_manager.event_timer_remove(self.draw_event)
        
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")
        
        self.draw_handle = None
        self.draw_event = None
        
    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()
            
        if event.type in {"ESC"}:
            self.unregister_handlers(context)
            return {'CANCELLED'}
        
        return {"PASS_THROUGH"}
    
    def finish(self):
        self.unregister_handlers(context)
        return {"FINISHED"}
    
    def create_batch(self, vertices=[(1,3,3), (0,4,4), (0,6,2), (0,0,3)]):
        
        #vertices = [(1,3,3), (0,4,4), (0,6,2), (0,0,3)]
        vertices = OT_draw_operator.v
        
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINE_STRIP', {"pos": vertices})
        
    # Draw hander to paint onto the screen
    def draw_callback_px(self, op, context):
        
        #Draw lines
        self.shader.bind()
        self.shader.uniform_float("color", (1,1,1,1))
        self.batch.draw(self.shader)


#######################################################################
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
#######################################################################

###OT_draw_operator

addon_keymaps = []

def register():
    bpy.utils.register_class(OT_draw_operator)
    
    kcfg = bpy.context.window_manager.keyconfigs.addon
    if kcfg:
        km = kcfg.keymaps.new(name='3D View', space_type='VIEW_3D')
        
        kmi = km.keymap_items.new("object.draw_op", 'F', 'PRESS', shift=True, ctrl=True)
        
        addon_keymaps.append((km, kmi))
        
def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(OT_draw_operator)
    
if False:#__name__== "__main__":  #FOR DEBUG ONLY
    register()
    #unregister()
    OT_draw_operator.v=[(1,3,3), (0,4,4), (0,6,2), (0,0,6)]
    #create_batch(self, vertices=v)
    
def starter():
    register()
    return OT_draw_operator