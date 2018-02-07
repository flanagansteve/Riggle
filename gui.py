#!/usr/bin/python3
from tkinter import *
import tkinter.filedialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.messagebox
from tkinter.colorchooser import askcolor
from solidityToDeployable import *
from setupDevnetAndDeploy import *

filename=""

def font():
    (triple,color) = askcolor()
    if color:
       text.config(foreground=color)

def kill():
    cleanUp(isWindows())
    root.destroy()

def opn():
    text.delete(1.0 , END)
    file = open(askopenfilename() , 'r')
    if file != '':
        file_text = file.read()
        text.insert(INSERT,file_text)

def save():
    global filename
    filename = asksaveasfilename()
    if filename:
        alltext = text.get(1.0, END)
        open(filename, 'w').write(alltext)

def copy():
    text.clipboard_clear()
    text.clipboard_append(text.selection_get())

def paste():
    try:
        paste = text.selection_get(selection='CLIPBOARD')
        text.insert(INSERT, paste)
    except:
        tkinter.messagebox.showerror("Error","The clipboard is empty")

def clear():
    sel = text.get(SEL_FIRST, SEL_LAST)
    text.delete(SEL_FIRST, SEL_LAST)

def clearall():
    text.delete(1.0 , END)

def background():
    (triple,color) = askcolor()
    if color:
       text.config(background=color)

#TODO
def deployToDev():
    #TODO: how get
    init_from_gui(filename)
    defineContractObject()
    instantiateContractObject(0)
    if not isWindows():
        instantiateNetwork(getDeployableContractPath(), isWindows())
        deployContract(fileToString(getDeployableContractPath()), isWindows())
        cleanUp(isWindows())
    else:
        print("Windows system detected. You will have to manually set up a development network")
        print("Please consult windowsSetup.md in this repository")

#TODO
def deployToRopsten():
    pass

#TODO
def deployToMain():
    pass

root = Tk()
root.title("Riggle")
menu = Menu(root)

filemenu = Menu(root)
root.config(menu = menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open", command=opn)
filemenu.add_command(label="Save", command=save)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=kill)

testmenu = Menu(root)
menu.add_cascade(label="Deploy", menu=testmenu)
testmenu.add_command(label="Deploy on devnet", command = deployToDev)
testmenu.add_command(label="Deploy to Ropsten", command = deployToRopsten)
testmenu.add_command(label="Deploy to mainnet", command = deployToMain)

modmenu = Menu(root)
menu.add_cascade(label="Edit",menu = modmenu)
modmenu.add_command(label="Copy", command = copy)
modmenu.add_command(label="Paste", command = paste)
modmenu.add_separator()
modmenu.add_command(label = "Clear selection", command = clear)
modmenu.add_command(label = "Clear all", command = clearall)

formatmenu = Menu(menu)
menu.add_cascade(label="Format",menu = formatmenu)
formatmenu.add_cascade(label="Color", command = font)

persomenu = Menu(root)
menu.add_cascade(label="Personalize",menu=persomenu)
persomenu.add_command(label="Night mode", command=background)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
text = Text(root, height=60, width=120, font = ("Arial", 10))

scroll = Scrollbar(root, command=text.yview)
scroll.config(command=text.yview)
text.config(yscrollcommand=scroll.set)
scroll.pack(side=RIGHT, fill=Y)
text.pack()

root.resizable(0,0)
root.mainloop()
