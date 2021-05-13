#HOTWIRE BLENDER GUI
#toolpath visualization and robot movement simulation
#
#Meant for failsafe purposes only:
#Preferrably use "Hotwire_Blender_GUI.blend"
#If the .blend file doesn't work use this script
#
#This script is to be run in Blender-Python
#
#copy this code into a Blender text editor
#edit the homepath to the location of your Hotwire_GUI source file
#save the file in Blender as ui.py and click run script      |
#                                                            \/
####################################################################
homepath = 'C:\\Users\\[***usrnme***]\\[***folder***]\\Hotwire_GUI'#
####################################################################
#
import sys
import numpy as np
from numpy import pi
sys.path.append(homepath)
import Hotwire_Blender_GUI.robo_caller as robo_caller
from src.robo_moveto import moveto
from src.robo_moveto import Rx, Ry, Rz
import Hotwire_Blender_GUI.draw_op as draw_op

obj_list = robo_caller.starter(homepath)
OP_Draw = draw_op.starter()
OP_Draw.v = [(1,3,3), (0,4,4), (0,6,2), (0,0,0)]

bl_info = {
    "name": "Add-on Template",
    "description": "",
    "author": "p2or",
    "version": (0, 0, 3),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}


import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------



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
import bgl
import gpu

from gpu_extras.batch import batch_for_shader
from bpy.types import Operator

##########################################################################
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
    
    def create_batch(self):
        vertices = OT_draw_operator.v
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINE_STRIP', {"pos": vertices})
        
    def draw_callback_px(self, op, context):    # Draw hander to paint onto the screen
        
        #Draw lines
        self.shader.bind()
        self.shader.uniform_float("color", (1,1,1,1))
        self.batch.draw(self.shader)
        
#################################################################################

def vec_from_abc(a,b,c):
    v = np.array([0,1,0])
    v = Rx(c*pi/180) @ v
    v = Ry(b*pi/180) @ v
    v = Rz(a*pi/180) @ v
    return v

class robo:
    obj_list = obj_list
    x = 0.715
    y = 0
    z = 1.200
    a = 0
    b = 0
    c = pi

class clocker:
    #t = time.
    def mouse_track():
        cl = bpy.context.scene.cursor.location
        moveto(cl[0], cl[1], cl[2], 0, 0, pi, robo.obj_list)

class MyProperties(PropertyGroup):      #####Property Klasse mit annotierten attributen

    my_bool: BoolProperty(
        name="Enable Mouse Track",
        description="A bool property",
        default = False
        )
        
    my_bool1: BoolProperty(
        name="Enable Euklidian Mode",
        description="A bool property",
        default = False
        )

    my_bool2: BoolProperty(
        name="Enable Axis Mode",
        description="A bool property",
        default = False
        )
        
    my_bool3: BoolProperty(
        name="show tool path",
        description="A bool property",
        default = False
        )

    my_int: IntProperty(
        name = "Step Size",
        description="A integer property",
        default = 10,
        min = 1,
        max = 100
        )
    #####float sliders#############################################
    my_float: FloatProperty(
        name = "A1",
        description = "A float property",
        default = 0,
        min = -180,
        max = 180,
        step = 50
        )
        
    my_float2: FloatProperty(
        name = "A2",
        description = "A float property",
        default = 0,
        min = -180,
        max = 180,
        step = 50
        )
        
    my_float3: FloatProperty(
        name = "A3",
        description = "A float property",
        default = 0,
        min = -180,
        max = 180,
        step = 50
        )
        
    my_float4: FloatProperty(
        name = "A4",
        description = "A float property",
        default = 0,
        min = -180,
        max = 180,
        step = 50
        )
        
    my_float5: FloatProperty(
        name = "A5",
        description = "A float property",
        default = 0,
        min = -180,
        max = 180,
        step = 50
        )
        
    my_float6: FloatProperty(
        name = "A6",
        description = "A float property",
        default = 0,
        min = -360,
        max = 360,
        step = 50
        )
            
    
    ####float sliders##########################################
    flv_xyz: FloatVectorProperty(
        name = "Float Vector Value",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= -2000, # float
        max = 2000,
        step = 50
    )
    
    flv_abc: FloatVectorProperty(
        name = "Float Vector Value",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= -180, # float
        max = 180,
        step = 10
    ) 

    my_string: StringProperty(
        name="User Input",
        description=":",
        default="",
        maxlen=1024,
        )

    my_path: StringProperty(
        name = "Directory",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
        )
        
    my_enum: EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[ ('OP1', "Option 1", ""),
                ('OP2', "Option 2", ""),
                ('OP3', "Option 3", ""),
               ]
        )

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------
class WM_Cam(Operator):        #######reinit button
    bl_label = "Set Camera"
    bl_idname = "wm.cam"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        camera_data = bpy.data.cameras.new(name='Camera')
        camera_object = bpy.data.objects.new('Camera', camera_data)
        bpy.context.scene.collection.objects.link(camera_object)
        
        i = LoadDat.pointer % LoadDat.datlen
        bpy.data.objects["Camera"].location[0] = LoadDat.x[i]
        bpy.data.objects["Camera"].location[1] = LoadDat.y[i]
        bpy.data.objects["Camera"].location[2] = LoadDat.z[i]
        
        
        unregister()
        register()
        return {'FINISHED'}

 
class WM_OT_HelloWorld(Operator):        #######GOTOMOUSE
    bl_label = "Go to Mouse"
    bl_idname = "wm.hello_world"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        cl = bpy.context.scene.cursor.location
        a, b, c = [mytool.flv_abc[i]/180*pi for i in (0, 1, 2)]
        moveto(cl[0], cl[1], cl[2], a, b, c, robo.obj_list)
        mytool.flv_xyz[0] = cl[0] * 1000
        mytool.flv_xyz[1] = cl[1] * 1000
        mytool.flv_xyz[2] = cl[2] * 1000
        return {'FINISHED'}
    
class WM_OT_HelloWorld1(Operator):        #######HOME BUTTON
    bl_label = "HOME"
    bl_idname = "wm.hello_world1"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        #OT_draw_operator.v = [(0,0,0), (0,4,4), (0,6,2), (0,0,0)]
        
        print("im home")
        moveto(0.815, 0, 1.000, 0, 0, pi, robo.obj_list)
        mytool.flv_xyz[0] = 0.815 * 1000
        mytool.flv_xyz[1] = 0.000 * 1000
        mytool.flv_xyz[2] = 1.000 * 1000
        mytool.flv_abc[0] = 0
        mytool.flv_abc[1] = 0
        mytool.flv_abc[2] = pi * 180/pi
        return {'FINISHED'}
    
class WM_OT_HelloWorld2(Operator):        #######reinit button
    bl_label = "Reinitialize"
    bl_idname = "wm.hello_world2"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        robo.obj_list = robo_caller.starter()
        unregister()
        register()
        return {'FINISHED'}
    
class GoToEuklid(Operator):        #######goto Euklid
    bl_label = "Update Euklidians"
    bl_idname = "wm.gotoeuklid"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        xyz = np.array(mytool.flv_xyz) /1000
        abc = np.array(mytool.flv_abc) /180*pi
        moveto(xyz[0], xyz[1], xyz[2], abc[0], abc[1], abc[2], robo.obj_list)
        return {'FINISHED'}
    
class GoToAxies(Operator):        #######goto axies
    bl_label = "Update Axies"
    bl_idname = "wm.gotoax"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        floaters = np.array([mytool.my_float, mytool.my_float2, mytool.my_float3, 
            mytool.my_float4, mytool.my_float5, mytool.my_float6]) /180*pi
        for obj, ang in zip(robo.obj_list, floaters):
            obj.rotate(ang)
            
        return {'FINISHED'}
    
class Bwd(Operator):        #######backwards
    bl_label = "Backwrad"
    bl_idname = "wm.bwd"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        if LoadDat.x is not None:
            LoadDat.pointer -= mytool.my_int
                
            i = LoadDat.pointer % LoadDat.datlen
            x, y, z = LoadDat.x[i], LoadDat.y[i], LoadDat.z[i]
            a, b, c = LoadDat.a[i], LoadDat.b[i], LoadDat.c[i]
            moveto(x, y, z, a, b, c, robo.obj_list)
            
            for i, euk in zip((0,1,2),(x,y,z)): mytool.flv_xyz[i]=euk*1000
            for i, ang in zip((0,1,2),(a,b,c)): mytool.flv_abc[i]=ang/pi*180
            
            print("bck button ordered xyz= ",x, y ,z)
            print("abc= ",a, b, c)
        return {'FINISHED'}
    
class Fwd(Operator):        #######forwards
    bl_label = "Forward"
    bl_idname = "wm.fwd"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        if LoadDat.x is not None:
            LoadDat.pointer += mytool.my_int
            i = LoadDat.pointer % LoadDat.datlen
            x, y, z = LoadDat.x[i], LoadDat.y[i], LoadDat.z[i]
            a, b, c = LoadDat.a[i], LoadDat.b[i], LoadDat.c[i]
                
            moveto(x, y, z, a, b, c, robo.obj_list)
            
            for i, euk in zip((0,1,2),(x,y,z)): mytool.flv_xyz[i]=euk*1000
            for i, ang in zip((0,1,2),(a,b,c)): mytool.flv_abc[i]=ang/pi*180
            
            print("=/=/=/=/=/=")
            print("loaddat.a \n{}".format(LoadDat.a))
        return {'FINISHED'}
    
class SetZero(Operator):        ####### SET ZERO
    bl_label = "Set Zero"
    bl_idname = "wm.setzero"
    zero = np.zeros(3)

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        ld = LoadDat.x, LoadDat.y, LoadDat.z
        for attr, i in zip((ld),(0,1,2)):
            attr -= SetZero.zero[i]
            
        SetZero.zero = np.array(list(mytool.flv_xyz)) /1000
        zer = SetZero.zero
        
        for attr, i in zip((ld),(0,1,2)):
            attr += SetZero.zero[i]
            
        dat = []
        draw_bridge = int(len(LoadDat.x) / 20)
            
        if LoadDat.sgs is None:
            for i in range(len(LoadDat.x)):
                dat.append( (LoadDat.x[i], LoadDat.y[i], LoadDat.z[i]) )
            
        else:
            for i in range(len(LoadDat.x)): 
                dat.append( (LoadDat.sgs[i][0]+zer[0], LoadDat.sgs[i][1]+zer[1], LoadDat.sgs[i][2]+zer[2]) )
                
                if i % draw_bridge == 0:
                    for y in range(draw_bridge):
                        dat.append( (LoadDat.sgs[i-y][3]+zer[0], LoadDat.sgs[i-y][4]+zer[1], LoadDat.sgs[i-y][5]+zer[2]) )
                        
                    for z in range(draw_bridge):
                        dat.append( (LoadDat.sgs[i-y+z][0]+zer[0], LoadDat.sgs[i-y+z][1]+zer[1], LoadDat.sgs[i-y+z][2]+zer[2]) )
                    
        OT_draw_operator.v = dat
            
        print("data zeroed, zero vector is: {}".format(SetZero.zero))
        return {'FINISHED'}
    
class LoadDat(Operator):        #######Load Data
    bl_label = "Load Data"
    bl_idname = "wm.loaddat"
    display = "...nothing loaded yet"
    iterator = "...0/-"
    pointer = 0
    datlen = 0
    sgs = None
    x, y, z, a, b, c = 0, 0, 0, 0, 0, 0
    
    def update_path(self):
        dat = np.array([LoadDat.x, LoadDat.y, LoadDat.z])
        dat = np.transpose(dat)    #format: [(0,0,0), (0,4,4), (0,6,2), (0,0,0)]
        OT_draw_operator.v = dat

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        path = mytool.my_path
        #try:
        if True:
            SetZero.zero = np.zeros(3)
            LoadDat.pointer = 0
            loaded = np.genfromtxt(path, delimiter=';')
            sgs = None
            if np.isnan(loaded).any():
                nandex = np.unique( np.where(np.isnan(loaded))[0] )
                print(nandex)
                ld = loaded[nandex[0]+1:nandex[1]]
                sgs = loaded[nandex[1]+1:] /1e3
            else: ld = loaded
            
            LoadDat.x, LoadDat.y, LoadDat.z = ld[:,0]/1e3, ld[:,1]/1e3, ld[:,2]/1e3
            LoadDat.a, LoadDat.b, LoadDat.c = ld[:,3], ld[:,4], ld[:,5]
            LoadDat.sgs = sgs
            
            print("loaded data looks like this: \n{}".format(ld))
            LoadDat.datlen = len(LoadDat.x)
            LoadDat.display = "Success: {} data points loaded".format(LoadDat.datlen)
            
            #########
            #format: [(0,0,0), (0,4,4), (0,6,2), (0,0,0)]
            dat = []
            draw_bridge = int(len(LoadDat.x) / 20)
            
            if LoadDat.sgs is None:
                for i in range(len(LoadDat.x)): 
                    dat.append( (LoadDat.x[i], LoadDat.y[i], LoadDat.z[i]) )
            
            else:
                for i in range(len(LoadDat.x)): 
                    dat.append( (LoadDat.sgs[i][0], LoadDat.sgs[i][1], LoadDat.sgs[i][2]) )
                    
                    if i % draw_bridge == 0:
                        for y in range(draw_bridge):
                            dat.append( (LoadDat.sgs[i-y][3], LoadDat.sgs[i-y][4], LoadDat.sgs[i-y][5]) )
                            
                        for z in range(draw_bridge):
                            dat.append( (LoadDat.sgs[i-y+z][0], LoadDat.sgs[i-y+z][1], LoadDat.sgs[i-y+z][2]) )
                    
            OT_draw_operator.v = dat
            
            
            
        #except:
            #LoadDat.display = "...couldn't load data!"
        
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Menus
# ------------------------------------------------------------------------

class OBJECT_MT_CustomMenu(bpy.types.Menu): ###########dropdown preset menü
    bl_label = "Select"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        layout = self.layout

        # Built-in operators
        layout.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'
        layout.operator("object.select_all", text="Inverse").action = 'INVERT'
        layout.operator("object.select_random", text="Random")

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel): #####################Hauptpanel0 ausklappbar
    bl_label = "Main Panel"
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

        layout.prop(mytool, "my_bool")
        row = layout.row()
        row.operator("wm.hello_world")
        row.operator("wm.hello_world1")
        row = layout.row()
        row.operator("wm.hello_world2")
        
        #if mytool.my_bool:
            #cl = bpy.context.scene.cursor.location
            #print(cl[0])
            #mouse_track()
        
        layout.separator()
        
        
##########################
class OBJECT_PT_CustomPanel2(Panel): #####################Hauptpanel2 EUKLIDIAN
    bl_label = "Euklidian Mode"
    bl_idname = "OBJECT_PT_custom_panel2"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_context = "objectmode"
    
    def __init__(self):
        pass
        #print("Start")

    def __del__(self):
        pass
        #print("End")

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        layout.prop(mytool, "my_bool1")
        layout.label(text= "X, Y, Z  /  A, B, C")
        layout.prop(mytool, "flv_xyz", text="")
        layout.prop(mytool, "flv_abc", text="")
        layout.operator("wm.gotoeuklid")
        
        self.xyz = mytool.flv_xyz
        self.abc = mytool.flv_abc
        
        layout.separator()
        
    def modal(self, context, event):
        print("get modal son")
        return {'RUNNING_MODAL'}
        
    def mouse_down(self):
        print("im updating!")
        
    def mouse_move(self):
        print("im updating")
        
    def invoke(self, context, event):
        print("im invoked")
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
        
############################        
class OBJECT_PT_CustomPanel3(Panel): #####################Hauptpanel3 AXISMODE
    bl_label = "Axis Mode"
    bl_idname = "OBJECT_PT_custom_panel3"
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
        
        layout.prop(mytool, "my_bool2", slider=True)
        layout.prop(mytool, "my_float")
        layout.prop(mytool, "my_float2")
        layout.prop(mytool, "my_float3")
        layout.prop(mytool, "my_float4")
        layout.prop(mytool, "my_float5")
        layout.prop(mytool, "my_float6")
        layout.operator("wm.gotoax")
        
        layout.separator()
        
        
###############################
class OBJECT_PT_CustomPanel4(Panel): #####################  Lodader Panel
    bl_label = "Loader Panel"
    bl_idname = "OBJECT_PT_loader_panel"
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
        
        layout.prop(mytool, "my_path")
        layout.operator("wm.loaddat")
        layout.operator("wm.setzero")
        layout.label(text=("zero set at: {}".format(SetZero.zero)))
        
        path = mytool.my_path
        layout.label(text=(LoadDat.display))
        
        try:
            progress = (LoadDat.pointer+1) % LoadDat.datlen
        except:
            progress = "NaN"
        layout.label(text="[{}/{}]".format(progress, LoadDat.datlen))
        #layout.prop(mytool, "my_string")
        
        row = layout.row()
        row.operator("wm.bwd")
        row.operator("wm.fwd")
        layout.prop(mytool, "my_int")
        
        layout.operator("wm.cam")
        #layout.menu(OBJECT_MT_CustomMenu.bl_idname, text="Presets", icon="SCENE")
        #layout.prop(mytool, "my_bool3", slider=True)
        layout.separator()



# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,          #
    WM_OT_HelloWorld,      #go to mouse button
    WM_OT_HelloWorld1,     #home button
    WM_OT_HelloWorld2,     #reinit button
    GoToEuklid,
    GoToAxies,
    Bwd,
    Fwd,
    LoadDat,
    SetZero,
    WM_Cam,
    OBJECT_MT_CustomMenu,  #dropdown preset menü
    OBJECT_PT_CustomPanel,  #hauptpanel ausklappbar
    OBJECT_PT_CustomPanel2,  #2. xyzabc controller
    OBJECT_PT_CustomPanel3, #Achsen controller
    OBJECT_PT_CustomPanel4,
)

addon_keymaps = []
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)
    #
    bpy.utils.register_class(OT_draw_operator)
    
    kcfg = bpy.context.window_manager.keyconfigs.addon
    if kcfg:
        km = kcfg.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("object.draw_op", 'F', 'PRESS', shift=True, ctrl=True)
        addon_keymaps.append((km, kmi))
    

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool
    #
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        
    addon_keymaps.clear()
    bpy.utils.unregister_class(OT_draw_operator)


if __name__ == "__main__":
    try: unregister()
    except: pass

    register()