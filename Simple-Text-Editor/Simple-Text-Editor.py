#---------------------------------------------------------------------------------------------
# Author: Samuel Johnson
# Program: Simple-Text-Editor
# Use: A rather gimmicky Tkinter text editor that uses a terminal rather than a toolbar or buttons
# Last Updated: 12/20/2025
#
# TODO: Maybe convert this over to customtkinter or Kivy, since I really want to have more font control
# TODO: Overhaul the ExecuteCommand() function to rely less on 'if' statements
# TODO: Add 'HELP' keywords to the remaining commands
# TODO: I might split this single document into several to avoid having one long file as this improves
# TODO: Focus on cross-OS functionality
# TODO: Better error handling/explanation + input sanitization
# TODO: Try to deal with funky app resizing.
#---------------------------------------------------------------------------------------------

import tkinter as tk
from tkinter import filedialog
import pathlib
import os

currentPythonFilePath = str(pathlib.Path(__file__).parent.resolve())
filesPath = os.path.join(currentPythonFilePath, "Files")

rootName = "TextEditor"
baseFont = ("Monospace", 24)
bgColor = "#090952"
fgColor = "#FFFFFF"
greyColor = "#383838"
lineChar = "—"
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
    ("BROWSE", "FIND"),
    ("NEW", "CLEAR", "WIPE"),
    ("LIST", "LS", "FILES"),
    ("BGCOLOR", "COLOR", "BGC", "C"),
    ("FGCOLOR", "FGC"),
    ("COLORSCHEME", "CS"),
    ("RESET", "REBOOT", "REFRESH"),
    ("EXIT", "QUIT", "STOP", "CLOSE"),
    ("HELP", "?"),
    ("FLIP", "MIRROR"),
    ("CENTER", "JUSTIFY"),
]

commandsHelp = [
    "# Load file by name\n",
    "# Save file by name\n",
    "# Delete file by name\n",
    "# Browse for a specific file\n",
    "# Empty text box\n",
    "# Show available files\n",
    "# Change background color\n",
    "# Change text color\n",
    "# Change colorscheme\n",
    "# Reboot the application\n",
    "# Close the application\n",
    "# List available commands\n",
    "# Mirror the text on screen.\n",
    "# Toggle text centering\n",
]

commandsInDepthHelp = [
    "Aliases: LOAD, OPEN, L; \nSyntax: LOAD <Filename>; \nExample(s): 'load test.txt', 'l test.txt'\n",
    "Aliases: SAVE, S; \nSyntax: SAVE <Filename>; \nExample(s): 'save test.txt', 's text.txt'\n",
    "Aliases: DELETE, DESTROY, DEL; \nSyntax: DELETE <Filename>; \nExample(s): 'delete test.txt', 'del test.txt'\n",
    "Aliases: BROWSE, FIND; \nSyntax: BROWSE; \nExample(s): 'browse', 'find'\n",
    "Aliases: NEW, CLEAR, WIPE; \nSyntax: NEW; \nExample(s): 'new', 'wipe'\n",
    "Aliases: LIST, LS, FILES; \nSyntax: LIST; \nExample(s): 'list', 'ls'\n",
    "Aliases: BGCOLOR, COLOR, BGC, C; \nSyntax: BGCOLOR <Hex string>; \nExample(s): 'bgcolor #FF0000', 'bgc F00', 'c FF0000'\n",
    "Aliases: FGCOLOR, FGC; \nSyntax: FGCOLOR <Hex string>; \nExample(s): 'fgcolor #FF0000', 'fgc F00', 'fgc FF0000'\n",
    "Aliases: COLORSCHEME, CS; \nSyntax: COLORSCHEME <Colorscheme name>; \nExample(s): 'colorscheme moon', 'cs machine'\n",
    "Aliases: RESET, REBOOT, REFRESH; \nSyntax: REBOOT; \nExample(s): 'reset', 'reboot'\n",
    "Aliases: EXIT, QUIT, STOP, CLOSE; \nSyntax: EXIT; \nExample(s): 'exit', 'close'\n",
    "Aliases: HELP, ?; \nSyntax: HELP; \nExample(s): 'help', '?'\n",
    "Aliases: FLIP, MIRROR; \nSyntax: FLIP; \nExample(s): 'flip', 'mirror'\n",
    "Aliases: CENTER, JUSTIFY; \nSyntax: CENTER; \nExample(s): 'center on', 'justify off'\n",
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

    if keywords[0].upper() in commands[0]:
        OnLoad(keywords[1])
    elif keywords[0].upper() in commands[1]:
        OnSave(keywords[1])
    elif keywords[0].upper() in commands[2]:
        OnDelete(keywords[1])
    elif keywords[0].upper() in commands[3]:
        OnLoad(keywords[0], True)
    elif keywords[0].upper() in commands[4]:
        OnNew(keywords[1])
    elif keywords[0].upper() in commands[5]:
        OnList(keywords[1])
    elif keywords[0].upper() in commands[6]:
        SetBGColor(keywords[1])
    elif keywords[0].upper() in commands[7]:
        SetFGColor(keywords[1])
    elif keywords[0].upper() in commands[8]:
        SetColorscheme(keywords[1])
    elif keywords[0].upper() in commands[9]:
        OnReset(keywords[1])
    elif keywords[0].upper() in commands[10]:
        OnEscape(keywords[1])
    elif keywords[0].upper() in commands[11]:
        OnHelp(keywords[1])
    elif keywords[0].upper() in commands[12]:
        OnFlip(keywords[1])
    elif keywords[0].upper() in commands[13]:
        OnCenter(keywords[1])
    else:
        WarningText.config(text="Invalid command")

def OnLoad(path, isBrowse = False, event=None):
    if path.upper() == "HELP":
        if isBrowse:
            ListHelp(3)
        else:
            ListHelp(0)
        return
    
    global TextEditor
    global currentlyOpenedFile
    loadedFile = ""

    try:
        if not isBrowse:
            file = open(os.path.join(filesPath, path), 'r')
        else:
            path = filedialog.askopenfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")],
                initialdir=(filesPath)
            )
            file = open(path, 'r')
        lines = file.readlines()
        file.close()
        
        for line in lines: 
            loadedFile += line

        TextEditor.delete("1.0", tk.END)
        TextEditor.insert("1.0", loadedFile)
        WarningText.config(text="Loaded file " + path)
        TextEditor.see(tk.END)
        currentlyOpenedFile = path
    except FileNotFoundError:
        WarningText.config(text="Error: File not found")
    except:
        WarningText.config(text="Error loading file")

def OnSave(path, event=None):
    if path.upper() == "HELP":
        ListHelp(1)
        return
    
    global TextEditor
    global WarningText
    try:
        file = open(os.path.join(filesPath, path), 'w')
        text = TextEditor.get("1.0", "end-1c")
        file.writelines(text)
        file.close()
        WarningText.config(text="Saved file " + path)
    except FileNotFoundError:
        WarningText.config(text="Error: File not found")
    except:
        WarningText.config(text="Error saving file")

def OnSaveShortcut(event=None):
    global currentlyOpenedFile
    OnSave(currentlyOpenedFile)

def OnDelete(path):
    if path.upper() == "HELP":
        ListHelp(2)
        return
    global WarningText
    try:
        os.remove(currentPythonFilePath + "/Files/" + path)
        WarningText.config(text="Deleted file " + path.upper())
    except FileNotFoundError:
        WarningText.config(text="Error: File not found")
    except:
        WarningText.config(text="Error deleting file")
        
def OnNew(keyword, event=None):
    if keyword.upper() == "HELP":
        ListHelp(4)
        return
    global TextEditor
    global WarningText
    TextEditor.delete("1.0", tk.END)
    WarningText.config(text="Cleared screen")

def OnList(keyword):
    if keyword.upper() == "HELP":
        ListHelp(5)
        return
    global TextEditor
    WarningText

    TextEditor.insert("end-1c", "\n\n" + (lineChar * 59) + "\n\nList of files in directory:\n\n" + (lineChar * 59) + "\n\n")
    for filename in os.listdir(currentPythonFilePath + "/Files"):
        TextEditor.insert("end-1c", filename + "\n")
    TextEditor.insert("end-1c", "\n" + (lineChar * 59) + "\n")
    WarningText.config(text="Listed available files")
    TextEditor.see(tk.END)

def SetBGColor(color):
    if color.upper() == "HELP":
        ListHelp(6)
        return
    
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
    if color.upper() == "HELP":
        ListHelp(7)
        return
    
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
    if colorscheme.upper() == "HELP":
        # Lists the colorschemes in addition to normal help information
        ListHelp(8)
        TextEditor.insert("end-1c", "List of acceptable colorschemes:\n" + (lineChar * 59) + "\n\n")
        for theme in themes:
            TextEditor.insert("end-1c", theme + "\n")
        TextEditor.insert("end-1c", "\n" + (lineChar * 59) + "\n")
        TextEditor.see(tk.END)
        return

    if colorscheme.upper() in themes:
        bg, fg, grey, warn = themeCodes[themes.index(colorscheme.upper())]
        CommandEntry.config(bg=bg, fg=fg, insertbackground=fg)
        TextEditor.config(bg=bg, fg=fg, insertbackground=fg)
        WarningText.config(bg=grey, fg=warn)
        NavFrame.config(bg=grey)
        WarningText.config(text="Colorscheme set to " + colorscheme.upper())
    else:
        WarningText.config(text="Invalid colorscheme name")

def OnReset(keyword):
    if keyword.upper() == "HELP":
        ListHelp(9)
        return
    SetColorscheme("OFF")
    OnNew("")
    global WarningText
    WarningText.config(text="Type 'help' for list of commands")

def OnEscape(keyword="", event=None):
    if keyword.upper() == "HELP":
        ListHelp(13)
        return
    root.destroy()

def OnHelp(keyword):
    global TextEditor
    global WarningText

    TextEditor.insert("end-1c", "\n" + (lineChar * 59) + "\n\nList of commands:\n\n" + (lineChar * 59) + "\n\n")

    for command in commands:
        commandString = ""
        for alias in command:
            commandString += alias + ", "

        TextEditor.insert("end-1c", (f"{str(commandString):<32}" + commandsHelp[commands.index(command)]))

    TextEditor.insert("end-1c", "\n" + (lineChar * 59) + "\n")
    TextEditor.insert("end-1c", "Hint: Type 'help' after a command for more information\n")
    TextEditor.insert("end-1c", "Hint: Press ESC to exit fullscreen mode\n")
    TextEditor.insert("end-1c", "Hint: You can close the app by pressing CTRL+ESC\n")
    TextEditor.insert("end-1c", (lineChar * 59) + "\n")
    WarningText.config(text="Listed commands")
    TextEditor.see(tk.END)

def ListHelp(commandId):
    global TextEditor
    TextEditor.insert("end-1c", "\n\n" + (lineChar * 59) + f"\n\n{commands[commandId]}:\n\n" + (lineChar * 59) + "\n\n")

    TextEditor.insert("end-1c", (commandsHelp[commandId] + "\n" + commandsInDepthHelp[commandId]))

    TextEditor.insert("end-1c", "\n" + (lineChar * 59) + "\n")
    WarningText.config(text="Listed syntax")
    TextEditor.see(tk.END)

# Mirrors text in the textbox
def OnFlip(keyword):
    if keyword.upper() == "HELP":
        ListHelp(12)
        return
    global TextEditor
    text = TextEditor.get("1.0", "end-1c")
    TextEditor.delete("1.0", tk.END)
    TextEditor.insert("1.0", text[::-1])

# Changes the justification of the main textbox
def OnCenter(doCenter = "on"):
    if doCenter.upper() == "HELP":
        ListHelp(13)
        return
    global TextEditor
    global WarningText
    if doCenter.upper() == "ON":

        TextEditor.tag_configure("justify", justify="center")
        TextEditor.tag_add("justify", "1.0", "end")
        WarningText.config(text="Centered text")
    elif doCenter.upper() == "OFF":
        TextEditor.tag_configure("justify", justify="left")
        TextEditor.tag_add("justify", "1.0", "end")
        WarningText.config(text="Aligned text left")
    else:
        WarningText.config(text="Invalid centering: use 'on' or 'off'")

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
root.bind("<Control-Escape>", lambda event: OnEscape(""))
root.bind("<Escape>", OnMinimize)
root.bind("<Control-s>", OnSaveShortcut)
root.bind("<Control-S>", OnSaveShortcut)
root.bind("<Control-o>", OnLoad)
root.bind("<Control-Tab>", lambda: CommandEntry.focus())
CommandEntry.bind("<Up>", lambda event: OnUpOrDown(1))
CommandEntry.bind("<Down>", lambda event: OnUpOrDown(-1))
CommandEntry.bind("<Return>", ExecuteCommand)

root.mainloop()