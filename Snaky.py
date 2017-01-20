#-------------------------------------------------------------------------------
# Name:        Snaky
# Purpose:
#
# Author:      Axel BERTRAND, Victor 
#
# Created:     27/02/2015
# Copyright:   (c) Axel BERTRAND, Victor  2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from tkinter import*
import random
import os

# Fonction d'initialisation
def init() :
   # Initialisation des variables
    global u, v, score, a, b, s, n, fruit, rectmenu, direction, lx, ly, serpent, color, fichmode, decors
    s = score = a = b = direction = 0
    n = 1
    decors = lisdecors(fichmode)
    dessine()
    rand1 = 25*random.randint(3, 27) + 2
    rand2 = 25*random.randint(3, 27) + 2
    while decors[int((rand2 - 2)/25)][int((rand1 - 2)/25)] == "X" or decors[int((rand2 + 23)/25)][int((rand1 - 2)/25)] == "X" :
        rand1 = 25*random.randint(3, 27) + 2
        rand2 = 25*random.randint(3, 27) + 2
    lx , ly = [rand1, rand1 + 25], [rand2, rand2 + 25]
    u , v = 25*random.randint(3, 27) + 2, 25*random.randint(3, 27) + 2
    while decors[int((v - 2)/25)][int((u - 2)/25)] == "X" :
        u , v = 25*random.randint(3, 27) + 2, 25*random.randint(3, 27) + 2
    rectmenu = C.create_rectangle(1500, 1500, 1500, 1500, fill = "gray")

    # Affichage du serpent
    tete = C.create_rectangle(lx[0], ly[0], lx[1], ly[1], fill = "dark" + color)
    corps = C.create_rectangle(lx[0], ly[0] + 25, lx[1], ly[1] + 25, fill = color)
    C.tag_lower(tete)
    C.tag_lower(corps)
    serpent = []
    serpent.append(tete)
    serpent.append(corps)

    # Creation du premier fruit
    fruit = C.create_oval(u + 5, v + 5, u + 20, v + 20, fill = "red")
    C.tag_lower(fruit)

    # Affichage du score
    scores.set("0")

# Fonction de deplacement du serpent
def deplacement() :
    global lx, ly, serpent, score, a, b, delai, decors, fichmode, x, y
    if direction == 1 : # Haut
        x = 0
        y = -25
    if direction == 2 : # Droite
        x = 25
        y = 0
    if direction == 3 : # Bas
        x = 0
        y = 25
    if direction == 4 : # Gauche
        x = -25
        y = 0

    # Les coordonnees du dernier carre sont remplacees par celles de l'avant dernier carre jusqu'a la tete
    for i in range(len(serpent) - 1, 0, -1) :
        lx[i] = lx[i - 1]
        ly[i] = ly[i - 1]

    # On change les coordonees de la tete
    lx[0] = lx[0] + x
    ly[0] = ly[0] + y

    # On applique les nouvelles coordonnees aux carres correspondant
    for i in range(len(serpent)) :
        C.coords(serpent[i], lx[i], ly[i], lx[i] + 25, ly[i] + 25)

    # Si le serpent arrive d'un cote il ressort de l'autre
    if lx[0] >= 752 :
        lx[0] = 2
    if lx[0] <= 1 :
        lx[0] = 727
    if ly[0] >= 752 :
        ly[0] = 2
    if ly[0] <= 1 :
        ly[0] = 727

    # Si les coordonnees de la tete sont egales a celle d'un morceau du serpent le jeu s'arrete
    for i in range(1, len(serpent)) :
        if lx[i] == lx[0] and ly[i] == ly[0] :
            a = 1
            perdu()

    # Si la tete touche un element du decor le jeu s'arrete
    if decors[int((ly[0] - 2)/25)][int((lx[0] - 2)/25)] == "X" :
        a = 1
        perdu()

    # Si la tete touche le fruit le score augmente, le serpent s'agrandit d'un carre et un nouveau fruit apparait aleatoirement
    if u == lx[0] and v == ly[0] :
        score = score + 100
        scores.set(str(score))
        manger()

    if a != 1 and b != 1:
        fenetre.after(delai, deplacement)

# Cette fonction cree un cercle de coordonees multiple de 25 pour eviter que le cercle soit partiellement coupe par le serpent
def manger() :
    global u, v, n, lx, ly, serpent, color, x, y
    u = 25*random.randint(3, 27) + 2
    v = 25*random.randint(3, 27) + 2
    for i in range(1, len(serpent)) :
        while u == lx[i] and v == ly[i] :
            u = 25*random.randint(3, 27) + 2
            v = 25*random.randint(3, 27) + 2
    while decors[int((v - 2)/25)][int((u - 2)/25)] == "X" :
        u = 25*random.randint(3, 27) + 2
        v = 25*random.randint(3, 27) + 2
    C.coords(fruit, u + 5, v + 5, u + 20, v + 20)
    # On ajoute un carre hors du canevas (pour alleger le code) qui se rajoutera a la suite
    corps = C.create_rectangle(1500, 1500, 1525, 1525, fill = color)
    C.tag_lower(corps)
    serpent.append(corps)
    lx.append(lx[n] + 25)
    ly.append(ly[n] + 25)
    n = n + 1

# Fonctions de direction permettant le deplacement du serpent dans les 4 directions
# grace aux modifications successives des coordonees du premier carree grace au valeur x et y
# La valeur s permet de ne pas accelerer la vitesse du serpent ou de modifier sa direction
# en appuyant successivement sur Haut/Bas/Gauche/Droite
def haut(evt) :
    global s, direction
    if direction != 3:
        direction = 1
        if s == 0 :
            s = 1
            deplacement()

def droite(evt) :
    global s, direction
    if direction != 4:
        direction = 2
        if s == 0 :
            s = 1
            deplacement()

def bas(evt) :
    global s, direction
    if direction != 1:
        direction = 3
        if s == 0 :
            s = 1
            deplacement()

def gauche(evt) :
    global s, direction
    if direction != 2:
        direction = 4
        if s == 0 :
            s = 1
            deplacement()

def perdu() :
    global nouveau, quitter
    C.create_rectangle(177, 227, 577, 527, fill = "gray")
    C.create_text(370, 280, text = "Vous avez perdu", font = ("Times", 25, "bold"))
    nouveau.place(x = 275, y = 380)
    quitter.place(x = 275, y = 480)

# Fonction pour mettre en pause
def pause(evt) :
    global a, b, direction, texte
    if a != 1 : # a = 0 : en jeu, a = 1 : perdu
        # Affichage ou Effacement du texte "PAUSE"
        # Et arret du serpent
        if b != 1: # b = 0 : pause desactivee, b = 1 : pause activee
            b = 1
            texte = C.create_text(375, 375, text = "PAUSE", font = ("Calibri", 25, "bold"))
        else:
            b = 0
            C.delete(texte)
            if direction != 0 :
                deplacement()

# Fonction pour recommencer la partie
def recommencer():
    C.delete(ALL)
    nouveau.place_forget()
    quitter.place_forget()
    init()
    mode()

# Fonction pour afficher les regles sur la page html
def regle() :
    os.startfile("page_html_snake.html")

# Fonction pour changer le mode de jeu
def mode() :
    global var1, fichmode
    if var1.get() == 0 :
        fichmode = "snake_ouvert.txt"
    elif var1.get() == 1 :
        fichmode = "snake_ferme.txt"
    else :
        rand = random.randint(1, 6)
        fichmode = "snake_labyrinthe" + str(rand) + ".txt"

# Fonction pour changer le niveau de difficulte
def difficulty() :
    global var2, delai
    if var2.get() == 0 :
        delai = 200
    elif var2.get() == 1 :
        delai = 100
    else :
        delai = 50

# Fonction pour personnaliser le serpent
def personnalisation() :
    global var3, color
    if var3.get() == 0 :
        color = "green"
    elif var3.get() == 1 :
        color = "blue"
    else :
        color = "red"
    C.itemconfig(serpent[0], fill = "dark" + color)
    for i in range (1, len(serpent)) :
        C.itemconfig(serpent[i], fill = color)

# Fonction qui lis le contenu du fichier texte et le place dans la liste 2D decors
def lisdecors(fichier) :
    fich = open(fichier, "r")
    R = [list(ligne.replace("\n","")) for ligne in fich]
    fich.close()
    return R

# Fonction qui dessine le plateau de jeu avec la liste decors
def dessine() :
    global decors
    for ligne in range(30) :
        for colonne in range(30) :
            if decors[ligne][colonne] == "X" :
                C.create_rectangle(25*colonne + 2, 25*ligne + 2, 25*(colonne + 1) + 2, 25*(ligne + 1) + 2, fill = "black")

# Affichage de la fenetre
fenetre = Tk()
fenetre.title("Snaky")
fenetre.geometry(str(fenetre.winfo_screenwidth()) + "x" + str(fenetre.winfo_screenheight()))
fenetre.resizable(height = "false", width = "false")

# On initialise les variables des radiobuttons
var1 = IntVar()
var2 = IntVar()
var2.set(1)
var3 = IntVar()

# On definit la barre de menu
menubar = Menu(fenetre)

# On definit un menu defilant
optionmenu = Menu(menubar, tearoff = 0)

# On cree trois menu defilants dans le menu defilant "optionmenu"
# Menu mode
modemenu = Menu(optionmenu, tearoff = 0)
modemenu.add_command(label = "Modes de jeu", state = DISABLED)
modemenu.add_separator()
modemenu.add_radiobutton(label = "Mode ouvert", variable = var1, value = 0, command = mode)
modemenu.add_radiobutton(label = "Mode ferme", variable = var1, value = 1, command = mode)
modemenu.add_radiobutton(label = "Mode labyrinthe", variable = var1, value = 2, command = mode)
optionmenu.add_cascade(label = "Modes de jeu", menu = modemenu)

# Menu difficulte
diffmenu = Menu(optionmenu, tearoff = 0)
diffmenu.add_command(label = "Difficulte", state = DISABLED)
diffmenu.add_separator()
diffmenu.add_radiobutton(label = "Facile", variable = var2, value = 0, command = difficulty)
diffmenu.add_radiobutton(label = "Normal", variable = var2, value = 1, command = difficulty)
diffmenu.add_radiobutton(label = "Difficile", variable = var2, value = 2, command = difficulty)
optionmenu.add_cascade(label = "Difficulte", menu = diffmenu)

# Menu personnalisation
persomenu = Menu(optionmenu, tearoff = 0)
persomenu.add_command(label = "Couleurs", state = DISABLED)
persomenu.add_separator()
persomenu.add_radiobutton(label = "Vert", variable = var3, value = 0, command = personnalisation)
persomenu.add_radiobutton(label = "Bleu", variable = var3, value = 1, command = personnalisation)
persomenu.add_radiobutton(label = "Rouge", variable = var3, value = 2, command = personnalisation)
optionmenu.add_cascade(label = "Personnalisation", menu = persomenu)

# On cree les menu de la barre de menu
menubar.add_command(label = "Nouveau", command = recommencer)
menubar.add_cascade(label = "Options", menu = optionmenu)
menubar.add_command(label = "Regles", command = regle)
menubar.add_command(label = "Quitter", command = fenetre.destroy)

# On cree le canva
C = Canvas(fenetre, height = 751, width = 751, bg = "white")
C.place(x = 50, y = 50)

# On initialise les variables
scores = StringVar()
color = "green"
delai = 100
fichmode = "snake_ouvert.txt"
init()

nouveau = Button(fenetre, text = "Nouvelle Partie", width = 18, font = ("Times", 20, "bold"), command = recommencer)
quitter = Button(fenetre, text = "Quitter", width = 18, font = ("Times", 20, "bold"), command = fenetre.destroy)

Label(fenetre, text = "Score :", font = ("Times", 20, "bold")).place(x = 900, y = 200)
Label(fenetre, textvariable = scores, font = ("Times", 20, "bold")).place(x = 900, y = 250)
Label(fenetre, text = "Echappe : Pause", font = ("Times", 20, "bold")).place(x = 900, y = 100)

# Gestion de la direction
C.bind_all('<Up>', haut)
C.bind_all('<Down>', bas)
C.bind_all('<Left>', gauche)
C.bind_all('<Right>', droite)
C.bind_all('<Escape>', pause)

fenetre.config(menu = menubar)
fenetre.mainloop()

# Portable : 1600x900
# Lycee : 1440x900

# Inspiration : http://codes-sources.commentcamarche.net/source/51022-jeu-du-serpent-snake
# Image de fond site : dreamstime