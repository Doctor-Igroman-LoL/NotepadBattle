 # -*- coding: utf_8 -*-
# ~~o~~o~~o~~o~~o~~o Класс хп и мп бара o~~o~~o~~o~~o~~o~~ #
from direct.showbase.ShowBase import ShowBase   
from direct.task import Task   
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from panda3d.core import *

class UI_Bar():

    def __init__(self, name, point, position, scale=1):
        self.font = loader.loadFont('Xarrovv.ttf')
        self.name = name
        self.point = point
        self.pos = position
        self.scale = scale
        self.minMaxPoint()
        self.posBar = self.setElement('hpbar', (-.11 + self.pos[0], 0, self.pos[1]), (.15 * self.scale, 0 ,.03 * self.scale))
        self.posBall = self.setElement('hpball', (self.findingX(self.point) + self.pos[0], 0, self.pos[1]), .03 * self.scale)
        self.posText = self.setDisplayPoint((.15 + self.pos[0], -.02 + self.pos[1]), .055 * self.scale)

    def updateBar(self, point):
        self.minMaxPoint()
        self.posBall.setPos(self.findingX(point) + self.pos[0], 0 ,self.pos[1])
        self.posText.setText(self.value100proc(point))

    def minMaxPoint(self):
        self.minPoint = -0.67 + self.pos[0]
        self.maxPoint = -0.41 + self.pos[0]           

    def value100proc(self, point):
        name = str(int(point * 100)) + '% ' + self.name
        return name

    def findingX(self, point):
        x = self.maxPoint - (point * self.range(self.minPoint, self.maxPoint))
        return x

    def range(self, minPoint, maxPoint):
        return abs(minPoint - maxPoint)

    def setElement(self, nameImage, position, scaleImage, colorImage=(1,1,1,1)):
        name = 'images/' + str(nameImage) + '.png'
        images = OnscreenImage(image = name, pos = position, scale = scaleImage, color=colorImage)
        images.setTransparency(TransparencyAttrib.MAlpha)
        return images

    def setDisplayPoint(self, position, scale=0.08):
        name = self.value100proc(self.point)
        return OnscreenText(text = name, pos = position, font = self.font, 
        scale = scale, align=TextNode.ACenter, mayChange=1)

uiBar = UI_Bar
