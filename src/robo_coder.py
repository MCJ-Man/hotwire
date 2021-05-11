import numpy as np
import time
from numpy import sin, cos, pi
from src.robo_moveto import moveto

class LoadDat:
    x, y, z = 0, 0, 0
    a, b, c = 0, 0, 0
    datlen = 0
    zero = np.array([0, 0, 0])
    
    
def PostProcess(path , zerovector, filename="OUTPUT.SRC"):
    LoadDat.zero = zerovector

    try:
    #if True:
        LoadDat.pointer = 0
        if type(path) == str:
            print("\n\n\nnow opening path: {}\n".format(path))
            loaded = np.genfromtxt(path, delimiter=';')
        else:
            loaded = path
            print(loaded)
        sgs = None
        if np.isnan(loaded).any():
            nandex = np.unique( np.where(np.isnan(loaded))[0] )
            print(nandex)
            ld = loaded[nandex[0]+1:nandex[1]]
            sgs = loaded[nandex[1]+1:] /1e3             #not needed for now
        else: ld = loaded
        
        LoadDat.x, LoadDat.y, LoadDat.z = ld[:,0]/1e3, ld[:,1]/1e3, ld[:,2]/1e3
        LoadDat.a, LoadDat.b, LoadDat.c = ld[:,3], ld[:,4], ld[:,5]
        
        print("loaded data looks like this: \n{}".format(ld))
        LoadDat.datlen = len(LoadDat.x)
        print("Success: {} data points loaded".format(LoadDat.datlen))

    except:
                raise Exception("...couldn't load data!")
                return None
                
    #set zero
    ld = LoadDat.x, LoadDat.y, LoadDat.z
    print("LoadDat.x at 25 {} \nzero vector: {}".format(LoadDat.x[25], LoadDat.zero))
    LoadDat.zero = zerovector

    for attr, i in zip((ld),(0,1,2)):
        attr += LoadDat.zero[i]

    #write to file            
    f = open(filename, "w")
    f.write('MPR "WINGT"\n')
    f.write(" BEWEG_ART #LINEAR\n")
    #f.wirte(" WERKZEUG Variable:Th")
    f.write(" PTP_GESCHW [%]:100\n")
    f.write(" UEBERSCHL #EIN\n")
    f.write(" BAHN_GESCHW [mm/s]:4.0\n")
    f.write(" C\n")
    f.write(" C\n")
    f.write(" C created using robo_coder on {}\n".format(time.asctime()))
    f.write(" C\n")
    f.write(" C\n")
    f.write(" STOP\n")
    
    #write all positions
    for i in range(LoadDat.datlen):
        x, y, z = LoadDat.x[i], LoadDat.y[i], LoadDat.z[i]
        a, b, c = LoadDat.a[i], LoadDat.b[i], LoadDat.c[i]
        
        """#debug:
        x, y, z = 0.750, 0.0, 0.750
        a, b, c = 0.0, 0.0, 0.0""" 
        
        A1, A2, A3, A4, A5, A6 = moveto(x, y, z, a, b, c)
        
        A1 *= 180/pi
        A2 *= 180/pi
        A3 *= 180/pi
        A4 *= 180/pi
        A5 *= 180/pi
        A6 *= 180/pi
        
        x *= 1000
        y *= 1000
        z *= 1000
        a *= 180/pi
        b *= 180/pi
        c *= 180/pi
        f.write(" POSITION #N,$BASE,X:{},Y:{},Z:{},A:{},B:{},C:{},A1:{},A2:{},A3:{},A4:{},A5:{},A6:{},A7:{},A8:{}\n".format( x,y,z-715,  a,b,c,  A1,A2,A3,A4,A5,A6,  0.0,0.0 ))
    
    #write end
    f.write(" C\n")
    f.write(" C\n")
    f.write("END")
    f.close()
    
    print("\nSuccess: File Saved as {}".format(filename))


#PostProcess("C:\\Users\\JMCrosair\\OneDrive\\70 USP\\code\\outupt_left.csv", np.array([1.176, 0.016, 0.515]), filename="WINGTIP_LEFT.SRC")


#np.array([0.1176, 16, 0.515])


















