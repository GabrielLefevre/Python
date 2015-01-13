#Version 1.2
#ajout ligne test
#Gabriel lefevre & Alexandre Pavy
#test commit conflit
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


Builder.load_file("example.kv");

class ZoneJeu(Widget):
    G = False
    path = False
    bestScore=ObjectProperty("0")
    
    gridSize = [18,13]
    def __init__(self,**kwargs):
        super(ZoneJeu,self).__init__(**kwargs)
        self.cases = []
        self.casesPath =[]
        self.colorGrid = (random(),random()) 
        self.bestScore = "0"
        
    def test(self):
        with self.canvas:
            self.casesPath =[]
            self.cases = []
            global aleax
            global aleay
            aleax= randint(0,self.size[0])
            aleay= randint(0,self.size[1])
            self.colorAlea()
            for i in range(self.gridSize[0]):#X
                tmp = []
                for j in range(self.gridSize[1]):#Y
                    tmp.append(Case2(self.colorGrid,pos=[i*41+30,j*41+50],size=[40,40]))
                self.cases.append(tmp)
            self.generateGraph()
            #C.r = 0;
    def colorAlea(self):
        self.colorGrid = (random(),random())
    def changeColor(self):
        self.colorAlea()
        for i in self.cases:
            for j in i:
                j.update(self.colorGrid);
                
    def generateGraph(self):
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
        self.path=nx.dijkstra_path(self.G,source=(0,self.gridSize[1]-1),target=(self.gridSize[0]-1,0))
        self.bestScore=str(nx.dijkstra_path_length(self.G,source=(0,self.gridSize[1]-1),target=(self.gridSize[0]-1,0)))
        #nx.draw(self.G)
        #plt.show()
         
    def drawPath(self):
        for c in self.path:
            self.cases[c[0]][c[1]].setColor(1,1,1)
            
    def affGraph(self):
        nx.draw(self.G)
        plt.show()
        

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
    #first = ObjectProperty()
    pass
        
if __name__ == "__main__":
    grapheColor().run()