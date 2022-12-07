import win32con
import win32gui
import win32api
import wx
import random
import math
import pylsl

import numpy as np

streams = pylsl.resolve_streams(wait_time=3.)
rvalue_inlet = []
for stream in streams:
    name = pylsl.StreamInlet(stream).info().name() 
    print(name)
    if (name == "RValues"):
        rvalue_inlet = pylsl.StreamInlet(stream)

display_width = win32api.GetSystemMetrics(0)

class AppFrame( wx.Frame ):
  r = 0
  rectangle_width = 0
  def __init__(self):
    # 常に最前面のウィンドウを生成
    wx.Frame.__init__(self,parent=None, title="Snow Layer",style= wx.STAY_ON_TOP)
    # ウィンドウハンドルを取得
    hwnd = self.GetHandle()

    # 追加設定へのポインタを取得
    extendedStyleSettings = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    # 追加設定に透過設定，ユーザ入力を受け付けない等を適用
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, extendedStyleSettings | win32con.WS_EX_LAYERED | win32con.WS_DISABLED)
    # 透過色の設定（今回は黒）
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), 0, win32con.LWA_COLORKEY)
    
    self.Maximize()
    self.snowPoints=[]
    self.Bind(wx.EVT_PAINT,self.OnPaint)
    self.timer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.onTimer)
    self.timer.Start(10)


  def OnPaint(self, evt):
    # 消去
    dc=wx.PaintDC(self)
    dc=wx.BufferedDC(dc)
    dc.SetPen(wx.BLACK_PEN)
    dc.SetBrush(wx.BLACK_BRUSH)
    dc.DrawRectangle(0,0,self.rectangle_width, 100)


    d, _ = rvalue_inlet.pull_chunk(max_samples=1024)    # バッファにあるデータを全部取る
    assert(len(d) < 1024)                        # 念のため、全部取り切れていることを確認する
    try:
        self.r = np.array(d)[-1, 0]            # とってきたデータの最後の部分を使う
    except:                                      # サンプリングレートが落ちてバッファが空になることもあるので...
        pass                                     # その時はpassしてごまかす

    # 更新
    self.rectangle_width = int(display_width  * self.r)

    print(self.r)
    
    # 描画
    dc.SetPen(wx.WHITE_PEN)
    dc.SetBrush(wx.WHITE_BRUSH)
    dc.DrawRectangle(0,0,self.rectangle_width, 100)
  def onTimer(self,event):
    self.Refresh(False)


app = wx.App(False)
AppFrame().Show()
app.MainLoop()
