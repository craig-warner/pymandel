#!/usr/bin/env python3
import tkinter as tk
import sys
from time import sleep

class MandelCalc:
  threshold = 1000.0
  MaxA = 2.0
  MinA = -1.0
  MaxDi = 1.5
  MinDi = -1.5
  AperDot = 1.0 
  DiperDot = 1.0 
  def SetRange(self,MinX,MinY,MaxX,MaxY,XDots,YDots):
    self.AperDot = (MaxX-MinX)/XDots
    self.DiperDot = (MaxY-MinY)/YDots
  def GetColor(self,c,di,numIters):
    for i in range(0,numIters):
      if i == 0:
        a=c
        bi=di
      else:
        newA=a*a-bi*bi-c
        newBi=2*a*bi-di
        a=newA
        bi=newBi
      if a>self.threshold:
        return i
    return 0 
  def GetA(self,xDot):
    a = self.AperDot*xDot + self.MinA   
    return a
  def GetDi(self,yDot):
    di = self.DiperDot*yDot + self.MinDi  
    return di
  def Inter2Color(self,numBits,i):
    if numBits == 4:
      str = "#%03x" % (i&0xfff)
      return str
    elif numBits == 8:
      str = "#%06x" % (i&0xffffff)
      return str
    elif numBits == 12:
      str = "#%09x" & (i&0xfffffffff)
      return str
    else:
      print ("Error 1")
      raise Exception("Not a Valid Color Width") 

  def ColorDot(self,numBits,x,y):
    a = self.GetA(x)
    di = self.GetDi(y)
    numIters = 1<<(numBits*3)
    colorI = self.GetColor(a,di,numIters)
    colorStr = self.Inter2Color(numBits,colorI)  
    return(colorStr)

class MandelApp(tk.Tk):
  def __init__(self):
    tk.Tk.__init__(self)
    self.MyCanvas = tk.Canvas(self,bg="black", height=400,width=400)
    self.MyCanvas.pack(expand = False)
    self.MyMandelCalc = MandelCalc()
    # def SetRange(self,MinX,MinY,MaxX,MaxY,XDots,YDots):
    self.MyMandelCalc.SetRange(-1.0,-1.5,2.0,1.5,400,400)
    self._create_menubar()
    self.text = tk.Text(height=3,width=40)
    self.text.pack(side="top", fill="both",  expand = False)
    self.wm_title("Mandelbrot")
    # Icon Code Python 2.7
    #img = PhotoImage(file="mandel-icon")
    #self.tk.call('wm','iconphoto',self._w,img)
    #self.tk.call('wm','iconphoto',self._w,img)
    #
    # Icon Code Python 3.0
    #if os.name == "nt":
    #  root.wm_iconbitmap(bitmap = "mandelicon.ico") 
    #else:
    #  root.wm_iconbitmap(bitmap = "mandelicon.xbm") 

  def _create_menubar(self):
    self.menubar = tk.Menu() 
    self.configure(menu=self.menubar)

    file_menu = tk.Menu(self.menubar,tearoff=False)  
    self.menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New",command=self.on_new)
    file_menu.add_command(label="Exit",command=self.on_exit)

  def log(self,s):
    self.text.insert("end",s+ "\n")
    self.text.see("end")

  def on_new(self): 
    self.log("New...")
    self.DrawCanvas();

  def on_exit(self): 
    self.log("Exit...")
    sys.exit(0)

  def DrawCanvas(self):
    for x in range(0,40):
      for y in range(0,40):
        x1 = x*10 + 10
        y1 = y*10 + 10 
        colorStr = self.MyMandelCalc.ColorDot(4,x1,y1)
        self.MyCanvas.create_rectangle(x*10,y*10,x1,y1,fill=colorStr)
        self.MyCanvas.pack()
        self.MyCanvas.update() 
        sleep(0.25)
  
if __name__ == "__main__":
  app = MandelApp()
  app.mainloop()

