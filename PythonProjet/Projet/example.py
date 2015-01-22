from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color
from random import *
import matplotlib.pyplot as plt
import copy

import networkx as nx
import math

global aleax
global aleay


Builder.load_file("example.kv");

class ZoneJeu(Widget): 
    G = False
    path = False
    bestScore=ObjectProperty("0")
    score=ObjectProperty("0")
    gridSize = [13,13]
    def __init__(self,**kwargs):
        super(ZoneJeu,self).__init__(**kwargs)
        self.cases = []
        self.casesPath =[]
        self.colorGrid = (random(),random()) 
        self.bestScore = "0"
        self.solution = False
        self.score="0"
        
    def test(self):
        with self.canvas:
            self.path=[]
            self.solution = False
            self.casesPath =[]
            self.score="Score : 0"
            self.cases = []
            global aleax
            global aleay
            aleax = randint(0, self.size[0])
            aleay = randint(0, self.size[1])
            self.colorAlea()
            for i in range(self.gridSize[0]):#X
                tmp = []
                for j in range(self.gridSize[1]):#Y
                    tmp.append(Case2(self.colorGrid,pos=[i*41+30,j*41+50],size=[39,39]))
                self.cases.append(tmp)
            self.generateGraph()
            self.getLengthPath()
    def colorAlea(self):
        self.colorGrid = (random()/2.0,random()/2.0)

    def changeColor(self):
        if len(self.cases) > 0:
            # Change la couleur du graphe
            self.colorAlea()
            for i in self.cases:
                for j in i:
                    j.update(self.colorGrid)
            if (self.solution):
                self.affMeilleurChemin()
            self.affPath()
        
    def getLengthPath(self):
        # Permet de recuprer davoir le chemin de lutilisateur
        length=0.0
        if(len(self.path)<2):
            return 0;
        
        for i in range(1,len(self.path)):
            length += self.G[self.path[i-1]][self.path[i]]['weight']
        return int(length*2550)
                
    def generateGraph(self): 
        #Creation du graphe de notre jeu et creation du chemin optimal avec Dijkstra
        self.casesPath =[]
        self.G=nx.Graph()       
        for i in range(self.gridSize[0]):#X
            for j in range(self.gridSize[1]):#Y
                self.G.add_node((i,j))
        for i in range(self.gridSize[0]):#X
            for j in range(self.gridSize[1]):#Y
                if(i-1>=0):
                    self.G.add_edge((i,j),(i-1,j),weight=self.cases[i][j].getWeight(self.cases[i-1][j]))
                if(i+1<self.gridSize[0]):
                    self.G.add_edge((i,j),(i+1,j),weight=self.cases[i][j].getWeight(self.cases[i+1][j]))
                if(j-1>=0):
                    self.G.add_edge((i,j),(i,j-1),weight=self.cases[i][j].getWeight(self.cases[i][j-1]))
                if(j+1<self.gridSize[1]):
                    self.G.add_edge((i,j),(i,j+1),weight=self.cases[i][j].getWeight(self.cases[i][j+1]))
                    
        self.bestPath=nx.dijkstra_path(self.G,source=(0,self.gridSize[1]-1),target=(self.gridSize[0]-1,0))
        self.bestScore="Meilleur score: "+str(int(nx.dijkstra_path_length(self.G,source=(0,self.gridSize[1]-1),target=(self.gridSize[0]-1,0))*2550))
    
    def affMeilleurChemin(self):
        if len(self.cases) > 0:
            #permet d avoir le meilleur chemin 
            self.solution = True
            for c in self.bestPath:
                self.cases[c[0]][c[1]].setColor(1,1,1)
            
    def affPath(self):
        # affiche le chemin de l utilisateur
        for c in self.path:
            self.cases[c[0]][c[1]].setColor(0,1,0)
            
        
    def affGraph(self):
        # affiche le graphe de matplolib
        if len(self.cases) > 0:
            nx.draw(self.G)
            plt.show()
        
    def addOnPath(self,x,y):
        # permet dajouter un noeud au chemin de lutilisateur
        if((x,y) in self.path):
            return;
        
        if(len(self.path)==0):
            if(x==0 and y ==self.gridSize[1]-1):
                self.path.append((x,y));
                self.cases[x][y].setColor(0,1,0);  
                return;
            else:
                return
        if(abs(x-self.path[len(self.path)-1][0])+abs(y-self.path[len(self.path)-1][1])>1):
            return;       
        
        self.path.append((x,y));
        self.cases[x][y].setColor(0,1,0);  
        self.score="Score : "+str(self.getLengthPath())
        
            
    def clickOnCase(self,x,y):
        # evenement du clique sur un case
        pos=[0,0];
        pos[0]=int((x-30)/41);
        pos[1]=int((y-50)/41);
        if(pos[0]<0):
            return;
        if(pos[1]<0):
            return;
        if(pos[0]>self.gridSize[0]-1):
            return;
        if(pos[1]>self.gridSize[1]-1):
            return;
        self.addOnPath(pos[0],pos[1])

                
    # evenement des cliques
    def on_touch_move(self, touch):
        self.clickOnCase(touch.x,touch.y)
    def on_touch_down(self, touch):
        self.clickOnCase(touch.x,touch.y)

            


class Case2(Widget):
    r=ObjectProperty(random())
    g=ObjectProperty(random())
    b=ObjectProperty(random())
    
    def __init__(self,color,**kwargs):
        super(Case2,self).__init__(**kwargs)
        global aleax
        global aleay
        self.b = ((math.sin(float(self.center_x+aleax)/100.0)+1)+(math.cos(float(self.center_y+aleay)/100.0)+1))/8.0 
        self.b = self.b*3/4.0 + random()/4.0
        self.update(color)
    def update(self,color):
        self.r = color[0]
        self.g = color[1]
    def getColor(self):
        return [self.r,self.g,self.b]
    def setColor(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b
    def getWeight(self,case):
        c2 = case.getColor()
        c1 = self.getColor()
        s=0
        for i in range(3):
            s+= (c1[i]-c2[i])*(c1[i]-c2[i])
        t=math.sqrt(s)
        return t
    

    
class grapheColor(App):
    
    def build(self):
        panneau = Panneau()
        return panneau
        
class Panneau(GridLayout):
    zone = ObjectProperty()
    pass
        
if __name__ == "__main__":
    grapheColor().run()