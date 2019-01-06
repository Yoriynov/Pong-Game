# Le célèbre jeu "Pong" codé par mes soins (enfin, j'ai essayé)
from tkinter import *
class Raquette(object):
    """Créer un rectangle (la raquette) et inclus la méthode de déplacement
    Il faut donner un parametre si on veut jouer à deux. Par défaut, le
    jeu se fait contre un mur.
    """
    def __init__(self, boss, x, y):
        self.boss = boss    # la ref de la fenêtre
        #création d'une raquette
        self.x = x
        self.y = y
        self.raq = boss.create_rectangle(self.x , self.y,
                                         self.x+10, self.y+60, fill='white')
        self.filet = boss.create_line(400, 0, 400, 480, fill='light grey',
                                      dash=(20, 10))
    def monter(self, depl):
        self.y -=10
        if self.y <=0:    # on contrôle que l'on ne sort pas du tableau
            self.y =0
        self.boss.coords(self.raq, self.x, self.y, self.x+10, self.y+60)
    def descendre(self, depl):
        self.y +=10
        if self.y >=420:    # on contrôle que l'on ne sort pas du tableau
            self.y =420
        self.boss.coords(self.raq, self.x, self.y, self.x+10, self.y+60)
class Balle(object):
    """Créer la balle et sa méthode de déplacement"""
    def __init__(self, boss, player1, player2,
                 compteur, scorep1, scorep2):
        self.boss = boss    #ref de la fenêtre
        self.player1 = player1
        self.player2 = player2
        # coordonnées initiales
        self.x, self.y = 400, 240
        self.rayon = 10    # rayon de la balle
        # création de la balle
        self.balle = boss.create_oval(self.x-self.rayon,
                                      self.y-self.rayon,
                                      self.x+self.rayon,
                                      self.y+self.rayon, fill='white')
        # déplacement initial
        self.dx, self.dy = 10, 10
        #compteur
        self.compteur = compteur
        self.scorep1 = scorep1
        self.scorep2 = scorep2
    def move(self):
        "Déplacement de la balle"
        self.flag = 1
        self.x += self.dx
        self.y += self.dy
        # On regarde si la balle tape à gauche où à droite
        if self.x <= 0:
            self.x =400    # balle au centre
            self.dx = -self.dx    # renvoi de l'autre côté
            self.scorep2 += 1    # on ajoute un point à p2
            compt = str(self.scorep1) + "   " + str(self.scorep2)
            self.boss.itemconfigure (self.compteur, text=compt)
        if self.x >= 800:
            self.x =400
            self.dx = -self.dx
            self.scorep1 += 1
            compt = str(self.scorep1) + "   " + str(self.scorep2)
            self.boss.itemconfigure (self.compteur, text=compt)
        # contrôle pour mettre fin à la partie
        if self.scorep1 ==5 or self.scorep2 ==5:
            self.flag =0
            self.boss.create_text(400, 240, text="Game over", fill='white',
                                  font=("Arial", "22" ))
        # Contrôles pour que la balle reste dans la zone (rebonds haut et bas)
        if self.y+self.rayon >=480 or self.y-self.rayon <= 0:
            self.dy = -self.dy
        # pour le rebond sur la raquette de player1
        if self.x-self.rayon <= 30:
            if self.y-self.rayon >= self.player1.y and\
            self.y+self.rayon <= self.player1.y+60:
                self.dx = -self.dx
        # pour le rebond sur la raquette de player2
        if self.x+self.rayon >= 770:
            if self.y-self.rayon >= self.player2.y and\
                    self.y+self.rayon <= self.player2.y+60:
                self.dx = -self.dx
        self.boss.coords(self.balle,
                         self.x-self.rayon,
                         self.y-self.rayon,
                         self.x+self.rayon,
                         self.y+self.rayon)
        # Récursivité pour animer la balle
        if self.flag == 1:
            self.boss.after(40, self.move)
class Application(Frame):
    """Fenêtre principale de l'application"""
    def __init__(self):
        Frame.__init__(self)
        self.master.title(">>> Pong <<<" )
        self.pack()
        self.jeu = Canvas(self, width =800, height =480, background ='black')
        self.jeu.pack()
        self.compteur = self.jeu.create_text(400, 20, text="0   0", fill='white',
                                             font=("Arial", "22" ))
        self.y = 210
        self.flag = 0
        self.aide = self.jeu.create_text(400, 100, text='Aide : \nRaquette\
gauche : a pour monter, z pour descendre\nRaquette droite : k pour monter,\
m pour descendre\np : pause, h : aide', fill='white', font =("Arial", "16" ))
        # score des joueurs
        self.scorep1 = 0
        self.scorep2 = 0
        player1 = Raquette(self.jeu, 20, self.y)
        player2 = Raquette(self.jeu, 770, self.y)
        self.balle = Balle(self.jeu, player1, player2,
                      self.compteur, self.scorep1, self.scorep2)
        # animation de la balle
        if self.flag == 1:
            self.balle.move()
        # on guette les touches a et z pour déplacer la raquette
        self.bind_all("a", player1.monter)
        self.bind_all("z", player1.descendre)
        self.bind_all("k", player2.monter)
        self.bind_all("m", player2.descendre)
        self.jeu.bind_all("h", self.displayAide)
        self.bind_all("p", self.pause)
    # si je ne met pas *arg, ça me met une erreur "takes exactly n positionnal
    # argument (n+1 given)", pourquoi ?
    def displayAide(self, *arg):
        if self.flag == 1:
            self.flag = 0
            self.aide = self.jeu.create_text(400, 100, text='Aide : \nRaquette\
gauche : a pour monter, z pour descendre\nRaquette droite : k pour monter,\
m pour descendre\np : pause, h : aide', fill='white', font =("Arial", "16" ))
        else:
            self.jeu.delete(self.aide)
            self.flag = 1
            self.balle.move()
    def pause(self, *arg):
        if self.flag ==1:
            self.flag = 0
        else:
            self.flag = 1
            self.balle.move()
if __name__ == '__main__':
    Application().mainloop()
