import numpy as np
from numpy import cos, sin, pi
import math

class Werkzeug_TCP:
    delta_z = 0.250
    
class o:
    e1 = np.array([1,0,0])
    e2 = np.array([0,1,0])
    e3 = np.array([0,0,1])


#Rotation Matricies: ####################################################
def Rx(A):                                                       
    return np.array([   [1,          0,           0],            
                                    [0, cos(A), -sin(A)],                
                                    [0, sin(A),  cos(A)]   ])           
                                                                        
def Ry(A):                                                       
    return np.array([   [cos(A),  0, sin(A)],     
                                    [    0 ,     1,      0    ],                       
                                    [-sin(A), 0, cos(A)]   ])          
                                                                       
def Rz(A):                                                            
    return np.array([   [cos(A), -sin(A), 0],         
                                    [sin(A),  cos(A), 0],                     
                                    [     0,       0,        1]   ])                       
####################################################
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
#####################################

def moveto(x, y, z, a, b, c, obj_list=None):
    xhat, yhat, zhat = o.e1, o.e2, o.e3
    xhat, yhat, zhat = np.dot(Rx(c), xhat), np.dot(Rx(c), yhat), np.dot(Rx(c), zhat)
    xhat, yhat, zhat = np.dot(Ry(b), xhat), np.dot(Ry(b), yhat), np.dot(Ry(b), zhat)
    xhat, yhat, zhat = np.dot(Rz(a), xhat), np.dot(Rz(a), yhat), np.dot(Rz(a), zhat)
    
    Ohat = np.array([x, y, z])
    Odash = Ohat - (zhat * 0.100) - (zhat * Werkzeug_TCP.delta_z)
    absVA1 = 0.280
    absVA2 = 0.615
    absVA3 = 0.540
    P1 = np.array( [absVA1, 0, 0.715] )
    P2 = np.zeros(3)
    
    #################  A1  #############################################
    sign = 1
    odashproj = Odash * (o.e1 + o.e2)
    odashproj = odashproj / np.linalg.norm(odashproj)
    if odashproj[1] < 0: sign = -1
    A1 = sign * vec_ang(odashproj, o.e1)
    
    #################  A2 & A3  ########################################
    P1 = np.dot(Rz(A1), P1)
    p1proj = P1 * (o.e1 + o.e2)
    p1proj = p1proj / np.linalg.norm(p1proj)
    
    KE_xtilde, KE_ztilde = p1proj, o.e3
    rk1, rk2 = absVA2, absVA3
    x1, z1 = np.dot(P1, KE_xtilde), np.dot(P1, KE_ztilde)
    x2, z2 = np.dot(Odash, KE_xtilde), np.dot(Odash, KE_ztilde)

    P2x1, P2z1, P2x2, P2z2 = circ_intersect(x1, z1, rk1, x2, z2, rk2)  
    if P2z1 >= P2z2: P2 = np.array(KE_xtilde * P2x1 + KE_ztilde * P2z1)
    else: P2 = np.array(KE_xtilde * P2x2 + KE_ztilde * P2z2)
    
    VA2 = P2 - P1
    VA3 = Odash - P2
    
    if P2[2] > 0: sign = -1
    else: sign = 1
    
    A2 = sign * vec_ang(p1proj, VA2)
    
    rotax3 = np.dot(Rz(A1), o.e2)
    rotax3 = rotax3 / np.linalg.norm(rotax3)
    crossVA2VA3 = np.cross(VA2, VA3)
    crossVA2VA3 = crossVA2VA3 / np.linalg.norm(crossVA2VA3)
    if np.allclose(crossVA2VA3, rotax3): sign = 1
    else: sign = -1
    
    A3 = sign * vec_ang(VA2, VA3)
    
    #################  A4  #############################################
    VA5 = Odash - P2
    
    E4z = np.cross(VA5, rotax3)
    E4z = E4z / np.linalg.norm(E4z)
    E4y = rotax3 / np.linalg.norm(rotax3)
    
    zh_E4y = np.dot(E4y, zhat)
    zh_E4z = np.dot(E4z, zhat)
    
    zhatproj = zh_E4y * E4y + zh_E4z * E4z
    
    proj_ytilde = zh_E4y
    proj_ztilde = zh_E4z
    
    if proj_ytilde > 0 and proj_ztilde > 0:     #Quadrant I
        sign = 1
        quadrant = "I"
    elif proj_ytilde <= 0 and proj_ztilde >= 0:     #Quadrant II
        sign = 1
        quadrant = "II"
    elif proj_ytilde <= 0 and proj_ztilde <= 0:     #Quadrant III
        sign = -1
        quadrant = "III"
    elif proj_ytilde >= 0 and proj_ztilde <= 0:     #Quadrant IV
        sign = -1
        quadrant = "IV"
    else: raise Exception("Failed to determine quadrant in E4yz!")
    
    print("vecang returns", vec_ang(E4y, zhatproj)/pi*180)
    print("sign is", sign) 
    A4 = sign * vec_ang(E4y, zhatproj)
    
    if np.isnan(A4):
        input("caught nan")
        A4 = 0
    
    #################  A5  #############################################
    """A5 sign always kept positive!
    continuous transision from quadrant I to IV in E4yz not possible!"""
    A5 = (vec_ang(VA5, zhat))
    
    #################  A6  #############################################
    rotax = np.cross(VA5,zhat)
    v6 = np.cross(rotax, zhat)
    A6 = vec_ang(v6, xhat)
    
    #sign: (not rigorously tested yet)
    VA5proj = VA5 * (o.e1 + o.e2)
    xhatproj = xhat * (o.e1 + o.e2)
    if np.cross(VA5proj, xhatproj)[2] > 0:
        if zhat[2] > 0: sign = -1
        else: sign = 1
    else:
        if zhat[2] > 0: sign = 1
        else: sign = -1
    A6 = sign * A6

    #################  Rotate  #########################################
    if obj_list is not None:
        obj_list[0].rotate(A1)
        obj_list[1].rotate(A2)
        obj_list[2].rotate(A3)
        obj_list[3].rotate(A4)
        obj_list[4].rotate(A5)
        obj_list[5].rotate(A6)    
        
    #################  Debug  ##########################################
    debug = False
    if debug:
        print("xhat", xhat)
        print("v6", v6)
        print("yhat", yhat)
        print("zhat", zhat)
        print('A1 =',A1, 'A2 = ', A2, 'A3 = ', A3)
        print(x1, z1, rk1)
        print(x2, z2, rk2)
        print("P1", P1)
        print("P2", P2)
        print("Odash", Odash)
        print("Ohat", Ohat)
        print("Ohat-Odash", Ohat- Odash)
        print("circ_intersect returns......",circ_intersect(x1, z1, rk1, x2, z2, rk2))
        print("A4 projected vector got quadrant {}".format(quadrant))
        print("zhatproj in E4", zhatproj)
        
    ################## Return #########################################
    return A1, A2, A3, A4, A5, A6