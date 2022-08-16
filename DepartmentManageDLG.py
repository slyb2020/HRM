#!/usr/bin/env python
# encoding: utf-8
'''
@author: slyb
@license: (C) Copyright 2017-2020, 天津定智科技有限公司.
@contact: slyb@tju.edu.cn
@file: DepartmentManageDLG.py.py
@time: 2019/10/9 14:43
@desc:
'''
from ID_DEFINE import *
from DepartmentTree import *
import os
dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')
picDir=os.path.join(dirName,'picture')
import wx
import pymysql as MySQLdb

class DepartmentManageDialog(wx.Dialog):
    def __init__(self, parent, master,log, size=wx.DefaultSize, pos=wx.DefaultPosition,style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.parent=parent
        self.master=master
        self.log=log
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "部门管理", pos, size, style)
        self.CreatePanel()
    def CreatePanel(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1, size=(500, 700))
        bSizer_total = wx.BoxSizer(wx.VERTICAL)
        self.department_manage_tree=DepartmentManageTree(panel,self.master,self.log,size=(200,300))
        bSizer_total.Add(self.department_manage_tree,1,wx.EXPAND|wx.TOP|wx.BOTTOM,15)
        panel.SetSizer(bSizer_total)
        sizer.Add(panel, 0, wx.ALIGN_CENTRE | wx.ALL,0)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)
        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap(os.path.normpath(os.path.join(bitmapDir, "ok4.png")), wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap(os.path.normpath(os.path.join(bitmapDir, "cancel1.png")), wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap(os.path.normpath(os.path.join(bitmapDir, "aquabutton.png")), wx.BITMAP_TYPE_PNG)
        btn_ok = wx.Button(self, wx.ID_OK, "确认", size=(200, 45))
        btn_ok.Bind(wx.EVT_BUTTON,self.OnOkBTN)
        btn_ok.SetBitmap(bitmap1, wx.LEFT)
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "取消", size=(200, 45))
        btn_cancel.Bind(wx.EVT_BUTTON,self.OnCancelBTN)
        btn_cancel.SetBitmap(bitmap2, wx.LEFT)
        btnsizer.Add(btn_ok, 1)
        btnsizer.Add((100, 35), 0)
        btnsizer.Add(btn_cancel, 1)
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        self.SetSizer(sizer)
        sizer.Fit(self)
    def OnOkBTN(self, event):
        self.master.company_name,self.master.department_list=self.department_manage_tree.InstallData()
        self.master.department_tree.ReCreateTree()
        self.master.BindEvent()
        self.SaveDepartmentInfoDB()
        event.Skip()
    def SaveDepartmentInfoDB(self):
        try:
            db = MySQLdb.connect(host="%s" % host_name, user='%s' % user_name, passwd='%s' % passwd_name,
                                 db='%s' % DATABASE_NAME[6], charset='utf8')
        except:
            wx.MessageBox("无法连接lyb_temp数据库", "错误信息")
            log.WriteText("无法连接lyb_temp数据库", colour=wx.RED)
            return -1, []
        cursor = db.cursor()
        # [["董事会",[["董事长",[]],["董事",[]]]],["管理部",[["总经理",[]],["副总经理",[]],["办公室",[]]]],["业务部",[["下单组",[]],["价审组",[]],["技审组",[]],["财务组",[]],["业务组",[]]]],["人事部",[]],["生产部",[["一车间",[["加工中心",[]],["模压前分拣工位",[]],["铣边工位",[]],["压条工位",[]],["异形机砂工位",[]],["手工打磨工位",[]],["半检分色工位",[]],["打孔工位",[]]]],["二车间",[]],["三车间",[]]]]]
        ls_str=str(self.master.department_list)
        data=""
        for i in ls_str:
            if(i=="'"):
                data+="#"
            else:
                data+=i
        sql = "UPDATE system_parameter SET `部门名称列表` = '%s' WHERE 1" %(data)
        cursor.execute(sql)
        db.commit()  # 更新操作，必须提交
        db.close()
    def OnCancelBTN(self, event):
        event.Skip()
class DepartmentManageTree(DepartmentTree):
    def __init__(self, parent,master,log,size):
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        DepartmentTree.__init__(self, parent,master,log,size)
        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        # self.tree.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit)
        # self.tree.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate)
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        # self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.tree.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.tree.ExpandAll()
    def InstallData(self):
        item=self.root
        company_name=self.tree.GetItemText(item)
        data=[]
        a=self.tree.GetFirstChild(self.root)
        while(a[1]):
            data_b=[]
            b=self.tree.GetFirstChild(a[0])
            while(b[1]):
                data_c=[]
                c=self.tree.GetFirstChild(b[0])
                while(c[1]):
                    data_c.append([self.tree.GetItemText(c[0]),[]])
                    c=self.tree.GetNextChild(c[0],c[1])
                data_b.append([self.tree.GetItemText(b[0]),data_c])
                b=self.tree.GetNextChild(b[0],b[1])
            data.append([self.tree.GetItemText(a[0]),data_b])
            a=self.tree.GetNextChild(a[0],a[1])
        return company_name,data
    def OnNewKe(self,event):
        item=self.tree.GetFocusedItem()
        child = self.tree.AppendItem(item, "新建科室")
        self.tree.SetItemData(child, "科")
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        self.tree.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(child, fldropenidx, wx.TreeItemIcon_Expanded)
    def OnNewPosition(self,event):
        item=self.tree.GetFocusedItem()
        child = self.tree.AppendItem(item, "新建工位")
        self.tree.SetItemData(child, "工位名")
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fileidx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        smileidx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        self.tree.SetItemImage(child, fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(child, smileidx, wx.TreeItemIcon_Selected)
    def OnNewDepartment(self,event):
        child = self.tree.AppendItem(self.root, "新建部门")
        self.tree.SetItemData(child, "处")
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        self.tree.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(child, fldropenidx, wx.TreeItemIcon_Expanded)
    def OnExpandRoot(self,event):
        self.tree.ExpandAll()
    def OnCollapseRoot(self,event):
        self.tree.CollapseAll()
    def OnRightDown(self, event):
        pt = event.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if item:
            self.tree.SelectItem(item)
            itemdata = self.tree.GetItemData(item)
            if(itemdata=="厂"):
                self.Bind(wx.EVT_MENU, self.OnNewDepartment, id=NewChuID)
                self.Bind(wx.EVT_MENU, self.OnExpandRoot, id=ExpandRootID)
                self.Bind(wx.EVT_MENU, self.OnCollapseRoot, id=CollapseRootID)
                # make a menu
                menu = wx.Menu()
                # Show how to put an icon in the menu
                item = wx.MenuItem(menu, NewChuID,"新建部门")
                # bmp = images.Smiles.GetBitmap()
                bmp = wx.Bitmap(os.path.normpath(os.path.join(bitmapDir, "folder_new.png")), wx.BITMAP_TYPE_PNG)
                # bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "folder_new.png"))).Scale(width=28, height=28,
                #                                                 quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                item.SetBitmap(bmp)
                menu.Append(item)
                item = wx.MenuItem(menu, ExpandRootID,"全部展开")
                bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "expand.png"))).Scale(width=28, height=28,
                                                                quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                item.SetBitmap(bmp)
                menu.Append(item)

                item = wx.MenuItem(menu, CollapseRootID,"全部收起")
                bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "collapse.png"))).Scale(width=28, height=28,
                                                                quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                item.SetBitmap(bmp)
                menu.Append(item)
                # add some other items
                item = wx.MenuItem(menu, DeleteChildrenID,"删除所属子部门")
                bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "delete-folder.png"))).Scale(width=28, height=28,
                                                                quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                item.SetBitmap(bmp)
                menu.Append(item)
            elif(itemdata=="处"):
                self.Bind(wx.EVT_MENU, self.OnNewKe, id=NewKeID)
                self.Bind(wx.EVT_MENU, self.OnDeleteItem, id=DeleteItemID)
                self.Bind(wx.EVT_MENU, self.OnDeleteChildren, id=DeleteChildrenID)
                # make a menu
                menu = wx.Menu()
                # Show how to put an icon in the menu
                item = wx.MenuItem(menu, NewKeID,"新建子部门")
                bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "lbnews.png"))).Scale(width=28, height=28,
                                                                quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                item.SetBitmap(bmp)
                menu.Append(item)
                # add some other items
                item = wx.MenuItem(menu, DeleteItemID,"删除此部门")
                bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "cancel1.png"))).Scale(width=28, height=28,
                                                                quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                item.SetBitmap(bmp)
                menu.Append(item)
                # add some other items
                item = wx.MenuItem(menu, DeleteChildrenID,"删除所属子部门")
                bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "delete-folder.png"))).Scale(width=28, height=28,
                                                                quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                item.SetBitmap(bmp)
                menu.Append(item)
            elif(itemdata=="科"):
                self.Bind(wx.EVT_MENU, self.OnNewPosition, id=NewPositionID)
                self.Bind(wx.EVT_MENU, self.OnDeleteItem, id=DeleteItemID)
                self.Bind(wx.EVT_MENU, self.OnDeleteChildren, id=DeleteChildrenID)
                # make a menu
                menu = wx.Menu()
                # Show how to put an icon in the menu
                item = wx.MenuItem(menu, NewPositionID,"新建子部门")
                bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "lbnews.png"))).Scale(width=28, height=28,
                                                                quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                item.SetBitmap(bmp)
                menu.Append(item)
                # add some other items
                item = wx.MenuItem(menu, DeleteItemID,"删除此部门")
                bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "cancel1.png"))).Scale(width=28, height=28,
                                                                quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                item.SetBitmap(bmp)
                menu.Append(item)
                # add some other items
                item = wx.MenuItem(menu, DeleteChildrenID,"删除所属子部门")
                bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "delete-folder.png"))).Scale(width=28, height=28,
                                                                quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                item.SetBitmap(bmp)
                menu.Append(item)
            else:
                self.Bind(wx.EVT_MENU, self.OnRenameItem, id=RenameItemID)
                self.Bind(wx.EVT_MENU, self.OnDeleteItem, id=DeleteItemID)
                self.Bind(wx.EVT_MENU, self.OnDeleteChildren, id=DeleteChildrenID)
                # make a menu
                menu = wx.Menu()
                # Show how to put an icon in the menu
                item = wx.MenuItem(menu, RenameItemID,"重命名")
                bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "lbnews.png"))).Scale(width=28, height=28,
                                                                quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                item.SetBitmap(bmp)
                menu.Append(item)
                # add some other items
                item = wx.MenuItem(menu, DeleteItemID,"删除此工位")
                bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "-.png"))).Scale(width=28, height=28,
                                                                quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                item.SetBitmap(bmp)
                menu.Append(item)
            # Popup the menu.  If an item is selected then its handler
            # will be called before PopupMenu returns.
            self.PopupMenu(menu)
            menu.Destroy()
    def OnRenameItem(self,event):
        item = self.tree.GetFocusedItem()
        self.tree.EditLabel(item)
    def OnDeleteItem(self,event):
        item=self.tree.GetFocusedItem()
        self.tree.Delete(item)
    def OnDeleteChildren(self,event):
        item=self.tree.GetFocusedItem()
        self.tree.DeleteChildren(item)
    def OnRightUp(self, event):
        event.Skip()
    def OnBeginEdit(self, event):
        event.Skip()

    def OnEndEdit(self, event):
        event.Skip()

    def OnLeftDClick(self, event):
        pt = event.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if item:
            self.tree.SelectItem(item)
            itemdata = self.tree.GetItemData(item)
            # if(itemdata=="厂"):
            self.tree.Toggle(item)
        event.Skip()

    def OnSize(self, event):
        w, h = self.GetClientSize()
        self.tree.SetSize(0, 0, w, h)

    def OnItemExpanded(self, event):
        item = event.GetItem()
        if item:
            self.log.WriteText("OnItemExpanded: %s\n" % self.tree.GetItemText(item))

    def OnItemCollapsed(self, event):
        item = event.GetItem()
        if item:
            self.log.WriteText("OnItemCollapsed: %s\n" % self.tree.GetItemText(item))

    def OnSelChanged(self, event):
        self.item = event.GetItem()
        if self.item:
            self.log.WriteText("OnSelChanged: %s\n" % self.tree.GetItemText(self.item))
            if wx.Platform == '__WXMSW__':
                self.log.WriteText("BoundingRect: %s\n" %
                                   self.tree.GetBoundingRect(self.item, True))
            # items = self.tree.GetSelections()
            # print(map(self.tree.GetItemText, items))
        event.Skip()

    def OnActivate(self, event):
        if self.item:
            self.log.WriteText("OnActivate: %s\n" % self.tree.GetItemText(self.item))
