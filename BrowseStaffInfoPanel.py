#!/usr/bin/env python
# encoding: utf-8
'''
@author: slyb
@license: (C) Copyright 2017-2020, 天津定智科技有限公司.
@contact: slyb@tju.edu.cn
@file: MyClass.py.py
@time: 2019/6/16 14:05
@desc:
'''
import wx.adv
import os
import sys
# # dirName = os.path.dirname(os.path.abspath(__file__))
# # bitmapDir = os.path.join(dirName, 'bitmaps')
# sys.path.append(os.path.split(dirName)[0])
from ID_DEFINE import *
###################HyperTreeListData######################################
import wx.lib.agw.hypertreelist as HTL
ArtIDs = [ "None",
           "wx.ART_ADD_BOOKMARK",
           "wx.ART_DEL_BOOKMARK",
           "wx.ART_HELP_SIDE_PANEL",
           "wx.ART_HELP_SETTINGS",
           "wx.ART_HELP_BOOK",
           "wx.ART_HELP_FOLDER",
           "wx.ART_HELP_PAGE",
           "wx.ART_GO_BACK",
           "wx.ART_GO_FORWARD",
           "wx.ART_GO_UP",
           "wx.ART_GO_DOWN",
           "wx.ART_GO_TO_PARENT",
           "wx.ART_GO_HOME",
           "wx.ART_FILE_OPEN",
           "wx.ART_PRINT",
           "wx.ART_HELP",
           "wx.ART_TIP",
           "wx.ART_REPORT_VIEW",
           "wx.ART_LIST_VIEW",
           "wx.ART_NEW_DIR",
           "wx.ART_HARDDISK",
           "wx.ART_FLOPPY",
           "wx.ART_CDROM",
           "wx.ART_REMOVABLE",
           "wx.ART_FOLDER",
           "wx.ART_FOLDER_OPEN",
           "wx.ART_GO_DIR_UP",
           "wx.ART_EXECUTABLE_FILE",
           "wx.ART_NORMAL_FILE",
           "wx.ART_TICK_MARK",
           "wx.ART_CROSS_MARK",
           "wx.ART_ERROR",
           "wx.ART_QUESTION",
           "wx.ART_WARNING",
           "wx.ART_INFORMATION",
           "wx.ART_MISSING_IMAGE",
           "SmileBitmap"
           ]
##########################################################################

class BrowseStaffInfoPanel(wx.Panel):
    def __init__(self, parent,data,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        self.tree = BrowseStaffInfoTreeList(self, data,log=self.log)
        self.Bind(wx.EVT_SIZE, self.OnSize)
    def ReCreateTree(self,data):
        self.tree.Destroy()
        self.tree = BrowseStaffInfoTreeList(self, data,log=self.log)
        self.tree.SetSize(self.GetSize())
        self.tree.Layout()
    def OnSize(self, evt):
        self.tree.SetSize(self.GetSize())
class BrowseStaffInfoTreeList(HTL.HyperTreeList):
    def __init__(self, parent,data,id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.SUNKEN_BORDER,
                 agwStyle=wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT|wx.TR_HIDE_ROOT|wx.TR_NO_LINES|wx.TR_ROW_LINES|wx.TR_FULL_ROW_HIGHLIGHT,
                 log=None):
        HTL.HyperTreeList.__init__(self, parent, id, pos, size, style, agwStyle)
        self.log = log
        self.CreateTree(data)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
    def OnSelChanged(self, event):
        item = event.GetItem()
        # if item:
        #     item_text=self.GetItemText(item)
        #     if("订单" in item_text):
        #         self.master.current_order_id=item_text[6:]
        #         self.master.current_section_id=''
        #     elif("门板"in item_text):
        #         self.master.current_door_id=item_text[6:]
        #         ls=self.master.current_door_id.split('S')
        #         self.master.current_order_id=ls[0]
        #     else:
        #         self.master.current_order_id=''
        #         self.master.current_section_id=''
        event.Skip()
    def CreateTree(self,data):
        WIDTH_LIST=[65,35,90]
        self.AddColumn("姓名")
        self.AddColumn("性别")
        self.AddColumn("职务")
        self.SetMainColumn(0) # the one with the tree in it...
        self.SetColumnWidth(0, WIDTH_LIST[0])
        self.SetColumnAlignment(0, wx.ALIGN_LEFT)
        for i in range(1,3):
            self.SetColumnWidth(i,WIDTH_LIST[i])
            self.SetColumnAlignment(i, wx.ALIGN_CENTER)
        self.root = self.AddRoot(COMPANY_NAME)
        for od in data:
            order_item = self.AppendItem(self.root, od[0])#这是添加这一行的第0列
            self.SetPyData(order_item, None)
            self.SetItemText(order_item, od[1], 1)#dealer_name
            self.SetItemText(order_item, od[5], 2)#receiver_addr
            self.SetItemImage(order_item, 24, which=wx.TreeItemIcon_Normal)
            self.SetItemImage(order_item, 13, which=wx.TreeItemIcon_Expanded)
            # self.SetItemTextColour(order_item, wx.BLUE)
            # self.SetItemFont(order_item, wx.Font(wx.FontInfo(12).Bold()))
            self.Expand(order_item)
        # self.Expand(self.root)
