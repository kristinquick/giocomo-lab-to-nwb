

from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from tkinter.simpledialog import askstring
import datetime
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
import pytz
import conversion
import os.path


#datetime_iso = ''
# setup Stanford timezone timezones
timezone_cali = pytz.timezone('US/Pacific')

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
        self.master.iconbitmap('giocomo_lab.ico')
        self.master.option_add("*font", "Helvetica 10")
        self.master.minsize(width=575, height=700)
        self.master.maxsize(width=575, height=700)
        self.master.title("Giocomo Lab")
        self.master.resizable(1, 1)  # Don't allow resizing in the x or y direction
        self.master.configure(background="#d3d3d3")


        #self.session_iso = ''


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
        self.select_file_button = Button(self.FrameLeft, text="Select File", command=self.select_file,
                                       background="#d3d3d3")
        self.select_file_button.grid(row=0, column=0, padx=20, pady=(20, 0), sticky='NEW')
        self.file_name = Entry(self.FrameLeft, width=32,
                              textvariable=StringVar(value=""))
        self.file_name.config(font='Helvetica 10 italic', state='disabled')
        self.file_name.grid(row=0, column=1, padx=(0, 0), pady=(20, 0), sticky="senw")

        #Subject Information
        self.label_subject = Label(self.FrameLeft, text='Subject Information:     ', background="#d3d3d3")
        self.label_subject.grid(row=1, column=0, padx=20, pady=(20,0), sticky='snw')

        # Subject Information - ID
        self.label_subject_id = Label(self.FrameLeft, text='ID:', background="#d3d3d3")
        self.label_subject_id.grid(row=2, column=0, padx=20, pady=0, sticky='ne')
        self.enter_subject_id = Entry(self.FrameLeft, width=40,
                                      textvariable=StringVar(value='L5'))
        self.enter_subject_id.config(font='Helvetica 10 italic', state='normal')
        self.enter_subject_id.grid(row=2, column=1, padx=(0, 0), pady=0, sticky="senw")

        # Subject Information - DOB
        today = datetime.date.today()
        datetime_dob = datetime.datetime(2016, 10, 4, 0, 0, 0)
        datetime_dob_tz = timezone_cali.localize(datetime_dob)
        self.datetime_dob = datetime_dob_tz
        self.dob_iso = datetime_dob_tz.isoformat()
        self.label_subject_dob = Label(self.FrameLeft, text='DOB:', background="#d3d3d3")
        self.label_subject_dob.grid(row=3, column=0, padx=20, pady=0, sticky='sne')
        self.dob_button = Button(self.FrameLeft, text=" Select ", command=self.dob_picker,
                                        background="#d3d3d3")
        self.dob_button.grid(row=3, column=1, padx=0, pady=(10,5), sticky='NWS')
        self.selected_dob = Label(self.FrameLeft, text= self.dob_iso, background="#d3d3d3",font='Helvetica 10 italic')
        self.selected_dob.grid(row=3, column=1, padx=80, pady=0, sticky='nsw')

        # Subject Information - Description
        #default_desc = 'Probe: +/-3.3mm ML, 0.2mm A of sinus, then as deep as possible'
        default_desc = 'naive'
        self.label_subject_desc = Label(self.FrameLeft, text='Description:', background="#d3d3d3")
        self.label_subject_desc.grid(row=4, column=0, padx=20, pady=0, sticky='sne')
        self.enter_subject_desc = Entry(self.FrameLeft, width=40,
                                     textvariable=StringVar(value=default_desc))
        self.enter_subject_desc.config(font='Helvetica 10 italic', state='normal')
        self.enter_subject_desc.grid(row=4, column=1, padx=(0, 0), pady=5, sticky="senw")

        # Subject Information - Sex
        self.label_subject_sex = Label(self.FrameLeft, text='Sex:', background="#d3d3d3")
        self.label_subject_sex.grid(row=5, column=0, padx=20, pady=5, sticky='sne')
        self.sex_var = StringVar(value="Male")
        self.select_sex = Radiobutton(self.FrameLeft, text="Male", background="#d3d3d3",
                                      variable=self.sex_var, value="Male")
        self.select_sex.grid(row=5, pady=5, padx=20, column=1, sticky="W")
        self.select_sex = Radiobutton(self.FrameLeft, text="Female", background="#d3d3d3", variable=self.sex_var,
                                      value="Female")
        self.select_sex.grid(row=5, pady=5, padx=80, column=1, sticky="W")

        # Subject Information - Weight
        self.label_subject_weight = Label(self.FrameLeft, text='Weight (grams):', background="#d3d3d3")
        self.label_subject_weight.grid(row=6, column=0, padx=20, pady=0, sticky='sne')
        self.enter_subject_weight = Entry(self.FrameLeft, width=10,
                                          textvariable=IntVar(value=""))
        self.enter_subject_weight.config(font='Helvetica 10 italic', state='normal')
        self.enter_subject_weight.grid(row=6, column=1, padx=(0, 0), pady=5, sticky="snw")

        #Subject Information- Species
        self.label_subject_species = Label(self.FrameLeft, text='Species:', background="#d3d3d3")
        self.label_subject_species.grid(row=7, column=0, padx=20, pady=0, sticky='sne')
        with open("species.txt", "r") as original:
            self.species_choices = []
            for line in original:
                line = line.strip('\n')
                self.species_choices.append(line)
        self.species_var = StringVar(value = self.species_choices[0])
        self.select_species = OptionMenu(self.FrameLeft, self.species_var, *self.species_choices)
        self.species_var.set(self.species_choices[0])
        self.select_species.configure(width=15,height=1)
        self.select_species.grid(row=7, column=1, padx=(0, 0), pady=0, sticky="snw")
        self.edit_species_button = Button(self.FrameLeft, text=" Add ", command=self.button_add_species,
                                             background="#d3d3d3")
        self.edit_species_button.grid(row=7, column=1, padx=0, pady=0, sticky='NES')

        # Subject Information - Brain Region
        self.label_subject_brain = Label(self.FrameLeft, text='Brain Region:', background="#d3d3d3")
        self.label_subject_brain.grid(row=8, column=0, padx=20, pady=0, sticky='sne')
        with open("brain_regions.txt", "r") as original:
            self.brain_choices = []
            for line in original:
                line = line.strip('\n')
                self.brain_choices.append(line)
        self.brain_var = StringVar(value=self.brain_choices[0])
        self.brain_var.set(self.brain_choices[0])
        self.select_brain = OptionMenu(self.FrameLeft, self.brain_var, *self.brain_choices)
        self.select_brain.configure(width=20, height=1)
        self.select_brain.grid(row=8, column=1, padx=(0, 0), pady=5, sticky="snw")
        self.edit_brain_button = Button(self.FrameLeft, text=" Add ", command=self.button_add_brain, background="#d3d3d3")
        self.edit_brain_button.grid(row=8, column=1, padx=0, pady=5, sticky='NES')

        # Subject Information - Surgery
        surgery_default_desc = 'Probe: +/-3.3mm ML, 0.2mm A of sinus, then as deep as possible'
        self.label_subject_surgery = Label(self.FrameLeft, text='Surgery:', background="#d3d3d3")
        self.label_subject_surgery.grid(row=9, column=0, padx=20, pady=0, sticky='sne')
        self.enter_subject_surgery = Entry(self.FrameLeft, width=40, textvariable=StringVar(value=surgery_default_desc))
        self.enter_subject_surgery.config(font='Helvetica 10 italic', state='normal')
        self.enter_subject_surgery.grid(row=9, column=1, padx=(0, 0), pady=5, sticky="senw")


        # Session Information
        self.label_session = Label(self.FrameLeft, text='Session Information:', background="#d3d3d3")
        self.label_session.grid(row=10, column=0, padx=20, pady=(10, 0), sticky='snw')

        # Session Information - ID
        self.label_session_id = Label(self.FrameLeft, text='ID:', background="#d3d3d3")
        self.label_session_id.grid(row=11, column=0, padx=20, pady=0, sticky='sne')
        self.enter_session_id = Entry(self.FrameLeft, width=32, textvariable=StringVar(value='npI5_0417_baseline_1'))
        self.enter_session_id.config(font='Helvetica 10 italic', state='normal')
        self.enter_session_id.grid(row=11, column=1, padx=(0, 0), pady=5, sticky="senw")

        today = datetime.date.today()
        datetime_session = datetime.datetime(2017, 4, 4, 0, 0, 0)
        datetime_session_tz = timezone_cali.localize(datetime_session)
        self.datetime_session = datetime_session_tz
        self.session_iso = datetime_session_tz.isoformat()
        self.label_session = Label(self.FrameLeft, text='Start Date & Time:', background="#d3d3d3")
        self.label_session.grid(row=12, column=0, padx=20, pady=0, sticky='sne')
        self.session_button = Button(self.FrameLeft, text="Select", command=self.session_picker, background="#d3d3d3")
        self.session_button.grid(row=12, column=1, padx=0, pady=5, sticky='NWS')
        self.session_date = Label(self.FrameLeft, text=self.session_iso, background="#d3d3d3", font='Helvetica 10 italic')
        self.session_date.grid(row=12, column=1, padx=80, pady=0, sticky='nsw')


        #Session - Experimenter
        self.label_session_exp = Label(self.FrameLeft, text='Experimenter:', background="#d3d3d3")
        self.label_session_exp.grid(row=15, column=0, padx=20, pady=0, sticky='sne')
        with open("experimenters.txt", "r") as original:
            self.experimenter_choices = []
            for line in original:
                line = line.strip('\n')
                self.experimenter_choices.append(line)
        self.experimenter_var = StringVar(value = self.experimenter_choices[0])
        self.select_experimenter = OptionMenu(self.FrameLeft, self.experimenter_var, *self.experimenter_choices)
        self.select_experimenter.config(width=20)
        self.select_experimenter.grid(row=15, column=1, padx=(0, 0), pady=5, sticky="swn")
        self.edit_experimenter_button = Button(self.FrameLeft, text=" Add ", command=self.button_add_experimenter, background="#d3d3d3")
        self.edit_experimenter_button.grid(row=15, column=1, padx=0, pady=5, sticky='NES')

        # Session - Description
        self.label_session_desc = Label(self.FrameLeft, text='Description:', background="#d3d3d3")
        self.label_session_desc.grid(row=16, column=0, padx=20, pady=0, sticky='sne')
        self.description_var = StringVar(value="Virtual Hallway Task")
        self.description_choices = ['Virtual Hallway Task']
        self.select_description = OptionMenu(self.FrameLeft, self.description_var, *self.description_choices)
        self.select_description.config(width=20)
        self.select_description.grid(row=16, column=1, padx=(0, 0), pady=5, sticky="snw")
        self.edit_descr_button = Button(self.FrameLeft, text=" Add ", command=self.button_add_description, background="#d3d3d3")
        self.edit_descr_button.grid(row=16, column=1, padx=0, pady=5 , sticky='NES')

        # Session - Lab
        self.label_session_lab = Label(self.FrameLeft, text='Lab:', background="#d3d3d3")
        self.label_session_lab.grid(row=17, column=0, padx=20, pady=0, sticky='sne')
        self.enter_session_lab = Entry(self.FrameLeft, width=32,
                                      textvariable=StringVar(value='Giocomo Lab'))
        self.enter_session_lab.config(font='Helvetica 10 italic', state='normal')
        self.enter_session_lab.grid(row=17, column=1, padx=(0, 0), pady=5, sticky="senw")

        # Session - Institution
        self.label_session_inst = Label(self.FrameLeft, text='Institution:', background="#d3d3d3")
        self.label_session_inst.grid(row=18, column=0, padx=20, pady=0, sticky='sne')
        self.enter_session_inst = Entry(self.FrameLeft, width=32,
                                     textvariable=StringVar(value='Stanford University School of Medicine'))
        self.enter_session_inst.config(font='Helvetica 10 italic', state='normal')
        self.enter_session_inst.grid(row=18, column=1, padx=(0, 0), pady=5, sticky="senw")

        self.run_button = Button(self.FrameLeft, text="RUN", command=self.button_run, background = "#d3d3d3")
        self.run_button.grid(row=19, column=1, padx=30, pady=(20,20), sticky='NESW')



    # Date Picker for the Subject's DOB
    def dob_picker(self):
        today = datetime.date.today()
        self.dob_date_picker = Tk()
        self.dob_date_picker.iconbitmap('giocomo_lab.ico')
        self.dob_date_picker.wm_title("Select Date")
        mindate = datetime.date(year=2015, month=1, day=1)
        maxdate = today + datetime.timedelta(days=1)
        self.cal_dob = Calendar(self.dob_date_picker, font="Arial 14", selectmode='day', locale='en_US',
        mindate=mindate, maxdate=maxdate, background='darkblue', foreground='white', borderwidth=2,
        cursor="hand1", year=2019, month=2, day=5)
        self.cal_dob.grid(row=1, pady=40, padx=50, column=1, sticky="W")
        self.dob_button = Button(self.dob_date_picker, text="Done", command=self.dob_selected, background="#d3d3d3")
        self.dob_button.grid(row=2, column=1, padx=220, pady=(0,30) , sticky='sW')

        #Subject's DOB Selected - Save
    def dob_selected(self):
        date_dob = self.cal_dob.selection_get()
        datetime_dob = datetime.datetime(date_dob.year, date_dob.month, date_dob.day, 0, 0, 0)
        datetime_dob_tz = timezone_cali.localize(datetime_dob)
        self.datetime_dob = datetime_dob
        self.dob_iso = datetime_dob_tz.isoformat()
        self.selected_dob.config(text=str(self.dob_iso))
        self.dob_date_picker.destroy()

    # Session Start Time Date and Time Picker
    def session_picker(self):
        today = datetime.date.today()
        self.session_date_picker = Tk()
        self.session_date_picker.iconbitmap('giocomo_lab.ico')
        self.session_date_picker.wm_title("Select Date and Time")
        mindate = datetime.date(year=2000, month=1, day=1)
        maxdate = today + datetime.timedelta(days=1)
        self.cal_session = Calendar(self.session_date_picker, font="Arial 14", selectmode='day', locale='en_US',
                                    mindate=mindate, maxdate=maxdate, background='darkblue', foreground='white',
                                    borderwidth=2,
                                    cursor="hand1", year=2018, month=2, day=5)
        self.cal_session.grid(row=1, pady=40, padx=40, column=1, sticky="W")
        self.label_session_hour = Label(self.session_date_picker, text='Hour:')
        self.label_session_hour.grid(row=2, column=1, padx=100, pady=0, sticky='snw')
        self.session_hour = ttk.Combobox(self.session_date_picker,
                                         value=["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                                "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])
        self.session_hour.grid(row=2, column=1, padx=140, pady=0, sticky="swn")
        self.session_hour.state = "Readonly"
        self.session_hour.current(0)
        self.session_hour.config(width=4)

        self.label_session_minute = Label(self.session_date_picker, text='Minute:')
        self.label_session_minute.grid(row=2, column=1, padx=150, pady=0, sticky='sne')
        self.session_minute = ttk.Combobox(self.session_date_picker,
                                           value=["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
                                                  "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
                                                  "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
                                                  "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
                                                  "40", "41", "42", "43", "44", "45", "46", "47", "88", "49",
                                                  "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"])
        self.session_minute.grid(row=2, column=1, padx=95, pady=0, sticky="sen")
        self.session_minute.state = "Readonly"
        self.session_minute.current(0)
        self.session_minute.config(width=4)


        self.session_button = Button(self.session_date_picker, text="Done", command=self.session_selected,
                                     background="#d3d3d3")
        self.session_button.grid(row=3, column=1, padx=200, pady=20, sticky='snw')
        self.session_button.config(state="normal")
        self.label_session_blank = Label(self.session_date_picker, text='')
        self.label_session_blank.grid(row=4, column=1, padx=100, pady=10, sticky='snw')



    def button_select_date_time(self):
        self.session_date_time = Tk()
        self.session_date_time.title("Session Date and Time")
        self.session_date_time.iconbitmap('giocomo_lab.ico')
        self.session_date_time.config(background="#d3d3d3")

        self.session_date_time.hour_choices = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                               "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
        self.session_date_time.hour_var = StringVar()
        self.session_date_time.hour_var.set(self.session_date_time.hour_choices[0])
        print(self.session_date_time.hour_var.get())
        self.var2 = tkinter.StringVar(root)
        self.var2.set("This one works.")
        w = 400  # popup window width
        h = 200  # popup window height
        sw = self.session_date_time.winfo_screenwidth()
        sh = self.session_date_time.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.session_date_time.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.session_date_button = Button(self.session_date_time, text="Select Date", command=self.dob_picker,
                                          background="#d3d3d3")
        self.session_date_button.grid(row=1, column=0, padx=10, pady=(10, 10), sticky='sW')
        self.label_session_hour = Label(self.session_date_time, text='Hour:', background="#d3d3d3")
        self.label_session_hour.grid(row=2, column=0, padx=10, pady=10, sticky='snw')
        self.session_hour = ttk.Combobox(self.session_date_time,
                                         value=["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                                "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])
        self.session_hour.grid(row=2, column=1, padx=5, pady=5, sticky="swn")
        self.session_hour.state = "Readonly"
        self.session_hour.current(0)
        self.session_hour.config(width=4)
        self.label_session_min = Label(self.session_date_time, text='Minute:', background="#d3d3d3")
        self.label_session_min.grid(row=3, column=0, padx=10, pady=10, sticky='snw')
        self.date_time_done_button = Button(self.session_date_time, text="Done", command=self.session_selected,
                                            background="#d3d3d3")
        self.date_time_done_button.grid(row=4, column=1, padx=10, pady=(0, 30), sticky='sW')

    # Session Date Selected - Save
    def session_selected(self):
        date_session = self.cal_session.selection_get()
        datetime_session = datetime.datetime(date_session.year, date_session.month, date_session.day, int(self.session_hour.get()), int(self.session_minute.get()), 0)
        datetime_session_tz = timezone_cali.localize(datetime_session)
        self.datetime_session = datetime_session_tz
        self.session_iso = datetime_session_tz.isoformat()
        self.session_date.config(text=str(self.session_iso))
        try:
            self.session_date_picker.destroy()
        except:
            pass


    def select_file(self):
        filename = askopenfilename()
        self.file_name.delete(0,END)
        self.file_name.config(font='Helvetica 10 italic', state='normal')
        self.file_name.insert(0,filename)

    #Prompt for a new species.  Add to OptionMenu and update file "species.txt"
    def button_add_species(self):
        species_new = askstring('Species', 'Enter New Species')
        if species_new is not None:
            self.species_choices.append(species_new)
            self.select_species["menu"].add_command(label=species_new,
                                                  command=tkinter._setit(self.species_var, species_new))
            self.species_var.set(self.species_choices[len(self.species_choices)-1])
            species_new = species_new + "\n"
            with open('species.txt', 'r') as original:
                data = original.read()
            with open('species.txt', 'w') as modified:
                modified.write(data + species_new )

    # Prompt for a new brain region.  Add to OptionMenu and update file "brain_region.txt"
    def button_add_brain(self):
        brain_new = askstring('Brain Region', 'Enter New Brain Reqion')
        if brain_new is not None:
            self.brain_choices.append(brain_new)
            self.select_brain["menu"].add_command(label=brain_new,
                                                    command=tkinter._setit(self.brain_var, brain_new))
            self.brain_var.set(self.brain_choices[len(self.brain_choices) - 1])
            brain_new = brain_new + "\n"
            with open('brain_regions.txt', 'r') as original:
                data = original.read()
            with open('brain_regions.txt', 'w') as modified:
                modified.write(data + brain_new)

    # Prompt for a new experimenter.  Add to OptionMenu and update file "experimenters.txt"
    def button_add_experimenter(self):
        experimenter_new = askstring('Experimenter', 'Enter New Experimenter Name')
        if experimenter_new is not None:
            self.experimenter_choices.append(experimenter_new)
            self.select_experimenter["menu"].add_command(label=experimenter_new,
                                                    command=tkinter._setit(self.experimenter_var, experimenter_new))
            self.experimenter_var.set(self.experimenter_choices[len(self.experimenter_choices) - 1])
            experimenter_new = experimenter_new + "\n"
            with open('experimenters.txt', 'r') as original:
                data = original.read()
            with open('experimenters.txt', 'w') as modified:
                modified.write(data + experimenter_new)

    # Prompt for a new description.  Add to OptionMenu and update file "descriptions.txt"
    def button_add_description(self):
        description_new = askstring('Description', 'Enter New Description')
        if description_new is not None:
            self.description_choices.append(description_new)
            self.select_description["menu"].add_command(label=description_new,
                                                         command=tkinter._setit(self.description_var,
                                                                                    description_new))
            self.description_var.set(self.description_choices[len(self.description_choices) - 1])
            description_new = description_new + "\n"
            with open('descriptions.txt', 'r') as original:
                data = original.read()
            with open('descriptions.txt', 'w') as modified:
                modified.write(data + description_new)

    #RUN Button is selected
    def button_run(self):
        self.gio_dict = {
            "input_file": self.file_name.get(),
            "subject_id": self.enter_subject_id.get(),
            "subject_date_of_birth": self.datetime_dob,
            "subject_description": self.enter_subject_desc.get(),
            "subject_sex": self.sex_var.get(),
            "subject_weight": self.enter_subject_weight.get(),
            "surgery": self.enter_subject_surgery.get(),
            "subject_brain_region": self.brain_var.get(),
            "subject_species": self.species_var.get(),
            "session_id": self.enter_session_id.get(),
            "session_start_time": self.datetime_session,
            "experimenter": self.experimenter_var.get(),
            "experiment_description": self.description_var.get() ,
            "institution": self.enter_session_inst.get(),
            "lab_name": self.enter_session_lab.get(),

        }

        print(self.gio_dict["subject_id"])
        conversion.convert(**self.gio_dict)



    def close_windows(self):
        self.master.destroy()
        sys.exit()





root = Tk()
root.withdraw()
w = 0
h = 0
x = 100
y = 10
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

myGui = guiMain(root)


center(root)
root.mainloop()


