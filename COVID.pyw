#!/usr/bin/env python
# coding: utf-8

# In[1]:


Info = """Simple self contained program for UI -> COVID
Written By: Joshua Tanner

Self Running Notes:
changing file type to .pyw and setting to open with pythonw.exe works. 
However it is best to have:
1.) A non anaconda version of python installed for self runs (installer can set to sys path): https://www.python.org/downloads/
2.) Updated Pip (not neccesary):
    -Set permenant SSL trusted for PIP (to avoid SSL error): pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pip setuptools
3.) Make sure the dependencies load as per the below (and check them individually if possible)
    -command prompt (as administrator or using sudo) can install individually if need be (pip install ***)
    -instant crash means it failed
    -it may not work programmatically with missing libraries unless it can be elevated to admin
    
Note: If Anaconda Python was installed to path (it is not recommended) then hunting down all reg keys is needed
"""
#____________________________________________________________________________________________________________
#Libraries

#System - Should Always Load (Base Libraries)
import os, sys, platform              #General OS interaction and major commands
import subprocess                     #Failsafe load
import datetime                       #Useful for time stamping
# import shutil                         #File copying, moving, etc.
# from ast import literal_eval as AE    #For safer string evaluation
import ast                             #For safer string evaluation
from copy import deepcopy as CY        #Deepcopy command that is easier to use - Note: usually "C"

#GUI
#Super useful general tkinter breakdown
#https://www.devdungeon.com/content/gui-programming-python
from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont    #Used for determining length of text

#Operations
import datetime                       #For WebData Time Formating
from datetime import datetime as dt   #For WebData Time Formating 
import functools as ft
import math

try:    
    import urllib.request as request      #For WebData
    import matplotlib.pyplot as plt       #Create Graph
    from matplotlib import lines          #Create Graph

    #Operations
    import numpy as np
    
    Fail = False #Checks if a library failed to load
    
except:
    Fail = True #Checks if a library failed to load

#Library Installer
def install(package, TryJupyter = True, Shell = False):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package], shell = Shell)
    except:
        if not TryJupyter: return "Subprocess Load Fail... "
        try:
            eval("!{sys.executable} -m pip install %s" % package)
        except:
            return "Jupyter/iPython Notebook Dependency Method Fail... "
        
    return "Package Installed"
        
def install_and_import(package, Overwrite = False, VarUpdate = None):
    
    if Overwrite or package not in globals().keys(): 
        try:
#             __import__('messages_en', globals={"__name__": __name__})
            globals()[package] = __import__(package, globals = globals())
        
            return "Library loaded: %s" % package
        except ImportError:
#         except:
            try:
                pip = __import__("pip", globals = globals())
    
                if int(pip.__version__.split('.')[0])>9:
                    from pip._internal import main as pip_main
                else:
                    from pip import main as pip_main
                    
                try:
                    pip_main(["install", package])
                except SystemExit as e:
                    pass
            except:
                if VarUpdate == None:
                    print(install(package))
                else:
                    VarUpdate.set(install(package))
            finally:
                if package in globals().keys():
                    globals()[package] = __import__(package, globals = globals())
                    return "Package installed -> Library loaded: %s" % package
                else:
                    return "Library failed to load/install: %s" % package
    return "Library Already Loaded: %s" % package

Windows = [] #Top level window holder

class PopUpWindow:
    def __init__(self, master, msg = "", Addons = [], Size = [], Pad = [0, 0, 0, 0], AdjSize = False, YScroll = False, XScroll = False, LibLoad = None, MainMaster = None):
        
        self.master = master
        self.Master = MainMaster
        self.Count = 0
        self.msg = StringVar()
        self.msg.set(msg)
        self.LibLoad = LibLoad
        self.Size = Size
        
        LabelNote = Label(master, textvariable = self.msg, justify = "left")
        
        if "MultiTableInput" in globals().keys() and Addons != []:
            
            if Size == []:
                XAddons = MultiTableInput(master, Addons, Size, Pad, AdjSize, YScroll, XScroll)
                XAddons.pack()
                ExitButton = Button(master, text = "Cancel", command = lambda: self.master.destroy())
                ExitButton.pack()
            else:
                LabelNote.grid(row = 0, column = 0, columnspan = self.Size[0], sticky = "NWES")
                XAddons = MultiTableInput(master, Addons, self.Size[:3] + [int(round(self.Size[3]* self.Size[1]/(self.Size[1]+2+1)))], Pad, AdjSize, YScroll, XScroll, Master = MainMaster)
                XAddons.grid(row = 1, column = 0, rowspan = self.Size[1], columnspan = self.Size[0], sticky = "NWES")
                ExitButton = Button(master, text = "Cancel", command = lambda: self.master.destroy())
                ExitButton.grid(row = self.Size[1] + 1, column = 0, columnspan = self.Size[0], sticky = "NWES")
                for i in range(2 + self.Size[1]+1): master.rowconfigure(i, weight = 1, minsize = int(round(self.Size[3]/(self.Size[1]+2))))
                for i in range(self.Size[0]): master.columnconfigure(i, weight = 1, minsize = int(round(self.Size[2]/self.Size[0])))
                
        elif Addons != []:
            LabelNote.pack()
            FailNote = Label(master, text = "Program Failure", justify = "left")
            FailNote.pack()
            ExitButton = Button(master, text = "Exit", width = 400, command = lambda: self.master.destroy())
            ExitButton.pack()
            ExitButton.focus_set()
        else:
            LabelNote.pack()
            self.Load = LibLoad
            ContinueButton = Button(master, text = "Continue", width = 400, command = lambda: self.Run(self.Count, self.msg))
            ContinueButton.pack()
            ContinueButton.focus_set()

        master.focus_set()

    def Run(self, Count, Note):
        if self.LibLoad != None and Count < len(self.Load):
#             for x in self.Load: Note.set(install_and_import(x, Overwrite = False, VarUpdate = Note))
            Note.set(install_and_import(self.Load[Count], Overwrite = False, VarUpdate = Note))
            self.Count += 1
        else:
            self.Master.destroy()
            
def PopUp(msg = "", Addons = [], Size = [], Pad = [0, 0, 0, 0], AdjSize = False, YScroll = False, XScroll = False, Load = None, Master = None):
    global Windows
    
#     Windows += [Tk()] #Main Loop
    Windows += [Toplevel()]
    Windows[-1].wm_title("Notice")
    if Size != []: Windows[-1].geometry("%dx%d" % (Size[2], Size[3]))                     
    Windows += [PopUpWindow(Windows[-1], msg, Addons, Size, Pad, 
          AdjSize, YScroll, XScroll, Load, Master)]  
    
#     Windows[-2].mainloop() #This is only for main loop
    
NonStandardLibs = ["urllib.request", "numpy", "matplotlib"]                   
CLI = sys.argv

if Fail:
    if len([x for x in CLI if ".json" in x]) > 0 or len([x for x in CLI if ".json" not in x]) <= 2:                     
        Windows += [PopUp("Failed to Load Libraries\nAttempting Dependency Install...", Load = NonStandardLibs)]
#         Windows[-2].mainloop() #****************        
        if len([x for x in NonStandardLibs if x not in globals().keys()])>0: sys.exit("Failed to load")
    else:
        for x in NonStandardLibs: print(install_and_import(x, Overwrite = False))

#Sub non standard libraries
import urllib.request as request      #For WebData
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Base Settings - Global
Settings = {"Size": [], "OS": ""}

#___________________________________________________________________________
#Read and calculate from CSV Data

#Typical Types/Shorthands
C = "Confirmed"
D = "Deaths"
R = "Recovered"
T = "Total"
S = "Sick"
P = "Place"
I = 'Infected'
ByDGC = "By Day Growth: Confirmed"
ByDGD = "By Day Growth: Deaths"
ByDGS = "By Day Growth: Sick"

St = "State"
States = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', "District of Columbia" : "DC", "Other" : "Others (Puerto Rico etc..)"}

#Process Date Info
def Date(In, Out = "num", Day0 = dt(2020, 1, 22), Custom = "%m-%d-%Y"):    
    if isinstance(In, str): 
        DateStyle = "%m/%d/%Y"          #Style of John Hopkins Data
        if "-" in In: 
            DateStyle  = "%m-%d-%Y"     #Base Style
            if len(In.split("-")[0])> 2: 
                DateStyle  = "%Y-%m-%d"
        elif "/" in In and len(In.split(" ")[0].split("/")[2]) == 2: 
            DateStyle = "%m/%d/%y"
        
        if ":" in In: DateStyle += " %H:%M:%S"
        if "m" in In.lower(): DateStyle += " %p"
        Day = dt.strptime(In, DateStyle)
    elif In.__class__ == datetime.datetime:
        Day = In #Day0
    else:
        Day = Day0 + datetime.timedelta(days = In)
    
    if Out == "str":
        Day = str(Day).split(" ")[0]
    elif Out == "num":
        Day = str(Day - Day0)
        if Day[0] != "0":
            Day = int(Day.split(" ")[0])
        else:
            Day = 0
    elif Out == "custom":    
        Day = dt.strftime(Day, Custom)
    else:
        print("Error in Date", In)
        Day = 0
               
    return Day

#Get CSV from website
def WebCSV(URL):
    Out = request.urlopen(URL).read().decode('utf8').split("\n")
    Out = [x.replace("\"", "").replace("\'", "").replace(", ", " - ").replace("\r","").replace("*","").split(",") for x in Out]
    return Out

#Either Read saved file (old) or get from the web
def GetData(Type = "web", Save = True, Files = []):
    if Type == "web":
        #Checks for old data first:
        if  "Data" not in globals().keys(): globals()["Data"] = {}  
        Data = globals()["Data"]
        if Data == {} or "Time" not in Data.keys(): 
            Data = GetData("web-old", False)
#             Last = Date(Data[C]["Raw"][0][-1], "num") #Dont Add one as there are 2 sets of 3/23 data

        Last = len(Data["Time"])
        Now  = Date(dt.now(), "num")
        
        while Now >= Last:
            try:
                New = WebCSV(r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/%s.csv" % Date(Last, "custom"))
                New = [x for x in New if len(x)>8]
                
                Blank = [0] * len(Data["Time"])
                if Last!= 61: Data.update({"Time":Data["Time"] + [Last]})
                
                for y in New[1:]:
                    if y[3] not in Data[P].keys(): 
                        Data[P].update({y[3]: {}})
                        for x in [C, D, R]: Data[P][y[3]].update({x: Blank})
                        print("Added: ", y[3])
                    
                    for i,x in enumerate([C, D, R]):
                        if len(Data[P][y[3]][x]) <= Last: 
                            Data[P][y[3]].update({x:Data[P][y[3]][x] + Blank[len(Data[P][y[3]][x]):] + [int(y[7+1])]})
                        else:
                            Temp = Data[P][y[3]][x]
                            Temp[Last] = Temp[Last] + int(y[7+i])
                            Data[P][y[3]].update({x:Temp})
                    
                    if y[3] == "US":
                        if not y[2] in States.keys(): y[2] = "Other"
                        y[2] = States[y[2]]
                        
                        #print(y)
                        #sys.exit()
                        for i,x in enumerate([C,D,R]):
                            if len(Data[St][y[2]][x]) <= Last: 
                                Data[St][y[2]].update({x:Data[St][y[2]][x] + Blank[len(Data[St][y[2]][x]):] + [int(y[7+i])]})
                                
                            else:
                                Temp = Data[St][y[2]][x]
                                Temp[Last] += int(y[7+i])
                                Data[St][y[2]].update({x:Temp})
                    
                    for y in [C,D,R]:
                        for x in Data[P].keys(): 
                            if len(Data[P][x][y]) < Last+1: 
                                Data[P][x].update({y:Data[P][x][y] + Blank[len(Data[P][x][y])-1:]})
                        for x in Data[St].keys(): 
                            if len(Data[St][x][y]) < Last+1: 
                                Data[St][x].update({y:Data[St][x][y] + Blank[len(Data[St][x][y])-1:]})
                        
                for x in [C,D,R]:
                    Data[T].update({x: [sum([Data[P][y][x][n] for y in Data[P].keys()]) for n,q in enumerate(Blank)]})                

                print("Grabbed Data for: %s" % Date(Last, "custom"))
            except:
                print("Failed to load day: %s" % Date(Last, "custom"))
                
            Last += 1
            
        Data[P].update({T: Data[T]})
                      
    elif Type == "web-old":
        #Data for - https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6
#John Hopkins COVID dashboard

        #Changed on 3/23 to new data source type. Will from here on out get base data and add to previous data by daily log
#         #Pre 3/23/2020
#         Data = {C: {"URL": r'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'}, D: {"URL": r'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'}, R: {"URL": r'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'}}
        
#         #Global switched out in new format(no state info!!)
#         Data = {C: {"URL": r'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'}, D: {"URL": r'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'}, R: {"URL": r'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_Recovered_global.csv'}}
        Data = {C:{}, D:{}, R:{}}
        for x in Data.keys():
            URL = "https://github.com/CSSEGISandData/COVID-19/raw/master/archived_data/archived_time_series/time_series_19-covid-%s_archived_0325.csv" % x
            Data[x].update({"Raw": WebCSV(URL)})
            Data[x].update({"Raw": [y for y in Data[x]["Raw"] if len(y)>2]})
        
        Data = ProcessRaw(Data)
        return Data
    
    elif Type == "file":
        if File == []: 
            Data = {C: {"file": "ncov-Confirmed.csv"}, D: {"file": "ncov-Deaths.csv"}, R: {"file": "ncov-Recovered.csv"}}
        else:
            Data = {C: Files[0], D: Files[1], R: Files[2]}
        
        for x in Data.keys():
            file = Data[x]["file"]
            with open(file, "r") as RF: Data[x].update({"Raw": [[z if z != "" else 0 for i,z in enumerate(y.replace(", ", " - ").replace("\r","").split(","))] for y in RF.read().replace("\"", "").replace("\'", "").split("\n") if len(y)>2], "Place": {}})
        return ProcessRaw(Data)

    if Save:
        for x in Data.keys():
            file = "COVID-%s-%s.csv" % (str(x), Date(dt.now(), "custom", "%m/%d"))
            with open(file, "w") as WF:
                WF.write("\n".join([",".join(str(y)) for y in Data[x]]))
    
    return Data

def ProcessRaw(Data):
    Data.update({"Time":[], P:{}, St: {}, T:{}})
    #Gets all dates (to ensure that everything has the same group of dates for same length lists), and places (to make sure all data has a place)
    for x in [C, R, D]:
        Times  = [Date(y, "num") for y in Data[x]["Raw"][0][4:] if Date(y, "num") not in Data["Time"]]
        Places = [y[1] for y in Data[x]["Raw"][1:] if len(Data[x]["Raw"]) > 1 and len(y)>1 and y[1] not in Data[P].keys()]
        State  = [y[0].split(" - ")[-1].strip(" ") if len(y[0].split(" - ")) > 1 else States[y[0].strip(" ")] if y[0] in States else States["Other"] for y in Data[x]["Raw"][1:] if y[0] != "" and y[0] not in Data[St].keys() and y[1].upper() == "US"]
        
        Data.update({"Time": sorted(Data["Time"] + Times)})
        for y in Places: Data[P].update({y:{}})
        for y in State: Data[St].update({y:{}})
                                         
    Blank = [0] * len(Data["Time"])
    for y in Data[P].keys():  Data[P][y].update({C: Blank, D: Blank, R: Blank})
    for y in Data[St].keys(): Data[St][y].update({C: Blank, D: Blank, R: Blank})
        
    for x in [C, R, D]:
        NewT = Blank
        qTime = [Date(q, "num") for q in Data[x]["Raw"][0][4:]]
        for z in Data[x]["Raw"][1:]:
            New  = [0 if y not in qTime or z[4:][qTime.index(y)] == '' or qTime.index(y)>=len(z[4:]) else int(z[4:][qTime.index(y)]) for y in Data["Time"]]
            New  = [y if i == 0 or (y == 0 and len([q for q in New[:i+1] if q!=0]) == 0) else [q for q in New[:i+1] if q!=0][-1] for i,y in enumerate(New)]
            NewT = [y + NewT[i] for i,y in enumerate(New)] 
            Data[P][z[1]].update({x:[y + Data[P][z[1]][x][i] for i,y in enumerate(New)]})
            if z[0] != "" and z[0] not in Data[St].keys() and z[1].upper() == "US":
                if len(z[0].split(" - ")) > 1: 
                    State = z[0].split(" - ")[-1].strip(" ")
                elif z[0] in States:
                    State = States[z[0]]
                else:
                    State = States["Other"]
                Data[St][State].update({x: [y + Data[St][State][x][i] for i,y in enumerate(New)]})
            
        del(Data[x]["Raw"])
                
        Data[T].update({x: [sum([Data[P][y][x][n] for y in Data[P].keys()]) for n,q in enumerate(Blank)]})            
    Data[P].update({T: Data[T]})
    return Data 

def CalcData(SubData):
    CL = SubData[C]
    DL = SubData[D]
    RL = SubData[R]
    
    SubData.update({S: [x - DL[i] - RL[i] for i,x in enumerate(CL)]})       #Sick
    SubData.update({ByDGC: [0] + [x - CL[i] for i,x in enumerate(CL[1:])]}) # By day growth rate confirmed
    SubData.update({ByDGS: [0] + [x - SubData[S][i] for i,x in enumerate(SubData[S][1:])]}) # By day growth rate sick
    SubData.update({ByDGD: [0] + [x - DL[i] for i,x in enumerate(DL[1:])]}) # By day growth rate death
    
    return SubData


# In[2]:


#_________________________________________________________________________

#Makes a float an integer
def MI(val):
    if isinstance(val, list):
        val = [int(np.floor(x)) for x in val]
        return val
    else:
        return int(np.floor(val))

#List sum value
def LS(L, Index, Sub = False):
    if Sub:
        Sum = [sum([y[Index] if len(y)>=Index else 0 for y in x]) for x in L]
    else:
        Sum = sum([x[Index] if len(x)>=Index else 0 for x in L])
    return Sum

#Mixed list sum and multiplied value (for appplying dist list to end of list 1)
def ML(L1, L2, Index = 0, Sub = None, SumL = True):
    
    if Sub != None: L1 = [x[Sub] for x in L1 if len(x) > Sub]
        
    if isinstance(L1, list) and len(L1)>0 and isinstance(L1[0], list) and isinstance(L2, list):
        Sum = [x[Index] * L2[-min(len(L2),len(L1)):][i] for i,x in enumerate(L1[-min(len(L2),len(L1)):])]
    elif isinstance(L1, list) and len(L1)>0 and isinstance(L1[0], list):
        Sum = [x[Index] * L2 for i,x in enumerate(L1) if len(x) > Index]
    elif isinstance(L1, list) and isinstance(L2, list):
        Sum = [x * L2[-min(len(L2),len(L1)):][i] for i,x in enumerate(L1[-min(len(L2),len(L1)):])]
    elif isinstance(L1, list):
        Sum = [x * L2 for x in L1]
    else:
        Sum = L1*L2
        
    if SumL:
        return sum(Sum)
    else:
        return Sum

#Normal distribution list
def NDist(mean = 0, sigma = None, factor = 1, sfact = 4):
    if sigma == None and mean!=0: 
        sigma = (mean/sfact)**0.5
    else:
        sfact = 1
    Dist = [(factor/(sigma*((2*math.pi)**.5)))*math.exp(-.5*(((x-mean)/sigma)**2)) for x in range(MI(mean-sigma**2),MI(mean+(sigma**2)*sfact))]
    Dist = ML(Dist, (factor/sum(Dist)), 0, None, False) #To make sure distribution is "complete" in this small arc
    return Dist
    
#Extended compartmental model
def Extrapolate(Val, ETime = 365):
    #Semi Compartmental (extended SIR), not currently a Monte Carlo version but uses normal distributions
    
    SD    = MI(Val["Start Date"])
    R0    = float(Val["Growth Rate"])
    DR    = float(Val["Death Rate"])
    DCAP  = MI(Val["Health care system overrun # of sick"])
    NDCAP = float(Val["Death Rate - Health care system overran"])
    SSD   = MI(Val["Social Distancing - Change Dates"])
    DSD   = [float(x) for x in Val["Social Distancing - Change"]]
    Pop   = MI(Val["Population"])
    NDMR  = float(Val["Normal daily mortality rate (per million)"])
    NICU  = float(Val["Normal ICU survial rate"])
    OICU  = float(Val["No ICU available survial rate"])
    NICUP = MI(Val["Normal ICU need by day"])
    ICUR  = float(Val["COVID ICU need rate"])
    CS    = MI(Val["Compartment Size"])
    EID   = [1-x for x in NDist(float(Val["Average Effective Immunity Duraration"]),None, 1, 8)]
    
    MIT   = NDist(float(Val["Mean Infection Time"]),None,1,1)
    AIS   = NDist(float(Val["Average infected to symptoms"]))   #This is about right for sigma
    MIT2  = NDist(abs((float(Val["Mean Infection Time"])-float(Val["Average infected to symptoms"])))+.01,None,1,1)
    
    TD    = NDist(float(Val["Average time to death"]), None, 1, 2) #This is about sigma factor of 2
    RT    = NDist(float(Val["Average time to recovery"]), float(Val["Average time to recovery - Sigma"]))
    DT    = NDist(float(Val["Average time to detection"]), None, float(Val["Average detection rate of non ICU or deaths"]), 1) 
    
    NOS   = float(Val["Non symptoms recovery ratio"])
    
    Flag = [] #Health care overrun flag
    ICU  = 1  #'Compartments' for approx ICU beds available
    
    EST0 = [0,R0,MI(R0),0,0,0,0,0,0,0,0,0,0,R0,R0,0,0] #Initial - 1 Compartment
    EST  = [[EST0]]
    
    #Day(0) - only the first one is "real" day, Newly Infected(1), Total Infected(2), Newly Sick (3), Sick(4), Sick - Confirmed (5), Confirmered (6), Recovered (day) (7), Total Recovered (8), Died (9), Direct Deaths (10), Indirect COVID deaths - by day(11), Indirect COVID death total(12), Reproduction Number(13), Growth Rate (14), non sick recoveries (lower suseciptible still) (15 - by day, 16 total) 
    
    #By Day
    for i in range(ETime - SD):
        
        NEST = CY(EST[-1])
        Flag += [[0]*MI(ICU)]
        
#         print(i, len(NEST), NEST[0])#,"\n")
        
        #By Compartment
        for n,z in enumerate(NEST):
            #Social distancing effect (can be day 0 and multiple same days)
            if i + min(0,SD) in SSD: z[13] = z[13]/(ft.reduce(lambda a,b: a*b, [1,1] + [DSD[m] for m,x in enumerate(SSD) if x == i + min(0,SD)]))
                
            SP = max(1, CS-z[10]-z[12]-ML(EST, EID, 7, n)-ML(EST, EID, 15, n)) 
            #Adjust growth by suspectiblity factor i.e. ratio of number of suspectible people each person is likely to come in contact with and infect - includes reinfection by only considering total recent reocoveries
            z[14] = z[13] * max(0,  SP - z[2])/SP
                        
            #Set Day
            z[0] += 1
                          
            #New & Total Infections (also checks sick for same time period)
            z[1]  = min(max(0,(ML(EST, MIT, 1, n) + ML(EST, MIT2, 3, n)) * z[14]), SP) #Can be non integer
#             if z[0] < 2: z[1] = max(z[14]/len(MIT), z[1]) #To ensure a cell gets started
            z[2] += MI(z[1]) #Not locked as rounded till here
                    
            #New & Total Sick (symptoms - possibly hospital - by ICUR) - sub status of infected
            z[3]  = ML(EST, AIS, 1, n, False)
            if sum(z[3])>=1:
                for m,x in enumerate(z[3]):
                    if len(EST) > m and len(EST[-m]) > n: 
                        EST[-m][n][1] = max(0, EST[-m][n][1] - x) #To prevent infected to sick double count
                z[3]  = sum(z[3]) #non integer
                z[4] += max(0, MI(z[3]))
                z[2] += -max(0, MI(z[3]))
            else:
                z[3]  = 0
                                
            #Confirmed
            z[5]  = MI(max(0, ML(EST, DT, 3, n))) #MI(ML(EST, DT, 1, n)
            z[6] += z[5]
                          
            #Health care over run effect (flag dates)
            if z[4]*ICUR + CS*NICUP/Pop > CS*DCAP/Pop and (i==0 or len(EST[2]) < n or EST[-2][n][2] + CS*NICUP/Pop < CS*DCAP/Pop): Flag[i][n] += i+1-min(SD,0)
            if z[4]*ICUR + CS*NICUP/Pop < CS*DCAP/Pop and (i==0 or (len(EST[-2]) > n and EST[-2][n][2] + CS*NICUP/Pop > CS*DCAP/Pop)): Flag[i][n] += -i-1+min(SD,0)
                          
            #Died (total, directly, and indirectly) taken from sick (effects hospital use)
            z[9]   = ML(EST, TD, 3, n, False)
            Temp   = (DR * max(0,min(CS*DCAP/Pop, z[4]*ICUR))) + (NDCAP * max(0, z[4]*ICUR - CS*DCAP/Pop))
            z[9]   = ML(z[9], Temp/max(1,sum(z[9])), 0, None, False)
            if sum(z[9])>=1:
                for m,x in enumerate(z[9]): 
                    if len(EST) > m and len(EST[-m]) > n: 
                        EST[-m][n][3] = max(0, EST[-m][n][3] - x)
#                         EST[-m][n][1] = max(0, EST[-m][n][1] - x)
                z[9]   = min(MI(sum(z[9])), SP)
                z[10] += z[9]
            else:
                z[9] = 0
                                
            #Indirect Deaths
            #How to triage?
            z[11]  = min(SP+ML(EST, EID, 7, n)+ML(EST, EID, 15, n), MI(abs(NICU - OICU) * max(0, (CS * NICUP/Pop) - min(max(0,(CS * (DCAP-NICUP)/Pop)- (z[4] * ICUR)), CS * NICUP/Pop))))
            z[12] += z[11]
                                    
            #Adjust sick totals by deaths
#             z[2] += -z[10]                  
            z[4] += -z[10]  
                                
            #Newly Recovered (from sick)
            z[7] = MI(ML(EST, RT, 3, n, False))
            if sum(z[7])>=1:
                for m,x in enumerate(z[7]):
                    if len(EST)>m and len(EST[-m]) > n: 
                        EST[-m][n][3] = max(0, EST[-m][n][3] - x) #To prevent sick to recovered double count
                z[7]  = sum(z[7]) #non integer
                z[8] += max(0, MI(z[7]))
            else:
                z[7]  = 0

            #Recovered but never got sick
            if z[0] > len(MIT):
                z[15] = min(z[2], MI(sum([x[n][1] for x in EST[:-len(MIT)] if len(x)>n])))
                z[16] += MI(NOS*z[15])
                z[3]  += MI((1-NOS)*z[15])
                z[15] = NOS*z[15]
                z[2]  = z[2]- z[15]
                for m,x in enumerate(EST[:-len(MIT)]): 
                    if len(EST[m])>n:
                        EST[m][n][1] = 0 
                        
                #Add to seperate recovered category to prevent double count but keep them as not suspectiable
                
            #Adjust sick by recovered and no symptoms buts still gets sick            
            z[4] = max(0, z[4] - z[7] + MI((1-NOS)*z[15]))
                             
            NEST[n] = z
            
        EST += [NEST]
                
        #Estimate of ICU's in use by same growth model for each "compartment"
        ICU += max(0, (LS(EST[-1],14)/ICU) * max(ML([len(EST[n + 1]) - len(x) for n, x in enumerate(EST[:-1])], MIT), (LS(EST[-1], 14)/MI(ICU))**(2/len(MIT))))
        ICU  = min(Pop/CS, ICU)
        EST[-1] += [EST0] * max(0,(MI(ICU) - len(EST[-1])))
                        
    #Day(0) - only the first one is "real" day, Newly Infected(1), Total Infected(2), Newly Sick (3), Sick(4), Sick - Confirmed (5), Confirmered (6), Recovered (day) (7), Total Recovered (8), Died (9), Direct Deaths (10), Indirect COVID deaths - by day(11), Indirect COVID death total(12), Reproduction Number(13), Growth Rate (14), non sick recoveries (lower suseciptible still) (15 - by day, 16 total)     
    Est = {"Time": [x[0][0] + min(0,SD) for x in EST], 
           I: MI([x+LS(EST, 4, True)[i] for i,x in enumerate(LS(EST, 2, True))]), 
           S: LS(EST, 4, True), 
           D: LS(EST, 10, True), 
           ByDGD: LS(EST, 9, True), 
           R: LS(EST, 8, True), 
           C: LS(EST, 6, True),
           "Sick - Confirmed": LS(EST, 5, True),
           "Reproduction Number": ML([sum([y[13] for y in x]) for x in EST], [1/len(x) for x in EST], 13, None, False), 
           "Growth Rate": ML([sum([y[13] for y in x]) for x in EST], [1/len(x) for x in EST], 14, None, False),
           "Indirect COVID deaths - by day": LS(EST, 11, True),
           "Indirect COVID deaths - Total": LS(EST, 12, True),
           "Total deaths": [x+LS(EST, 12, True)[i] for i,x in enumerate(LS(EST, 10, True))],
           "Total deaths by day": [x+LS(EST, 11, True)[i] for i,x in enumerate(LS(EST, 9, True))],
           "Normal non COVID deaths in same period": MI(len(EST) * Pop * NDMR/1e6),
           "Normal non COVID deaths by day": MI(len(EST)* Pop * NDMR/(365* 1e6)),
           "Health care system over ran dates": Flag, 
           "Compartments": [len(x) for x in EST],
           "No symptoms recovery by day": LS(EST, 15, True),
           "No symptoms recovery total": LS(EST, 16, True),
           "Per million (Pop) Deaths": ML( LS(EST, 10, True), ((1e6)/Pop), None, None, False  )}
    return Est


# In[ ]:


#Plot Data (Class Style)
class GPlot:
    def __init__(self, PData = [], DateLines = [], Legend = [], StartDate = dt(2020,1,22), LOGY = False, LOGX = False, Range = [], YLines = [], FillR = []):
    
        self.Lines         = []
        self.DateLines = DateLines
        self.YLines       = YLines
        self.Range        = Range
        self.PData        = PData
        self.StartDate  = StartDate
        self.Legend      = Legend
        self.FillR           = FillR
    
        plt.style.use("seaborn")
        plt.rcParams['xtick.minor.size'] = 1
        plt.rcParams['xtick.minor.width'] = 1
        plt.rcParams.update({'font.size': SizeSet(8, {"android": 14}) })
        plt.rcParams.update({'font.weight': "bold"})

        self.fig = plt.figure(figsize = SizeSet([.01*.6, .01*.7*.95], {"android": [.01*.6, .01*.6*.95]}), dpi = 100)
        self.fig.clf()
        self.ax  = self.fig.add_subplot(1, 1, 1)
        self.ax.set_xlabel("Day")

        if self.Range != []:
            if self.Range[0] != []: ax.set_xlim(self.Range[0])
            if self.Range[1] != []: ax.set_ylim(self.Range[1])

        LS = ["dashed" if "estimate" in x else "solid" for x in self.Legend]
        
        for i,x in enumerate(self.PData): self.Lines += [self.ax.plot(*x, linewidth = SizeSet(1, {"android": 3},1,False), linestyle = LS[i])]
        MaxY   = max([max(y[1]) for y in self.PData])
        
        #Range filled cases
        if FillR != []: 
            for z in FillR:
                x1 = self.PData[z[0]][0]
                x2 = self.PData[z[1]][0]
                x  = [x for x in x1 if x in x2]
                y1 = self.PData[z[0]][1][x1.index(x[0]):x1.index(x[-1])+1]
                y2 = self.PData[z[1]][1][x2.index(x[0]):x2.index(x[-1])+1]
                self.ax.fill_between(x, y1, y2, where=y1 >= y2, facecolor='blue', interpolate=True, alpha =.4)
                self.ax.fill_between(x, y1, y2, where=y1 <= y2, facecolor='red',  interpolate=True, alpha =.4)
        
        #Add Date Lines
        for x in DateLines: self.ax.plot([Date(x, "num", self.StartDate)] * 2, [1, MaxY]) 
        
        #Add Y Lines
        if self.YLines != []: 
            RangeX = [min([min(y[0]) for y in self.PData]), max([max(y[0]) for y in Data])]
            for x in self.YLines: self.ax.plot(RangeX, [x]*2)

        #Plot Legend
        self.ax.legend(self.Legend + [Date(x, "str", self.StartDate) for x in self.DateLines] + [x for x in self.YLines], fontsize = SizeSet(6, {"android": 14},1 ,False))
        
        #Log scaling
        if LOGX: self.ax.set_yscale("log")
        if LOGY: self.ax.set_yscale("log")

        #Make the graph less overlarge
        plt.tight_layout(pad = 0.25)
        
        #Hover anotation 
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(0,0), textcoords='axes pixels', wrap = True, bbox = dict(boxstyle="round", fc="w"), arrowprops=dict(facecolor='navy', width = .5, headwidth = 5))
        self.annot.set_visible(False)

    #Try except in a list comprehension
    def Catch(self, L, I):
        L, = L
        x,y = L.get_data()
        try:
            D = np.argwhere(x == int(round(I.xdata)))
            if len(D)>0: return abs(y[D[0][0]] - I.ydata)
        except:
            pass
        return max(abs(max(y)- I.ydata), abs(min(y)- I.ydata))
        
    #Hover Annotation - https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib
    def hover(self, event):
        if event.inaxes == self.ax:
            try:
                self.lines = {self.Catch(x, event): i for i,x in enumerate(self.Lines)}
                self.lines = self.lines[min(list(self.lines.keys()))]
                self.line, = self.Lines[self.lines]
                x, y  = self.line.get_data()
                index = np.argwhere(x == int(round(event.xdata)))[0][0]
                self.annot.xy = (x[index], y[index])
                x2,y2 = self.ax.transData.transform((x[index], y[index]))
                text  = "%s\n(%s): %s" % (self.Legend[self.lines], Date(int(x[index]), "custom", self.StartDate, "%m/%d"), str(y[index]))
                self.annot._x = max(min(Settings["Size"][0]*.6*.8, x2), 200) - 200
                self.annot._y = max(0, min(y2, SizeSet(.35, {"android":.3})*.95 - 150)) + 50
                self.annot.set_text(text)
                self.annot.get_bbox_patch().set_alpha(0.4)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
            except:
                pass
        elif self.annot.get_visible():
            self.annot.set_visible(False)
            self.fig.canvas.draw_idle()

#_____ GUI _____
        
#Gives weight to the cells in the grid - for non pixel based spacing
#Needs to be done for every notebook "Page"
def GridMake(TObject, rows = 50, columns = 100, FrameRes = Settings["Size"], FrameRatio = 1):
    for i in range(rows): TObject.rowconfigure(i, weight = 1, minsize = FrameRes[1] * FrameRatio / rows)
    for i in range(columns): TObject.columnconfigure(i, weight = 1, minsize = FrameRes[0] * FrameRatio / columns)        

#Multi OS sizing juggling
def SizeSet(Base = [1, 1, 1, 1], OSFlag = {}, Size = [], MultiplyCheck = True):
    global Settings
    if Size == []: Size = Settings["Size"]
    if Settings["OS"] in OSFlag.keys():
        if not isinstance(OSFlag[Settings["OS"]],list): OSFlag[Settings["OS"]] = [OSFlag[Settings["OS"]]]
        if MultiplyCheck:
            Size = OSFlag[Settings["OS"]][:-len(Size)] + [x if x > 1 else int(round(x * Size[i])) for i,x in enumerate(OSFlag[Settings["OS"]][-len(Size):])]
        else:
            Size = OSFlag[Settings["OS"]]
    else:
        if not isinstance(Base, list): Base = [Base]
        if MultiplyCheck: 
            Size = Base[:-len(Size)] + [x if x > 1 else int(round(x * Size[i])) for i,x in enumerate(Base[-len(Size):])]
        else:
            Size = Base
    
    if len(Size) == 1: Size = Size[0]
    return Size
    
def IndexedCommand(Item = None, Index = None, keyword = None, Master = None):
    global Windows, Settings

    keyword = keyword.replace("__","_") #Error fixing dont know where __ is coming from atm
    
    if keyword == "Location":
        #Current row values
        CV = Item.get()
        WO = Item.WidgetOpt
        if CV[Index[0]][0].lower() == "estimation": 
            #Current widget setup
            WO[Index[0]][1]  = {"type" : "list", "Options" : {}, "State" : "", "ComboList" : Master.TypeOptions + ["Sick - Confirmed", "Growth Rate", "Newly Sick", "Infected", "Total deaths by day", "Total deaths", "Indirect COVID deaths - Total", "Indirect COVID deaths - by day", "Compartments", "No symptoms recovery by day", "No symptoms recovery total", "Per million (Pop) Deaths"]}
            WO[Index[0]][3]  = {"type" : "list", "Options" : {}, "State" : "", "postcommand" : WO[1][3]["postcommand"], "ComboList" : list(Master.Vars.keys()) + ["Modify"]}
            Item.Update(WO, False, False, CV)
        if CV[Index[0]][0].lower() != "estimation":
            WO[Index[0]][0] = Master.BaseTable[1][0]
            Item.Update(WO, False, False, CV)
                
    elif keyword[:7] == "Options":
        CV = Item.get()
        if CV[Index[0]][-1].lower() == "modify":
            NewN = [x[0] for x in CV if x[0] in Master.Vars.keys()]
            if NewN ==[]: 
                NewN = [list(Master.Vars.keys())[0]]
#                 NewN = ["CUSTOM %d" % (len(Master.Vars.keys())+1)]
            VarSet = [[x, str(Master.Vars[NewN[0]][x])] for x in sorted(Master.Vars[NewN[0]].keys())]
            CV[Index[0]][-1] = NewN[0]
            Windows += [PopUp("Modify Variables:", [[{"type" : "label", "Options" : {"text" : "Name:"}}, {"type" : "list", "State" : CV[Index[0]][-1], "postcommand": "VarName_%s_%d" % (keyword.split("_")[1], Index[0]), "ComboList" : Master.Vars.keys()}], [{"type" : "label", "Options" : {"text" : "Save"}}, {"type" : "button", "command" : "SaveVar_%s_%d" % (keyword.split("_")[1], Index[0]), "Options" : {"text" : "Save"}, "columnspan": 2}], [{"type" : "label", "Options" : {"text" : "Variable"}}, {"type" : "label", "Options" : {"text" : "Current Value"}}]] + [[{"type" : "label", "Options" : {"text" : x[0], "font": Master.FONT, "wraplength" : SizeSet(200*.9 ,{"android":.4*.9})}}, {"type" : "entry", "State" : x[1]}] for x in VarSet] + [[{"type" : "button", "command" : "Special_%s" % (keyword.split("_")[1]), "Options" : {"text" : "Range Fill"}, "columnspan": 1}, {"type" : "entry", "State" : "[[]]"}]], SizeSet([2, min(len(VarSet)+ 3,15), 400, 600] ,{"android":[2, min(len(VarSet)+ 3, 7), .4, .88]}), [0,0,0,0], True, True, Master = Master)]
        if CV[Index[0]][-1].lower() == "estimation" or CV[Index[0]][0].lower() == "estimation":
            WO = Item.WidgetOpt
            CV[Index[0]][0] = "Estimation"
            #Current widget setup
            WO[Index[0]][1]  = {"type" : "list", "Options" : {}, "State" : "", "ComboList" : Master.TypeOptions + ["Sick - Confirmed", "Growth Rate", "Newly Sick", "Infected", "Total deaths by day", "Total deaths", "Indirect COVID deaths - Total", "Indirect COVID deaths - by day", "Compartments", "No symptoms recovery by day", "No symptoms recovery total", "Per million (Pop) Deaths"]}
            NewN = [x[0] for x in CV if x[0] in Master.Vars.keys()]
            if NewN ==[]: NewN = [list(Master.Vars.keys())[0]]
            WO[Index[0]][3]  = {"type" : "list", "Options" : {}, "State" : NewN[0], "postcommand" : WO[1][3]["postcommand"], "ComboList" : list(Master.Vars.keys()) + ["Modify"]}
            Item.Update(WO, False, False, CV)
        else:
            WO = Item.WidgetOpt
#             CV[Index[0]][0] = "Estimation"
            #Current widget setup
            WO[Index[0]][1]  = {"type" : "list", "Options" : {}, "State" : "", "ComboList" : Master.TypeOptions}
            WO[Index[0]][3]  = {"type" : "list", "Options" : {}, "State" : "", "postcommand" : WO[1][3]["postcommand"], "ComboList" : Master.DefOptions}
            Item.Update(WO, False, False, CV)
            
    elif keyword[:7] == "VarName":
        CV   = Item.get()
        Name = CV[0][1]
        if Name != "Modify":
            if Name in Master.Vars.keys(): 
                CV = CV[:3] + [[str(x), str(Master.Vars[Name][x])] for x in sorted(Master.Vars[Name].keys())] + [CV[-1]]        
                Item.Update(Item.WidgetOpt, False, False, CV)
                
            CV = Master.PageW[int(keyword.split("_")[1])]["MainTable"].get()
            CV[int(keyword.split("_")[2])][-1] = Name
            Master.PageW[int(keyword.split("_")[1])]["MainTable"].Update(Master.PageW[int(keyword.split("_")[1])]["MainTable"].WidgetOpt, False, False, CV)
            
    elif keyword[:7] == "SaveVar":
        CV = Item.get()
        Master.Vars.update({CV[0][1]: {x[0]: ast.literal_eval(x[1]) for x in CV[3:-1]}})
        Master.Save()
        Master.CreateGraph(Master.PageW[int(keyword.split("_")[1])]["MainTable"], int(keyword.split("_")[1]))
        Item.focus_set()
        
#********************************************************************************************************
    elif keyword[:7] == "Special":
        #Range Graphs etc. 
        CV = Item.get()
        Master.Save()
        Master.GraphOpt[int(keyword.split("_")[1])].update({"FilledGraph": ast.literal_eval(CV[-1][1])})
        Master.CreateGraph(Master.PageW[int(keyword.split("_")[1])]["MainTable"], int(keyword.split("_")[1]))
        Item.focus_set()
        
            #Add YLines - change from settings to individual Opt group
#            "Normal non COVID deaths in same period": len(Est)* pop * NDMR/1e6,
#            "Normal non COVID deaths by day": len(Est)* pop * NDMR/(365* 1e6)}
            
    elif keyword == "Help":
        #Add Help file and window/tab**************************
        topic = Item.get()
        if topic[0][1].lower() in [x.lower() for x in HelpFile.keys()]:
            Item.Update(index.WidgetOpt, False, False, [topic[0]] + [[HelpFile[topic]]])
#********************************************************************************************************

#__________________________________________________________________________________________________
#Custom Classes (Except for PopUp)

#Modified from: https://stackoverflow.com/questions/47839813/python-tkinter-autocomplete-combobox-with-like-search
class AutocompleteCombobox(ttk.Combobox):
    
    def onselect(self, evt):
        if "ID" not in self.__dict__.keys():
            self.set_links(None)
        #Note here that Tkinter passes an event object to onselect()
        IndexedCommand(self.ID, self.Index, self.Keyword, self.Master)

    #Only used in setup
    def set_links(self, ID, Index = [], Keyword = None, Master = None):
        self.ID      = ID
        self.Index   = Index
        self.Keyword = Keyword
        self.Master  = Master
        self.bind('<<ComboboxSelected>>', self.onselect)

    #Only used in setup
    def set_completion_list(self, completion_list):
        #Use completion list as drop down selection menu, arrows move through menu.
        self._completion_list = sorted(completion_list, key = str.lower) #Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  #Setup our popup menu

    #This is the intermediate and where secondary actions can take place
    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        if delta: #Need to delete selection otherwise we would fix the current position
                self.delete(self.position, Tkinter.END)
        else: #Set position to end so selection starts where textentry ended
                self.position = len(self.get())
        #Collect hits
        _hits = []
        for element in self._completion_list:
                if element.lower().startswith(self.get().lower()): #Match case insensitively
                        _hits.append(element)
        #If we have a new hit list, keep this in mind
        if _hits != self._hits:
                self._hit_index = 0
                self._hits=_hits
        #Only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
                self._hit_index = (self._hit_index + delta) % len(self._hits)
        #Perform the auto completion
        if self._hits:
                self.delete(0, END)
                self.insert(0, self._hits[self._hit_index])
                self.select_range(self.position, END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
                self.delete(self.index(INSERT), END)
                self.position = self.index(END)
        if event.keysym == "Left":
                if self.position < self.index(END): # Delete the selection
                        self.delete(self.position, END)
                else:
                        self.position = self.position-1 # Delete one character
                        self.delete(self.position, END)
        if event.keysym == "Right":
                self.position = self.index(END) # Go to end (no selection)
        if len(event.keysym) == 1:
                self.autocomplete()

        # No need for up/down, we'll jump to the popup
        # list at the position of the autocompletion
        self.onselect(event)
                
#Excel like multi type table input with interconnects
#Add Row and Coloumn now just comes from Update command which either appends to self.WidgetOpts and overwrites it. Remove and Reset and Clear are also all similarly controlled.
class MultiTableInput(ttk.Frame):
    
    def __init__(self, parent, WidgetIndex = [[{}]], Size = [1, 1, 200, 100], Pad = [0, 0, 0, 0], AdjSize = True, YScroll = False, XScroll = False, Master = None):
        
        #Scroll bar size adjustment
        self.SX = 0
        self.SY = 0
        if YScroll: self.SY = SizeSet(15, {'android' : 50}) #shortens X
        if XScroll: self.SX = SizeSet(15, {'android' : 50}) #Shortens Y
        
        self.Size = SizeSet(Size, {}, Size)  #Overall size (set) - [columnspan, rowspan % px X, % px Y]
            
        #Main Frame
        Frame.__init__(self, parent, borderwidth = 0, highlightthickness = 0)
        self.grid_columnconfigure(0, weight = 100, minsize = self.Size[2] - self.SY)
        self.grid_rowconfigure(0, weight = 100, minsize = self.Size[3] - self.SX)
        self.grid_columnconfigure(1, weight = 1, minsize = self.SY)
        self.grid_rowconfigure(1, weight = 1, minsize = self.SX)
        self.grid_propagate(False)
    
        #Canvas (scrollable) for main frame
        self.Canvas = Canvas(self, borderwidth = 0, highlightthickness = 0)
        self.Canvas.grid(row = 0, column = 0, sticky = "NSWE")
        self.Canvas.grid_columnconfigure(0, weight = 100)
        self.Canvas.grid_rowconfigure(0, weight = 100)
        self.Canvas.config(width  = (self.Size[2] - self.SY), 
                           height = (self.Size[3] - self.SX))
        self.Canvas.grid_propagate(False)
        
        #Widget holding frame for canvas - can be bigger than canvas (and thus scrollable)
        self.Canvas.X = Frame(self.Canvas, borderwidth = 0, highlightthickness = 0)
        self.Canvas.create_window((0, 0), window = self.Canvas.X, anchor = 'nw')
        self.Canvas.X.grid_propagate(False)
        
        self._Widgets     = {}
        self._LabelVars   = {}
        
        self.WidgetOpt  = WidgetIndex    #List of lists of dicts by type (rows and columns comes from this)        
        self.Pad        = Pad  + [0] * min((4 - len(Pad)), 0)  #Default Paddings - [padx, pady, ipadx, ipady]
        
        #Register a command to use for validation - will be in Widget Index
        ValidateE = "key"
        self.vcmd = (self.register(self._validate), "%P")
        self.ValidateE = ValidateE
        
        self.WidgetDefaults = {'type' : "Entry", 
                               'entry' : {"Options" : {'justify' : 'center'}}, 
                               'list' : {"Options" : {}},
                               'label' : {"Options" : {"justify" : "left", "borderwidth" : 0, "highlightthickness" : 0}},
                               'button' : {"Options" : {"text" : "BUTTON", "justify" : "center"}}}

        self.AdjSize = AdjSize #AdjSize - General Options
        
        self.Master = Master
        
        self.CreateTable()
    
    def _validate(self, P):
        #Perform input validation. 
        #Allow only an empty value, or a value that can be converted to a float
        if P.strip() == "":
            return True
        try:
            f = float(P)
        except ValueError:
            self.bell()
            return False
        return True
    
    def AdjustSizing(self, MaxColumns = 1, MaxRows = 1):
        
        self.MaxRows      = max(self.Size[1], MaxRows)
        self.MaxColumns   = max(self.Size[0], MaxColumns)
        self.MaxRows_b    = max(len(self.WidgetOpt), self.MaxRows)
        self.MaxColumns_b = max(max([len(x) for x in self.WidgetOpt] +[0]), self.MaxColumns)
            
        if self.SY != 0: self.MaxRows    = self.MaxRows_b
        if self.SX != 0: self.MaxColumns = self.MaxColumns_b
        
        SW = int(np.floor((self.Size[2] - self.SY) / self.Size[0]))
        SH = int(np.floor((self.Size[3] - self.SX) / self.Size[1]))
        
        self.Canvas.X.config(width  = (SW * self.MaxColumns), height = (SH * self.MaxRows)) 
            
        #Adjust column weights so they all expand equally 
        for column in range(self.MaxColumns_b):
            self.Canvas.X.grid_columnconfigure(column, weight = 1, minsize = SW)
#             self.Canvas.X.grid_columnconfigure(column, weight = 1) #Works on current number of columns rather then set size 
        self.Canvas.X.grid_columnconfigure(self.MaxColumns_b, weight = 0, minsize = 0)
        
#         #Added to keep rows on top part of grid
        for row in range(self.MaxRows_b):
            self.Canvas.X.grid_rowconfigure(row, weight = 1, minsize = SH)
#             self.Canvas.X.grid_rowconfigure(row, weight = 1) #Works on current number of rows rather then set size 
        self.Canvas.X.grid_rowconfigure(self.MaxRows_b, weight = 0, minsize = 0)
        self.Canvas.X.grid_rowconfigure(self.MaxRows_b + 1, weight = 0, minsize = 0)

        self.Canvas.X.update() #tk.update() needed to read width and height etc. (Tk -> widget)  

        #Activated y scroll (can be similarly done for x scroll)
        if self.SY > 0 and self.Canvas.X.winfo_height() > SH*self.Size[1]:
            self.ScrollY = Scrollbar(self, orient = VERTICAL)        
            self.ScrollY.grid(row = 0, column = 1, sticky = "NSEW")
            self.ScrollY.config(command = self.Canvas.yview)
            self.Canvas.config(yscrollcommand = self.ScrollY.set)
            self.Canvas.config(scrollregion = self.Canvas.bbox("all"))
        elif "ScrollY" in self.__dict__.keys():
            self.ScrollY.destroy()
            
        if self.SX > 0 and self.Canvas.X.winfo_width() > SW*self.Size[0]:
            self.ScrollX = Scrollbar(self, orient = HORIZONTAL)        
            self.ScrollX.grid(row = 1, column = 0, sticky = "NSEW")
            self.ScrollX.config(command = self.Canvas.xview)
            self.Canvas.config(xscrollcommand = self.ScrollX.set)
            self.Canvas.config(scrollregion = self.Canvas.bbox("all"))
        elif "ScrollX" in self.__dict__.keys():
            self.ScrollX.destroy()
        
    # Create the table of widgets
    def CreateTable(self):
        
        #Always clear and create to keep memory leakage down
        if self._Widgets != {}:
            for key in self._Widgets.keys():
                self._Widgets[key].destroy()
            del self._Widgets#[key]   #Not needed if dictionary is recreated as below
        if self._LabelVars != {}:
            Keys = [x for x in self._LabelVars.keys()]
            for key in Keys:
                del self._LabelVars[key]
        
        self._Widgets   = {}
        self._LabelVars = {}
        self._ButtonID  = {}
        
        for row in range(len(self.WidgetOpt)):
            for column in range(len(self.WidgetOpt[row])):
                index  = (row, column)
                Widget = self.WidgetOpt[row][column]
                
                #Set/Checks Defaults
                if 'type' not in [x.lower() for x in Widget.keys()]: 
                    Widget.update({'type' : self.WidgetDefaults['type']})
                if 'options' not in [x.lower() for x in Widget.keys()]: 
                    Widget.update({'Options' : self.WidgetDefaults[Widget['type'].lower()]['Options']})
                
                for key in self.WidgetDefaults[Widget['type'].lower()]["Options"].keys(): 
                    if key.lower() not in Widget["Options"].keys():
                        Widget["Options"].update({key : self.WidgetDefaults[Widget['type'].lower()]["Options"][key]})
                
                if Widget['type'].lower() == "entry":
                    w = Entry(self.Canvas.X, **Widget["Options"])
                    if "State" in Widget.keys():
                        w.delete(0, END)
                        w.insert(0, Widget["State"])
                    
                elif Widget['type'].lower() == "list":
                    w = AutocompleteCombobox(self.Canvas.X)
                    
                    #Set individual indexed commands
                    if "postcommand" in Widget.keys():                     
                        w.set_links(self, index, Widget["postcommand"], self.Master)
                    if "State" in Widget.keys():
                        w.delete(0, END)
                        w.insert(0, Widget["State"])
                    if "ComboList" in Widget.keys(): 
                        w.set_completion_list(Widget["ComboList"])
                        
                elif Widget['type'].lower() == "label":
                    if "textvariable" in Widget.keys():
                        templabel = StringVar()
                        templabel.set(Widget["textvariable"])
                        self._LabelVars[index] = templabel
                        Widget["Options"].update({"textvariable": templabel})
                    w = Label(self.Canvas.X, **Widget["Options"])
                    
                elif Widget['type'].lower() == "button":                    
                    if "command" in Widget.keys(): 
                        w = Button(self.Canvas.X, **Widget["Options"])
                        w.config(command = lambda I = index, K = Widget["command"]: IndexedCommand(self, I, K, self.Master))                            
                    else:
                        w = Button(self.Canvas.X, **Widget["Options"]) #A do nothing button - can be configured later
                    
                else:
                    w = Entry(self.Canvas.X, **self.WidgetDefaults["entry"]["Options"])
                
                if ("columnspan" not in Widget.keys() or Widget["columnspan"] != 0) and ("rowspan" not in Widget.keys() or Widget["rowspan"] != 0):
                    w.grid(row = row, column = column, padx = self.Pad[0], pady = self.Pad[1], 
                           ipadx = self.Pad[2], ipady = self.Pad[3], sticky = "NSWE", 
                           rowspan = ([Widget[x] for x in Widget.keys() if x.lower() == "rowspan"]+[1])[0],
                           columnspan = ([Widget[x] for x in Widget.keys() if x.lower() == "columnspan"]+[1])[0] )

                self._Widgets[index] = w
                #Update original just in case
                self.WidgetOpt[row][column] = Widget
        
        if self.AdjSize: self.AdjustSizing() #Scrollable checks only work after 
                
    def get(self, Index = None):
        #Return a list of lists, containing the data in the table'
        if Index == None :
            rows    = range(len(self.WidgetOpt))
            columns = [len(x) for x in self.WidgetOpt]
        elif len(Index) == 1:
            rows    = [Index[0]]
            columns = [len(self.WidgetOpt[x]) for x in rows]
        else:
            rows    = [Index[0]]
            columns = [Index[1]]
                
        result = []
        for i,row in enumerate(rows):
            current_row = []
            for column in range(columns[i]):
                index = (row, column)
                if self.WidgetOpt[row][column]["type"].lower() == "list" or self.WidgetOpt[row][column]["type"].lower() == "entry":
                    current_row.append(self._Widgets[index].get()) 
                elif self.WidgetOpt[row][column]["type"].lower() == "label" and "textvariable" in self.WidgetOpt[row][column].keys():
                    current_row.append(self._LabelVars[index].get())
                elif "text" in self.WidgetOpt[row][column]["Options"].keys():
                    current_row.append(self.WidgetOpt[row][column]["Options"]["text"])                    
                else:
                    current_row.append("")
            result.append(current_row)
        return result
    
    #Can possibly be recondensed with correct Reset settings...
    def Update(self, New, Append = True, Clear = False, AltFill = []):
        if not Clear and AltFill == []: Current = self.get()
        
        if Append:
            self.WidgetOpt += [New]
        else:
            self.WidgetOpt =  New
        
        self.CreateTable()
        if not Clear and AltFill == []: 
            self.FillData([[y for n,y in x in n < len(self.WidgetOpt[i])] for i,x in enumerate(Current) if i < len(self.WidgetOpt)])
        elif not Clear and AltFill != []: 
            self.FillData(AltFill)
        else:
            self.FillData(AltFill, True)
            
        if self.AdjSize: self.AdjustSizing()
    
    def FillData(self, Values, Clear = False):
        if Clear:
            for x,row in enumerate(self.WidgetOpt):
                for y,w in enumerate(self.WidgetOpt[x]):
                    index = (x, y)
                    if w["type"].lower() == "entry" or self.WidgetOpt[x][y]["type"].lower() == "list":
                        self._Widgets[index].delete(0, END)
                        if "State" in w.keys(): self._Widgets[index].insert(0, w["State"])
                    elif w["type"].lower() == "label" and "textvariable" in w.keys():
                        self._LabelVars[index].set(w["textvariable"])
                    elif w["type"].lower() == "button":
                        self._Widgets[index].config(text = w["Options"]["text"])
        if Values !=[]:
            #If a change is desired a .get() should be preformed followed by edit then resend
            for x,row in enumerate(Values):
                for y,value in enumerate(row):
                    index = (x, y)
                    if len(self.WidgetOpt) >= x and len(self.WidgetOpt[x]) >= y and value != "":
                        if self.WidgetOpt[x][y]["type"].lower() == "entry":
                            self._Widgets[index].delete(0, END)                
                            self._Widgets[index].insert(0, value)
                        elif self.WidgetOpt[x][y]["type"].lower() == "list":
                            self._Widgets[index].set(value)
                        elif self.WidgetOpt[x][y]["type"].lower() == "label" and "textvariable" in self.WidgetOpt[x][y].keys():
                            self._LabelVars[index].set(value)
                        elif self.WidgetOpt[x][y]["type"].lower() == "button":
                            self._Widgets[index].config(text = value)

class CustomNotebook(ttk.Notebook):
    #A ttk Notebook with close buttons on each tab
    #Modifed from: https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close-buttons-to-tabs-in-tkinter-ttk-notebook
    __initialized = False
    
    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            CustomNotebook.__initialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)
        self.bind("<Enter>", self.MEnter)
        self.bind("<Leave>", self.MLeave)
       
    def SetState(self, event):
        if ":" in self.tab(event.widget, "text"):
            self.state(['!invalid'])
        else:
            self.state(['invalid'])
            
    def Toggle(self, index):
        for x in self.tabs(): 
            if self.index(x) == index:
                self.tab(self.index(x), state= "normal")
            else:
                self.tab(self.index(x), state="disabled")
        
    def MEnter(self, event):
        self.bind("<Motion>", self.Mouse)
        self.Mouse(event)
        
    def Mouse(self, event):
        try:
            index = self.index("@%d,%d" % (event.x, event.y))
            if ":" in self.tab(index, "text") and self.index(self.select()) == index:
                self.state(['!invalid'])
            else:
                self.state(['invalid'])
            return index
        except:
            self.state(['invalid'])
            return None
                
    def MLeave(self, event):
        self.state(['invalid'])
        self.unbind("<Motion>")

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""
        TM = self.Mouse(event)
        if TM != None: self.Toggle(TM)
        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))
        
        if "close" in element and self._active == index and ":" in self.tab(index, "text"):
        #Greater than 1 is added to prevent closure of Add and Main Tabs
            self.tab(max(index-1, 0), state = "normal")
            self.select(max(index-1, 0)) #Jump back not forward 
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")
            
        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        
        #No image unless hovering over it
        
        self.images = (
        
           PhotoImage("img_close", data='''''' , height = SizeSet(100, {"windows":20, "others": 20}) , width = 10),#SizeSet(1, {"windows":1, "others": 1})),
           
           PhotoImage("img_close2", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                ''' , height = SizeSet(10, {"windows": 1, "others": 1}) , width = SizeSet(10, {"windows": 1, "others": 1})),

            PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                ''', height = SizeSet(100, {"windows":20, "others": 20}) , width = SizeSet(5, {"windows":20, "others": 20})),
            
            PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''', height = SizeSet(100, {"windows":20, "others": 20}) , width = SizeSet(80, {"windows":20, "others": 20})),
        )
                
        style.element_create("close", "image", "img_close",
                            ("!invalid", "!disabled", "img_close2"),
                            ("!invalid", "active",  "!disabled", "img_closeactive"),
                            ("!invalid", "pressed", "!disabled", "img_closepressed"), sticky = "NSWE" )
        
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe", 
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top", 
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top", 
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])

#Main Window
class MainGUI:
    global Settings
    def __init__(self, master, Data = {}, PL = [], SL = [], TypeOptions = [C, S, R, D, ByDGD], Vars = {}, Tables = []):
        self.Master = master #Reference point for outside buttons to use for commands like self.Master.destroy()
        
        self.PL          = PL
        self.SL          = SL
        self.Data        = Data
        self.TypeOptions = TypeOptions
        self.DefOptions  = ["Estimation"]
        self.Res         = SizeSet([1, .95], {"android": [1,.9]}, Settings["Size"])
         
        self.GridRows    = 50
        self.GridColumns = 100
 
        #Main window grid
        GridMake(master, self.GridRows, self.GridColumns, self.Res)
        
        #Defines and places the notebook widget
        self.nb = CustomNotebook(master)
        self.nb.grid(row = 0, column = 0, columnspan = self.GridColumns, rowspan = self.GridRows, sticky = 'NESW')
        
        master.focus_set()
        
        #Defualt Fonts - For use if word length and word wrapping need to be set
        #tkFont.Font(font='TkDefaultFont').configure()
        self.FONT = tkFont.Font(family = 'DejaVu Sans', weight = 'normal', slant = 'roman', overstrike = 0, underline = 0, size = -SizeSet(18, {"windows": 9}))
	    
        self.Pages = []
        self.PageW = {}
        self.GraphOpt = {}

        #Main Table Input
        self.BaseTable  = [[{"type" : "label", "Options" : {"text" : "Location"}}, 
                           {"type" : "label", "Options" : {"text" : "Type"}}, 
                           {"type" : "label", "Options" : {"text" : "Days"}},
                           {"type" : "label", "Options" : {"text" : "Options"}}], 
                          [{"type" : "list", "Options" : {}, "State" : "", "postcommand" : "Location", "ComboList" : self.PL + self.SL + ["Estimation"]},
                           {"type" : "list", "Options" : {}, "State" : "", "ComboList" : self.TypeOptions},
                           {"type" : "entry", "Options" : {}},
                           {"type" : "list", "Options" : {}, "State" : "", "postcommand" : "Options_", "ComboList" : self.DefOptions, "TAG": True}]]

        self.Vars = Vars
        
        self.BaseCS = {"type":"label", "textvariable":"Waiting for input...", "Options" : {"borderwidth" :2, "font" : self.FONT, "wraplength" : SizeSet(.55, {"android": .52}, 1,  False) * self.Res[0]}}

        if Tables != []:
            #Add Main Page: !frame
            self.AddPage(True, Load = Tables[0])

            #New Page Adder
            self.ADD = self.AddPage(True, "+")
            
            for i,x in enumerate(Tables.keys()):
                if i>1: self.AddPage(Load = Tables[x])
        else:
            self.AddPage(True)
            self.ADD = self.AddPage(True, "+")
        
        self.nb.tab(self.nb.index(self.ADD), state="disabled")
        
        #Binding for detection of changes to add or delete
        self.nb.bind("<<NotebookTabChanged>>", self.NDCheck)
        self.nb.enable_traversal()
    #________________________________________Sub Class Functions
    
    def NDCheck(self, evt):
        #Checks if "+" is pressed
        try:
            if self.nb.tab(self.nb.index(self.nb.select()), "text") == "+": 
                self.nb.tab(self.nb.index(self.ADD), state = "disabled")
                NP = self.AddPage(False)
                self.nb.tab(self.nb.index(NP), state = "normal")
                self.nb.select(self.nb.index(NP))
        except:
            pass
            
    def AddPage(self, Initial = False, Name = " Main ", Load = None):
        #Adds tab to the notebook 
        
        Ref = len(self.Pages)
        self.Pages += [Frame(self.nb)]
        self.PageW.update({Ref:{}})
        
        if not Initial: 
            Name = " P: %d   " % Ref
            self.nb.insert(self.ADD, self.Pages[Ref], text = Name)
            self.nb.tab(Ref-1, state="disabled")
        else:
            self.nb.add(self.Pages[Ref], text = Name)
        self.Pages[Ref].bind("<Visibility>", self.nb.SetState)
         
        #Add grid to page
        GridMake(self.Pages[Ref], self.GridRows, self.GridColumns, self.Res, (self.GridRows-1)/self.GridRows)
        
        #Current Status (Bottom)
        self.PageW[Ref].update({"CS": MultiTableInput(self.Pages[Ref], [[self.BaseCS]], SizeSet([1,1,.6,.1], {"android": [1,1,.6,.15]}, self.Res), [0.1, 0.1, 0, 0], True, True, Master = self)})
        self.PageW[Ref]["CS"].grid(row = SizeSet(40, {"android": 35}), column = 0, rowspan = SizeSet(10,{"android":15}), columnspan = 60, sticky = 'NSEW')
        self.PageW[Ref]["CS"].Update([[self.BaseCS]],False,False,[["Waiting for input..."]])
        
        #Main Table_______________________________________________________________________________________
        self.PageW[Ref].update({"MainTable": MultiTableInput(self.Pages[Ref], self.Tag(self.BaseTable, Ref), SizeSet([4, 20, .4, .82], {"android": [4, 9,.4,.82]}, self.Res), [0.2, 0.2, 0, 0], True, True, Master = self)})
        self.PageW[Ref]["MainTable"].grid(row = 5, column = 60, rowspan = 41, columnspan = 40, sticky = 'NEWS')
        
        #Graph Button
        self.PageW[Ref].update({"GButton" : Button(self.Pages[Ref], text = "Graph", command = lambda: self.CreateGraph(self.PageW[Ref]["MainTable"], Ref))})
        self.PageW[Ref]["GButton"].grid(row = 0, column = 80 , rowspan = 5, columnspan = 20, sticky = 'NEWS')
        
        #Add Row Button
        self.PageW[Ref].update({"ARButton" : Button(self.Pages[Ref], text = "+", width = 3, command = lambda: self.MainTableAddRow(self.PageW[Ref]["MainTable"], self.BaseTable))}) 
        self.PageW[Ref]["ARButton"].grid(row = 46, column = 60 , rowspan = 4, columnspan = 4, sticky = 'NEWS')
        
        #Remove Row Button
        self.PageW[Ref].update({"RRButton" : Button(self.Pages[Ref], text = "-", width = 3, command = lambda: self.MainTableRemoveRow(self.PageW[Ref]["MainTable"], self.BaseTable))}) 
        self.PageW[Ref]["RRButton"].grid(row = 46, column = 64 , rowspan = 4, columnspan = 4, sticky = 'NEWS')
        
        #Reset All Button
        #self.PageW[Ref].update({"RRButton" : Button(self.Pages[Ref], text = "Reset", width = 10, command = lambda: self.PageW[Ref]["MainTable"].Update(self.BaseTable , False, True))})
        #self.PageW[Ref]["RRButton"].grid(row = 44, column = 65 , rowspan = 3, columnspan = 34, sticky = 'NEWS')
        
        #Preview Frame_______________________________________________________________
        self.PageW[Ref].update({"PreviewFrame" : Label(self.Pages[Ref], text = "<>")})
        self.PageW[Ref]["PreviewFrame"].grid(row = 5, column = 0, rowspan = SizeSet(35,{"android":30}), columnspan = 60, sticky= "NSWE")
        
        #Retrieve Data
        self.PageW[Ref].update({"RDButton" : Button(self.Pages[Ref], text = "Retrieve Data", command = lambda: self.GetData())})
        self.PageW[Ref]["RDButton"].grid(row = 0, column = 0 , rowspan = 5, columnspan = 20, sticky = 'NEWS')
        
        #Log Y
        self.PageW[Ref].update({"LogYButton" : Button(self.Pages[Ref], text = "Toggle Log Y Axis", command = lambda: self.Toggle(self.GraphOpt[Ref],"LOGY",self.PageW[Ref]["MainTable"], Ref))})
        self.PageW[Ref]["LogYButton"].grid(row = 0, column = 20 , rowspan = 5, columnspan = 20, sticky = 'NEWS')
        
        #Set all 0
        self.PageW[Ref].update({"ZeroButton" : Button(self.Pages[Ref], text = "Set to common x = 0", command = lambda: self.Toggle(self.GraphOpt[Ref],"ZeroX",self.PageW[Ref]["MainTable"], Ref))})
        self.PageW[Ref]["ZeroButton"].grid(row = 0, column = 40 , rowspan = 5, columnspan = 20, sticky = 'NEWS')
        
        #Save Graph
        self.PageW[Ref].update({"SaveGraphButton" : Button(self.Pages[Ref], text = "Save Graph", command = lambda: self.SaveGraph(self.PageW[Ref]["MainTable"], Ref))})
        self.PageW[Ref]["SaveGraphButton"].grid(row = 0, column = 60 , rowspan = 5, columnspan = 20, sticky = 'NEWS')
        
        self.GraphOpt.update({Ref: {"LOGY": False, "ZeroX" : False, "Save" : None, "FilledGraph" : [], "DateLines":["1/22/20", dt.now()]}})
        Settings.update({Ref:[]})
        
        if Load != None: self.PageW[Ref]["MainTable"].Update(self.Tag(Load[0], Ref, True), False, False, Load[1])
        
        return self.Pages[Ref]
        
    #Tags post commands for multitables
    def Tag(self, Addons, Tag = 0, ClearOld = False):
        Tag = str(Tag)
        if ClearOld:
            Addons = [[y if i!=3 else {z: y[z] if not isinstance(y[z], str) or len(y[z])<1 or "_" not in y[z] else "%s_%s" % (y[z].split("_")[0], Tag) for z in y.keys()} for i,y in enumerate(x)] for x in Addons]
        else:
            Addons = [[y if "TAG" not in y.keys() else {z: y[z] if not isinstance(y[z], str) or len(y[z])<1 or y[z][-1] != "_" else "%s%s" % (y[z], Tag) for z in y.keys()} for y in x] for x in Addons]       
        return Addons
    
    def Toggle(self, D, Key, Graph = None, Ref = None, A = True, B = False):
        if D[Key] == A: 
            D.update({Key:B})
        else:
            D.update({Key:A})
        if Graph!= None and Ref!= None: self.CreateGraph(Graph, Ref)
        return D
        
    def SaveGraph(self, Table, Ref, Type = "png"):
        self.PageW[Ref]["Data"]["Plot"].savefig("COVID - %d.%s" % (Ref, Type), format = Type)
        with open("COVID (EST) - %d.txt" % (Ref),  "w") as OF: OF.write("\n\n\n".join(self.PageW[Ref]["Data"]["Print"]))

    def PrintKey(self, Place, Vs, Vs2):
        P0  = [C,D,S,ByDGD,I,"Indirect COVID deaths - Total","Total deaths","Normal non COVID deaths in same period","Normal non COVID deaths by day", "Per million (Pop) Deaths"]
        P1 = {i:Vs2[x] for i,x in enumerate(P0)}
        
        #"Health care system overrun # of sick"
        #"Average time to detection"
        
        PrintKeyS = f"%s population %s (Est): Started on %s with R0 = %s and social distancing effects on: %s | Avg time of - Transmission: %s, Incubation: %s, Death: %s, Recovery: %s, Effective Immunity: %s | Totals - Confirmed: {P1[0]:,}, Direct Deaths: {P1[1]:,}, Indirect Deaths: {P1[5]:,}, Total COVID deaths: {P1[6]:,} | Max - Deaths in 1 day: {P1[3]:,}, Deaths (direct) per million: {P1[9]}, Sick at once: {P1[2]:,}, Mortality Rate: %s/%s, Normal deaths in same period/per day: {P1[7]:,}/{P1[8]:,}\n" % (Place, "{:,}".format(Vs["Population"]), Date(Vs["Start Date"],"custom",Custom = "%m/%d/%Y"), "{:.2f}".format(Vs["Growth Rate"]), " ".join([":".join([Date(x,"custom",Custom = "%m/%d"),"{:.2f}".format(1/Vs["Social Distancing - Change"][i])]) for i,x in enumerate(Vs["Social Distancing - Change Dates"])]), "{:.2f}".format(Vs["Mean Infection Time"]), "{:.2f}".format(Vs["Average infected to symptoms"]), "{:.2f}".format(Vs["Average time to death"]), "{:.2f}".format(Vs["Average time to recovery"]), "{:.2f}".format(Vs["Average Effective Immunity Duraration"]), "{:.2f}".format(Vs["Death Rate"]), "{:.2f}".format(Vs["Death Rate - Health care system overran"]))

        return PrintKeyS
            
    #Send to Graph Creator
    def CreateGraph(self, Table, Ref, Defaults = []):
        Opt = self.GraphOpt[Ref]
        
        #Update from table specific saved settings (tied to Ref) *****************************
        Defaults = [T, C, len(self.Data[P]["US"][C]), ""]#"Base"]
        
        SubData = Table.get()[1:]
        SubData = [[y if y != '' else Defaults[i] if i != 3 or x[0].lower() != "estimation" else "" for i,y in enumerate(x)] for x in SubData]
        
#         Table.Update(Table.WidgetOpt, False, False, [[""]*4] + SubData) #Causes more problems then it helps
        
        #Reduces multi runs by having the repeated parts reduced times and options all start at the same part
        ESTx = {}
        ESTs = {i: [x[3], int(x[2])] for i,x in enumerate(SubData) if x[0].lower() == "estimation"}
        for x in ESTs.keys(): 
            if ESTs[x][0] not in ESTx.keys() or (ESTs[x][0] in ESTx.keys() and ESTx[ESTs[x][0]] < ESTs[x][1]): 
                ESTx.update({ESTs[x][0]: ESTs[x][1]})
        ESTx = {x: Extrapolate(self.Vars[x], ESTx[x]) for x in ESTx.keys()}
        #Estimation Data
        ESTs = {}
        for x in ESTx.keys():
            ESTs.update({x: {y:max(ESTx[x][y]) if isinstance(ESTx[x][y], list) and ESTx[x][y] != [] else ESTx[x][y] for y in ESTx[x].keys()}})
        
        if Opt["ZeroX"] == True:
            Lim0 = 10 #10 seems to aim a bit low for non uncontrolled growth - make adjustable************ - changed to death instead of confirmed (this does not change estimation as well though - should have an additional factor for confirmed vs. death time and growtg rate used 10 for now
            
            SD0 = [ [i for i,y in enumerate(self.Data[P][x[0]][D]) if y > Lim0] if x[0] in self.PL else [i for i,y in enumerate(self.Data[St][x[0]][D]) if y > Lim0] if x[0] in self.SL else max(int(self.Vars[x[3]]["Start Date"]) + MI(self.Vars[x[3]]["Average time to death"])  + 10 , 0) for x in SubData]
            SD0 = [0 if x == [] else x[0] if isinstance(x,list) else x for x in SD0]
            LineD = []
        else:
            SD0 = [0 for x in SubData]
            LineD = Opt["DateLines"]

        self.PageW[Ref]["PlotClass"] = GPlot([[self.Data["Time"][:int(x[2])-SD0[i]],
                                    self.Data[P][x[0]][x[1]][SD0[i]:int(x[2]) + SD0[i]]] if x[0] in self.PL 
                                   else [self.Data["Time"][:int(x[2])-SD0[i]],
                                         self.Data[St][x[0]][x[1]][SD0[i]:int(x[2]) + SD0[i]]] if x[0] in self.SL 
                                   else [[y + max(int(self.Vars[x[3]]["Start Date"]),0) - SD0[i] for y in ESTx[x[3]]["Time"][:int(x[2]) - int(self.Vars[x[3]]["Start Date"])]], 
                                         ESTx[x[3]][x[1]][:int(x[2]) - int(self.Vars[x[3]]["Start Date"])]] for i,x in enumerate(SubData)], 
                                  LineD, ["%s - %s" % (x[0], x[1]) for x in SubData], LOGY = Opt["LOGY"], FillR = Opt["FilledGraph"])
        
        SubData={"Plot": []}
        SubData["Plot"] = self.PageW[Ref]["PlotClass"].fig
        
        if Opt["Save"] != None: SubData["Plot"].savefig(Opt["Save"] , format = Opt["Save"].split(".")[-1])
        
        SubData.update({"Print" : [[self.PrintKey(x, self.Vars[x], ESTs[x])] for x in ESTs.keys()]})
        
        if "Preview" in self.PageW[Ref].keys() and "Data" in self.PageW[Ref].keys():
            plt.close(self.PageW[Ref]["Data"]["Plot"])
            for widget in self.PageW[Ref]["PreviewFrame"].winfo_children(): widget.destroy()

        self.PageW[Ref].update({"Preview" :FigureCanvasTkAgg(SubData["Plot"], self.PageW[Ref]["PreviewFrame"])})
        self.PageW[Ref]["Preview"].get_tk_widget().pack()
        
        #Add Annotation for hover and click events
        if Settings["OS"] == "android":
            self.PageW[Ref]["Preview"].mpl_connect("button_press_event", self.PageW[Ref]["PlotClass"].hover)
        else:
            self.PageW[Ref]["Preview"].mpl_connect("motion_notify_event", self.PageW[Ref]["PlotClass"].hover)
        
        self.PageW[Ref]["CS"].Update([[self.BaseCS]]*len(SubData["Print"]),False, False, SubData["Print"])
        self.PageW[Ref].update({"Data": SubData})
        
        self.Save()
        
    def MainTableAddRow(self, Table, Base = []):
        #Adds optional column for # of boards after more than 1 line is entered
        Data = Table.get()
        Table.Update(Table.WidgetOpt[-1], True, False, Data + [Data[-1]])
        
    def MainTableRemoveRow(self, Table, Base = []):        
        #Removes optional column for # of boards after more than 1 line is entered
        Data = Table.get()
        if len(Data) > 2: Table.Update(Table.WidgetOpt[:-1] , False, False, Data[:-1])    
              
    def GetData(self, Type = "web", Save = True):
        global Data, PL, SL
        #Base processed data
        self.Data = GetData(Type, Save)

        #Calculate
        self.PL = list(self.Data[P].keys())
        self.SL = list(self.Data[St].keys())

        for x in self.PL: self.Data[P][x].update(CalcData(self.Data[P][x]))
        for x in self.SL: self.Data[St][x].update(CalcData(self.Data[St][x]))
        
        #Update all lists
        PL   = self.PL
        SL   = self.SL
        Data = self.Data
        
        self.UpdateCLists()
        self.Save()
        
    def UpdateCLists(self):
        #Update all
        for x in self.PageW.keys():
            t = self.PageW[x]["MainTable"].get()
            z = self.PageW[x]["MainTable"].WidgetOpt
            z = [[{u:w[u] if u != "ComboList" else self.PL + self.SL + ["Estimation"] for u in w.keys()} if i==0 and n!=0 else w for i,w in enumerate(q)] for n,q in enumerate(z)]
            self.PageW[x]["MainTable"].Update(z, False, False, t)
            
        self.BaseTable = [[{u:w[u] if u != "ComboList" else self.PL + self.SL + ["Estimation"] for u in w.keys()} if i==0 and n!=0 else w for i,w in enumerate(q)] for n,q in enumerate(self.BaseTable)]
    
    def Save(self):
        with open("COVID_WIP.txt", "w") as WF:
            WF.write(str({"Tables":{x: str([self.PageW[x]["MainTable"].WidgetOpt, self.PageW[x]["MainTable"].get()]) for x in self.PageW.keys() if str(self.PageW[x]["MainTable"]).split(".!multi")[0] in [str(y) for y in self.nb.tabs()]}, "Vars": str(self.Vars), "Data": str(self.Data), "PL": str(self.PL), "SL": str(self.SL)}))

            
SVarD = {"Base": {"Start Date": 0, 
         "Growth Rate": 2.0, 
         "Death Rate": 0.01, 
         "Death Rate - Health care system overran": 0.04, 
         "Health care system overrun # of sick": MI(12*7.7e5), 
         "Social Distancing - Change Dates": [], 
         "Social Distancing - Change": [], 
         "Population": 7.7e9, 
         "Average time to death": 14, 
         "Average time to recovery": 31, 
         "Average time to detection": 10,
         "Normal daily mortality rate (per million)": 8.1,
         "Normal ICU survial rate": .477,
         "No ICU available survial rate": .24,
         "Normal ICU need by day": MI(4e6/365),
         "Average infected to symptoms": 3.5,
         "COVID ICU need rate": 0.05,
         "Average Effective Immunity Duraration": 180, 
         "Compartment Size": 1e6,
         "Mean Infection Time" : 5, 
         "Average detection rate of non ICU or deaths": .9,
         "Non symptoms recovery ratio":.9,
         "Average time to recovery - Sigma": 10}}

def VarUp(SVar):
    for x in SVar.keys(): 
        for y in SVarD["Base"].keys(): 
            if y not in SVar[x].keys(): 
                SVar[x].update({y:SVarD["Base"][y]})
    
    return SVar         
    
#____________________________________________________________________________________________________________
#Main Run Line

#Determine operating system (for mobile vs. PC)
if "android" in str(platform).lower():
    Settings["OS"] = "android"
elif "windows" in platform.system().lower():
    Settings["OS"] = "windows"
else:
    #Unchecked for other OS compatiability at the moment (linux may not be an issue)
    Settings["OS"] = "others"

Tables = []
PL     = []
SL     = []
Data   = {}
SVars  = SVarD
if os.path.exists("COVID_WIP.txt"):
    try:
        with open("COVID_WIP.txt", "r") as RF:
            Data = ast.literal_eval(RF.read())
        SVars  = ast.literal_eval(Data["Vars"])
        Tables = {x: ast.literal_eval(Data["Tables"][x]) for x in Data["Tables"].keys()}
        PL       = ast.literal_eval(Data["PL"])
        SL       = ast.literal_eval(Data["SL"])
        Data     = ast.literal_eval(Data["Data"])
    except:
        pass
    
SVars = VarUp(SVars)    
    
if len([x for x in CLI if ".json" in x]) > 0 or len([x for x in CLI if ".json" not in x]) <= 2:
    main = Tk()
    main.title('COVID-19 Tracker')
    
    #Base screen info
    Settings["Size"] = [max(main.winfo_screenwidth(), main.winfo_screenheight()), min(main.winfo_screenwidth(), main.winfo_screenheight())] # meant for widescreen use. note pixel4 is  2148 1080
    
    Settings["Size"] = SizeSet(Settings["Size"], OSFlag = {"windows": [1200, 600]})
    
    #Full screen if it is android (or others)
    main.geometry("%dx%d" % tuple(Settings["Size"]))

    my_gui = MainGUI(main, Data, PL, SL, Vars = SVars, Tables = Tables)
    main.mainloop()
else:
    #Command Line Interface
    sys.exit("Not yet implemented")

#Modify can be passed to Var fix this
#Finish "Special" Operations button integration
#Redo General Info Display (split using a multitable with scroll)

