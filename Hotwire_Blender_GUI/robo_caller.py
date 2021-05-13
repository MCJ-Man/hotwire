'''how to run this: Type in Blneder Python Console:
import sys
import numpy as np
from numpy import pi
sys.path.append('C:\\Users\\JMCrosair\\Documents\\20-Studiwerkstatt\\01 Robotik\\10_Blender')
import robo_caller
obj_list = robo_caller.starter()
robo_caller.moveto(0.750, 0.000, 0.750, pi/2, pi/4, pi, obj_list)
'''
import bpy
import numpy as np
from numpy import cos, sin, pi
import time
import math

class Werkzeug_TCP:
    delta_z = 0.250


def ignition(hp):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    A1_path = ".\\Hotwire_Blender_GUI\\sr16_obj\\A1.obj"
    A2zuA3_path = ".\\Hotwire_Blender_GUI\\sr16_obj\\A2zuA3.obj"
    A3_path = ".\\Hotwire_Blender_GUI\\sr16_obj\\A3.obj"
    A4zuA5_path = ".\\Hotwire_Blender_GUI\\sr16_obj\\A4zuA5.obj"
    A5_path = ".\\Hotwire_Blender_GUI\\sr16_obj\\A5.obj"
    A6_path = ".\\Hotwire_Blender_GUI\\sr16_obj\\A6_hotwire.obj"
    base_path = ".\\Hotwire_Blender_GUI\\sr16_obj\\Base.obj"
    filepaths = [A1_path, A2zuA3_path, A3_path, A4zuA5_path, A5_path, A6_path, base_path]

    jointlist = []
    #obj_list = [A1, A2zuA3, A4, A4zuA5, A5, A6]

def circ_intersect(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    # non intersecting
    if d > r0 + r1 :
        print("error, non intersecting")
        return None
    # One circle within other
    if d < abs(r0-r1):
        print("error, circlie within other")
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        print("error, coincident circles")
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        
        print("circle intersect successful")
        return (x3, y3, x4, y4)

def vec_ang(v1, v2):
    if np.allclose(v1/np.linalg.norm(v1), v2/np.linalg.norm(v2)): return 0
    if np.allclose(v1/np.linalg.norm(v1), -v2/np.linalg.norm(v2)): return pi
    ang = np.arccos( np.dot(v1,v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)) )
    if np.isnan(ang):
        print("this is vecang: v1, v2 are")
        print(v1)
        print(v2)
        print("angle is: {}\n".format(ang*180/pi))#"""
    return ang

class jp:
    def sign(i):
        if i >= 0: return 1
        if i < 0: return -1
    
class o:
    e1 = np.array([1,0,0])
    e2 = np.array([0,1,0])
    e3 = np.array([0,0,1])

#Rotation Matricies: ####################################################
def Rx(A):                                                              #
    return np.array([   [1,      0,       0],                           #
                        [0, cos(A), -sin(A)],                           #
                        [0, sin(A),  cos(A)]   ])                       #
                                                                        #
def Ry(A):                                                              #
    return np.array([   [cos(A),  0, sin(A)],                           #
                        [    0 ,  1,  0    ],                           #
                        [-sin(A), 0, cos(A)]   ])                       #
                                                                        #
def Rz(A):                                                              #
    return np.array([   [cos(A), -sin(A), 0],                           #
                        [sin(A),  cos(A), 0],                           #
                        [     0,       0, 1]   ])                       #
                                                                        #
def rot_from_vec(v, phi):                                               #
    #input("vec = {}, lenvec = {}".format(v, np.linalg.norm(v)))  
    a, b, c = v[0], v[1], v[2]                                                 
    K = np.array([ [0, -c, b], [c, 0, -a], [-b, a, 0] ])
    I = np.identity(3)
    R = I + sin(phi) * K + (1-cos(phi)) * np.linalg.matrix_power(K,2)
    
    return R                                                      
                                                                        #
                                                                        #
#########################################################################
def ang_from_mat(mat):
    print("input mat is:")
    print(mat)
    print("<><><><><><><>")
    w, v = np.linalg.eig(mat)
    print(w)
    
    for i in range(3):
        if 1-1e-6 < w[i] < 1+1e-6: EW1atPos = i
        
    if EW1atPos is None: raise Exception("EW is not 1")
    else: print("EW position: {}\n".format(EW1atPos))
    rot_axis = v[:,EW1atPos]
    rot_angle = np.arccos( 0.5*(np.trace(mat) - 1))
    print("rotation axis is: {}, \ntotal rotatoin angle is: {}".format(rot_axis, rot_angle*180/pi))
    print("\n\n\n")
    
    if (rot_axis == np.array([0,0,1])).all():
        skv = np.array([1,0,0])
    elif (rot_axis == np.array([0,1,0])).all():
        skv = np.array([1,0,0])
    elif (rot_axis == np.array([1,0,0])).all():
        skv = np.array([0,1,0])
    elif (rot_axis == np.array([0,0,0])).any():
        for i in range(2):
            if rot_axis[i] == 0: break
        skv = rot_axis
        skv[i-1] = -skv[i-1]
    else:
        skv = rot_axis
        skv[1] = 0
        skv[0] = -skv[0]
        
    rskv = np.dot(mat, skv)    
    xrskv = np.cross(skv, rskv)
    xrskv = xrskv / np.linalg.norm(xrskv)
    
    print(xrskv, rot_axis.real)
    print(xrskv == rot_axis.real)
        
    if (xrskv == rot_axis.real).all(): return rot_axis * rot_angle
    else: return rot_axis * -rot_angle

class cA1:
    orig = (0.0, 0.0, 0.715)
    def __init__(self, jointlist_element):
        self.obj_list = []
        self.ax_name = 'A1'
        self.pointer = jointlist_element
        self.pointer.rotation_mode = 'XYZ'
        #self.subordinate_joints = self.obj_list[1:]
        self.subordinate = 1
        
        self.delta_R = np.array([ [1,0,0], [0,1,0], [0,0,1] ])
        self.vector = np.array( [0.280, 0, 0] )
        self.orig_v = np.array([])
        self.rot_ax = np.array( [0,0,1] )
        self.ax_angle = 0
        self.R = Rz
        
        if self.pointer == None: input("pointer is none " + self.ax_name)
        
    def eu1(self): return 0
    def eu2(self): return 0
    def eu3(self):
        sign = jp.sign(self.ax_angle)
        return sign * vec_ang(o.e1, self.vector) #winkel von self.vector zu zx-ebene

    def rotate(self, angle, abs=True):        
        if abs:
            A = angle - self.ax_angle
            self.ax_angle = angle            
        else:
            A = angle
            self.ax_angle += angle
            
        R = rot_from_vec(self.rot_ax, A)
        self.vector = np.dot(R, self.vector)
        
        print("rotate main axis {}".format(self.ax_name))
        eu1, eu2, eu3 = self.eu1(), self.eu2(), self.eu3()
        self.pointer.rotation_euler = (eu1, eu2, eu3)
        
        if self.subordinate is not None:
            sub_obj = self.obj_list[self.subordinate]
            
            #rotate subordinate objects:
            for obj in self.obj_list[self.subordinate:]:
                obj.rotate_passive(A, self.rot_ax)
            
            #move subortinate objects:
            sub_obj.move(self.vector, self.pointer.location)
        
    def rotate_passive(self, A, rot_ax):
        #input("I am {}, passive rotation around axis: {}".format(self.ax_name, rot_ax))
    
        R = rot_from_vec(rot_ax, A)
        self.vector = np.dot(R, self.vector)
        self.rot_ax = np.dot(R, self.rot_ax)
        
        print("\nrotate passive {}".format(self.ax_name))
        eu1 = self.eu1()
        eu2 = self.eu2()
        eu3 = self.eu3()
        self.pointer.rotation_euler = (eu1, eu2, eu3)
            
    def move(self, vector, orig):
        sub_obj = self.obj_list[self.subordinate]
        
        #select myself
        self.pointer.select_set(True)
        
        self.pointer.location[0] = vector[0] + orig[0]
        self.pointer.location[1] = vector[1] + orig[1]
        self.pointer.location[2] = vector[2] + orig[2]
        #deselect myself
        bpy.ops.object.select_all(action='DESELECT')
        
        print("i'm {}, now moving {}".format(self.ax_name, sub_obj.ax_name))
        sub_obj.move(self.vector, self.pointer.location)
        
class cA2zuA3(cA1):
    orig = (0.280, 0.0, 0.715)
    def __init__(self, jointlist_element):
        cA1.__init__(self, jointlist_element)
        self.ax_name = 'A2zuA3'
        self.subordinate = 2
        self.vector = np.array( [0.615, 0, 0] )
        self.rot_ax = np.array( [0,1,0] )
        self.ax_angle =0
        self.R = Ry
    def eu1(self): return 0
    def eu2(self):
        sign = jp.sign(self.ax_angle)
        return sign * vec_ang(self.obj_list[0].vector, self.vector)
    def eu3(self):
        sign = jp.sign(self.obj_list[0].ax_angle)
        return sign * vec_ang(o.e1, self.obj_list[0].vector) 

class cA3(cA1):
    orig = (0.895, 0.0, 0.715)
    def __init__(self, jointlist_element):
        cA1.__init__(self, jointlist_element)
        self.ax_name = 'A3'
        self.subordinate = 3
        self.vector = np.array( [0.540, 0, 0] )
        self.rot_ax = np.array( [0,1,0] )
        self.ax_angle = 0
        self.R = Ry
    def eu1(self): return 0
    def eu2(self):
        return self.obj_list[1].ax_angle + self.ax_angle
    def eu3(self):
        sign = jp.sign(self.obj_list[0].ax_angle)
        return sign * vec_ang(o.e1, self.obj_list[0].vector) 
    
class cA4zuA5(cA1):
    orig = (1.435, 0.0, 0.715)
    def __init__(self, jointlist_element):
        cA1.__init__(self, jointlist_element)
        self.ax_name = 'A4zuA5'
        self.subordinate = 4
        self.vector = np.array( [0, 0, 0] )
        self.rot_ax = np.array( [1,0,0] )
        self.ax_angle = 0
        self.R = Rx
    def eu1(self): return self.ax_angle
    def eu2(self): return self.obj_list[1].ax_angle + self.obj_list[2].ax_angle
    def eu3(self):
        sign = jp.sign(self.obj_list[0].ax_angle)
        return sign * vec_ang(o.e1, self.obj_list[0].vector) 

class cA5(cA1):
    orig = (1.435, 0.0, 0.715)
    def __init__(self, jointlist_element):
        cA1.__init__(self, jointlist_element)
        self.ax_name = 'A5'
        self.subordinate = 5
        self.vector = np.array( [0.100, 0, 0] )
        self.rot_ax = np.array( [0,0,1] )
        self.ax_angle = 0
        self.R = Rz
        
    def eu1(self):
        v = self.vector / np.linalg.norm(self.vector)
        rotax = o.e3
        eu2, eu3 = self.eu2() ,self.eu3()
        print("eu2", eu2, "eu3", eu3)
        rotax = np.dot(Ry(eu2), rotax)
        rotax = np.dot(Rz(eu3), rotax)
        crossax = np.cross(self.rot_ax, rotax)
        if not np.allclose(crossax, np.zeros(3)):
            crossax = crossax / np.linalg.norm(crossax)
            if np.allclose(crossax, v): sign = -1
            elif np.allclose(crossax,-v): sign = 1
            else: raise Exception("Failed to determine Euler-X sign on A5! \ncrossax: {}, \nv: {}".format(crossax, v))
        else: return 0
        return sign * vec_ang(self.rot_ax, rotax)
    def eu2(self):
        v = self.vector / np.linalg.norm(self.vector)
        vproj = v*(o.e1+o.e2)
        if v[2] > 0: sign = -1
        else: sign = 1
        return sign * vec_ang(vproj, v)
    def eu3(self):
        v = self.vector / np.linalg.norm(self.vector)
        vproj = v*(o.e1+o.e2)
        if v[1] >= 0: sign = 1
        else: sign = -1
        return sign * vec_ang(o.e1, vproj)
    
class cA6(cA1):
    orig = (1.535, 0.0, 0.715)
    def __init__(self, jointlist_element):
        cA1.__init__(self, jointlist_element)
        self.ax_name = 'A6'
        self.subordinate = None
        self.vector = np.array( [0, 0.100, 0] )
        self.rot_ax = np.array( [1,0,0] )
        self.ax_angle = 0
        self.R = Rx
    def eu1(self): return self.obj_list[4].eu1() + self.ax_angle
    def eu2(self): return self.obj_list[4].eu2()
    def eu3(self): return self.obj_list[4].eu3()
    def move(self, vector, orig):
        #select myself
        self.pointer.select_set(True)
        #move myself
        self.pointer.location[0] = vector[0] + orig[0]
        self.pointer.location[1] = vector[1] + orig[1]
        self.pointer.location[2] = vector[2] + orig[2]
        #deselect myself
        bpy.ops.object.select_all(action='DESELECT')
        print("////////// END OF RECURSIVE CHAIN /////////////\n\n")
        
def isalive():
    print("isalive and well, V2")
    
def starter(hp):
    A1_path =     hp + "\\Hotwire_Blender_GUI\\sr16_obj\\A1.obj"
    A2zuA3_path = hp + "\\Hotwire_Blender_GUI\\sr16_obj\\A2zuA3.obj"
    A3_path =     hp + "\\Hotwire_Blender_GUI\\sr16_obj\\A3.obj"
    A4zuA5_path = hp + "\\Hotwire_Blender_GUI\\sr16_obj\\A4zuA5.obj"
    A5_path =     hp + "\\Hotwire_Blender_GUI\\sr16_obj\\A5.obj"
    A6_path =     hp + "\\Hotwire_Blender_GUI\\sr16_obj\\A6_hotwire.obj"
    base_path =   hp + "\\Hotwire_Blender_GUI\\sr16_obj\\Base.obj"
    filepaths = [A1_path, A2zuA3_path, A3_path, A4zuA5_path, A5_path, A6_path, base_path]

    #delete default cube
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    jointlist, obj_list = [], []
    
    bpy.ops.import_scene.obj(filepath=base_path, axis_up='Z', axis_forward='Y')
    for file, cla in zip(filepaths, (cA1, cA2zuA3, cA3, cA4zuA5, cA5, cA6)):
        tset = set(bpy.context.visible_objects)
        bpy.ops.import_scene.obj(filepath=file, axis_up='Z', axis_forward='Y')
        bpy.context.scene.cursor.location = cla.orig
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        jointlist.append(list(set(bpy.context.visible_objects)-tset)[0])
        obj_list.append(cla(jointlist[-1]))
    
    bpy.ops.object.select_all(action='DESELECT')
    for obj in obj_list:
        obj.obj_list = obj_list
        obj.orig_v = obj.vector

    print("=================================================")
    print(jointlist)

    obj_list[0].rotate(45 * pi/180)
    obj_list[1].rotate(-80 * pi/180)
    obj_list[2].rotate(110 * pi/180)
    obj_list[3].rotate(0 * pi/180)
    obj_list[4].rotate(-45 * pi/180)
    obj_list[5].rotate(0 * pi/180)
        
    print("\n\n\n==============================================")
    for obj in obj_list:
        print("{}: ax_angle is: {}".format(obj.ax_name, obj.ax_angle * 180/pi))

    print("\nEND OF PROGRAM\n")
    return obj_list

###################################################################
"""    
obj_list = starter()
A, B, C, D, E, F = 0, -pi/2, pi/2, -pi*0.9, pi/2, 0
A, B, C, D, E, F = moveto(0.750, 0.300, 0.750, pi/4, -pi/4, pi, obj_list)
#D = -135 *pi/180
#E = -pi/2
#E = -E
#D = -D
"""
"""
obj_list[0].rotate(A)
obj_list[1].rotate(B)
obj_list[2].rotate(C)
obj_list[3].rotate(D)
obj_list[4].rotate(E)
#obj_list[5].rotate(-30 /180*pi)"""

"""
obj_list[0].rotate(-29.74488 /180*pi)
obj_list[1].rotate(-43.0149 /180*pi)
obj_list[2].rotate(124.865 /180*pi)
obj_list[3].rotate(-90 /180*pi)
obj_list[4].rotate(-8.1499 /180*pi)
#obj_list[5].rotate(-30 /180*pi)"""

"""
print("\n\nreached end")
for obj in obj_list:
    print(obj.ax_name, obj.ax_angle/pi*180)
    
"""