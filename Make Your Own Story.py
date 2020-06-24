import tkinter as tk
from tkinter import ttk
import glob
import csv
import os

nodes = []
x = []
choices = []

def createfile(filename,lst):
    csvfile=open(filename,'w', newline='')
    obj=csv.writer(csvfile)
    for i in lst:
        obj.writerow(i)
    csvfile.close()

def update_choice():
    fn = int(f_node.get())
    tn = int(t_node.get())
    ch_tx = ch_text.get()

    if len(nodes)==0:
        nodes.append(fn)
    if fn not in nodes and len(nodes)!=0:
        tk.Label(window, text = 'From node "'+str(fn)+'" not added before').grid(row = 8, column = 0)
        return
    if tn not in nodes:
        nodes.append(tn)

    if ch_tx == '':
        choices.append(tn)
        return
    kar = karma.get()
    if kar == "":
        kar = 0
    else:
        kar = int(kar)
    choices.append([tn, ch_tx, kar])
    print(nodes)
    print(choices)
    tk.Label(window, text = 'Choice to Node "'+str(t_node.get())+'" has been added').grid(row = 7, column = 2)

def read():
    global choices

    fn = int(f_node.get())
    tx = text.get()
    tn = int(t_node.get())
    print(fn, tn)

    if len(nodes)==0:
        nodes.append(fn)
    if fn not in nodes:
        tk.Label(window, text = 'From node "'+str(fn)+'" not added before').grid(row = 8, column = 0)
        return
    if tn not in nodes:
        nodes.append(tn)
    print(nodes)

    bg = bg_image.get()
    mus = music.get()
    nd_ty = nd_type.get()
    if choices == []:
        if tn == '':
            choices = '.'
        else:
            choices = tn
    else:
        nd_ty = "choices"
    edge = [fn, bg, mus, nd_ty, tx, choices]
    x.append(edge)
    tk.Label(window, text='last node added = ' + str(f_node.get())).grid(row=12, column=0)

    print(x)

def refresh_choices():
    global choices
    choices = []

def do():
    read()
    refresh_choices()

def end():
    tk.Label(window, text = "File created").grid(row = 13, column = 1)
    print(x)
    createfile('games\\'+title.get()+" by "+ creator.get()+'.csv', x)


window = tk.Tk()
window.title("Make Your Own Adaptive Story")
wid = 30

# Title #
tk.Label(window, text = "Story Title:", font = ("gillsansnova", 10)).grid(row = 0, column = 0)
title = tk.Entry(window, width = wid)
title.grid(row = 1, column = 0, padx=0, pady=10)

# Creator #
tk.Label(window, text = "Created By:", font = ("gillsansnova", 10)).grid(row = 0, column = 1)
creator = tk.Entry(window, width =wid)
creator.grid(row = 1, column = 1, padx=0, pady=10)

# From Node #
tk.Label(window, text = "Current Node", font = ("gillsansnova", 10)).grid(row = 3, column = 0)
f_node = tk.Entry(window, width = wid//2)
f_node.grid(row = 4, column = 0, padx=0, pady=10)

# To Node #
tk.Label(window, text = "Next Node", font = ("gillsansnova", 10)).grid(row = 3, column = 1)
t_node = tk.Entry(window, width = wid//2)
t_node.grid(row = 4, column = 1, padx=0, pady=10)

# Display Text #
tk.Label(window, text = "Text to be Displayed", font = ("gillsansnova", 10)).grid(row = 3, column = 2)
text = tk.Entry(window, width = wid)
text.grid(row = 4, column = 2, padx=0, pady=10)



# Choice Text #
tk.Label(window, text = "Choice Text\n(leave empty if no choice)", font = ("gillsansnova", 10)).grid(row = 6, column = 0)
ch_text = tk.Entry(window, width = wid)
ch_text.grid(row = 7, column = 0, padx=0, pady=10)

# Karma Points #
tk.Label(window, text = "Karma Points", font = ("gillsansnova", 10)).grid(row = 6, column = 1)
karma = tk.Entry(window, width = wid//2)
karma.grid(row = 7, column = 1, padx=0, pady=10)

# Choice Button #
tk.Button(window, text = "Add Choice", font = ("gillsansnova", 12), height = 1, width = 10, command = update_choice).grid(row = 6, column = 2, padx=0, pady=10)

# Background Image #
tk.Label(window, text = "Background Image\n(with .jpeg, .png, etc)", font = ("gillsansnova", 10)).grid(row = 8, column = 1)
bg_image = tk.Entry(window, width = int((wid//2)*1.5))
bg_image.grid(row = 9, column = 1, padx=0, pady=10)

# Music #
tk.Label(window, text = "Music\n(with .mp3, .wav, etc)", font = ("gillsansnova", 10)).grid(row = 8, column = 0)
music = tk.Entry(window, width = wid//2)
music.grid(row = 9, column = 0, padx=0, pady=10)

# Node Type #
tk.Label(window, text = "Node Type", font = ("gillsansnova", 10)).grid(row = 8, column = 2)
nd_type = ttk.Combobox(window, width = wid//2)
nd_type.grid(row = 9, column = 2, padx=0, pady=10)
nd_type['values'] = ('start','straight', 'choices', 'karma', 'end')

# Next #
tk.Button(window, text = "Add Node", height = 1, width = 10, command = do, font = ("gillsansnova", 12)).grid(row = 12, column = 1, padx=0, pady=10)

# End #
tk.Button(window, text = "Create File", height = 1, width = 10, command = end, font = ("gillsansnova", 12)).grid(row = 12, column = 2, padx=0, pady=10)
window.mainloop()

