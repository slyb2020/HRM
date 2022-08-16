#!/usr/bin/env python
# encoding: utf-8
'''
@author: slyb
@license: (C) Copyright 2017-2020, 天津定智科技有限公司.
@contact: slyb@tju.edu.cn
@file: MyClass.py
@time: 2019/10/2 11:31
@desc:
'''
import wx
import cv2
class TakePictureDialog(wx.Dialog):
    def __init__(self, parent, log,size=wx.DefaultSize, pos=wx.DefaultPosition,style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.parent=parent
        self.log=log
        self.Create(parent, -1, "拍摄照片", pos, size, style)
        self.CreatePanel()
        self.t1 = wx.Timer(self)
        self.t1.Start(200)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
    def OnTimer(self,event):
        ret, imag = self.capture.read()
        try:
            cv2.imwrite("example.jpg", imag)
        except:
            self.t1.Stop()
            wx.MessageBox("摄像头故障，无法完成照片采集，请安装摄像头后重试","系统故障信息")
            self.Destroy()
        Pic = wx.Image("example.jpg").Scale(width=550, height=450,
                                            quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.PicBmp = wx.StaticBitmap(self.pic_panel, wx.ID_ANY, Pic)
    def CreatePanel(self):
        self.panel = wx.Panel(self,-1)
        self.pic_panel=wx.Panel(self.panel,-1,size=(550,450))
        hbox = wx.BoxSizer()
        # Pic = wx.Image("timg12.jpg").Scale(width=450, height=400, quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        # self.PicBmp = wx.StaticBitmap(self.panel, wx.ID_ANY, Pic)
        hbox.Add(self.pic_panel, 0, wx.EXPAND | wx.ALL, 5)
        self.take_BTN = wx.Button(self.panel, -1, "拍\r\n照", size=(40, 60))
        self.redo_BTN = wx.Button(self.panel, -1, "重\r\n拍", size=(40, 60))
        self.redo_BTN.Enable(False)
        self.OK_BTN = wx.Button(self.panel, wx.ID_OK, "保\r\n存", size=(40, 60))
        self.OK_BTN.Enable(False)
        self.cancel_BTN = wx.Button(self.panel, wx.ID_CANCEL, "取\r\n消", size=(40, 60))
        self.take_BTN.Bind(wx.EVT_BUTTON, self.OnTakeBTN)
        self.redo_BTN.Bind(wx.EVT_BUTTON, self.OnRedoBTN)
        self.OK_BTN.Bind(wx.EVT_BUTTON, self.OnSaveBTN)
        self.cancel_BTN.Bind(wx.EVT_BUTTON, self.closepic)
        self.Bind(wx.EVT_CLOSE, self.closepic)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.take_BTN, 1, wx.EXPAND | wx.LEFT, 0)
        vbox.Add(self.redo_BTN, 1, wx.EXPAND | wx.LEFT, 0)
        vbox.Add(self.OK_BTN, 1, wx.EXPAND | wx.LEFT, 0)
        vbox.Add(self.cancel_BTN, 1, wx.EXPAND | wx.LEFT, 0)
        hbox.Add(vbox, 0, wx.EXPAND | wx.ALL, 10)
        self.panel.SetSizer(hbox)
        hbox.Fit(self)
        self.capture = cv2.VideoCapture(0)
    def OnTakeBTN(self,event):
        self.t1.Stop()
        self.take_BTN.Enable(False)
        self.redo_BTN.Enable(True)
        self.OK_BTN.Enable(True)
    def OnRedoBTN(self,event):
        self.t1.Start(200)
        self.take_BTN.Enable(True)
        self.redo_BTN.Enable(False)
        self.OK_BTN.Enable(False)
    def OnSaveBTN(self,event):
        event.Skip()
    def closepic(self,event):
        event.Skip()
