from PIL import Image

class ProgressImage:
  def __init__(self,bmp,size):
    self.scale = Image.open(bmp).convert('L')
    self.count = 0
    self.size = size
  def __iter__(self):
    return self
  def next(self):
    if self.count > self.size:
        raise StopIteration
    j = 255-self.count
    self.count+=1
    print(self.count)
    return self.scale.point(lambda p: p > j and 255).convert('1')
