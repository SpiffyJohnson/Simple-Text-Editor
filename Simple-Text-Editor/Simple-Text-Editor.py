#---------------------------------------------------------------------------------------------
# Author: Samuel Johnson
# Program: Simple-Text-Editor
# Use: A rather gimmicky Tkinter text editor that uses a terminal rather than a toolbar or buttons
# Last Updated: 12/17/2025
#
# TODO: Maybe convert this over to customtkinter, since I really want to have more font control
# TODO: Overhaul the ExecuteCommand() function to rely less on 'if' statements
# TODO: Add 'HELP' keywords to each command to display syntax and options
# TODO: I might split this single document into several to avoid having one long file as this improves
# TODO: Focus on cross-OS functionality
# TODO: Add 'Browse' command to create a copy of the chosen text file in the Files folder for editing.
# TODO: Better error handling/explanation + input sanitization
# TODO: Try to deal with funky app resizing.
#---------------------------------------------------------------------------------------------

import tkinter as tk
import pathlib
import os

currentPythonFilePath = str(pathlib.Path(__file__).parent.resolve())
filesPath = os.path.join(currentPythonFilePath, "Files")

rootName = "TextEditor"
baseFont = ("Monospace", 24)
bgColor = "#090952"
fgColor = "#FFFFFF"
greyColor = "#383838"
lineChar = "-"
global isFullscreen
isFullscreen = True
global currentlyOpenedFile
currentlyOpenedFile = ""
global pastCommands
pastCommands = []
global pastCommandCounter
pastCommandCounter = -1

commands = [
    ("LOAD", "OPEN", "L"),
    ("SAVE", "S"),
    ("DELETE", "DESTROY", "DEL"),
    ("NEW", "CLEAR", "WIPE"),
    ("LIST", "LS", "FILES"),
    ("BGCOLOR", "COLOR", "BGC", "C"),
    ("FGCOLOR", "FGC"),
    ("COLORSCHEME", "CS"),
    ("RESET", "REBOOT", "REFRESH"),
    ("EXIT", "QUIT", "STOP", "CLOSE"),
    ("HELP", "?"),
]

commandsHelp = [
    "# Load file by name\n",
    "# Save file by name\n",
    "# Delete file by name\n",
    "# Empty text box\n",
    "# Show available files\n",
    "# Change background color\n",
    "# Change text color\n",
    "# Change colorscheme\n",
    "# Reboot the application\n",
    "# Close the application\n",
    "# List available commands\n",
]

themes = [
    "DRDARK", 
    "LIGHTMODE", 
    "DARKMODE", 
    "MACHINE", 
    "MATRIX", 
    "PEACH", 
    "SYSTEM", 
    "OFF", 
    "MOON", 
    "QUIET", 
    "NIGHTLIGHT", 
    "DIVER", 
    "X", 
    "BLACK"
]

themeCodes = [
    ("#300", "#f00", "#000", "#af0000"), 
    ("#DDD", "#333", "#bbb", "#888"),
    ("#000", "#aaa", "#222", "#444"), 
    ("#192215", "#a5c96a", "#110f0f", "#4d4444"),
    ("#000", "#0f0", "#1d1d1d", "#0f0"), 
    ("#DBB2B2", "#8D0D0D", "#D35858", "#E4BABA"),
    ("#0000FF", "#FFFFFF", "#000000", "#FF0000"), 
    ("#090952", "#FFFFFF", "#383838", "#777"),
    ("#20005C", "#FFEFA9","#07002E", "#5100D4" ), 
    ("#010101", "#444", "#020202", "#232323",),
    ("#210101", "#644444", "#220202", "#432323"), 
    ("#000", "#00f", "#008", "#ccc"), 
    ("#000", "#F00", "#000", "#F00"),
    ("#000", "#000", "#000", "#000"),
]

def OnSave(path, event=None):
    global TextEditor
    global WarningText
    try:
        file = open(os.path.join(filesPath, path), 'w')
        text = TextEditor.get("1.0", "end-1c")
        file.writelines(text)
        file.close()
        WarningText.config(text="Saved file " + path)
    except:
        WarningText.config(text="Error saving file")

def OnSaveShortcut(event=None):
    global currentlyOpenedFile
    OnSave(currentlyOpenedFile)

def OnLoad(path, event=None):
    global TextEditor
    global currentlyOpenedFile
    loadedFile = ""

    try:
        file = open(os.path.join(filesPath, path), 'r')
        lines = file.readlines()
        file.close()
        
        for line in lines: 
            loadedFile += line

        TextEditor.delete("1.0", tk.END)
        TextEditor.insert("1.0", loadedFile)
        WarningText.config(text="Loaded file " + path)
        TextEditor.see(tk.END)
        currentlyOpenedFile = path
    except:
        WarningText.config(text="Error opening file")

def ExecuteCommand(event):
    global CommandEntry
    global pastCommands
    global pastCommandCounter
    
    pastCommandCounter = -1
    command = (CommandEntry.get())
    pastCommands = [CommandEntry.get()] + pastCommands
    CommandEntry.delete(0, tk.END)
    keywords = command.split(' ')
    keywords += [""]
    if keywords[0].upper() == "BGCOLOR" or keywords[0].upper() == "COLOR" or keywords[0].upper() == "C" or keywords[0].upper() == "BGC":
        SetBGColor(keywords[1])
    elif keywords[0].upper() == "FGCOLOR" or keywords[0].upper() == "FGC":
        SetFGColor(keywords[1])
    elif keywords[0].upper() == "COLORSCHEME" or keywords[0].upper() == "CS":
        SetColorscheme(keywords[1])
    elif keywords[0].upper() == "LOAD" or keywords[0].upper() == "OPEN" or keywords[0].upper() == "L":
        OnLoad(keywords[1])
    elif keywords[0].upper() == "SAVE" or keywords[0].upper() == "S":
        OnSave(keywords[1])
    elif keywords[0].upper() == "EXIT" or keywords[0].upper() == "QUIT" or keywords[0].upper() == "STOP" or keywords[0].upper() == "CLOSE":
        OnEscape()
    elif keywords[0].upper() == "NEW" or keywords[0].upper() == "CLEAR" or keywords[0].upper() == "WIPE":
        OnNew()
    elif keywords[0].upper() == "RESET" or keywords[0].upper() == "REBOOT" or keywords[0].upper() == "REFRESH":
        OnReset()
    elif keywords[0].upper() == "HELP" or keywords[0].upper() == "?" or keywords[0].upper() == "'HELP'":
        OnHelp()
    elif keywords[0].upper() == "LIST" or keywords[0].upper() == "LS" or keywords[0].upper() == "FILES":
        OnList()
    elif keywords[0].upper() == "DELETE" or keywords[0].upper() == "DESTROY" or keywords[0].upper() == "DEL":
        OnDelete(keywords[1])
    elif keywords[0].upper() == "FLIP":
        OnFlip()
    else:
        WarningText.config(text="Invalid command")
        

def SetBGColor(color):
    global CommandEntry
    global TextEditor
    if "#" not in color:
        color = "#" + color
    try:
        TextEditor.config(bg=color)
        CommandEntry.config(bg=color)
        WarningText.config(text="Background color set to " + color.upper())
    except:
        WarningText.config(text="Invalid color")

def SetFGColor(color):
    global CommandEntry
    global TextEditor
    if "#" not in color:
        color = "#" + color
    try:
        TextEditor.config(fg=color, insertbackground=color)
        CommandEntry.config(fg=color, insertbackground=color)
        WarningText.config(text="Text color set to " + color.upper())
    except:
        WarningText.config(text="Invalid color")

def SetColorscheme(colorscheme):
    global CommandEntry
    global TextEditor
    global WarningText
    global NavFrame

    if colorscheme.upper() in themes:
        bg, fg, grey, warn = themeCodes[themes.index(colorscheme.upper())]
        CommandEntry.config(bg=bg, fg=fg, insertbackground=fg)
        TextEditor.config(bg=bg, fg=fg, insertbackground=fg)
        WarningText.config(bg=grey, fg=warn)
        NavFrame.config(bg=grey)
        WarningText.config(text="Colorscheme set to " + colorscheme.upper())
    elif colorscheme.upper() == "LIST" or colorscheme.upper() == "HELP" or colorscheme.upper() == "LS":
        TextEditor.insert("end-1c", "\n\n" + (lineChar * 59) + "\nLIST OF COLORSCHEMES:\n" + (lineChar * 59) + "\n\n")
        for theme in themes:
            TextEditor.insert("end-1c", theme + "\n")
        TextEditor.insert("end-1c", "\n" + (lineChar * 59) + "\n")
        TextEditor.see(tk.END)
    else:
        WarningText.config(text="Invalid colorscheme")


def OnNew(event=None):
    global TextEditor
    global WarningText
    TextEditor.delete("1.0", tk.END)
    WarningText.config(text="Cleared screen")

def OnReset():
    SetColorscheme("OFF")
    OnNew()
    global WarningText
    WarningText.config(text="Type 'help' for list of commands")

def OnHelp():
    global TextEditor
    global WarningText

    TextEditor.insert("end-1c", "\n\n" + (lineChar * 59) + "\n\nList of commands:\n\n" + (lineChar * 59) + "\n\n")

    for command in commands:
        commandString = ""
        for alias in command:
            commandString += alias + ", "

        TextEditor.insert("end-1c", (f"{str(commandString):<32}" + commandsHelp[commands.index(command)]))

    TextEditor.insert("end-1c", "\n" + (lineChar * 59) + "\n")
    WarningText.config(text="Listed commands")
    TextEditor.see(tk.END)

def OnList():
    global TextEditor
    WarningText

    TextEditor.insert("end-1c", "\n\n" + (lineChar * 59) + "\n\nList of files in directory:\n\n" + (lineChar * 59) + "\n\n")
    for filename in os.listdir(currentPythonFilePath + "/Files"):
        TextEditor.insert("end-1c", filename + "\n")
    TextEditor.insert("end-1c", "\n" + (lineChar * 59) + "\n")
    WarningText.config(text="Listed available files")
    TextEditor.see(tk.END)

def OnDelete(path):
    global WarningText
    try:
        os.remove(currentPythonFilePath + "/Files/" + path)
        WarningText.config(text="Deleted file " + path.upper())
    except:
        WarningText.config(text="Error deleting file")

# Mirrors text in the textbox
def OnFlip():
    global TextEditor
    text = TextEditor.get("1.0", "end-1c")
    TextEditor.delete("1.0", tk.END)
    TextEditor.insert("1.0", text[::-1])

# Used for command memory
def OnUpOrDown(direction):
    global CommandEntry
    global pastCommands
    global pastCommandCounter
    try:
        pastCommands[pastCommandCounter + direction] # just make sure that an out of range error isn't thrown.
        if pastCommandCounter + direction > -2:
            pastCommandCounter += direction
            if pastCommandCounter == -1:
                CommandEntry.delete(0, tk.END)
            else:
                CommandEntry.delete(0, tk.END)
                CommandEntry.insert(0, pastCommands[pastCommandCounter])
    except IndexError:
        pass

def OnMinimize(event):
    global isFullscreen
    isFullscreen = not isFullscreen
    root.attributes("-fullscreen", isFullscreen)

def OnEscape(event=None):
    root.destroy()


root = tk.Tk()
root.title = rootName
root.config(bg="#000")
root.attributes("-fullscreen", True)

global TextEditor
TextEditor = tk.Text(root, bg=bgColor, font=baseFont, fg="#FFF", insertbackground="#FFFFFF", highlightthickness=0, wrap="word")
TextEditor.pack(fill="both")

global WarningText
WarningText = tk.Label(root, font=baseFont, bg=greyColor, fg="#777", text="Type 'help' for list of commands")
WarningText.pack(fill="x")

global NavFrame
NavFrame = tk.Frame(root, height=156, bg=greyColor)
NavFrame.grid_columnconfigure(0, weight=1)
NavFrame.pack(fill="x", side="bottom")

global CommandEntry
CommandEntry = tk.Entry(NavFrame, justify="left", font=baseFont, bg=bgColor, fg="#fff", insertbackground=fgColor, highlightthickness=0)
CommandEntry.grid(row=0, column=0, pady=25, ipady=50, ipadx=50, sticky="we")

CommandEntry.focus()

# Bind shortcuts to the editor:
root.bind("<Control-Escape>", OnEscape)
root.bind("<Escape>", OnMinimize)
root.bind("<Control-s>", OnSaveShortcut)
root.bind("<Control-S>", OnSaveShortcut)
root.bind("<Control-o>", OnLoad)
root.bind("<Control-Tab>", lambda: CommandEntry.focus())
CommandEntry.bind("<Up>", lambda event: OnUpOrDown(1))
CommandEntry.bind("<Down>", lambda event: OnUpOrDown(-1))
CommandEntry.bind("<Return>", ExecuteCommand)

root.mainloop()
