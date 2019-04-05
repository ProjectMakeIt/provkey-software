from __future__ import division

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from progress import ProgressImage

font = ImageFont.load_default()

class Menu:
  def __init__(self,height=6,navigatable=True,firstEntry=0):
    self.lines=[]
    self.selectable=[]
    self.firstEntry=firstEntry
    self.currentLine=firstEntry
    self.navigatable=navigatable
    self.img = Image.new('1', (128,64))
    self.firstLine = 0
    self.height=height
  def reset(self):
    self.currentLine=self.firstEntry
    self.firstLine = 0
    if self.firstLine<self.currentLine-(self.height-1):
        self.firstLine=self.currentLine-(self.height-1)
  def addLine(self,line,selectable=True):
    self.lines.append(line)
    self.selectable.append(selectable)
  def down(self):
    if not self.navigatable:
      return
    self.currentLine+=1
    if self.firstLine<self.currentLine-(self.height-1):
        self.firstLine=self.currentLine-(self.height-1)
    if self.currentLine>len(self.lines)-1:
      self.currentLine=0
      self.firstLine=0
    if not self.selectable[self.currentLine]:
      self.down()
  def up(self):
    if not self.navigatable:
      return
    self.currentLine-=1
    if self.firstLine>self.currentLine:
        self.firstLine=self.currentLine
    if self.currentLine<0:
      self.currentLine=len(self.lines)-1
      if len(self.lines)-(self.height)<0:
        self.firstLine=0
      else:
        self.firstLine=len(self.lines)-(self.height)
    if not self.selectable[self.currentLine]:
      self.up()
  def enter(self,ctl):
    line = self.lines[self.currentLine]
    if isinstance(line,MenuLine):
      line.execute(ctl)
  def render(self):
    draw = ImageDraw.Draw(self.img)
    draw.rectangle((0,0,128,64), outline=0, fill=0)
    selectLine = self.currentLine-self.firstLine
    for i in xrange(0,self.height) :
      if len(self.lines)-1 < i:
          continue
      line = self.lines[i+self.firstLine]
      if selectLine==i:
        box=255
        text=0
      else:
        box=0
        text=255
      if isinstance(line,MenuLine):
        image=line.render(selectLine==i)
        mask = Image.new('1',(128,64))
        maskDraw = ImageDraw.Draw(mask)
        maskDraw.rectangle((0,(i*10),128,(i*10)+10), outline=0, fill=255)
        self.img.paste(image,(0,(i*10)))
      else:
        draw.rectangle((0,(i*10),128,(i*10)+10), outline=0, fill=box)
        draw.text((3, i*10), str(line), font=font, fill=text)
    return self.img
  def getPos(self):
    return self.currentLine
  def setPos(self,line):
    self.currentLine=line

class TitleMenu(Menu):
  def __init__(self,title,height=6,navigatable=True,firstEntry=0):
    Menu.__init__(self,height-1,navigatable,firstEntry)
    self.title=title
  def render(self):
    draw = ImageDraw.Draw(self.img)
    draw.rectangle((0,0,128,64), outline=0, fill=0)
    if isinstance(self.title,MenuLine):
      image = self.title.render(True)
      self.img.paste(image,(0,-1))
    else:
      draw.rectangle((0,0,128,9), outline=0, fill=1)
      draw.text((3, -1), str(self.title), font=font, fill=0)
    selectLine = self.currentLine-self.firstLine
    for i in xrange(0,self.height) :
      if len(self.lines)-1 < i:
          continue
      line = self.lines[i+self.firstLine]
      if selectLine==i:
        box=255
        text=0
      else:
        box=0
        text=255
      if isinstance(line,MenuLine):
        image=line.render(selectLine==i)
        mask = Image.new('1',(128,64))
        maskDraw = ImageDraw.Draw(mask)
        maskDraw.rectangle((0,((i+1)*10),128,((i+1)*10)+10), outline=0, fill=255)
        self.img.paste(image,(0,((i+1)*10)))
      else:
        draw.rectangle((0,((i+1)*10),128,((i+1)*10)+10), outline=0, fill=box)
        draw.text((3, (i+1)*10), str(line), font=font, fill=text)
    return self.img

class LoaderMenu(Menu):
  def __init__(self,image,count,nextMenu):
      Menu.__init__(self,navigatable=False,firstEntry=0)
      self.loader = ProgressImage(image,count)
      self.nextMenu = nextMenu
  def setCtl(self,ctl):
      self.ctl = ctl
  def reset(self):
      self.loader.reset()
  def render(self):
    try:
      self.img = self.loader.next()
    except StopIteration as e:
      self.ctl.rootMenu = self.nextMenu
      self.ctl.changeMenu(self.nextMenu)
    return self.img

class MenuLine:
  def __init__(self,label,cb):
    self.label = label
    self.cb = cb
  def execute(self,ctl):
    self.cb()
  def render(self,current):
    img = Image.new('1', (128,10))
    if current:
      box=255
      text=0
    else:
      box=0
      text=255
    draw = ImageDraw.Draw(img)
    draw.rectangle((0,0,128,10), outline=0, fill=0)
    draw.rectangle((0,0,128,10), outline=0, fill=box)
    draw.text((3, 0), str(self.label), font=font, fill=text)
    return img

class ProgressLine(MenuLine):
  def __init__(self,mx):
    self.max = mx
    self.current = 0
  def update(self,current):
    self.current = current;
  def execute(self,ctl):
    pass
  def render(self,current):
    img = Image.new('1', (128,10))
    if current:
      box=255
      text=0
    else:
      box=0
      text=255
    percent = self.current/self.max
    size = 124*percent
    draw = ImageDraw.Draw(img)
    draw.rectangle((0,0,128,10), fill=box)
    draw.rectangle((1,1,126,8), fill=text)
    draw.rectangle((2,2,125,7), fill=box)
    draw.rectangle((3,3,size,6), fill=text)
    return img

class MenuEntry(MenuLine):
  def __init__(self,label,menu):
    self.label = label
    self.nextMenu = menu
  def execute(self,ctl):
    self.next(ctl)
  def next(self,ctl):
    ctl.changeMenu(self.nextMenu)

class MenuText(MenuLine):
  def __init__(self,label):
    MenuLine.__init__(self,label,None)
  def execute(self,ctl):
    pass

class MenuCustom(MenuLine):
    def __init__(self,renderer):
        self.label = renderer()
        self.renderer = renderer
    def render(self,current):
        self.label = self.renderer()
        return MenuLine.render(self,current)
    def execute(self,ctl):
        pass;

class Controller:
    def __init__(self,menu):
        self.menu = menu
        self.rootMenu = menu
        menu.reset()
        self.menuImg = menu.img
        self.menuTree = []
    def loop(self):
        pass
    def changeMenu(self,menu):
        if menu is self.rootMenu:
            self.menuTree = []
        else:
            self.menuTree.append(self.menu)
        self.menu = menu
        menu.reset()
        self.menuImg = menu.img
    def up(self,_=None):
        self.menu.up()
    def down(self,_=None):
        self.menu.down()
    def enter(self,_=None):
        self.menu.enter(self)
    def back(self,_=None):
        if len(self.menuTree) > 0:
            self.menu = self.menuTree.pop()
            self.menu.setPos(0)
            self.menuImg = self.menu.img

class PyGameMenuController(Controller):
    def __init__(self,menu):
        self.pygame = __import__('pygame')
        Controller.__init__(self,menu)
        self.size = 128,64
        self.screen = self.pygame.display.set_mode(self.size)
    def loop(self):
        eventList = self.pygame.event.get(self.pygame.KEYDOWN)
        for key in eventList:
            if key.key == self.pygame.K_UP:
                self.up()
            if key.key == self.pygame.K_DOWN:
                self.down()
            if key.key == self.pygame.K_BACKSPACE:
                self.back()
            if key.key == self.pygame.K_RETURN:
                self.enter()
        menuImage = self.menu.render().convert('RGB')
        image = self.pygame.image.fromstring(menuImage.tobytes("raw",'RGB'),menuImage.size,'RGB')
        self.screen.blit(image,[0,0])
        self.pygame.display.flip()

class OledMenuController(Controller):
  def __init__(self,menu,display,upin,dpin,epin,bpin):
    RPi = __import__('RPi.GPIO')
    GPIO = RPi.GPIO
    Controller.__init__(self,menu)
    self.disp = display
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(upin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(dpin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(epin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(bpin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(upin, edge=GPIO.RISING, callback=self.up, bouncetime=200)
    GPIO.add_event_detect(dpin, edge=GPIO.RISING, callback=self.down, bouncetime=200)
    GPIO.add_event_detect(epin, edge=GPIO.RISING, callback=self.enter, bouncetime=200)
    GPIO.add_event_detect(bpin, edge=GPIO.RISING, callback=self.back, bouncetime=200)
  def loop(self):
    self.disp.image(self.menu.render())
    self.disp.display()
