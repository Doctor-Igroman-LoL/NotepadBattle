 # -*- coding: utf_8 -*-
from direct.showbase.ShowBase import ShowBase   
from direct.task import Task   
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from panda3d.core import *
import time
#from ui_bar import UI_Bar

class MyApp(ShowBase): 

    def __init__(self):   
    	ShowBase.__init__(self)
        self.font = loader.loadFont('Xarrovv.ttf')
        #~~o~~o Загрузка фоновых элементов o~~o~~#
        self.background = self.setElement('background', (0, -2, 0), (1.5, 0 ,1))
        self.notebook = self.setElement('notebook', (0, -2, 0), (1.5, 0 ,1))
        self.loadButtoms() 
        self.save_timer = None
        self.status_timer = False
        self.turn = 'Player'
        self.list_action = ['Hello', 'Bye']
        
        # ~~o~~o~~o~~o~~o~~o Отображение Врага o~~o~~o~~o~~o~~o~~ #

        self.enemy = GameEnemy('Враг', 100, 3, 60)

        self.starRating = self.setStarRating(self.enemy.rank)            #~~o~~o Загрузка звездочек
        self.enemy_name = self.setDisplay(self.enemy.name, (-.25,0.3))   #~~o~~o Отображение имени врага

        self.display_box_enemy = self.setElement('box', (-.25, -2, .32), (.3, 0 ,.06)) #~~o~~o Загрузка рамочки

        self.enemy_hp_bar = UI_Bar('хп', self.enemy.converterHP(), [.43,.32])          #~~o~~o Загрузка хпбара
        
        # ~~o~~o~~o~~o~~o~~o Отображение Героя o~~o~~o~~o~~o~~o~~ #

        self.actor = GamePlaer('Герой', 300, 60, 30)
        self.actorAttack = self.actor.attack

        self.actor_name = self.setDisplay(self.actor.name, (-.25,-0.15)) #~~o~~o Отображение имени героя   
        self.display_box_actor = self.setElement('box', (-.25, -2, -.13), (.3, 0 ,.06)) #~~o~~o Загрузка рамочки  

        self.actor_hp_bar = UI_Bar('хп', self.actor.converterHP(), [.43,-.08])          #~~o~~o Загрузка хпбара
        self.actor_mp_bar = UI_Bar('мп', self.actor.converterMP(), [.43,-.15])          #~~o~~o Загрузка мпбара

        # ~~o~~o~~o~~o~~o~~o Отображение Действий o~~o~~o~~o~~o~~o~~ #
        
        #self.battle = GameBattle(self.actor, self.enemy)
        self.text_action = 'Доктор Баг представляет'
        self.actionDisplay = self.setDisplay(self.text_action, (0.02,0.09))             #~~o~~o Отображение действий
        self.actionDisplay['Wordwrap'] = (15)

        self.skillDisplay = self.setDisplay('', (0.02,-0.49), scale=0.06)           #~~o~~o Отображение описаний навыков
        self.skillDisplay['Wordwrap'] = (20)

        self.alive = taskMgr.add(self.alive, 'Alive?', extraArgs=[self.actor, self.enemy], appendTask=True)  #~~o~~o Проверка уровни хп
        self.battle = taskMgr.add(self.startBattle, 'Start Battle')                 #~~o~~o Запуск основного цикла битвы
          

    def loadButtoms(self):
        self.LoadAllButtons()       #~~o~~o Загрузка всех существующих кнопок. Активных и не активных
        self.basicSkills()          #~~o~~o Включение основного меню разделов навыков

    def LoadAllButtons(self):
        #~~o~~o Загрузка кнопок o~~o~~#
        self.btmAttack = self.setButtom(('Атака', '', 'Атаковать?', ''), self.attackMenu, (-.4, 0,-0.37))
        self.btmGuard = self.setButtom(('Защита', '', 'Защититься? ', ''), self.guard, (0, 0,-0.37))
        self.btmMagic = self.setButtom(('Магия', '', 'Колдовать? ', ''), self.magic, (.4, 0,-0.37)) 
        self.btmAttackSkill1 = self.setButtom(('Толчек', 'Толчек!!!', 'Толкнуть?', ''), self.damage, (-.4, 0,-0.37))
        self.btmAttackSkill2 = self.setButtom(('Уколоть', 'Удар!!!', 'Проткнуть?', ''), self.damage, (0, 0,-0.37))
        self.btmAttackSkill3 = self.setButtom(('Размахивать', 'Удар!!!', 'Атаковать?', ''), self.damage, (.4, 0,-0.37))   
        #self.btmAttack['text'] = ('1', '2', '3', '') #DGG.DISABLED  
        # ~~o~~o Настройка кнопок o~~o~~ #
        self.setButtomPresets(self.btmAttack, 'Здесь размещены атакующие скиллы')
        self.setButtomPresets(self.btmGuard, 'Здесь размещены защищающие скиллы')
        self.setButtomPresets(self.btmMagic, 'Здесь размещены магические скиллы') 
        self.setButtomPresets(self.btmAttackSkill1, 'Здесь размещены магические скиллы') 
        self.setButtomPresets(self.btmAttackSkill1, 'Здесь размещены магические скиллы') 
        self.setButtomPresets(self.btmAttackSkill1, 'Здесь размещены магические скиллы') 
        self.returnMenu([self.btmAttackSkill1, self.btmAttackSkill2, self.btmAttackSkill3]) 

    #~~o~~o основное меню разделов навыков o~~o~~#
    def basicSkills(self, x=''):
        self.buttonMenu('hide', [self.btmAttackSkill1,self.btmAttackSkill2,self.btmAttackSkill3])
        self.buttonMenu('show', [self.btmAttack,self.btmGuard,self.btmMagic])       

    #~~o~~o подменюшка навыка "атака", открывает еще три навыка атаки o~~o~~#
    def attackMenu(self):
        self.buttonMenu('hide', [self.btmAttack,self.btmGuard,self.btmMagic])
        self.buttonMenu('show', [self.btmAttackSkill1,self.btmAttackSkill2,self.btmAttackSkill3])

    def lockButtons(self):
        self.buttonMenu('hide', [
                                self.btmAttack,
                                self.btmGuard,
                                self.btmMagic,
                                self.btmAttackSkill1,
                                self.btmAttackSkill2,
                                self.btmAttackSkill3])

    #~~o~~o Показывает инфу навыка o~~o~~#
    def setButtomPresets(self, button, text):
        button.bind(DGG.WITHIN, self.skDisplay, extraArgs = [text])
        button.bind(DGG.WITHOUT, self.skDisplayClear)

    #~~o~~o ПКМ возвращает в предыдущие меню навыков o~~o~~#
    def returnMenu(self, listButton):
        [button.bind(DGG.B3PRESS, self.basicSkills) for button in listButton]   

    #~~o~~o Метод который прячит или показывает список кнопок o~~o~~#
    def buttonMenu(self, visible, listButton):
        if visible == 'show':
            [button.show() for button in listButton] 
        elif visible == 'hide':
            [button.hide() for button in listButton]

    #~~o~~o Метод для загрузки изображений и не большие настройки для удобства
    def setElement(self, nameImage, position, scaleImage, colorImage=(1,1,1,1)):
        name = 'images/' + str(nameImage) + '.png'
        images = OnscreenImage(image = name, pos = position, scale = scaleImage, color=colorImage)
        return images.setTransparency(TransparencyAttrib.MAlpha)

    #~~o~~o Загрузка рейтинга врага. Загрузка звездочек
    def setStarRating(self, number):
        name = 'Star' + str(number) 
        self.setElement(name, (.5, -2, .39), (.15, 0 ,.03))

    #~~o~~o Загрузка и отображение, выводящих текстов на экран
    def setDisplay(self, text, position, scale=0.08):
        return OnscreenText(text = text, pos = position, font = self.font, 
        scale = scale, align=TextNode.ACenter, mayChange=1)
    
    #~~o~~o Метод выводящий описание навыков на экран
    def skDisplay(self, text, xy):
        self.skillDisplay.setText(text)

    #~~o~~o Метод удаляющий текст, описание навыков, после того как курсор покинет кнопку
    def skDisplayClear(self, x):
        self.skillDisplay.setText('')

    #~~o~~o Загрузка кнопки
    def setButtom(self, text, command, position):
        return DirectButton(text = text, text_font =  self.font, 
        command = command, relief =None, scale = 0.07, pos = position, color=(1,1,1,1))

    #~~o~~o Раздел навыков магии. Пока нет подразделов
    def magic(self):
        self.actionDisplay.setText('Вы скастовали что-то мощное, могучие!')

    #~~o~~o Раздел навыков защиты. Пока нет подразделов
    def guard(self):
        self.actor.hp = self.actor.hp - int(self.enemy.attack * 0.25)
        self.actor_hp_bar.updateBar(self.actor.converterHP()) 
        self.actionDisplay.setText('Текущее здоровье героя: ' + str(self.actor.hp))

    #~~o~~o Метод наносящий урон врагу
    def damage(self):
        self.enemy.hp -= self.actor.attack
        self.enemyCurrentHP = self.enemy.converterHP()     
        self.enemy_hp_bar.updateBar(self.enemyCurrentHP)   
        self.lockButtons()
        self.actionDisplay.setText('Текущее здоровье врага: ' + str(self.enemy.hp))
        self.turn = 'Enemy'

    #~~o~~o Метод высчитывание удара врага по герою
    def attackEnemy(self):
        self.actor.hp = self.actor.hp - self.enemy.attack
        self.actor_hp_bar.updateBar(self.actor.converterHP()) 
        self.actionDisplay.setText('Текущее здоровье героя: ' + str(self.actor.hp))

    #~~o~~o Основной цикл битвы
    def startBattle(self, task):
        # message
        if self.turn == 'Player':
            pass
        elif self.turn == 'Enemy':
            if self.status_timer == False:
                self.save_timer = task.time
                self.status_timer = True
            else:
                if self.save_timer + 3.0 < task.time:
                    self.attackEnemy()
                    self.outputActions()
                    self.turn = 'Player'
                    #message
                    self.status_timer = False
        return task.cont

    def outputActions(self):
        self.lockButtons()
        taskMgr.doMethodLater(2, self.message, 'message')

    def message(self, task):
        if len(self.list_action) > 0:
            self.actionDisplay.setText(self.list_action[0])
            del self.list_action[0]
        else:
            self.basicSkills()
            return task.done
        return task.again

    #~~o~~o Метод проверяющий жив ли аппонент
    def alive(self, actor, enemy, task):
        if (actor.hp <= 0):
            self.actionDisplay.setText(str(actor.name) + ' повержан')
            return task.done
        elif (enemy.hp <= 0):
            self.actionDisplay.setText(str(enemy.name) + ' повержан')
            return task.done            
        return task.again

'''
	#clear the text
	#def clearText():
	#	entry.enterText('')#entry.get()

	#def passDef(text):
	#	entry.set(text)


class GameBattle:

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 1   # Player

    def run(self):
        while True:
            pass
            

    def actionAttack(attacking, getting):
        getting.hp -= attacking.attack


class Setting:

    def __init__(self):
        pass

'''
    # ~~o~~o~~o~~o~~o~~o Класс хп и мп бара o~~o~~o~~o~~o~~o~~ #

class UI_Bar:

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

class GameUnit:

    def __init__(self, name, hp, mp, attack):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.primaryHP = float(hp)   # Изначальное хп
        self.primaryMP = mp          # Изначальное мп
        self.attack = attack

    def converterHP(self):
        if self.hp <= 0:
            self.hp = 0
            return 0
        return self.hp/self.primaryHP

    def converterMP(self):
        return self.mp/self.primaryMP

class GamePlaer(GameUnit):

    def __init__(self, name, hp, mp, attack):
        GameUnit.__init__(self, name, hp, mp, attack)
        pass


class GameEnemy(GameUnit):

    def __init__(self, name, hp, rank, attack):
        self.mp = 100
        GameUnit.__init__(self, name, hp, self.mp, attack)
        self.rank = rank

    def ai(self):
        pass


#run the tutorial
app = MyApp() 
app.run()