import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import os
import subprocess

from tkinter.scrolledtext import ScrolledText

TypeFactMiner = "TypeChangeMiner"
typeFactMinerURL = "https://github.com/ameyaKetkar/TypeChangeMiner.git"
simpleTypeFactMinerURL = "https://github.com/ameyaKetkar/SimpleTypeChangeMiner.git"
projectPath = None

installed = False

# Main window
mainWindow = tk.Tk()

mainWindow.title("Welcome to TypeChangeMiner")

# Installation frame
installation_frame = tk.LabelFrame(master=mainWindow, text="Installation")
installation_frame.pack()

labelText = tk.StringVar()
labelText.set("Where to install TypeChangeMiner")
labelPath = tk.Label(installation_frame, textvariable=labelText)
labelPath.grid(row=1, column=1)

path = tk.StringVar(None)
tfMinerLocationUI = tk.Entry(master=installation_frame,relief=tk.RIDGE)
tfMinerLocationUI.grid(row=1, column=2)
# tfMinerLocationUI.pack()
search = tk.Button(master=installation_frame, text="Search")
search.grid(row=1, column=3)
# searchImage = tk.PhotoImage(file="Search.png")
installButton = tk.Button(master=installation_frame, text="Install")
installButton.grid(row=2, column=2)

# Configuration Frame
config_frame = tk.LabelFrame(master=mainWindow, text="Configuration")
config_frame.pack()

# ROW 1
clabelText = tk.StringVar()
clabelText.set("Where to clone the subject systems?")
clabelPath = tk.Label(config_frame, textvariable=clabelText)
clabelPath.grid(row=1, column=1)
corpussearch = tk.Button(master=config_frame, text="Search", state=tk.DISABLED)
corpussearch.grid(row=1, column=3)

pathToCorpus = tk.Entry(master=config_frame, state=tk.DISABLED,relief=tk.RIDGE)
pathToCorpus.grid(row=1, column=2)

# Row 2
epochStart = tk.StringVar()
epochStart.set("Start mining from date?  (YYY-mm-dd)")
epochStartLabel = tk.Label(config_frame, textvariable=epochStart)
epochStartLabel.grid(row=2, column=1)

epochStart = tk.Entry(master=config_frame, state=tk.DISABLED,relief=tk.RIDGE)
epochStart.grid(row=2, column=2)

# Row 3
projectLst = tk.StringVar()
projectLst.set("Projects to Analyze <Project name, Github URL>")
projectListLabel = tk.Label(config_frame, textvariable=projectLst)
projectListLabel.grid(row=3, column=1)
projectList = tk.Text(master=config_frame, state=tk.DISABLED, height=2, borderwidth=2, relief=tk.RIDGE)
projectList.grid(row=3, column=2)

projectListSearch = tk.Button(master=config_frame, text="Search", state=tk.DISABLED)
projectListSearch.grid(row=3, column=3)


#
# configureButton = tk.Button(master=installation_frame, text='Configure', state=tk.DISABLED)
# configureButton.pack()


def switchOnConfigure():
    corpussearch['state'] = tk.NORMAL
    pathToCorpus['state'] = tk.NORMAL
    epochStart['state'] = tk.NORMAL
    projectList['state'] = tk.NORMAL
    projectListSearch['state'] = tk.NORMAL
    installButton['state'] = tk.DISABLED
    search['state'] = tk.DISABLED


def mavenBuild(p, name):
    global installed
    global projectPath
    projectPath = os.path.join(p, name)
    os.chdir(projectPath)
    if os.path.isfile(os.path.join(projectPath, "target", "TypeChangeMiner-1.0-SNAPSHOT.jar")):
        installed = True
        messagebox.showinfo('Installation status', 'Already Installed!')
        return True
    print("Building ------ " + name)
    e, o = runLongCommand(["mvn", "clean", "install"])
    if e is None and "BUILD SUCCESS" in o.decode("utf-8"):
        installed = True
        messagebox.showinfo('Installation status', 'Successful!!!')
        return True
    else:
        print("BUILD \"" + name + "\" ------ FAILURE")
        installed = False
        messagebox.showinfo('Installation status', 'Failure!!!')
        return False


def runLongCommand(s):
    out = subprocess.Popen(s, stdout=subprocess.PIPE)
    out.wait()
    o, e = out.communicate()
    return e, o


def handle_click_install(location):
    if location == '':
        return
    if not os.path.isdir(os.path.normpath(location)):
        messagebox.showerror("Invalid Location", "Location not found")
        return
    if not installed:
        tfMinerLocation = os.path.normpath(location)
        if not os.path.isdir(os.path.join(tfMinerLocation, TypeFactMiner)):
            import git
            git.Git(tfMinerLocation).clone(typeFactMinerURL)
            git.Git(tfMinerLocation).clone(simpleTypeFactMinerURL)
        mavenBuild(tfMinerLocation, TypeFactMiner)

    if installed:
        switchOnConfigure()


def searchForDirectoryTypeFactMiner():
    dir = filedialog.askdirectory()
    tfMinerLocationUI.delete(0, tk.END)
    tfMinerLocationUI.insert(0, dir)


def searchForDirectoryPathToCorpus():
    dir = filedialog.askdirectory()
    pathToCorpus.delete(0, tk.END)
    pathToCorpus.insert(0, dir)


def searchForDirectoryProjectList():
    dir = filedialog.askopenfilenames()
    projectList.delete(0, tk.END)
    projectList.insert(0, dir)

installButton.bind("<Button-1>", lambda e: handle_click_install(tfMinerLocationUI.get()))
search.bind("<Button-1>", lambda e: searchForDirectoryTypeFactMiner())

corpussearch.bind("<Button-1>", lambda e: searchForDirectoryPathToCorpus())
projectListSearch.bind("<Button-1>", lambda e: searchForDirectoryProjectList())
# label.pack()

tk.mainloop()
