#!/usr/bin/env python
# encoding: utf-8
'''
@author: slyb
@license: (C) Copyright 2017-2020, 天津定智科技有限公司.
@contact: slyb@tju.edu.cn
@file: DepartmentTree.py
@time: 2019/9/1 15:54
@desc:
'''
import wx
from math import *
from ID_DEFINE import *
import  string
import  images
class MyTreeCtrl(wx.TreeCtrl):
    def __init__(self, parent, id, pos, size, style, log):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        self.log = log
    def OnCompareItems(self, item1, item2):
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        self.log.WriteText('compare: ' + t1 + ' <> ' + t2 + '\n')
        if t1 < t2: return -1
        if t1 == t2: return 0
        return 1
class DepartmentTree(wx.Panel):
    def __init__(self, parent,master,log,size):
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.Panel.__init__(self, parent, -1, size,style=wx.WANTS_CHARS)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.log = log
        self.master=master
        tID = wx.NewIdRef()
        # department_list=[
        #                 ["董事会",[["董事长",[]],["董事",[]]]],
        #                 ["管理部",[["总经理",[]],["副总经理",[]],["办公室",[]]]],
        #                 ["财务部",[]],
        #                 ["技术部",[]],
        #                 ["业务部",[["下单员",[]],["业务员",[]]]],
        #                 ["人事部",[]],
        #                 ["生产部",[["一车间",[["加工中心",[]],["模压前分拣工位",[]],["铣边工位",[]],["压条工位",[]],["异形机砂工位",[]],["手工打磨工位",[]],["半检分色工位",[]],["打孔工位",[]]]],["二车间",[]],["三车间",[]]]],
        # ]
        self.tree = MyTreeCtrl(self, tID, wx.DefaultPosition, size,
                               wx.TR_HAS_BUTTONS
                               | wx.TR_EDIT_LABELS
                               #| wx.TR_MULTIPLE
                               #| wx.TR_HIDE_ROOT
                               , self.log)
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        fileidx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        smileidx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        # smileidx    = il.Add(images.Smiles.GetBitmap())
        self.tree.SetImageList(il)
        self.il = il
        self.root = self.tree.AddRoot(self.master.company_name)
        self.tree.SetItemData(self.root, "厂")
        self.tree.SetItemImage(self.root, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, fldropenidx, wx.TreeItemIcon_Expanded)
        for i in self.master.department_list:
            child = self.tree.AppendItem(self.root, i[0])
            self.tree.SetItemData(child, "处")
            self.tree.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(child, fldropenidx, wx.TreeItemIcon_Expanded)
            for j in i[1]:
                last = self.tree.AppendItem(child,j[0])
                self.tree.SetItemData(last, "科")
                self.tree.SetItemImage(last, fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(last, fldropenidx, wx.TreeItemIcon_Expanded)
                for k in j[1]:
                    item = self.tree.AppendItem(last,k[0])
                    self.tree.SetItemData(item, "工位名")
                    self.tree.SetItemImage(item, fileidx, wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(item, smileidx, wx.TreeItemIcon_Selected)
        self.tree.ExpandAll()
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.tree)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit, self.tree)

    def OnSize(self, event):
        w,h = self.GetClientSize()
        self.tree.SetSize(0, 0, w, h)
    def OnBeginEdit(self, event):
        event.Veto()
    def OnEndEdit(self, event):
        event.Veto()
    def ReCreateTree(self):
        self.tree.Destroy()
        tID = wx.NewIdRef()
        self.tree = MyTreeCtrl(self, tID, wx.DefaultPosition, (200,900),
                               wx.TR_HAS_BUTTONS
                               | wx.TR_EDIT_LABELS
                               #| wx.TR_MULTIPLE
                               #| wx.TR_HIDE_ROOT
                               , self.log)
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        fileidx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        smileidx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        # smileidx    = il.Add(images.Smiles.GetBitmap())
        self.tree.SetImageList(il)
        self.il = il
        self.root = self.tree.AddRoot(self.master.company_name)
        self.tree.SetItemData(self.root, "厂")
        self.tree.SetItemImage(self.root, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, fldropenidx, wx.TreeItemIcon_Expanded)
        for i in self.master.department_list:
            child = self.tree.AppendItem(self.root, i[0])
            self.tree.SetItemData(child, "处")
            self.tree.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(child, fldropenidx, wx.TreeItemIcon_Expanded)
            for j in i[1]:
                last = self.tree.AppendItem(child,j[0])
                self.tree.SetItemData(last, "科")
                self.tree.SetItemImage(last, fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(last, fldropenidx, wx.TreeItemIcon_Expanded)
                for k in j[1]:
                    item = self.tree.AppendItem(last,k[0])
                    self.tree.SetItemData(item, "工位名")
                    self.tree.SetItemImage(item, fileidx, wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(item, smileidx, wx.TreeItemIcon_Selected)
        self.tree.ExpandAll()
        # self.tree.Refresh()
