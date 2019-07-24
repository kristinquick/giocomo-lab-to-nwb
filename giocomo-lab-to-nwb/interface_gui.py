from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
import os.path
import conversion



def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.withdraw()  #me
    win.update_idletasks()
    win.deiconify()





class guiMain():


    def __init__(self, master):
        self.master = master
        #self.master.iconbitmap('wink.ico')
        self.master.option_add("*font", "Helvetica 10")
        self.master.minsize(width=500, height=600)
        self.master.maxsize(width=500, height=600)
        self.master.title("Giocomo Connect")
        self.master.resizable(1, 1)  # Don't allow resizing in the x or y direction
        self.master.configure(background="#d3d3d3")



        # Setup the drop down menus
        self.menubar = Menu(master, tearoff=0)
        self.menuOpt1 = Menu(self.menubar)
        self.menuOpt2 = Menu(self.menubar)
        self.menuOpt3 = Menu(self.menubar)
        self.menuOpt1.add_command(label="Exit", command=self.close_windows)
        self.menuOpt3.add_command(label="About", state = DISABLED, command=self.close_windows)
        self.menuOpt3.add_command(label="Contents", state = DISABLED, command=self.close_windows)
        self.menubar.add_cascade(label="File", menu=self.menuOpt1)
        self.menubar.add_cascade(label="Setup", menu=self.menuOpt2)
        self.menubar.add_cascade(label="Help", menu=self.menuOpt3)
        self.master.config(menu=self.menubar)


        #Create frames
        #Left Frame
        self.FrameLeft = Frame(master,background = "#d3d3d3")
        self.FrameLeft.grid(row=0, column=0, rowspan=5, columnspan=1, sticky=N+S+E+W)


        #
        ################################ Frame Left Contents ###########################################
        #


        #File Selector
        self.selectFileButton = Button(self.FrameLeft, text="Select File", command=self.selectFile,
                                       background="#d3d3d3")
        self.selectFileButton.grid(row=0, column=0, padx=20, pady=(20, 0), sticky='NEW')
        self.fileName = Entry(self.FrameLeft, width=32,
                              textvariable=StringVar(value=""))
        self.fileName.config(font='Helvetica 10 italic', state='disabled')
        self.fileName.grid(row=0, column=1, padx=(0, 0), pady=(20, 0), sticky="senw")

        #Subject Infomation
        self.labelSubject = Label(self.FrameLeft, text='Subject Information:     ', background="#d3d3d3")
        self.labelSubject.grid(row=1, column=0, padx=20, pady=(20,0), sticky='snw')

        self.labelSubjectID = Label(self.FrameLeft, text='ID:', background="#d3d3d3")
        self.labelSubjectID.grid(row=2, column=0, padx=20, pady=0, sticky='ne')
        self.enterSubjectID = Entry(self.FrameLeft, width=32,
                                      textvariable=StringVar(value='L5'))
        self.enterSubjectID.config(font='Helvetica 10 italic', state='normal')
        self.enterSubjectID.grid(row=2, column=1, padx=(0, 0), pady=0, sticky="senw")

        self.labelSubjectDOB = Label(self.FrameLeft, text='DOB (mm/dd/yyyy):', background="#d3d3d3")
        self.labelSubjectDOB.grid(row=3, column=0, padx=20, pady=0, sticky='sne')
        self.enterSubjectDOB = Entry(self.FrameLeft, width=32,
                                    textvariable=StringVar(value=''))
        self.enterSubjectDOB.config(font='Helvetica 10 italic', state='normal')
        self.enterSubjectDOB.grid(row=3, column=1, padx=(0, 0), pady=5, sticky="senw")

        self.labelSubjectDesc = Label(self.FrameLeft, text='Description:', background="#d3d3d3")
        self.labelSubjectDesc.grid(row=4, column=0, padx=20, pady=0, sticky='sne')
        self.enterSubjectDesc = Entry(self.FrameLeft, width=32,
                                     textvariable=StringVar(value=''))
        self.enterSubjectDesc.config(font='Helvetica 10 italic', state='normal')
        self.enterSubjectDesc.grid(row=4, column=1, padx=(0, 0), pady=5, sticky="senw")


        self.labelSubjectSex = Label(self.FrameLeft, text='Sex:', background="#d3d3d3")
        self.labelSubjectSex.grid(row=5, column=0, padx=20, pady=5, sticky='sne')
        self.sexVar = StringVar(value="Male")
        self.selectSex = Radiobutton(self.FrameLeft, text="Male", background="#d3d3d3",
                                      variable=self.sexVar, value="Male")
        self.selectSex.grid(row=5, pady=5, padx=20, column=1, sticky="W")
        self.selectSex = Radiobutton(self.FrameLeft, text="Female", background="#d3d3d3", variable=self.sexVar,
                                      value="Female")
        self.selectSex.grid(row=5, pady=5, padx=80, column=1, sticky="W")


        self.labelSubjectSpecies = Label(self.FrameLeft, text='Species:', background="#d3d3d3")
        self.labelSubjectSpecies.grid(row=6, column=0, padx=20, pady=0, sticky='sne')
        self.speciesVar = StringVar(value = "Mouse")
        self.speciesChoices = ['Mouse']
        self.selectSpecies = OptionMenu(self.FrameLeft, self.speciesVar, *self.speciesChoices)
        self.selectSpecies.grid(row=6, column=1, padx=(0, 0), pady=5, sticky="senw")

        self.labelSubjectWeight = Label(self.FrameLeft, text='Weight (grams):', background="#d3d3d3")
        self.labelSubjectWeight.grid(row=7, column=0, padx=20, pady=0, sticky='sne')
        self.enterSubjectWeight = Entry(self.FrameLeft, width=32,
                                        textvariable=IntVar(value="0"))
        self.enterSubjectWeight.config(font='Helvetica 10 italic', state='normal')
        self.enterSubjectWeight.grid(row=7, column=1, padx=(0, 0), pady=5, sticky="senw")

        # Session Information
        self.labelSession = Label(self.FrameLeft, text='Session Information:', background="#d3d3d3")
        self.labelSession.grid(row=8, column=0, padx=20, pady=(20, 0), sticky='snw')

        self.labelSessionID = Label(self.FrameLeft, text='ID:', background="#d3d3d3")
        self.labelSessionID.grid(row=9, column=0, padx=20, pady=0, sticky='sne')
        self.enterSessionID = Entry(self.FrameLeft, width=32,
                                     textvariable=StringVar(value='npI5_0417_baseline_1'))
        self.enterSessionID.config(font='Helvetica 10 italic', state='normal')
        self.enterSessionID.grid(row=9, column=1, padx=(0, 0), pady=5, sticky="senw")

        self.labelSessionStart = Label(self.FrameLeft, text='Start Time:', background="#d3d3d3")
        self.labelSessionStart.grid(row=10, column=0, padx=20, pady=0, sticky='sne')
        self.enterSessionStart = Entry(self.FrameLeft, width=32,
                                     textvariable=StringVar(value=''))
        self.enterSessionStart.config(font='Helvetica 10 italic', state='normal')
        self.enterSessionStart.grid(row=10, column=1, padx=(0, 0), pady=5, sticky="senw")

        self.labelSessionExp = Label(self.FrameLeft, text='Experimenter:', background="#d3d3d3")
        self.labelSessionExp.grid(row=11, column=0, padx=20, pady=0, sticky='sne')
        self.enterSessionExp = Entry(self.FrameLeft, width=32,
                                       textvariable=StringVar(value=''))
        self.enterSessionExp.config(font='Helvetica 10 italic', state='normal')
        self.enterSessionExp.grid(row=11, column=1, padx=(0, 0), pady=5, sticky="senw")

        self.labelSessionDesc = Label(self.FrameLeft, text='Description:', background="#d3d3d3")
        self.labelSessionDesc.grid(row=12, column=0, padx=20, pady=0, sticky='sne')
        self.descriptionVar = StringVar(value="Virtual Hallway Task")
        self.descriptionChoices = ['Virtual Hallway Task']
        self.selectDescription = OptionMenu(self.FrameLeft, self.descriptionVar, *self.descriptionChoices)
        self.selectDescription.grid(row=12, column=1, padx=(0, 0), pady=5, sticky="senw")


        self.labelSessionLab = Label(self.FrameLeft, text='Lab:', background="#d3d3d3")
        self.labelSessionLab.grid(row=13, column=0, padx=20, pady=0, sticky='sne')
        self.enterSessionLab = Entry(self.FrameLeft, width=32,
                                      textvariable=StringVar(value='Giocomo Lab'))
        self.enterSessionLab.config(font='Helvetica 10 italic', state='normal')
        self.enterSessionLab.grid(row=13, column=1, padx=(0, 0), pady=5, sticky="senw")

        self.labelSessionInst = Label(self.FrameLeft, text='Institution:', background="#d3d3d3")
        self.labelSessionInst.grid(row=14, column=0, padx=20, pady=0, sticky='sne')
        self.enterSessionInst = Entry(self.FrameLeft, width=32,
                                     textvariable=StringVar(value='Stanford University School of Medicine'))
        self.enterSessionInst.config(font='Helvetica 10 italic', state='normal')
        self.enterSessionInst.grid(row=14, column=1, padx=(0, 0), pady=5, sticky="senw")

        self.RunButton = Button(self.FrameLeft, text="RUN", command=self.buttonRun, background = "#d3d3d3")
        self.RunButton.grid(row=15, column=1, padx=30, pady=(20,20), sticky='NESW')


    def selectFile(self):
        filename = askopenfilename()
        self.fileName.delete(0,END)
        self.fileName.config(font='Helvetica 10 italic', state='normal')
        self.fileName.insert(0,filename)

    #RUN Button is selected
    def buttonRun(self):
        self.gio_tuple = (self.fileName.get(),\
                         self.enterSubjectID.get(), \
                         self.enterSubjectDOB.get(),\
                         self.enterSubjectDesc.get(),\
                         self.sexVar.get(),\
                         self.speciesVar.get(),\
                         int(self.enterSubjectWeight.get()),\
                         self.enterSessionID.get(), \
                         self.enterSessionStart.get(), \
                         self.enterSessionExp.get() , \
                         self.descriptionVar.get() ,
                         self.enterSessionInst.get(),
                         self.enterSessionLab.get())
        conversion.convert(self.gio_tuple)



    def close_windows(self):
        self.master.destroy()
        sys.exit()





root = Tk()
root.withdraw()
#root = Tk()
#root.withdraw()
#client = Connect()
myGui = guiMain(root)


center(root)
root.mainloop()


