import pprint
import pygame
import random
import textwrap
import time
from os import system, name 
import pygame.freetype
import csv
import tkinter as tk
from tkinter import ttk
import glob
import ast

def clear(): 
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear')

def addNodes(G, node):
    if node not in G:
            G[node] = []

def addEdges(G, edge):
    if len(edge)==3:
        weight = edge[2]
        G[edge[0]].append((edge[1], *weight))
    else:
        G[edge[0]].append((edge[1],1))

# def evaluator(s):
#     if s == '.':
#         return []
#     lst = s.split('.')
#     for i in range(len(lst)):
#         lst[i] = lst[i].split(',')
#         lst[i][0] = int(lst[i][0])
#         try:
#             lst[i][2] = eval(lst[i][2])
#         except:
#             pass
#     if len(lst)==1:
#         return lst[0]
#     return lst

'''
def draw(parent_name, child_name):
    edge = pydot.Edge(parent_name, child_name[0])
    graph.add_edge(edge)
def visit(G, parent=None):
    for i in G.keys():
        graph.add_node(pydot.Node(i))
    for key in G:
        for node in G[key]:
            draw(key, node)

graph = pydot.Dot(graph_type='graph')
visit(G)
for i in graph.get_edge_list():
    print(i.get_source(), i.get_destination())
for i in graph.get_node_list():
    print(i.get_name())

graph.write_png('example1_graph.png')
'''

def LoadData(filename):
    # gameFile = open(filename, encoding="utf8")
    # lst = gameFile.read()
    # lst = lst.split('\n')
    # gameFile.close()
    # for i in range (len(lst)):
    #     lst[i] = lst[i].split('\t')
    #     lst[i][0] = int(lst[i][0])
    #     lst[i][-1] = evaluator(lst[i][-1])
    # return lst
    
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ",")
        lst = []
        for row in readCSV:
            lst.append(row)
    for i in range (len(lst)):
        # lst[i] = lst[i].split('\t')
        lst[i][0] = eval(lst[i][0])
        if lst[i][-1]=='.':
            lst[i][-1] = []
        elif lst[i][-1].isdigit():
            lst[i][-1] = [ast.literal_eval(lst[i][-1])]
        else:
            lst[i][-1] = ast.literal_eval(lst[i][-1])
    csvfile.close()
    return(lst)

def createGraph(dataList):
    G = {}
    global infoList
    for nodeData in dataList:
        addNodes(G, nodeData[0])
        infoList.append(nodeData[1:5])
        if nodeData[3] in ['choices', 'karma']:
            for tup in nodeData[-1]:
                addEdges(G, (nodeData[0],tup[0],tup[1:]))
        else:
            for node in nodeData[-1]:
                addEdges(G, (nodeData[0], node))
    return G

# print(dataList)

# print()
# pprint.pprint(G)
# pprint.pprint(infoList)

def Wrap_text(text, font, color):
    text = text.split()
    newText = ""
    array = []
    for word in text:
        newText = newText + " " + word
        new_game_Text = font.render(newText, True, color)
        if 800 <= new_game_Text.get_width():
            array.append(old_game_Text)
            newText = ""
        old_game_Text = new_game_Text
    array.append(old_game_Text)
    return array

def choices_buttons(choices, font, color = (28, 28, 28)):
    array = []
    for choice in choices: 
        text = font.render(choice[1], True, color)
        array.append((text, text.get_width() + 40, 500 - text.get_width()//2, choice[0], choice[-1]))
    return array
        

def display(G, node, screen, karma = 0, condition = True):
    running = True
    condition = 0
    pygame.mixer.music.load('music\\'+infoList[node][1])
    pygame.mixer.music.play(-1)
    bg = pygame.image.load('backgrounds\\'+infoList[node][0])
    ScoreText = ScoreFont.render("Score : {}".format(karma), True, (250,250,250))
    
    color = (207, 248, 240)
    nextPressed = False
    endPressed = False
    next_y = 400
    next_x = 830
    next_h = 50
    next_w = 120
    nextText = buttonFont.render("Next", True, buttonTxtColor)
    endText = buttonFont.render("End", True, buttonTxtColor)

    backPressed = False
    back_y = 400
    back_x = 50
    back_h = 50
    back_w = 120
    backText = buttonFont.render("Back", True, buttonTxtColor)
    
    mainText = Wrap_text(infoList[node][3], textFont, color)
    
    if infoList[node][2] == "choices":
        choice_List = choices_buttons(G[node], choiceFont, choiceTxtColor)

    while running:
        screen.blit(bg,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 2
        if nextPressed:
            nextPressed = False
            if infoList[node][2] == "straight" or infoList[node][2] == "start":
                condition = display(G, G[node][0][0], screen, karma)
            if infoList[node][2] == "choices":
                condition = display(G, choice, screen, karma + karma_change)
            if infoList[node][2] == "karma":
                for i in range(len(G[node])):
                    if eval(str(karma)+G[node][i][2]):
                        condition = display(G,G[node][i][0],screen, karma) 
        if endPressed:
            return 1
        if backPressed:
            backPressed = False
            running = False
            return 0
        if condition == 0:
            pass
        if condition in [1,2]:
            return condition

        y = 50
        for i in mainText:
            screen.blit(i,(100,y))
            y += 30
        screen.blit(ScoreText, (50 - ScoreText.get_width() // 2, 20 - ScoreText.get_height() // 2))

        # Choices Buttons
        
        if infoList[node][2] == "choices":
            choice_y = 250
            choice_h = 50
            for j in choice_List:
                #Choice Buttons
                if j[2] <= pygame.mouse.get_pos()[0] <= j[2]+j[1] and choice_y <= pygame.mouse.get_pos()[1] <= choice_y + choice_h:
                    if pygame.mouse.get_pressed()[0]:
                        pygame.draw.rect(screen, choiceOnClick, pygame.Rect(j[2], choice_y, j[1], choice_h))
                        time.sleep(0.5)
                        choice = j[3]
                        karma_change = j[-1]
                        nextPressed = True
                    else:
                        pygame.draw.rect(screen, choiceHover, pygame.Rect(j[2], choice_y, j[1], choice_h))
                else:
                    pygame.draw.rect(screen, choiceColor, pygame.Rect(j[2], choice_y, j[1], choice_h))
                pygame.draw.rect(screen, (38, 38, 38), pygame.Rect(j[2]+5, choice_y+5, j[1]-10, choice_h-10) )
                screen.blit(j[0], (j[2] + (j[1] - j[0].get_width()) // 2, choice_y + (choice_h - j[0].get_height()) // 2))
                choice_y += 75
        else:   
            # Next Button
            if next_x <= pygame.mouse.get_pos()[0] <= next_x+next_w and next_y <= pygame.mouse.get_pos()[1] <= next_y + next_h:
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(screen, backPressed, pygame.Rect(next_x, next_y, next_w, next_h))
                    time.sleep(0.5)
                    if infoList[node][2] == "end":
                        endPressed = True
                    else:
                        nextPressed = True
                else:
                    pygame.draw.rect(screen, button_hover, pygame.Rect(next_x, next_y, next_w, next_h))
            else:
                pygame.draw.rect(screen, button_idle, pygame.Rect(next_x, next_y, next_w, next_h))
            pygame.draw.rect(screen, white, pygame.Rect(next_x+5, next_y+5, next_w-10, next_h-10) )
            if infoList[node][2] == "end":
                screen.blit(endText, (next_x + (next_w - endText.get_width()) // 2, next_y + (next_h - endText.get_height()) // 2))
            else:
                screen.blit(nextText, (next_x + (next_w - nextText.get_width()) // 2, next_y + (next_h - nextText.get_height()) // 2))
        
        # Back Button
        if back_x <= pygame.mouse.get_pos()[0] <= back_x+next_w and back_y <= pygame.mouse.get_pos()[
            1] <= back_y + back_h:
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(screen, button_onclick, pygame.Rect(back_x, back_y, back_w, back_h))
                time.sleep(0.5)
                backPressed = True
            else:
                pygame.draw.rect(screen, button_hover, pygame.Rect(back_x, back_y, back_w, back_h))
        else:
            pygame.draw.rect(screen, button_idle, pygame.Rect(back_x, back_y, back_w, back_h))
        pygame.draw.rect(screen, white, pygame.Rect(back_x+5, back_y+5, back_w-10, back_h-10) )
        screen.blit(backText, (back_x + (back_w - backText.get_width()) // 2, back_y + (back_h - backText.get_height()) // 2))

        pygame.display.flip()
    


# all_fonts = pygame.font.get_fonts()
# for font in all_fonts:
#     print(font)



def startScreen():
    done = False
    condition = 0
    titleText = titleFont.render("Adaptive Story Game", True, (250,250,250))
    startText = buttonFont.render("Start", True, buttonTxtColor)
    quitText = buttonFont.render("Quit", True, buttonTxtColor)
    pygame.mixer.music.load('music\\unsure(2).mp3')
    pygame.mixer.music.play(-1)
    for i in range(101):
        pygame.mixer.music.set_volume(i/20)
        screen.fill(((i/200)*28, (i/200)*52, (i/200)*52))
        pygame.display.flip()
        time.sleep(0.005)
    bg = pygame.image.load('backgrounds\\bg.png')

    startPressed = False
    quitPressed = False

    while not done:
        screen.blit(bg,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        if not pygame.mouse.get_pressed()[0]:
            if startPressed:
                startPressed = False
                condition = display(G, list(G.keys())[0], screen)
            if quitPressed:
                return
            if condition == 2:
                return


        buttonsHeight = 200

        #Start Button
        if 420 <= pygame.mouse.get_pos()[0] <= 580 and buttonsHeight <= pygame.mouse.get_pos()[
            1] <= buttonsHeight+50:
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(screen, button_onclick, pygame.Rect(420, buttonsHeight, 160, 50))
                startPressed = True
            else: pygame.draw.rect(screen, button_hover, pygame.Rect(420, buttonsHeight, 160, 50))
        else: pygame.draw.rect(screen, button_idle, pygame.Rect(420, buttonsHeight, 160, 50))

        #Quit Button
        if 420 <= pygame.mouse.get_pos()[0] <= 580 and buttonsHeight+100 <= pygame.mouse.get_pos()[
            1] <= buttonsHeight+150:
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(screen, button_onclick, pygame.Rect(420, buttonsHeight+100, 160, 50))
                quitPressed = True
            else:
                pygame.draw.rect(screen, button_hover, pygame.Rect(420, buttonsHeight+100, 160, 50))
        else: pygame.draw.rect(screen, button_idle, pygame.Rect(420, buttonsHeight+100, 160, 50))

        pygame.draw.rect(screen, white, pygame.Rect(425, buttonsHeight+5, 150, 40))
        pygame.draw.rect(screen, white, pygame.Rect(425, buttonsHeight+105, 150, 40))

        screen.blit(startText, (500 - startText.get_width() // 2, buttonsHeight+25 - startText.get_height() // 2))
        screen.blit(quitText, (500 - quitText.get_width() // 2, buttonsHeight+125 - quitText.get_height() // 2))
        screen.blit(titleText, (500 - titleText.get_width() // 2, 100- titleText.get_height() // 2))

        pygame.display.flip()

def fileSelectionMenu():
    def read():
        print('command')
        global story
        story = storychosen.get()

    fileList = [f[:-4][6:] for f in glob.glob("games\\*.csv")]
    window = tk.Tk()
    window.title('Adaptive Story Game')
    window.geometry('500x250')

    tk.Label(window, text="Select your story", background='green', foreground="white",font=("alienencounters", 15)).pack()

    storychosen = ttk.Combobox(window, width=27)
    storychosen.pack()
    storychosen['values'] = fileList

    tk.Button(window, text = 'Enter', command = read).pack()
    window.mainloop()
    return


story = ''
infoList = []
fileSelectionMenu()
dataList = LoadData('games\\'+story+'.csv')
pprint.pprint(dataList)
G = createGraph(dataList)
pprint.pprint(G)

pygame.init()
screen = pygame.display.set_mode((1000, 500))
buttonFont = pygame.font.SysFont("nasalization", 30)
textFont = pygame.font.SysFont("perpetua", 30)
titleFont = pygame.font.SysFont("alienencounters", 50)
ScoreFont = pygame.font.SysFont("gillsansnova", 30)
choiceFont = pygame.font.SysFont("gillsansnova", 30)
buttonTxtColor = (8, 99, 117)
button_idle = (8, 99, 117)
button_hover = (63, 212, 242)
button_onclick = (182, 238, 250)
white = (250,250,250)
choiceTxtColor = white
choiceColor = (101, 101, 101)
choiceHover = (184, 248, 95)
choiceOnClick = (152, 152, 152)

startScreen()
pygame.quit()
