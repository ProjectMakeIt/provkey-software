from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from progress import ProgressImage

font = ImageFont.load_default()

class Menu:
  def __init__(self,navigatable=True,firstEntry=0):
    self.lines=[]
    self.selectable=[]
    self.firstEntry=firstEntry
    self.currentLine=firstEntry
    self.navigatable=navigatable
    self.img = Image.new('1', (128,64))
  def reset(self):
    self.currentLine=self.firstEntry
  def addLine(self,line,selectable=True):
    self.lines.append(line)
    self.selectable.append(selectable)
  def down(self):
    if not self.navigatable:
      return
    self.currentLine+=1
    if self.currentLine>len(self.lines)-1:
      self.currentLine=0
    if not self.selectable[self.currentLine]:
      self.down()
  def up(self):
    if not self.navigatable:
      return
    self.currentLine-=1
    if self.currentLine<0:
      self.currentLine=len(self.lines)-1
    if not self.selectable[self.currentLine]:
      self.up()
  def enter(self,ctl):
    line = self.lines[self.currentLine]
    if isinstance(line,MenuLine):
      line.execute(ctl)
  def render(self):
    draw = ImageDraw.Draw(self.img)
    draw.rectangle((0,0,128,64), outline=0, fill=0)
    for i,line in enumerate(self.lines):
      if self.currentLine==i:
        box=255
        text=0
      else:
        box=0
        text=255
      if isinstance(line,MenuLine):
        image=line.render(self.currentLine==i)
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

class ProgressMenu(Menu):
  def __init__(self,image,count,nextMenu):
      Menu.__init__(self,navigatable=False,firstEntry=0)
      self.loader = ProgressImage(image,count)
      self.nextMenu = nextMenu
  def setCtl(self,ctl):
      self.ctl = ctl
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
    GPIO = __import__('RPi.GPIO')
    Controller.__init__(self,menu)
    self.disp = display
    GPIO.add_event_detect(upin, edge=GPIO.RISING, callback=self.up, bouncetime=200)
    GPIO.add_event_detect(dpin, edge=GPIO.RISING, callback=self.down, bouncetime=200)
    GPIO.add_event_detect(epin, edge=GPIO.RISING, callback=self.enter, bouncetime=200)
    GPIO.add_event_detect(bpin, edge=GPIO.RISING, callback=self.back, bouncetime=200)
  def loop(self):
    self.disp.image(self.menu.render())
    self.disp.display()
