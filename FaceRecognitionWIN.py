#!/usr/bin/env python
# encoding: utf-8
'''
@author: slyb
@license: (C) Copyright 2017-2025, 天津定智科技有限公司.
@contact: slyb@tju.edu.cn
@file: FaceRecognition.py
@time: 2020/04/06 19:43
@desc:
'''
import wx.lib.scrolledpanel as scrolled
import wx
import os
import images
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np
import requests
from json import JSONDecoder
compare_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"
key = "DfAZF7jao01yPQCa-89xAXZEVpNEEue2"
secret = "gys5Ii89qqBv68Igysk4-n_gzrRzB3hP"

dirName = os.path.dirname(os.path.abspath(__file__))
tempDir=os.path.join(dirName,'temp')
bitmapDir = os.path.join(dirName, 'bitmaps')

class FaceRecognitionPanel(wx.MDIChildFrame):
    def __init__(self, parent, log):
        wx.MDIChildFrame.__init__(self, parent, size=(800,600))
        self.log = log
        panel=wx.Panel(self)
        self.left_panel = scrolled.ScrolledPanel(panel,-1,size=(280,300))
        self.left_panel.SetBackgroundColour('light blue')
        self.right_panel = scrolled.ScrolledPanel(panel,-1,size=(280,300))
        self.right_panel.SetBackgroundColour(wx.Colour(123,241,135))
        self.thumbnail_panel=scrolled.ScrolledPanel(panel, -1, size=(-1, 100),style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.info_panel=scrolled.ScrolledPanel(panel,-1,size=(100,-1),style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.top_panel=wx.Panel(panel,-1,size=(-1,100))
        self.startBTN = wx.Button(self.top_panel, -1, "开始识别",size=(150, 50))
        self.startBTN.Bind(wx.EVT_BUTTON,self.OnStartRec)
        hbox=wx.BoxSizer()
        hbox.Add(wx.Panel(self.top_panel,-1),1)
        hbox.Add(self.startBTN,0,wx.ALL,30)
        self.top_panel.SetSizer(hbox)
        self.parent=parent
        self._bShowImages = False
        self._bVCStyle = False
        self._newPageCounter = 0
        self._ImageList = wx.ImageList(16, 16)
        self._ImageList.Add(images._book_red.GetBitmap())
        self._ImageList.Add(images._book_green.GetBitmap())
        self._ImageList.Add(images._book_blue.GetBitmap())
        self.SetIcon(images.Mondrian.GetIcon())
        #################################################################################################################
        vbox=wx.BoxSizer(wx.VERTICAL)
        hbox=wx.BoxSizer()
        vbox.Add(self.top_panel,0,wx.EXPAND)
        hbox.Add(self.left_panel,0,wx.EXPAND)
        hbox.Add(self.right_panel,0,wx.EXPAND)
        hbox.Add(self.info_panel,1,wx.EXPAND)
        vbox.Add(hbox,1,wx.EXPAND)
        vbox.Add(self.thumbnail_panel,0,wx.EXPAND)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_TIMER,self.OnTimer)
    def OnTimer(self,event):
        self.position+=1
        if(self.position>len(self.pic_data)):
            self.position=0
            self.t1.Stop()
            self.recognizing_state=False
            self.startBTN.Enable()
        else:
            self.Recognize()
    def OnStartRec(self,event):
        from Function import GetAllIDWithPicture, GetPicture
        error, self.pic_data = GetAllIDWithPicture(self.log)
        if (error != -1):
            self.t1=wx.Timer(self)
            self.t1.Start(10)
            self.startBTN.Disable()
            self.recognizing_state=True
            self.faceId1="me.jpg"
            self.position=0
            self.Recognize()
    def Recognize(self):
        from Function import GetPicture
        error, picture_data = GetPicture(self.log, self.pic_data[self.position])
        if (error != -1):
            faceId2 = 'ls.jpg'
            import base64
            with open(faceId2, 'wb') as file:
                image = base64.b64decode(picture_data)  # 解码
                file.write(image)
            data = {"api_key": key, "api_secret": secret}
            files = {"image_file1": open(self.faceId1, "rb"), "image_file2": open(faceId2, "rb")}
            response = requests.post(compare_url, data=data, files=files)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
            # print(req_dict)
            confindence = req_dict['confidence']
            print(confindence)
            self.ShowKnownPic('ls.jpg')
            if confindence >= 65:
                print('True')
                self.position = 0
                self.t1.Stop()
                self.recognizing_state = False
                self.startBTN.Enable()
            else:
                print('False')

    def ShowUnknownPic(self,pic_file_name):
        # lena = mpimg.imread(os.path.normpath(os.path.join(bitmapDir, "aquabutton.png")))  # 读取和代码处于同一目录下的 lena.png
        # 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
        # lena.shape  # (512, 512, 3)
        # plt.imshow(lena)  # 显示图片
        # plt.axis('off')  # 不显示坐标轴
        # plt.show()
        # plt.imshow(lena)
        # plt.show()
        self.left_panel.DestroyChildren()
        if(pic_file_name!=""):
            # bmp_common = wx.Image(pic_file_name).ConvertToBitmap()
            bmp_common = wx.Image(pic_file_name).Scale(width=260, height=350,quality=wx.IMAGE_QUALITY_BOX_AVERAGE).ConvertToBitmap()
            self.statBmp = wx.StaticBitmap(self.left_panel, wx.ID_ANY, bmp_common)
            top_panel=wx.Panel(self.left_panel)
            bottom_panel=wx.Panel(self.left_panel)
            left_panel=wx.Panel(self.left_panel)
            right_panel=wx.Panel(self.left_panel)
            vbox=wx.BoxSizer(wx.VERTICAL)
            hbox = wx.BoxSizer()
            vbox.Add(top_panel,1,wx.EXPAND)
            vbox.Add(self.statBmp, 0,wx.EXPAND)
            vbox.Add(bottom_panel,1,wx.EXPAND)
            hbox.Add(left_panel,1,wx.EXPAND)
            hbox.Add(vbox,0,wx.EXPAND)
            hbox.Add(right_panel,1,wx.EXPAND)
            self.left_panel.SetSizer(hbox)
            self.left_panel.SetAutoLayout(1)
            self.left_panel.SetupScrolling()
    def ShowKnownPic(self,pic_file_name):
        self.right_panel.DestroyChildren()
        if(pic_file_name!=""):
            # bmp_common = wx.Image(pic_file_name).ConvertToBitmap()
            bmp_common = wx.Image(pic_file_name).Scale(width=260, height=350,quality=wx.IMAGE_QUALITY_BOX_AVERAGE).ConvertToBitmap()
            self.statBmp = wx.StaticBitmap(self.right_panel, wx.ID_ANY, bmp_common)
            top_panel=wx.Panel(self.right_panel)
            bottom_panel=wx.Panel(self.right_panel)
            left_panel=wx.Panel(self.right_panel)
            right_panel=wx.Panel(self.right_panel)
            vbox=wx.BoxSizer(wx.VERTICAL)
            hbox = wx.BoxSizer()
            vbox.Add(top_panel,1,wx.EXPAND)
            vbox.Add(self.statBmp, 0,wx.EXPAND)
            vbox.Add(bottom_panel,1,wx.EXPAND)
            hbox.Add(left_panel,1,wx.EXPAND)
            hbox.Add(vbox,0,wx.EXPAND)
            hbox.Add(right_panel,1,wx.EXPAND)
            self.right_panel.SetSizer(hbox)
            self.right_panel.SetAutoLayout(1)
            self.right_panel.SetupScrolling()
    def ShowThumbnailPic(self):
        self.thumbnail_panel.DestroyChildren()
        vbox=wx.BoxSizer(wx.VERTICAL)
        self.parent.pic_file_name_list=[]
        for thumbnail in os.listdir(tempDir):
            self.parent.pic_file_name_list.append(tempDir+'/' + thumbnail)
            bmp = wx.Image(tempDir+'/' + thumbnail).Scale(width=100, height=50,quality=wx.IMAGE_QUALITY_BOX_AVERAGE).ConvertToBitmap()
            panel=wx.Panel(self.thumbnail_panel)
            hbox=wx.BoxSizer()
            btn = wx.Button(panel, -1, size=(120,60),name=thumbnail)
            btn.SetBitmap(bmp)
            ls=thumbnail.split('.')
            check_CHK=wx.CheckBox(panel, -1, label=ls[0],name=thumbnail)
            check_CHK.SetValue(True)
            hbox.Add(btn,0,wx.EXPAND)
            hbox.Add((10,-1))
            hbox.Add(check_CHK,0,wx.EXPAND)
            panel.SetSizer(hbox)
            vbox.Add(panel,0,wx.ALL,10)
        self.thumbnail_panel.SetSizer(vbox)
        self.thumbnail_panel.SetAutoLayout(1)
        self.thumbnail_panel.SetupScrolling()
