import win32con
import win32gui
import win32api
import wx
import random
import math

class Snow:
  def __init__(self,x,y):
    self.beforex=self.x=x
    self.beforey=self.y=y
    self.baseX=x
    self.size=random.randint(1,3)
  def update(self):
    self.beforex=self.x
    self.beforey=self.y
    self.x=self.baseX+2*math.sin(self.y*0.1)
    self.y+=1


class AppFrame( wx.Frame ):
  def __init__(self):
    wx.Frame.__init__(self,parent=None, title="Snow Layer",style= wx.STAY_ON_TOP)

    hwnd = self.GetHandle()
    extendedStyleSettings = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, extendedStyleSettings | win32con.WS_EX_LAYERED | win32con.WS_DISABLED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), 0, win32con.LWA_COLORKEY)
    self.Maximize()
    self.snowPoints=[]
    self.Bind(wx.EVT_PAINT,self.OnPaint)
    self.timer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.onTimer)
    self.timer.Start(10)


  def OnPaint(self, evt):
    dc=wx.PaintDC(self)
    dc=wx.BufferedDC(dc)
    if not random.randint(0,3):
      self.snowPoints.append(Snow(random.randint(0, self.GetSize()[0]),0))
    for snow in self.snowPoints:
      dc.SetPen(wx.BLACK_PEN)
      dc.SetBrush(wx.BLACK_BRUSH)
      dc.DrawCircle(int(snow.beforex),int(snow.beforey),snow.size)
      snow.update()
      dc.SetPen(wx.WHITE_PEN)
      dc.SetBrush(wx.WHITE_BRUSH)
      dc.DrawCircle(int(snow.x),int(snow.y),snow.size)
      if snow.y>self.GetSize()[1]:
        self.snowPoints.remove(snow)
  def onTimer(self,event):
    self.Refresh(False)


app = wx.App(False)
AppFrame().Show()
app.MainLoop()
