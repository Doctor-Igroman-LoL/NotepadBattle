class UI_Bar:

    def __init__(self, name, point, position, scale=1):
        self.font = loader.loadFont('Xarrovv.ttf')
        self.name = name
        self.point = point
        self.position = position
        self.scale = scale
        self.posBar(self.name, self.point, self.position, self.scale)

    def posBar(self, name, point, pos, scale):
        minPoint = -0.67 + pos[0]
        maxPoint = -0.41 + pos[0]
        x = maxPoint - (point * self.range(minPoint, maxPoint))
        posBar = self.setElement('hpbar', (-.11 + pos[0], 0, pos[1]), (.15 * scale, 0 ,.03 * scale))
        posBall = self.setElement('hpball', (x + pos[0], 0, pos[1]), .03 * scale)
        posText = self.setDisplayPoint(point, name, (.15 + pos[0], -.02 + pos[1]), .055 * scale)

    def range(self, minPoint, maxPoint):
        return abs(minPoint - maxPoint)

    def setElement(self, nameImage, position, scaleImage, colorImage=(1,1,1,1)):
        name = 'images/' + str(nameImage) + '.png'
        images = OnscreenImage(image = name, pos = position, scale = scaleImage, color=colorImage)
        return images.setTransparency(TransparencyAttrib.MAlpha)

    def setDisplayPoint(self, count, text, position, scale=0.08):
        name = str(count) + '% ' + text
        return OnscreenText(text = name, pos = position, font = self.font, 
        scale = scale, align=TextNode.ACenter, mayChange=1)

