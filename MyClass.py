#!/usr/bin/env python
# encoding: utf-8
'''
@author: slyb
@license: (C) Copyright 2017-2020, 天津定智科技有限公司.
@contact: slyb@tju.edu.cn
@file: MyClass.py
@time: 2019/6/3 14:07
@desc:
'''
import wx
from ID_DEFINE import *
from DepartmentTree import *
from BrowseStaffInfoPanel import *
from EditStaffInfoPanel import *
from Function import *
from WorkZoneBrowseInfo import *
# Importing ScrolledWindow demo to make use of the MyCanvas
# class defined within.
import ScrolledWindow
import images
from GetFileName import *
import requests
from json import JSONDecoder
import cv2
from FaceRecognitionWIN import *

compare_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"
key = "DfAZF7jao01yPQCa-89xAXZEVpNEEue2"
secret = "gys5Ii89qqBv68Igysk4-n_gzrRzB3hP"


class MyMDI(wx.MDIParentFrame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.MDIParentFrame.__init__(self, parent, id, title, pos,size,style)
        self.winCount = 0
        self.workzonepageselection = 0
        self.search_value=""
        self.staff_current_info=[]
        self.picture_list = GetFileList(picDir)
        self.CreateMenuBar()
        self.CreateStatusBar()
        self.CreateWinStruct()
        self.BindEvent()
        if SHOW_BACKGROUND:
            self.bg_bmp = images.GridBG.GetBitmap()
            self.GetClientWindow().Bind(
                wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground
                )
        self.workzoneFaceRecognitionWindow=None
    def BindEvent(self):
        self.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag, id=ID_WINDOW_BOTTOM,
                  id2=ID_WINDOW_LEFT)  # BOTTOM和LEFT顺序不能换，要想更改哪个先分，只需更改上面窗口定义的顺序
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_Exit)
        self.Bind(wx.EVT_MENU, self.OnFaceRecognition, id=FACE_RECOGNITION_ID)
        self.Bind(wx.EVT_MENU, self.OnFaceRecognitionPlusPlus, id=FACE_PLUS_PLUS_ID)
        self.Bind(wx.EVT_MENU, self.OnUpdateFaceAll, id=UPDATE_FACE_CHARACTOR_ALL_ID)
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch, self.searchctrl)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel, self.searchctrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearch, self.searchctrl)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnDepartmentChanged, self.department_tree.tree)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnStaffListChanged, self.edit_staff_info.list)
        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_CHANGED,self.OnNotebookPageChange,self.workzoneBrowseInfoWindow.ntb)
        self.Bind(EVT_UPDATE_TREE, self.OnUpdateStaffTree)#这个是自建的事件处理
        # self.Bind(wx.EVT_TEXT, self.OnDoSearch, self.search)
    def OnFaceRecognitionPlusPlus(self,event):
        if(not self.workzoneFaceRecognitionWindow):
            self.workzoneFaceRecognitionWindow = FaceRecognitionPanel(self,self.log)
            self.workzoneFaceRecognitionWindow.SetTitle("人脸识别")
        self.workzoneFaceRecognitionWindow.ShowUnknownPic('me.jpg')
        self.workzoneFaceRecognitionWindow.Maximize(True)
        self.workzoneFaceRecognitionWindow.Show(True)
        # faceId1="me.jpg"
        # from Function import GetAllIDWithPicture, GetPicture
        # error, data = GetAllIDWithPicture(self.log)
        # for i in data:
        #     error, picture_data = GetPicture(self.log, i)
        #     if (error != -1):
        #         faceId2 = 'ls.jpg'
        #         self.workzoneFaceRecognitionWindow.ShowKnownPic('ls.jpg')
        #         import base64
        #         with open(faceId2, 'wb') as file:
        #             image = base64.b64decode(picture_data)  # 解码
        #             file.write(image)
        #         data = {"api_key": key, "api_secret": secret}
        #         files = {"image_file1": open(faceId1, "rb"), "image_file2": open(faceId2, "rb")}
        #         response = requests.post(compare_url, data=data, files=files)
        #         req_con = response.content.decode('utf-8')
        #         req_dict = JSONDecoder().decode(req_con)
        #         # print(req_dict)
        #         confindence = req_dict['confidence']
        #         print(confindence)
        #         if confindence >= 65:
        #             print('True')
        #             # break
        #         else:
        #             print('False')
    def OnFaceRecognition(self,event):
        unknown_image = face_recognition.load_image_file("me.jpg")
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        # from Function import GetAllIDWithFaceCharactor,GetFaceCharacter
        # error,data=GetAllIDWithPicture(self.log)
        # import numpy as np
        # # darr =  np.array('[1 2 3 4 5]')
        # # print("darr=",darr)
        # for i in data:
        #     print("ID=",i)
        #     error,face_encoding_data=GetFaceCharacter(self.log,i)
        #     if(error!=-1):
        #         face_encoding_data=np.array(face_encoding_data)
        #         print("face_encoding_data=",face_encoding_data)
        #         #好吧，这个数据是个矩阵，难道要我把数据写成文件，再把文件读出来？
        #         # a=eval(face_encoding_data)
        #         known_faces = [
        #             face_encoding_data
        #         ]
        #     results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
        #     print(i,"'s result is:",results[0])
        from Function import GetAllIDWithPicture,GetPicture
        error,data=GetAllIDWithPicture(self.log)
        for i in data:
            error,picture_data=GetPicture(self.log,i,whichDB=WHICHDB)
            if(error!=-1):
                pic_file_name='ls.jpg'
                import base64
                with open(pic_file_name, 'wb') as file:
                    image = base64.b64decode(picture_data)  # 解码
                    file.write(image)
            image = face_recognition.load_image_file(pic_file_name)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_faces = [
                face_encoding
            ]
            results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
            print(i,"'s result is:",results[0])



    def OnUpdateFaceAll(self,event):
        # box=wx.MessageBox("正在更新数据，请稍候","系统提示信息")
        from Function import GetAllIDWithPicture,GetPicture
        error,data=GetAllIDWithPicture(self.log)
        for i in data:
            error,picture_data=GetPicture(self.log,i,whichDB=WHICHDB)
            if(error!=-1):
                pic_file_name='ls.jpg'
                import base64
                with open(pic_file_name, 'wb') as file:
                    image = base64.b64decode(picture_data)  # 解码
                    file.write(image)
            image = face_recognition.load_image_file(pic_file_name)
            face_encoding = face_recognition.face_encodings(image)[0]
            from Function import UpdateIndividualFaceCharactor
            UpdateIndividualFaceCharactor(i, face_encoding)
        try:
            os.remove(pic_file_name)
        except:
            pass
    def OnUpdateStaffTree(self,event):
        item=self.department_tree.tree.GetFocusedItem()
        itemdata=self.department_tree.tree.GetItemData(item)
        itemtext=self.department_tree.tree.GetItemText(item)
        error,self.staff_department_info=GetStaffBriefInfo(self.log,itemdata,itemtext,whichDB=WHICHDB)
        self.staff_current_info=self.staff_department_info
        self.edit_staff_info.Freeze()
        self.edit_staff_info.ReCreateTree(self.staff_current_info)
        self.edit_staff_info.Thaw()
    def OnNotebookPageChange(self,event):
        current_individual_name=self.workzoneBrowseInfoWindow.exist_page_name_list[self.workzoneBrowseInfoWindow.ntb.GetSelection()]
        from_item=self.edit_staff_info.list.GetFocusedItem()
        for i in self.staff_current_info:
            if(current_individual_name==i[0]):
                to_item = self.staff_current_info.index(i)
                self.edit_staff_info.list.SetItemState(to_item,wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
                self.edit_staff_info.list.Focus(to_item)
            else:
                self.edit_staff_info.list.SetItemState(self.staff_current_info.index(i), 0, wx.LIST_STATE_SELECTED)
    def OnStaffListChanged(self,event):
        self.currentItem = event.Index
        data=[]
        for i in self.staff_current_info[self.currentItem]:
            data.append(i)
        if(not self.workzoneBrowseInfoWindow):
            self.workzoneBrowseInfoWindow = WorkZoneBrowseInfoWindow(self, self, self.log)
            self.workzoneBrowseInfoWindow.SetTitle("浏览个人档案信息")
            self.workzoneBrowseInfoWindow.Maximize(True)
            self.workzoneBrowseInfoWindow.Show(True)
            self.ntb = FNB.FlatNotebook(self, wx.ID_ANY,
                                        agwStyle=FNB.FNB_NODRAG | FNB.FNB_X_ON_TAB | FNB.FNB_FANCY_TABS)
            self.exist_page_name_list = []
        self.workzoneBrowseInfoWindow.ShowIndividualInfoPage(data)
    def OnNewRecordBTN(self,event):
        if(not self.workzoneBrowseInfoWindow):
            self.workzoneBrowseInfoWindow = WorkZoneBrowseInfoWindow(self, self, self.log)
            self.workzoneBrowseInfoWindow.SetTitle("浏览个人档案信息")
            self.workzoneBrowseInfoWindow.Maximize(True)
            self.workzoneBrowseInfoWindow.Show(True)
            self.ntb = FNB.FlatNotebook(self, wx.ID_ANY,
                                        agwStyle=FNB.FNB_NODRAG | FNB.FNB_X_ON_TAB | FNB.FNB_FANCY_TABS)
            self.exist_page_name_list = []
        #此处应先向数据库中增加一条记录，从而获得一个新的员工编号以及返回一个data列表，后面的程序用这个列表来创建编辑页面
        data=self.InsertDataInDB()
        self.workzoneBrowseInfoWindow.NewIndividualInfoPage(data)
    def InsertDataInDB(self,whichDB=0):
        try:
            db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                                 passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
        except:
            wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
            if log:
                log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
            return -1, []
        cursor = db.cursor()
        sql = "DELETE FROM info_staff WHERE 姓名 = '新建员工'"
        cursor.execute(sql)
        db.commit()
        cursor.execute("INSERT INTO info_staff (姓名      ,性别,IC卡编号,电话,密码,工作状态,职别名,出生日期     ,民族,身份证号码,职称,籍贯,入职时间     ,离职时间     ,学历 ,学位,毕业学校,毕业时间,省    ,市,区,街道,照片) "
                                        "VALUES('新建员工','男',''      ,'' ,''  ,'在职'  ,''    ,'1980-01-01','汉族',''     ,'无',''  ,'2019-01-09','1980-01-01','无','无',''      ,'1980' ,'北京','','','','' )")
        db.commit()
        sql = """SELECT `Index` from `info_staff` WHERE `姓名`='新建员工'"""
        cursor.execute(sql)
        data=cursor.fetchone()
        data=str(data[0])
        length = len(data)
        for i in range(5 - length):
            data = '0' + data
        today = datetime.datetime.now()
        year = str(today.year)[2:4]
        data = year + data
        sql = "UPDATE info_staff SET `员工编号` = %s WHERE 姓名='新建员工'"  % data
        cursor.execute(sql)
        db.commit()
        sql = """SELECT `姓名`,`性别`,`员工编号`,`IC卡编号`,`工位编号`,`处`,`科`,`工位名`,`电话`,`密码`,`工作状态`,`职别`,`职别名`,出生日期,民族,身份证号码,职称,籍贯,入职时间,离职时间,学历,学位,毕业学校,毕业时间,婚姻状况,省,市,区,街道 from `info_staff` WHERE `姓名`='新建员工'"""
        cursor.execute(sql)
        data = cursor.fetchone()  # 获得压条信息
        db.close()
        data = list(data)
        return data
    def OnDepartmentChanged(self, event):
        # self.CreateWorkzoneWindow()
        item = event.GetItem()
        itemdata=self.department_tree.tree.GetItemData(item)
        itemtext=self.department_tree.tree.GetItemText(item)
        self.searchctrl.ChangeValue("")
        error,self.staff_department_info=GetStaffBriefInfo(self.log,itemdata,itemtext,whichDB=WHICHDB)
        self.itemdata=itemdata
        self.itemtext=itemtext
        self.staff_current_info=self.staff_department_info
        self.edit_staff_info.Freeze()
        self.edit_staff_info.ReCreateTree(self.staff_current_info)
        self.edit_staff_info.Thaw()
    ######################这部分是search按钮相关的方法###############################################################
    def OnSearch(self, evt):
        self.log.write("OnSearch\r\n")
    def OnCancel(self, evt):
        if not self.search_value:
            return
        self.search_value=""
        self.edit_staff_info.ReCreateTree(self.staff_department_info)
    def OnDoSearch(self, evt):
        self.search_value = self.searchctrl.GetValue()
        if not self.search_value:
            return
        wx.BeginBusyCursor()
        ls_buffer=[]
        for i in self.staff_current_info:
            for j in i:
                if(i.index(j) not in [4,10,11,13,18,19,23]):
                    if(self.search_value in j):
                        ls_buffer.append(i)
                        break
        self.staff_current_info=ls_buffer
        self.edit_staff_info.ReCreateTree(self.staff_current_info)
        wx.EndBusyCursor()

    def MakeMenu(self):
        menu = wx.Menu()
        item = menu.Append(-1, "Recent Searches")
        item.Enable(False)
        for txt in [ "You can maintain",
                     "a list of old",
                     "search strings here",
                     "and bind EVT_MENU to",
                     "catch their selections" ]:
            menu.Append(-1, txt)
        return menu
    ################################################################################################################
    def OnSashDrag(self, event):
        if event.GetDragStatus() == wx.adv.SASH_STATUS_OUT_OF_RANGE:
            return
        eID = event.GetId()
        if eID == ID_WINDOW_LEFT:
            self.leftWindow.SetDefaultSize((event.GetDragRect().width, 1000))
        elif eID == ID_WINDOW_BOTTOM:
            self.bottomWindow.SetDefaultSize((1000, event.GetDragRect().height))
        wx.adv.LayoutAlgorithm().LayoutMDIFrame(self)
        self.GetClientWindow().Refresh()
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutMDIFrame(self)
    def OnExit(self, evt):
        self.Close(True)
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        # tile the background bitmap
        try:
            sz = self.GetClientSize()
        except RuntimeError:#closing demo
            return
        w = self.bg_bmp.GetWidth()
        h = self.bg_bmp.GetHeight()
        x = 0

        while x < sz.width:
            y = 0

            while y < sz.height:
                dc.DrawBitmap(self.bg_bmp, x, y)
                y = y + h

            x = x + w
    def CreateMenuBar(self):
        menu_SYS = wx.Menu()
        item = wx.MenuItem(menu_SYS, ID_Exit, "&X  退出")
        bmp = wx.Bitmap(os.path.normpath(os.path.join(bitmapDir, "exit-16.png")), wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menu_SYS.Append(item)

        menubar = wx.MenuBar()
        menubar.Append(menu_SYS, "&F 系统管理")
        menu_HR = wx.Menu()
        menu_HR.Append(ID_New, "&New Window")
        menu_HR.AppendSeparator()
        menu_HR.Append(ID_Exit, "E&xit")
        menubar.Append(menu_HR, "&S 参数设置")
        menu_HA = wx.Menu()
        item = wx.MenuItem(menu_HA, UPDATE_FACE_CHARACTOR_ALL_ID, "更新面部特征数据")
        bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "ok5.png"))).Scale(width=16, height=16,
                                                                                      quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        item.SetBitmap(bmp)
        menu_HA.Append(item)
        item = wx.MenuItem(menu_HA, FACE_RECOGNITION_ID, "人脸识别1")
        bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "ok5.png"))).Scale(width=16, height=16,
                                                                                      quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        item.SetBitmap(bmp)
        menu_HA.Append(item)
        item = wx.MenuItem(menu_HA, FACE_PLUS_PLUS_ID, "人脸识别2")
        bmp = wx.Image(os.path.normpath(os.path.join(bitmapDir, "ok5.png"))).Scale(width=16, height=16,
                                                                                      quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        item.SetBitmap(bmp)
        menu_HA.Append(item)
        menu_HA.AppendSeparator()
        menu_HA.Append(ID_Exit, "E&xit")
        menubar.Append(menu_HA, "&H 人事管理")
        menu_CHECKIN_OUT = wx.Menu()
        menu_CHECKIN_OUT.Append(ID_New, "&New Window")
        menu_CHECKIN_OUT.AppendSeparator()
        menu_CHECKIN_OUT.Append(ID_Exit, "E&xit")
        menubar.Append(menu_CHECKIN_OUT, "&K 考勤管理")
        menu_SALAY = wx.Menu()
        menu_SALAY.Append(ID_New, "&New Window")
        menu_SALAY.AppendSeparator()
        menu_SALAY.Append(ID_Exit, "E&xit")
        menubar.Append(menu_SALAY, "&P 工资管理")
        menu_CONSUME = wx.Menu()
        menu_CONSUME.Append(ID_New, "&New Window")
        menu_CONSUME.AppendSeparator()
        menu_CONSUME.Append(ID_Exit, "E&xit")
        menubar.Append(menu_CONSUME, "&C 消费管理")
        menu_OTHERS = wx.Menu()
        menu_OTHERS.Append(ID_New, "&New Window")
        menu_OTHERS.AppendSeparator()
        menu_OTHERS.Append(ID_Exit, "E&xit")
        menubar.Append(menu_OTHERS, "&O 其它管理")
        self.SetMenuBar(menubar)
    def CreateWinStruct(self):
        self.CreateLeftWindow()
        self.CreateBottomWindow()
        self.log = MyLogCtrl(self.bottomWindow, -1, "")
        self.log.WriteText('系统开始运行\r\n')
        self.company_name="伊纳克赛有限公司"
        error,data=GetDepartmentInfo(self.log,whichDB=WHICHDB)
        department_list=""
        for i in data:
            if(i=='#'):
                department_list+="'"
            else:
                department_list+=i
        print("department=",department_list)
        self.department_list=eval(department_list)
        error,self.staff_department_info=GetStaffBriefInfo(self.log,"厂","",whichDB=WHICHDB)
        self.CreateLeftPanel()
        self.CreateWorkzoneBrowseInfoWindow()
    def OnDepartmentManageBTN(self,event):
        from DepartmentManageDLG import DepartmentManageDialog
        dlg = DepartmentManageDialog(self, self,self.log)
        dlg.CenterOnScreen()
        if (dlg.ShowModal() == wx.ID_OK):
            pass
        dlg.Destroy()
    def CreateLeftPanel(self):
        leftpanel = wx.Panel(self.leftWindow,-1)
        hbox=wx.BoxSizer()
        vbox = wx.BoxSizer(wx.VERTICAL)
        title_button=wx.Button(leftpanel,-1,"部门管理",size=(100,26),style=wx.ALIGN_LEFT)
        title_button.Bind(wx.EVT_BUTTON,self.OnDepartmentManageBTN)
        vbox.Add(title_button,0,wx.EXPAND)
        self.department_tree=DepartmentTree(leftpanel,self,self.log,size=(200,300))
        self.department_tree.tree.SelectItem(self.department_tree.root)
        vbox.Add(self.department_tree,1,wx.EXPAND)
        # line = wx.StaticLine(leftpanel, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        # vbox.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, 3)
        new_record_btn=wx.Button(leftpanel,-1,"新建人事档案",size=(30,30))
        new_record_btn.Bind(wx.EVT_BUTTON,self.OnNewRecordBTN)
        vbox.Add(new_record_btn, 0, wx.EXPAND)
        hbox.Add(vbox,0,wx.EXPAND,0)
        vbox=wx.BoxSizer(wx.VERTICAL)
        self.NB_HR_Info=self.CreateLeftNoteBook(leftpanel)
        vbox.Add(self.NB_HR_Info, 1, wx.EXPAND)
        # line = wx.StaticLine(leftpanel, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        # vbox.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, 1)
        self.searchctrl = wx.SearchCtrl(leftpanel, size=(100,-1), style=wx.TE_PROCESS_ENTER)
        self.searchctrl.ShowCancelButton(True)
        self.searchctrl.SetMenu(self.MakeMenu())
        # label=wx.StaticText(leftpanel,-1,"查找：")
        # vbox.Add(label, 0, wx.EXPAND|wx.LEFT, 5)
        vbox.Add(self.searchctrl, 0, wx.EXPAND|wx.TOP|wx.BOTTOM,2)
        hbox.Add(vbox,1,wx.EXPAND)
        leftpanel.SetSizer(hbox)

    def CreateLeftNoteBook(self,parent):
        leftnotebook=wx.Notebook(parent, -1, size=(260, 21), style=
                            wx.BK_DEFAULT |
                            wx.BK_TOP
                            # wx.BK_BOTTOM
                            # wx.BK_LEFT
                            # wx.BK_RIGHT
                            # | wx.NB_MULTILINE
                            )
        # Show how to put an image on one of the notebook tabs,
        # first make the image list:
        self.edit_staff_info =EditStaffInfoPanel(leftnotebook,self.log,[])
        leftnotebook.AddPage(self.edit_staff_info, "浏览人事资料")
        self.staff_current_info=self.staff_department_info
        self.edit_staff_info.Freeze()
        self.edit_staff_info.ReCreateTree(self.staff_current_info)
        self.edit_staff_info.Thaw()
        # self.browse_staff_info = BrowseStaffInfoPanel(leftnotebook,[],self.log)
        # leftnotebook.AddPage(self.browse_staff_info, "浏览人事资料")
        il = wx.ImageList(16, 16)
        idx1 = il.Add(images.Smiles.GetBitmap())
        leftnotebook.AssignImageList(il)
        # now put an image on the first tab we just created:
        leftnotebook.SetPageImage(0, idx1)
        return leftnotebook
    def CreateLeftWindow(self):
        self.leftWindow = wx.adv.SashLayoutWindow(self, ID_WINDOW_LEFT, style=wx.NO_BORDER | wx.adv.SW_3D)
        self.leftWindow.SetDefaultSize((440, 1000))
        self.leftWindow.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self.leftWindow.SetAlignment(wx.adv.LAYOUT_LEFT)
        # win.SetBackgroundColour(wx.Colour(0, 255, 0))
        self.leftWindow.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self.leftWindow.SetExtraBorderSize(5)
        # 现在这样先定义左窗口，再定义下窗口，则先把窗口左右切一刀，再把右窗口上下切一刀
    def CreateBottomWindow(self):
        self.bottomWindow = wx.adv.SashLayoutWindow(self, ID_WINDOW_BOTTOM, style=wx.NO_BORDER | wx.adv.SW_3D)
        self.bottomWindow.SetDefaultSize((1000, 150))
        self.bottomWindow.SetOrientation(wx.adv.LAYOUT_HORIZONTAL)
        self.bottomWindow.SetAlignment(wx.adv.LAYOUT_BOTTOM)
        # win.SetBackgroundColour(wx.Colour(0, 0, 255))
        self.bottomWindow.SetSashVisible(wx.adv.SASH_TOP, True)
        self.bottomWindow.SetExtraBorderSize(5)
    def CreateWorkzoneBrowseInfoWindow(self):
        self.workzoneBrowseInfoWindow = WorkZoneBrowseInfoWindow(self,self,self.log)
        self.workzoneBrowseInfoWindow.SetTitle("浏览个人档案信息")
        self.workzoneBrowseInfoWindow.Maximize(True)
        self.workzoneBrowseInfoWindow.Show(True)
class MyLogCtrl(wx.TextCtrl):#系统日志显示控件
    def __init__(self, parent,id=-1,title="",position=wx.Point(0,0),size=wx.Size(150,90),style=wx.NO_BORDER | wx.TE_MULTILINE|wx.TE_READONLY| wx.TE_RICH2):
        self.parent=parent
        wx.TextCtrl.__init__(self, parent,id,title, position,size,style)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_DCLICK,self.OnLeftDown)
    def OnLeftDown(self,evt):
        pass
    def SaveLogFile(self):
        import time
        t = time.localtime(time.time())
        filename = time.strftime("%Y%m%d%H.log", t)
        file=open(filename,'w+')
        content=self.GetValue()
        file.write(content)
        file.close()
        self.SetValue("")
    def WriteText(self, text, enable=True, font=wx.NORMAL_FONT, colour=wx.BLACK,bk_colour=wx.NullColour):
        import time
        if (enable):
            if(colour!=wx.BLACK):
                wx.Bell()
            try:
                t = time.localtime(time.time())
                st = time.strftime("%Y年%m月%d日%H:%M:%S  ", t)
                text = st + text
            # wx.TextCtrl.SetFont(self, font)
            # wx.TextCtrl.SetForegroundColour(self, colour)
            # wx.TextCtrl.SetBackgroundColour(self,backgroundcolour)
                start=self.GetLastPosition()
                wx.TextCtrl.WriteText(self, text)
                self.SetStyle(start, self.GetLastPosition(), wx.TextAttr(colour,bk_colour))
                self.ShowPosition(start)
            except:
                pass
