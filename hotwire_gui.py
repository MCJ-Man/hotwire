import os
import platform
import shutil

from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog, Text

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib import cm

import src.functional_hotwire as functional_hotwire
import src.robo_coder as robo_coder

class OutputData:
    def __init__():
        pass
    
    def set_output(shiny_output):
        pass
    
    shiny_output = None
    b2 = None
    savename = None
    e1 = None
    e2 = None
    e3 = None
    outname = None
    outname2 = None

root = Tk()
root.geometry("700x750")
root.resizable(width=False, height=False)
root.title("Hotwire")

###########Paramteters##########
boolvar = False
bpath = "./src/clarky.csv"#"nothing selected yet"
spath = "./src/n0012.csv"#"nothing selected yet"
img = Image.open("./src/foldericon.png")
img = img.resize((20, 20), Image.ANTIALIAS)
image = ImageTk.PhotoImage(img)
###########Functions
def addPath(label, x, framename):
    y = 20
    filename = filedialog.askopenfilename(initialdir="./Source_Profiles/", title="Select File", filetypes=(("executables","*.csv"), ("all files", "*.*")))
    label.config(text=str(filename))
    graph(x, y, filename, framename)
    
def graph(x, y, filename, framename):
    if platform.system() == 'Windows':
        filename = filename.replace("/", "\\")
    print("filename is {}".format(filename))
    x_data, y_data = functional_hotwire.data_refiner(filename)
    figure = plt.figure(figsize = (3.3,1.25), dpi=100)
    
    ax = figure.add_subplot(111)
    ax.plot(x_data, y_data)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    plt.axis('equal')
    chart = FigureCanvasTkAgg(figure, framename)
    plt.grid('on')
    #plt.axis('off')
    chart.get_tk_widget().place(x=x+10, y=y)
    
def ddd_graph(ddd_plot, x):
    fig = plt.figure(figsize=(1, 1), dpi=100)
    
    chart = FigureCanvasTkAgg(fig, root)
    chart.draw()
    plt.axis('off')
    
    ax = fig.add_subplot(111, projection="3d")
    if ddd_plot is not None:
        wingspan = ddd_plot[2][0]
        l_profile_len = ddd_plot[2][1]
        
        ax.plot_trisurf(ddd_plot[0][0], ddd_plot[0][1], ddd_plot[0][2], linewidth=0.5, antialiased=True, shade=True, cmap=cm.coolwarm)
        ax.plot_trisurf(ddd_plot[1][0], ddd_plot[1][1], ddd_plot[1][2], linewidth=0.5, antialiased=True, shade=True, cmap=cm.coolwarm)
    
        ax.set_xlim3d(-10, -l_profile_len)
        ax.set_ylim3d(-10, l_profile_len)
        ax.set_zlim3d(-l_profile_len/2, l_profile_len/2)
    
    toolbar = NavigationToolbar2Tk(chart, root)
    toolbar.update()
    chart.get_tk_widget().place(x=x, y=500, width=250, height=250)
    
def movgraph(x, y, plot):
    twodlineobj = plot
    
    figure = twodlineobj.get_figure()
    plt.figure(figsize = (3,2), dpi=100)
    
    ax = figure.add_subplot(111)
    
    pot_ylim = (ax.get_xlim()[0],ax.get_xlim()[1]*0.5)
    new_ylim = [ax.get_ylim()[0], ax.get_ylim()[1]]
    if abs(pot_ylim[0]) > abs(ax.get_ylim()[0]):
        new_ylim[0] = pot_ylim[0]
    if abs(pot_ylim[1]) > abs(ax.get_ylim()[1]):
        new_ylim[1] = pot_ylim[1]
    ax.set_ylim( (new_ylim[0],new_ylim[1]) )
    plt.axes().set_aspect('equal', 'datalim')
    chart = FigureCanvasTkAgg(figure, root)
    plt.grid('on')
    plt.axis('scaled')
    chart.get_tk_widget().place(x=200, y=176, width=550, height=324)
    
    toolbar = NavigationToolbar2Tk(chart, root)
    toolbar.update()
    toolbar.place(x=200, y=176, width=500, height=35)

def run_segmenter(bd, sd, entryz, chkValue):
    plt.cla()
    plt.clf()
    bd = bd.cget("text")
    sd = sd.cget("text")
    p = []
    for item in entryz:
        p.append(float(item.get()))
        
    print("checkbox state is: {}".format(chkValue.get()))
    if chkValue.get() == 0:
        bol = False
    else: bol = True
    p.append(bol)
    
    print("\n\nbd is {} \nsd is {} \np is {}".format(bd, sd, p))
    
    post_seg_plot, ddd_plots, shiny_output = functional_hotwire.hotwire(bd, sd, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10])
    
    movgraph(176,250, post_seg_plot)
    ddd_graph(ddd_plots[0], 200)
    if len(ddd_plots) == 2:
        print("ddd_plots is len 2")
        ddd_graph(ddd_plots[1], 450)
    else:
        print("ddd_plots is len {}".format(len(ddd_plots)))
        ddd_graph(None, 450)
        
    OutputData.b2['state'] = 'normal'
    OutputData.b3['state'] = 'disabled'
    OutputData.shiny_output = shiny_output
    
    
def save_CSV():
    savename = OutputData.savename.get()
    shiny_output = OutputData.shiny_output
    
    if os.path.exists("./Output_Files/" + savename):
        shutil.rmtree("./Output_Files/" + savename)
        os.mkdir("./Output_Files/" + savename)
    else:
        print("\n\n triged else")
        print(savename)
        os.mkdir("./Output_Files/" + savename)
    
    
    if len(shiny_output) == 2:
        OutputData.outname = "./Output_Files/" + savename + "/" + savename + "_r"+".csv"
        OutputData.outname2 = "./Output_Files/" + savename + "/" + savename + "_l"+".csv"
        np.savetxt(OutputData.outname, shiny_output[0], delimiter=";", fmt="%s")
        np.savetxt(OutputData.outname2, shiny_output[1], delimiter=";", fmt="%s")
        print("\nSaved successfully to file named {}, \n and {}!".format(OutputData.outname, OutputData.outname2))
    else:
        OutputData.outname = "./Output_Files/" + savename + "/" + savename + ".csv"
        np.savetxt(OutputData.outname, shiny_output[0], delimiter=";", fmt="%s")
        print("\nSaved successfully to file named {}!".format("{}".format(OutputData.outname)))
        
    OutputData.b3['state'] = 'normal'
        
    
def gen_robocode():
    x = float(OutputData.e1.get()) / 1000
    y = float(OutputData.e2.get()) / 1000
    z = float(OutputData.e3.get()) / 1000
    zerovector = np.array( [x, y, z] )
    if OutputData.outname == None:
        raise Exception("ERROR with output file name1")
    else:
        robo_coder.PostProcess(OutputData.outname, zerovector, filename=OutputData.outname[0:-4] + ".SRC")
    if OutputData.outname2 != None:
        robo_coder.PostProcess(OutputData.outname2, zerovector, filename=OutputData.outname2[0:-4] + ".SRC")
        
##########Load Dat###############

load_dat_frame = Label(root, width=700, height=250, borderwidth=1, relief="ridge")
load_dat_frame.pack(fill=X, side=TOP, expand=False, padx=0, pady=0)

can = Canvas(load_dat_frame, width=700, height=176, bg="#bfbfbf")
can.place(x=0, y=0)

#File selector
sdat_frame = LabelFrame(load_dat_frame, text="Source File: Small Data").place(x=0, y=0, width=350, height=178)
smalllab = Label(load_dat_frame, text=spath, borderwidth=3, relief="ridge", anchor=E)
openFile = Button(load_dat_frame, text="", image=image, padx=2, pady=2, command=lambda: addPath(smalllab, 0, sdat_frame))
smalllab.place(x=2, y=150, width=320, height=25)
openFile.place(x=322, y=150, width=25, height=25)

bdat_frame = LabelFrame(load_dat_frame, text="Source File: Big Data").place(x=350, y=00, width=350, height=178)
biglab = Label(load_dat_frame, text=bpath, borderwidth=3, relief="ridge", anchor=E)
openFile = Button(load_dat_frame, text="", image=image, padx=2, pady=2, command=lambda: addPath(biglab, 350, bdat_frame))
biglab.place(x=352, y=150, width=320, height=25)
openFile.place(x=672, y=150, width=25, height=25)

##########Body###################
###Segmenting Paramters
can = Canvas(root, width=700, height=574, bg="#bfbfbf")
can.place(x=0, y=176)

parameters = LabelFrame(root, text="Segmenting Paramters", padx=5, pady=5)
parameters.place(x=0, y=176+74, width=200, height=280)

chkValue = IntVar()

labelz = [Label(parameters, text="wingspan", anchor=W),
    Label(parameters, text="sweep", anchor=W),
    Label(parameters, text="dihedral", anchor=W),
    Label(parameters, text="twist", anchor=W),
    Label(parameters, text="tooldiameter", anchor=W),
    Label(parameters, text="dihedral angle [°]", anchor=W),
    Label(parameters, text="small profile len", anchor=W),
    Label(parameters, text="large profile len", anchor=W),
    Label(parameters, text="nmb of segments", anchor=W),
    Label(parameters, text="retract path len", anchor=W),
    Label(parameters, text="mirror", anchor=W)]
    
entryz = [Entry(parameters, width=35, borderwidth=2),
    Entry(parameters, width=35, borderwidth=2),
    Entry(parameters, width=35, borderwidth=2),
    Entry(parameters, width=35, borderwidth=2),
    Entry(parameters, width=35, borderwidth=2),
    Entry(parameters, width=35, borderwidth=2),
    Entry(parameters, width=35, borderwidth=2),
    Entry(parameters, width=35, borderwidth=2),
    Entry(parameters, width=35, borderwidth=2),
    Entry(parameters, width=35, borderwidth=2),
    Checkbutton(parameters, width=10, text="", var=chkValue)]

for labl, e in zip(labelz, entryz):
    i = labelz.index(labl)
    labl.config(font=('Arial', 11))
    e.config(width=10)
    labl.grid(sticky=W, row=i, column=0)
    e.grid(sticky=W, row=i, column=1, padx=0)

for e, default in zip(entryz[0:-1], [230, 0, 0, 0, 1, 0, 100, 300, 250, 50]):
    e.insert(0, default)
    
####Control Panel
controlpanel = LabelFrame(root, text="Control Panel", padx=5, pady=5)
controlpanel.place(x=0, y=456+74, width=200, height=220)

b1 = Button(controlpanel, text="Run Segmenter", width=25, command=lambda: run_segmenter(biglab, smalllab, entryz[0:-1], chkValue))
b1.grid(row=0, column=0, columnspan=3)

l1 = Label(controlpanel, text="")
l1.grid(row=1, column=0)

l2 = Label(controlpanel, text="Output Folder Name:", anchor=W)
l2.grid(sticky=W, row=2, column=0, columnspan=3)
OutputData.savename = Entry(controlpanel, width=30, borderwidth=2)
OutputData.savename.insert(0, "default")
OutputData.savename.grid(row=3, column=0, columnspan=3)

OutputData.b2 = Button(controlpanel, text="Save CSV", width=25, state="disabled", command=save_CSV)
OutputData.b2.grid(row=4, column=0, columnspan=3)

l1.grid(row=5, column=0)

l3 = Label(controlpanel, text="Set TCP XYZ Zero in mm:", anchor=W)
l3.grid(sticky=W, row=6, column=0, columnspan=3)
OutputData.e1 = Entry(controlpanel, width=7, borderwidth=2)
OutputData.e1.grid(sticky=W, row=7, column=0)
OutputData.e2 = Entry(controlpanel, width=7, borderwidth=2)
OutputData.e2.grid(sticky=W, row=7, column=1)
OutputData.e3 = Entry(controlpanel, width=7, borderwidth=2)
OutputData.e3.grid(sticky=W, row=7, column=2)

OutputData.b3 = Button(controlpanel, text="Generate RoboCode", width=25, command=gen_robocode, state="disabled")
OutputData.b3.grid(row=8, column=0, columnspan=3)

img = Image.open("./src/hotwire.png")
perc = 0.71
img = img.resize((int(285*perc), int(78*perc)), Image.ANTIALIAS)
my_img = ImageTk.PhotoImage(img)
my_label = Label(root, image=my_img, borderwidth=0)
my_label.place(x=1, y=685-500)#, height=150, width=150)

#init
graph(0, 20, "./src/n0012.csv", sdat_frame)
graph(350, 20, "./src/clarky.csv", bdat_frame)

root.mainloop()
root.destroy()





