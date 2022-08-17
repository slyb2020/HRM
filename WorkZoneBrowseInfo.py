#!/usr/bin/env python
# encoding: utf-8
'''
@author: slyb
@license: (C) Copyright 2017-2020, 天津定智科技有限公司.
@contact: slyb@tju.edu.cn
@file: EditStaffInfoPanel.py
@time: 2019/9/2 9:18
@desc:
'''
import wx
import cv2
from Function import *
from TakePicture import *
import images
from ID_DEFINE import *
import wx.lib.agw.flatnotebook as FNB
import datetime
import ID_VERIFY
import  string
from Validator import *

import wx.lib.newevent
# import face_recognition

(UpdateTreeEvent, EVT_UPDATE_TREE) = wx.lib.newevent.NewEvent()

def opj(path):
    """Convert paths to the platform-specific separator"""
    st = os.path.join(*tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        st = '/' + st
    return st

class WorkZoneBrowseInfoWindow(wx.MDIChildFrame):
    def __init__(self, parent,master,log):
        wx.MDIChildFrame.__init__(self, parent, size=(800,600))
        self.log = log
        self.master=master
        self.parent=parent
        self._bShowImages = False
        self._bVCStyle = False

        self._newPageCounter = 0
        self._ImageList = wx.ImageList(16, 16)
        self._ImageList.Add(images._book_red.GetBitmap())
        self._ImageList.Add(images._book_green.GetBitmap())
        self._ImageList.Add(images._book_blue.GetBitmap())
        self.SetIcon(images.Mondrian.GetIcon())
        self.ntb = FNB.FlatNotebook(self, wx.ID_ANY, agwStyle=FNB.FNB_NODRAG|FNB.FNB_X_ON_TAB|FNB.FNB_FANCY_TABS)
        self.ntb.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_CLOSING,self.OnPageClose)
        self.exist_page_name_list=[]
    def OnPageClose(self,event):
        self.exist_page_name_list.pop(self.ntb.GetSelection())
        event.Skip()
    def NewIndividualInfoPage(self,data):
        self.exist_page_name_list.append(data[0])
        self.ntb.Freeze()
        page = BrowseIndividualInfoPanel(self.ntb, self.master, self.log, data,EDIT_MODE)
        self.ntb.Thaw()
        self.ntb.AddPage(page, "新建档案信息")
        self.ntb.SetSelection(self.exist_page_name_list.index(data[0]))

    def ShowIndividualInfoPage(self,data):
            if (data[0] not in self.exist_page_name_list):
                self.exist_page_name_list.append(data[0])
                self.ntb.Freeze()
                page=BrowseIndividualInfoPanel(self.ntb,self.master,self.log,data)
                self.ntb.Thaw()
                self.ntb.AddPage(page,"%s档案信息"%data[0])
                self.ntb.SetSelection(self.exist_page_name_list.index(data[0]))
            else:
                self.ntb.SetSelection(self.exist_page_name_list.index(data[0]))
class BrowseIndividualInfoPanel(wx.Panel):
    def __init__(self, parent,master,log,data,mode=BROWSE_MODE):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        self.master=master
        self.parent=parent
        self.data=data
        self.picture_changed = False
        self.SetBackgroundColour('light blue')
        vbox=wx.BoxSizer(wx.VERTICAL)
        ########################左上部基本信息区########################################################################
        hbox=wx.BoxSizer()
        label=wx.StaticText(self,-1,"员工编号:",size=(60,-1),style=wx.TE_RIGHT)
        # self.member_ID=str(data[2],'utf-8')
        self.member_ID=data[2]
        self.member_ID_CTRL=wx.TextCtrl(self,-1,self.member_ID,size=(150,25))
        self.member_ID_CTRL.Enable(False)
        hbox.Add((10,-1))
        hbox.Add(label,0,wx.TOP|wx.RIGHT,5)
        hbox.Add(self.member_ID_CTRL,0)
        # hbox.Add((15,-1))
        self.name=data[0]
        if(self.name=="新建员工"):
            self.name=""
        label=wx.StaticText(self,-1,"姓名:",size=(60,-1),style=wx.TE_RIGHT)
        self.name_CTRL=wx.TextCtrl(self,-1,self.name,size=(100,25))
        self.name_CTRL.Enable(False)
        self.name_CTRL.Bind(wx.EVT_KILL_FOCUS,self.OnNameKillFocus)
        hbox.Add((10,-1))
        hbox.Add(label,0,wx.TOP|wx.RIGHT,5)
        hbox.Add(self.name_CTRL,0)
        # hbox.Add((15,-1))
        self.sexy=data[1]
        label=wx.StaticText(self,-1,"性别:",size=(50,-1),style=wx.TE_RIGHT)
        self.sexy_COMB=wx.ComboBox(self,-1,self.sexy,size=(120,25),choices=["男","女"])
        self.sexy_COMB.Enable(False)
        # hbox.Add((10,-1))
        hbox.Add(label,0,wx.TOP|wx.RIGHT,5)
        hbox.Add(self.sexy_COMB,0)
        # hbox.Add((15,-1))
        vbox.Add((-1,15))
        vbox.Add(hbox,0)
        today=datetime.datetime.now()
        hbox=wx.BoxSizer()
        label=wx.StaticText(self,-1,"出生日期:",size=(60,-1),style=wx.TE_RIGHT)
        self.birthday=data[13]
        self.birthday_CTRL=wx.adv.DatePickerCtrl(self, size=(150,-1),dt=self.birthday,
                                style = wx.adv.DP_DROPDOWN
                                      # | wx.adv.DP_SHOWCENTURY
                                      # | wx.adv.DP_ALLOWNONE
                                        )
        early_day=datetime.datetime(1900,1,1)
        self.birthday_CTRL.SetRange(early_day,today)
        self.birthday_CTRL.Enable(False)
        hbox.Add((10,-1))
        hbox.Add(label,0,wx.TOP|wx.RIGHT,5)
        hbox.Add(self.birthday_CTRL,0)
        # hbox.Add((15,-1))
        label=wx.StaticText(self,-1,"年龄:",size=(60,-1),style=wx.TE_RIGHT)
        self.age=str(today.year-self.birthday.year)
        self.age_CTRL=wx.TextCtrl(self,-1,self.age,size=(100,25))
        self.age_CTRL.Enable(False)
        hbox.Add((10,-1))
        hbox.Add(label,0,wx.TOP|wx.RIGHT,5)
        hbox.Add(self.age_CTRL,0)
        # hbox.Add((15,-1))
        label=wx.StaticText(self,-1,"民族:",size=(50,-1),style=wx.TE_RIGHT)
        self.nationality=data[14]
        self.nationality_COMBO=wx.ComboBox(self,-1,self.nationality,size=(120,25),choices=['汉族','蒙古族','回族','藏族','维吾尔族','苗族','彝族','壮族','布依族','朝鲜族','满族','侗族','瑶族','白族','土家族','哈尼族','哈萨克族','傣族','黎族','僳僳族','佤族','畲族','高山族','拉祜族','水族','东乡族','纳西族','景颇族','柯尔克孜族','土族','达斡尔族','仫佬族','羌族','布朗族','撒拉族','毛南族','仡佬族','锡伯族','阿昌族','普米族','塔吉克族','怒族','乌孜别克族','俄罗斯族','鄂温克族','德昂族','保安族','裕固族','京族','塔塔尔族','独龙族','鄂伦春族','赫哲族','门巴族','珞巴族','基诺族'])
        self.nationality_COMBO.Enable(False)
        # hbox.Add((10,-1))
        hbox.Add(label,0,wx.TOP|wx.RIGHT,5)
        hbox.Add(self.nationality_COMBO,0)
        # hbox.Add((15,-1))
        vbox.Add((-1,15))
        vbox.Add(hbox,0)

        hbox = wx.BoxSizer()
        label = wx.StaticText(self, -1, "身份证号:", size=(60, -1), style=wx.TE_RIGHT)
        self.id=data[15]
        self.ID_CTRL = wx.TextCtrl(self, -1, self.id, size=(150, 25),validator = MyValidator(ID_ONLY))
        self.ID_CTRL.Bind(wx.EVT_KILL_FOCUS,self.OnIDKillFocus)
        self.ID_CTRL.Enable(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.ID_CTRL, 0)
        # hbox.Add((15,-1))
        self.marriage=data[24]
        label = wx.StaticText(self, -1, "婚姻状况:", size=(60, -1), style=wx.TE_RIGHT)
        self.marriage_COMBO = wx.ComboBox(self, -1,self.marriage, size=(100, 25), choices=["未婚","已婚","离异","丧偶"])
        self.marriage_COMBO.Enable(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.marriage_COMBO, 0)
        # hbox.Add((15,-1))
        self.phone_number=data[8]
        self.marriage=data[24]
        label = wx.StaticText(self, -1, "电话:", size=(50, -1), style=wx.TE_RIGHT)
        self.phone_CTRL = wx.TextCtrl(self, -1, self.phone_number, size=(120, 25))
        self.phone_CTRL.Enable(False)
        # hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.phone_CTRL, 0)
        # hbox.Add((15,-1))
        vbox.Add((-1, 20))
        vbox.Add(hbox, 0)
        hbox = wx.BoxSizer()
        self.IC=data[3]
        label = wx.StaticText(self, -1, "IC卡编号:", size=(60, -1), style=wx.TE_RIGHT)
        # self.IC_BUTTON = wx.TextCtrl(self, -1, self.IC, size=(150, 25), style=wx.TE_READONLY)
        self.IC_BUTTON = wx.Button(self, -1, self.IC, size=(150, 25))
        self.IC_BUTTON.Enable(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.IC_BUTTON, 0)
        # hbox.Add((15,-1))
        label = wx.StaticText(self, -1, "职称:", size=(60, -1), style=wx.TE_RIGHT)
        self.techtitle=data[16]
        self.techtitle_COMBO = wx.ComboBox(self, -1, self.techtitle, size=(100, 25), choices=["无","正高级","副高级","中级","初级"])
        self.techtitle_COMBO.Enable(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.techtitle_COMBO, 0)
        # hbox.Add((15,-1))
        self.rank=data[12]
        label = wx.StaticText(self, -1, "职务:", size=(50, -1), style=wx.TE_RIGHT)
        # self.rank_CTRL = wx.TextCtrl(self, -1, self.rank, size=(100, 25))
        self.rank_CTRL = wx.ComboBox(self,-1,size=(120,25))
        self.rank_CTRL.SetValue(self.rank)
        self.rank_CTRL.Enable(False)
        # hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.rank_CTRL, 0)
        # hbox.Add((15,-1))
        vbox.Add((-1, 20))
        vbox.Add(hbox, 0)

        hbox = wx.BoxSizer()
        self.onboarding_time=data[18]
        label = wx.StaticText(self, -1, "入职时间:", size=(60, -1), style=wx.TE_RIGHT)
        self.Onboarding_time_CTRL=wx.adv.DatePickerCtrl(self, size=(150,-1),dt=self.onboarding_time,
                                style = wx.adv.DP_DROPDOWN
                                      # | wx.adv.DP_SHOWCENTURY
                                      # | wx.adv.DP_ALLOWNONE
                                        )
        self.Onboarding_time_CTRL.Enable(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.Onboarding_time_CTRL, 0)
        # hbox.Add((15,-1))
        # self.employment_state=str(data[10],'utf-8')
        self.employment_state=data[10]
        self.ex_employment_state=self.employment_state
        label = wx.StaticText(self, -1, "任职状态:", size=(60, -1), style=wx.TE_RIGHT)
        self.employment_state_COMBO = wx.ComboBox(self, -1,self.employment_state, size=(100, 25), choices=['在职','离职','病假','产假','停薪留职','退休'])
        self.employment_state_COMBO.Bind(wx.EVT_COMBOBOX,self.OnEmploymentStateChanged)
        self.employment_state_COMBO.Enable(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.employment_state_COMBO, 0)
        # hbox.Add((15,-1))
        self.panel2=wx.Panel(self,-1)
        if(self.employment_state=="离职"):
            self.employment_state_COMBO.SetBackgroundColour("pink")
            label = wx.StaticText(self.panel2, -1, "离职时间:", size=(60, -1), style=wx.TE_RIGHT)
            self.dimission_year=data[19]
            self.dimission_year_CTRL = wx.adv.DatePickerCtrl(self.panel2, size=(100, -1), dt=self.dimission_year,
                                              style=wx.adv.DP_DROPDOWN
                                              # | wx.adv.DP_SHOWCENTURY
                                              # | wx.adv.DP_ALLOWNONE
                                              )
            self.dimission_year_CTRL.Enable(False)
        else:
            label = wx.StaticText(self.panel2, -1, "工龄:", size=(50, -1), style=wx.TE_RIGHT)
            self.job_year_CTRL = wx.TextCtrl(self.panel2, -1, str(today.year-self.onboarding_time.year), size=(100, 25), style=wx.TE_READONLY)
            unit_label = wx.StaticText(self.panel2, -1, "年", size=(20, -1), style=wx.TE_RIGHT)
        # hbox.Add((10, -1))
        ls_box=wx.BoxSizer()
        ls_box.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        if(self.employment_state=="离职"):
            ls_box.Add(self.dimission_year_CTRL, 0)
        else:
            ls_box.Add(self.job_year_CTRL, 0)
            ls_box.Add(unit_label, 0, wx.TOP | wx.RIGHT, 5)
        self.panel2.SetSizer(ls_box)
        hbox.Add(self.panel2,0)
        vbox.Add((-1, 20))
        vbox.Add(hbox, 0)

        hbox = wx.BoxSizer()
        label = wx.StaticText(self, -1, "任职部门:", size=(60, -1), style=wx.TE_RIGHT)
        chu_list = []
        ke_list=[]
        self.chu=data[5]
        if(self.master.department_list!=[]):
            for i in self.master.department_list:
                chu_list.append(i[0])
                if(i[0]==self.chu):
                    ke_list=i[1]
        else:
            chu_list.append(data[5])
        self.chu_COMBO = wx.ComboBox(self, -1, self.chu, size=(150, 25),choices=chu_list,style=wx.TE_READONLY)
        self.chu_COMBO.Bind(wx.EVT_COMBOBOX,self.OnChuComboChanged)
        self.chu_COMBO.Enable(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.chu_COMBO, 0)
        # hbox.Add((15,-1))
        self.ke=data[6]
        self.position=data[7]
        list=[]
        position_list=[]
        for i in ke_list:
            list.append(i[0])
            if(i[0]==self.ke):
                position_list=i[1]
        self.ke_COMBO = wx.ComboBox(self, -1, self.ke, size=(155, 25), choices=list, style=wx.TE_READONLY)
        hbox.Add((20, -1))
        hbox.Add(self.ke_COMBO, 0)
        self.position_COMBO = wx.ComboBox(self, -1, self.position, size=(155, 25), choices=list, style=wx.TE_READONLY)
        self.position_COMBO.Bind(wx.EVT_COMBOBOX,self.OnPositionCOMBOChanged)
        hbox.Add((20, -1))
        hbox.Add(self.position_COMBO, 0)
        self.ke_COMBO.Bind(wx.EVT_COMBOBOX, self.OnKeComboChanged)
        if(self.ke!=""):
            self.ke_COMBO.Enable(False)
            if(position_list!=[]):
                list=[]
                for i in position_list:
                    list.append(i[0])
            self.position_COMBO.SetItems(list)
            self.position_COMBO.SetValue(self.position)
            self.position_COMBO.Enable(False)
            # self.ke_COMBO.Show(True)
            # self.position_COMBO.Show(True)
        # else:
        #     self.ke_COMBO.Show(False)
        #     self.position_COMBO.Show(False)
        if self.position=='':
            position=self.ke
        else:
            position=self.position
        items=[]
        if position!='':
            items = jobTitleDic[position]
        self.rank_CTRL.SetItems(items)
        self.rank_CTRL.SetValue(self.rank)
        vbox.Add((-1, 20))
        vbox.Add(hbox, 0)
        vbox.Add((-1,15))
        hbox = wx.BoxSizer()
        self.hometown=data[17]
        label = wx.StaticText(self, -1, "出生地:", size=(60, -1), style=wx.TE_RIGHT)
        self.hometown_CTRL = wx.TextCtrl(self, -1, self.hometown, size=(150, 25))
        self.hometown_CTRL.Enable(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.hometown_CTRL, 0)
        self.password=data[9]
        label = wx.StaticText(self, -1, "密码:", size=(30, -1), style=wx.TE_RIGHT)
        self.password_CTRL = wx.TextCtrl(self, -1, self.password, size=(130, 25), style=wx.TE_READONLY|wx.TE_PASSWORD)
        self.password_BTN = wx.Button(self,-1,"更改密码",size=(155,25))
        self.password_BTN.Bind(wx.EVT_BUTTON,self.OnChangePassword)
        self.password_BTN.Show(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.password_CTRL, 0)
        hbox.Add((20,-1))
        hbox.Add(self.password_BTN, 0)
        vbox.Add(hbox, 0)
        vbox.Add((-1,15))

        hhbox=wx.BoxSizer()
        hhbox.Add(vbox,0)
        hhbox.Add((20,-1))
        line=wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        hhbox.Add(line,0,wx.EXPAND)
        ########################右上部照片显示息区######################################################################
        self.picture_PANEL = wx.Panel(self, wx.ID_ANY, size=(250, 285), style=wx.TAB_TRAVERSAL)
        error,self.picture_data=GetPicture(self.log,self.member_ID,whichDB=WHICHDB)
        if(error==-1):
            picture_state=False
        else:
            if(self.picture_data==""):
                picture_state=False
            else:
                picture_state=True
        if(picture_state==True):
            self.pic_file_name=picDir + '\\%s.jpg' % self.member_ID
            import base64
            with open(self.pic_file_name, 'wb') as file:
                image = base64.b64decode(self.picture_data)  # 解码
                file.write(image)
        else:
            self.pic_file_name=picDir + "\\default.jpg"
        self.ex_pic_file_name=self.pic_file_name
        bmp_common = wx.Image(self.pic_file_name).Scale(width=210, height=285,
                                                        quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.statBmp = wx.StaticBitmap(self.picture_PANEL, wx.ID_ANY, bmp_common)
        pic_box = wx.BoxSizer()
        pic_box.Add(self.statBmp, 0)
        pic_btn_box=wx.BoxSizer(wx.VERTICAL)
        self.take_pic_btn=wx.Button(self.picture_PANEL,-1,"拍\r\n摄\r\n照\r\n片",size=(40,60))
        self.load_pic_btn=wx.Button(self.picture_PANEL,-1,"选\r\n择\r\n照\r\n片",size=(40,60))
        self.load_pic_btn.Bind(wx.EVT_BUTTON,self.OnLoadPicBtn)
        self.take_pic_btn.Bind(wx.EVT_BUTTON,self.OnTakePicBtn)
        self.take_pic_btn.Show(False)
        self.load_pic_btn.Show(False)
        pic_btn_box.Add(self.take_pic_btn,1,wx.EXPAND|wx.LEFT,5)
        pic_btn_box.Add(self.load_pic_btn,1,wx.EXPAND|wx.LEFT,5)
        pic_box.Add(pic_btn_box,0,wx.EXPAND)
        self.picture_PANEL.SetSizer(pic_box)
        self.picture_PANEL.Layout()
        self.picture_PANEL.Refresh()

        hhbox.Add((10,-1))
        hhbox.Add(self.picture_PANEL,0,wx.TOP,15)

        vvbox=wx.BoxSizer(wx.VERTICAL)
        vvbox.Add(hhbox,0,wx.EXPAND)
        line=wx.StaticLine(self, -1)
        vvbox.Add(line,0,wx.EXPAND)
        ########################底部学历信息区##########################################################################
        hbox = wx.BoxSizer()
        self.education=data[20]
        label = wx.StaticText(self, -1, "学历:", size=(60, -1), style=wx.TE_RIGHT)
        self.education_COMBO = wx.ComboBox(self, -1, self.education, size=(150, 25), choices=["研究生","本科","大专","中专","技校","高中","初中","小学","无"],style=wx.TE_READONLY)
        self.education_COMBO.Enable(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.education_COMBO, 0)
        # hbox.Add((15,-1))
        self.education_degree=data[21]
        label = wx.StaticText(self, -1, "学位:", size=(60, -1), style=wx.TE_RIGHT)
        self.education_degree_COMBO = wx.ComboBox(self, -1, self.education_degree, size=(100, 25),choices=['博士','硕士','本科','学士','无'], style=wx.TE_READONLY)
        self.education_degree_COMBO.Enable(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.education_degree_COMBO, 0)
        # hbox.Add((15,-1))
        self.school_name=data[22]
        label = wx.StaticText(self, -1, "毕业学校:", size=(80, -1), style=wx.TE_RIGHT)
        self.school_name_CTRL = wx.TextCtrl(self, -1, self.school_name, size=(150, 25))
        self.school_name_CTRL.Enable(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.school_name_CTRL, 0)
        # hbox.Add((15,-1))
        self.graduate_year=str(data[23])
        label = wx.StaticText(self, -1, "毕业时间:", size=(60, -1), style=wx.TE_RIGHT)
        self.graduate_year_CTRL=wx.SpinCtrl(self,-1, value=self.graduate_year, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.SP_ARROW_KEYS, min=1960, max=2020, initial=0)
        self.graduate_year_CTRL.Enable(False)
        hbox.Add((10, -1))
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.graduate_year_CTRL, 0)
        vvbox.Add((-1, 20))
        vvbox.Add(hbox, 0)

        hbox = wx.BoxSizer()
        label = wx.StaticText(self, -1, "家庭住址:", size=(70, -1), style=wx.TE_RIGHT)
        self.province=data[25]
        self.province_COMBO = wx.ComboBox(self, -1, self.province, size=(90, 25), choices=["黑龙江","吉林","辽宁","北京","天津","内蒙古",
                "山东","河北","河南","山西","陕西","甘肃","宁夏","青海","新疆","西藏","云南","贵州","四川","广西","广东","湖南","湖北","江西",
                "江苏", "安徽", "浙江", "重庆", "上海", "福建","香港", "澳门", "台湾", "海南",],style=wx.TE_READONLY)
        self.province_COMBO.Bind(wx.EVT_COMBOBOX,self.OnProvinceChanged)
        self.province_COMBO.Enable(False)
        label2 = wx.StaticText(self, -1, "省", size=(15, -1), style=wx.TE_RIGHT)
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add(self.province_COMBO, 0)
        hbox.Add(label2, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5)
        hbox.Add((10, -1))
        self.city=data[26]
        city_list=[data[26]]
        for i in PROVINCE_CITY_LIST:
            if(self.province==i[0]):
                city_list=i[1]
        self.city_COMBO = wx.ComboBox(self, -1, self.city, size=(100, 25),choices=city_list, style=wx.TE_READONLY)
        self.city_COMBO.Enable(False)
        label = wx.StaticText(self, -1, "市", size=(15, -1), style=wx.TE_RIGHT)
        hbox.Add(self.city_COMBO, 0)
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add((10,-1))
        self.county=data[27]
        self.county_CTRL = wx.TextCtrl(self, -1,self.county, size=(150, 25))
        self.county_CTRL.Enable(False)
        label = wx.StaticText(self, -1, "县、区", size=(45, -1), style=wx.TE_RIGHT)
        hbox.Add(self.county_CTRL, 0)
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        hbox.Add((10,-1))
        self.road=data[28]
        self.road_CTRL=wx.TextCtrl(self,-1, value=self.road, size=(280, 25), style=wx.TE_READONLY)
        self.road_CTRL.Enable(False)
        label = wx.StaticText(self, -1, "街道", size=(30, -1), style=wx.TE_RIGHT)
        hbox.Add(self.road_CTRL, 0)
        hbox.Add(label, 0, wx.TOP | wx.RIGHT, 5)
        vvbox.Add((-1, 20))
        vvbox.Add(hbox, 0)
        vvbox.Add((10,10),1,wx.EXPAND)
        line=wx.StaticLine(self, -1)
        vvbox.Add(line,0,wx.EXPAND)
        hhbox=wx.BoxSizer()
        self.btn_panel=wx.Panel(self,-1)
        btn_box=wx.BoxSizer()
        self.btn_edit=wx.Button(self.btn_panel,-1,"修改个人信息",size=(200,40))
        self.btn_edit.Bind(wx.EVT_BUTTON,self.OnEditInfoButton)
        btn_box.Add(self.btn_edit,1,wx.EXPAND)
        self.btn_panel.SetSizer(btn_box)
        hhbox.Add(self.btn_panel,1)
        vvbox.Add(hhbox,0,wx.EXPAND|wx.ALL,20)
        self.SetSizer(vvbox)
        if(mode==EDIT_MODE):
            self.SwitchToEditMode()
    def OnPositionCOMBOChanged(self,event):
        position = self.position_COMBO.GetValue()
        if position!=self.position:
            self.position = position
            items = jobTitleDic[position]
            self.rank_CTRL.SetItems(items)
            self.rank_CTRL.SetValue(items[0])
    def OnKeComboChanged(self,event):
        self.position_COMBO.SetItems([])
        self.position_COMBO.Enable(False)
        chu=self.chu_COMBO.GetValue()
        ke=self.ke_COMBO.GetValue()
        list=[]
        if(ke):
            chu = self.chu_COMBO.GetValue()  # 获得选择的处名
            ke_list = []
            for i in self.master.department_list:  # 那么把此处下的各个科及工位信息生成一个"ke"列表
                if (i[0] == chu):
                    ke_list = i[1]
            for i in ke_list:
                if(i[0]==ke):
                    position_list=i[1]
            for i in position_list:
                list.append(i[0])
        if(list):#说明有工位列表
            # self.position_COMBO.Show(True)
            self.position_COMBO.SetItems(list)
            if(len(list)==1):#只有一个工位可选
                self.position_COMBO.SetValue(list[0])
                self.position_COMBO.Enable(False)
            else:
                self.position_COMBO.SetValue("")
                self.position_COMBO.Enable(True)
        else:
            jobTitle = jobTitleDic[ke]
            # jobTitle = eval(jobTitle)
            self.rank_CTRL.SetValue(jobTitle[0])
            # self.position_COMBO.Show(False)
            self.position_COMBO.SetValue("")
            self.position_COMBO.Enable(False)
        # self.Layout()
        # self.Refresh()
    def OnChangePassword(self,event):
        dlg = wx.TextEntryDialog(
                self, '在修改密码之前，请先输入原密码：',
                '修改用户密码对话框', 'Python',style=wx.TE_PASSWORD|wx.OK)
        dlg.SetValue("")
        dlg.CenterOnScreen()
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
            if dlg.GetValue()!=self.password:
                wx.MessageBox("密码错误，修改密码操作被取消！")
                return
        dlg = wx.TextEntryDialog(
                self, '请输入新密码：',
                '修改用户密码对话框', 'Python',style=wx.TE_PASSWORD|wx.OK)
        dlg.SetValue("")
        dlg.CenterOnScreen()
        if dlg.ShowModal() == wx.ID_OK:
            password1 = dlg.GetValue()
        dlg.Destroy()
        dlg = wx.TextEntryDialog(
                self, '请再输入一次新密码：',
                '修改用户密码对话框', 'Python',style=wx.TE_PASSWORD|wx.OK)
        dlg.SetValue("")
        dlg.CenterOnScreen()
        if dlg.ShowModal() == wx.ID_OK:
            password2 = dlg.GetValue()
        dlg.Destroy()
        if password2==password1:
            wx.MessageBox("密码修改成功！")
            self.password_CTRL.SetValue(password1)
            self.password=password1
        else:
            wx.MessageBox("两次输入的密码不一致，密码修改操作被取消！")

    def OnChuComboChanged(self,event):
        chu=self.chu_COMBO.GetValue()#获得选择的处名
        ke_list = []
        for i in self.master.department_list:#那么把此处下的各个科及工位信息生成一个"ke"列表
            if (i[0] == chu):
                ke_list = i[1]
        if ke_list!=[]:
            self.ke_COMBO.Show(True)
        self.ke_COMBO.SetItems([])
        self.ke_COMBO.Enable(False)
        self.position_COMBO.SetItems([])
        self.position_COMBO.Enable(False)
        # self.Layout()
        # self.Refresh()
        if ke_list!=[]:#如果"ke"列表不为空，说明后面害的通过combo控件来选择可，所以需要对ke_combo控件进行初始化
            list=[]
            for i in ke_list:#根据"ke"列表生成一个纯粹的下属科名列表（科列表里还包括各个科所属的工位名，不能直接用）
                list.append(i[0])
            if(len(list)==1):#ke_list不为空则list一定不会为空，所以不对len（list）==0的情况进行判断
                self.ke_COMBO.SetItems(list)
                self.ke_COMBO.SetValue(list[0])
                self.ke_COMBO.Enable(False)
            else:
                self.ke_COMBO.SetItems(list)
                self.ke_COMBO.SetValue("")
                self.ke_COMBO.Enable(True)
                return
        else:
            self.ke_COMBO.SetValue("")
            self.ke_COMBO.Enable(False)

    def OnNameKillFocus(self,event):
        if(self.name_CTRL.GetValue()):
            self.name_CTRL.SetBackgroundColour("white")
            event.Skip()
        else:
            self.name_CTRL.SetBackgroundColour("pink")
            self.name_CTRL.SetFocus()
    def InstallData(self):
        self.name=self.name_CTRL.GetValue()
        self.sexy=self.sexy_COMB.GetValue()
        self.birthday=self.birthday_CTRL.GetValue()
        self.nationality=self.nationality_COMBO.GetValue()
        self.id=self.ID_CTRL.GetValue()
        self.marriage=self.marriage_COMBO.GetValue()
        self.phone_number=self.phone_CTRL.GetValue()
        self.IC=self.IC_BUTTON.GetLabel()
        self.techtitle=self.techtitle_COMBO.GetValue()
        self.rank=self.rank_CTRL.GetValue()
        self.onboarding_time=self.Onboarding_time_CTRL.GetValue()
        self.employment_state=self.employment_state_COMBO.GetValue()
        if(self.employment_state=='离职'):
            self.dimission_year=self.dimission_year_CTRL.GetValue()
        else:
            self.dimission_year = ""
        self.chu=self.chu_COMBO.GetValue()
        self.ke=self.ke_COMBO.GetValue()
        self.position=self.position_COMBO.GetValue()
        self.hometown=self.hometown_CTRL.GetValue()
        self.password=self.password_CTRL.GetValue()
        self.education=self.education_COMBO.GetValue()
        self.education_degree=self.education_degree_COMBO.GetValue()
        self.school_name=self.school_name_CTRL.GetValue()
        self.graduate_year=self.graduate_year_CTRL.GetValue()
        self.province=self.province_COMBO.GetValue()
        self.city=self.city_COMBO.GetValue()
        self.county=self.county_CTRL.GetValue()
        self.road=self.road_CTRL.GetValue()
    def OnLoadPicBtn(self,event):
        wildcard = "JPEG文件 (*.jpg)|*.jpg|" \
                   "PNG 文件 (*.png)|*.png|" \
                   "BMP 文件 (*.bmp)|*.bmp|" \
                   "所有文件 (*.*)|*.*"
        dlg = wx.FileDialog(
            self, message="请选择照片文件",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN
                  # | wx.FD_MULTIPLE
                  | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                  wx.FD_PREVIEW
            )
        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            self.picture_changed=True
            pic_file_names = dlg.GetPaths()
            self.pic_file_name=pic_file_names[0]
            bmp_common = wx.Image(self.pic_file_name).Scale(width=210, height=285,quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
            self.statBmp = wx.StaticBitmap(self.picture_PANEL, wx.ID_ANY, bmp_common)
            self.statBmp.Refresh()
        dlg.Destroy()
    def OnEmploymentStateChanged(self,event):
        employment_state=self.employment_state_COMBO.GetValue()
        today = datetime.datetime.now()
        if(employment_state!=self.ex_employment_state):
            if(self.ex_employment_state=='离职'):
                # print"换成工龄"
                self.panel2.DestroyChildren()
                hbox=wx.BoxSizer()
                label = wx.StaticText(self.panel2, -1, "工龄:", size=(60, -1), style=wx.TE_RIGHT)
                self.job_year_CTRL = wx.TextCtrl(self.panel2, -1, str(today.year - self.onboarding_time.year),
                                                 size=(80, 25), style=wx.TE_READONLY)
                unit_label = wx.StaticText(self.panel2, -1, "年", size=(20, -1), style=wx.TE_RIGHT)
                hbox.Add(label,0,wx.TOP|wx.RIGHT,5)
                hbox.Add(self.job_year_CTRL,0)
                hbox.Add(unit_label,0,wx.TOP|wx.RIGHT,5)
                self.panel2.SetSizer(hbox)
                self.panel2.Layout()
            elif(employment_state=='离职'):
                # print"换成离职时间"
                self.panel2.DestroyChildren()
                hbox=wx.BoxSizer()
                label = wx.StaticText(self.panel2, -1, "离职时间:", size=(60, -1), style=wx.TE_RIGHT)
                self.dimission_year=today
                self.dimission_year_CTRL = wx.adv.DatePickerCtrl(self.panel2, size=(100, -1), dt=self.dimission_year,
                                                                 style=wx.adv.DP_DROPDOWN
                                                                 # | wx.adv.DP_SHOWCENTURY
                                                                 # | wx.adv.DP_ALLOWNONE
                                                                 )
                hbox.Add(label,0,wx.TOP|wx.RIGHT,5)
                hbox.Add(self.dimission_year_CTRL,0)
                self.panel2.SetSizer(hbox)
                self.panel2.Layout()
            self.ex_employment_state = employment_state
    def OnProvinceChanged(self,event):
        province=self.province_COMBO.GetValue()
        city_list=[]
        for i in PROVINCE_CITY_LIST:
            if(province==i[0]):
                city_list=i[1]
                break
        if(city_list==[]):
            self.city_COMBO.SetValue("")
            self.city_COMBO.Enable(False)
        elif(len(city_list)==1):
            self.city_COMBO.SetItems(city_list)
            self.city_COMBO.SetValue(city_list[0])
            self.city_COMBO.Enable(False)
        else:
            self.city_COMBO.SetItems(city_list)
    def ID_Check(self):
        error=0
        ls_id=self.ID_CTRL.GetValue()
        if(len(ls_id)!=18):
            error=1
            self.ID_CTRL.SetBackgroundColour('pink')
            self.ID_CTRL.SetFocus()
        else:
            for i in range(17):
                if(ls_id[i] not in string.digits):
                    error=1
                    self.ID_CTRL.SetBackgroundColour('pink')
        if(error==0):
            id_result=ID_VERIFY.checkIdcard(ls_id)
            if(id_result=='验证通过'):
                id_result=ID_VERIFY.getIdInfo(ls_id)
                self.ID_CTRL.SetBackgroundColour('white')
                self.hometown_CTRL.ChangeValue(id_result[0])
                self.sexy_COMB.SetValue(id_result[1])
                self.birthday_CTRL.SetValue(id_result[2])
                today = datetime.datetime.now()
                age = str(today.year - id_result[2].year)
                self.age_CTRL.ChangeValue(age)
            else:
                error=1
                self.ID_CTRL.SetBackgroundColour('pink')
                self.log.write("%s\r\n"%id_result)
        return error
    def OnIDKillFocus(self,event):
        self.ID_Check()
        self.ID_CTRL.Refresh()
        event.Skip()
    def OnEditInfoButton(self,event):
        self.SwitchToEditMode()
    def SwitchToEditMode(self):
        self.btn_panel.DestroyChildren()
        hbox=wx.BoxSizer()
        self.btn_save=wx.Button(self.btn_panel,-1,"保存",size=(200,40))
        self.btn_save.Bind(wx.EVT_BUTTON,self.OnSave)
        self.btn_cancel=wx.Button(self.btn_panel,-1,"取消",size=(200,40))
        self.btn_cancel.Bind(wx.EVT_BUTTON,self.OnCancel)
        hbox.Add(self.btn_save,1)
        hbox.Add((50,-1))
        hbox.Add(self.btn_cancel,1)
        self.btn_panel.SetSizer(hbox)
        # self.btn_panel.Layout()
        # self.member_ID_CTRL.Enable(True)
        self.name_CTRL.Enable(True)
        # self.sexy_COMB.Enable(True)
        # self.birthday_CTRL.Enable(True)
        # self.age_CTRL.Enable(True)
        self.nationality_COMBO.Enable(True)
        self.marriage_COMBO.Enable(True)
        self.phone_CTRL.Enable(True)
        self.ID_CTRL.Enable(True)
        self.IC_BUTTON.Enable(True)
        self.techtitle_COMBO.SetValue(self.techtitle)
        self.techtitle_COMBO.Enable(True)
        self.rank_CTRL.Enable(True)
        self.Onboarding_time_CTRL.Enable(True)
        self.employment_state_COMBO.Enable(True)
        # self.hometown_CTRL.Enable(True)
        self.chu_COMBO.Enable(True)
        if(self.ke):
            self.ke_COMBO.Enable(True)
        if(self.position):
            self.position_COMBO.Enable(True)
        self.province_COMBO.Enable(True)
        self.city_COMBO.Enable(True)
        self.county_CTRL.Enable(True)
        self.road_CTRL.Enable(True)
        self.education_COMBO.Enable(True)
        self.education_degree_COMBO.Enable(True)
        self.school_name_CTRL.Enable(True)
        self.graduate_year_CTRL.Enable(True)
        self.password_BTN.Show()
        self.take_pic_btn.Show()
        self.load_pic_btn.Show()
        bmp_common = wx.Image(self.pic_file_name).Scale(width=210, height=285,
                                                        quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.statBmp = wx.StaticBitmap(self.picture_PANEL, wx.ID_ANY, bmp_common)
        # self.picture_PANEL.Layout()
        self.Layout()
    def ValidateCheck(self):
        if(self.name_CTRL.GetValue()=="" or self.name_CTRL.GetValue()=="新建员工"):
            self.name_CTRL.SetBackgroundColour("pink")
            wx.MessageBox("姓名不能为空")
            self.name_CTRL.SetFocus()
            return False
        elif(self.ID_Check()==1):
            self.name_CTRL.SetBackgroundColour("white")
            wx.MessageBox("身份证号码不合理")
            return False
        # elif(self.password_CTRL.GetValue()==""):
        #     wx.MessageBox("密码不能为空")
        else:
            return True
    def OnSave(self,event):
        if(self.ValidateCheck()):
            self.InstallData()
            if(self.picture_changed==True):
                self.picture_changed=False
                from TransformImage import UpdateIndividualPIC
                UpdateIndividualPIC(self.member_ID,self.pic_file_name,whichDB=WHICHDB)
                from TransformImage import MakeImage
                MakeImage(self.member_ID)
                self.pic_file_name=picDir+"\\%s.jpg"%self.member_ID
                self.ex_pic_file_name=self.pic_file_name
                # face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(self.pic_file_name))[0]
                # from Function import UpdateIndividualFaceCharactor
                # UpdateIndividualFaceCharactor(self.member_ID,face_encoding)
                bmp_common = wx.Image(self.pic_file_name).Scale(width=210, height=285,
                                                                quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                self.statBmp = wx.StaticBitmap(self.picture_PANEL, wx.ID_ANY, bmp_common)
            self.SaveDataInDB(whichDB=WHICHDB)
            self.btn_panel.DestroyChildren()
            btn_box=wx.BoxSizer()
            self.btn_edit=wx.Button(self.btn_panel,-1,"修改个人信息",size=(200,40))
            self.btn_edit.Bind(wx.EVT_BUTTON,self.OnEditInfoButton)
            btn_box.Add(self.btn_edit,1,wx.EXPAND)
            self.btn_panel.SetSizer(btn_box)
            self.btn_panel.Layout()
            self.name_CTRL.ChangeValue(self.name)
            self.name_CTRL.Enable(False)
            self.sexy_COMB.SetValue(self.sexy)
            self.sexy_COMB.Enable(False)
            self.birthday_CTRL.SetValue(self.birthday)
            self.birthday_CTRL.Enable(False)
            self.age_CTRL.SetValue(self.age)
            self.nationality_COMBO.SetValue(self.nationality)
            self.nationality_COMBO.Enable(False)
            self.marriage_COMBO.SetValue(self.marriage)
            self.marriage_COMBO.Enable(False)
            self.ID_CTRL.ChangeValue(self.id)
            self.ID_CTRL.Enable(False)
            self.phone_CTRL.ChangeValue(self.phone_number)
            self.phone_CTRL.Enable(False)
            self.IC_BUTTON.SetLabel(self.IC)
            self.IC_BUTTON.Enable(False)
            self.techtitle_COMBO.SetValue(self.techtitle)
            self.techtitle_COMBO.Enable(False)
            self.rank_CTRL.SetValue(self.rank)
            self.rank_CTRL.Enable(False)
            self.chu_COMBO.Enable(False)
            self.ke_COMBO.Enable(False)
            self.position_COMBO.Enable(False)
            self.Onboarding_time_CTRL.SetValue(self.onboarding_time)
            self.Onboarding_time_CTRL.Enable(False)
            self.employment_state_COMBO.SetValue(self.employment_state)
            self.employment_state_COMBO.Enable(False)
            self.hometown_CTRL.ChangeValue(self.hometown)
            self.hometown_CTRL.Enable(False)
            self.province_COMBO.SetValue(self.province)
            self.province_COMBO.Enable(False)
            self.city_COMBO.SetValue(self.city)
            self.city_COMBO.Enable(False)
            self.county_CTRL.ChangeValue(self.county)
            self.county_CTRL.Enable(False)
            self.road_CTRL.ChangeValue(self.road)
            self.road_CTRL.Enable(False)
            self.password_BTN.Show(False)
            self.education_COMBO.SetValue(self.education)
            self.education_COMBO.Enable(False)
            self.education_degree_COMBO.SetValue(self.education_degree)
            self.education_degree_COMBO.Enable(False)
            self.school_name_CTRL.ChangeValue(self.school_name)
            self.school_name_CTRL.Enable(False)
            self.graduate_year_CTRL.SetValue(self.graduate_year)
            self.graduate_year_CTRL.Enable(False)
            self.take_pic_btn.Show(False)
            self.load_pic_btn.Show(False)
            evt = UpdateTreeEvent(barNum=50, value=110)
            self.parent.SetPageText(self.parent.GetSelection(),"%s档案信息"%self.name)
            wx.PostEvent(self.master, evt)
    def SaveDataInDB(self,whichDB=WHICHDB):
        try:
            db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                                 passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
        except:
            wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
            if self.log:
                self.log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
            return -1, []
        cursor = db.cursor()
        birthday=str(self.birthday.year)+'-'+str(self.birthday.month+1)+'-'+str(self.birthday.day)
        onboardyear=str(self.onboarding_time.year)+'-'+str(self.onboarding_time.month+1)+'-'+str(self.onboarding_time.day)
        if(self.employment_state=="离职"):
            dimissionyear=str(self.dimission_year.year)+'-'+str(self.dimission_year.month+1)+'-'+str(self.dimission_year.day)
        else:
            dimissionyear="1900-01-01"
        cursor.execute("UPDATE info_staff SET 姓名='%s',性别='%s',IC卡编号='%s',电话='%s',密码='%s',工作状态='%s',职别名='%s',出生日期='%s',民族='%s',身份证号码='%s',职称='%s',处='%s',科='%s',工位名='%s',籍贯='%s',入职时间='%s',离职时间='%s',学历='%s',学位='%s',毕业学校='%s',毕业时间='%s',省='%s',市='%s',区='%s',街道='%s' WHERE 员工编号='%s'"
            %(self.name,self.sexy,self.IC,self.phone_number,self.password,self.employment_state,self.rank,str(birthday),self.nationality,self.id,self.techtitle,self.chu,self.ke,self.position,self.hometown,str(onboardyear),str(dimissionyear),self.education,self.education_degree,self.school_name,str(self.graduate_year),self.province,self.city,self.county,self.road,self.member_ID))
        db.commit()
        db.close()
        return 0
    def OnCancel(self,event):
        self.btn_panel.DestroyChildren()
        btn_box=wx.BoxSizer()
        self.btn_edit=wx.Button(self.btn_panel,-1,"修改个人信息",size=(200,40))
        self.btn_edit.Bind(wx.EVT_BUTTON,self.OnEditInfoButton)
        btn_box.Add(self.btn_edit,1,wx.EXPAND)
        self.btn_panel.SetSizer(btn_box)
        self.btn_panel.Layout()
        self.name_CTRL.ChangeValue(self.name)
        self.name_CTRL.Enable(False)
        self.sexy_COMB.SetValue(self.sexy)
        self.sexy_COMB.Enable(False)
        self.birthday_CTRL.SetValue(self.birthday)
        self.birthday_CTRL.Enable(False)
        self.age_CTRL.SetValue(self.age)
        self.nationality_COMBO.SetValue(self.nationality)
        self.nationality_COMBO.Enable(False)
        self.marriage_COMBO.SetValue(self.marriage)
        self.marriage_COMBO.Enable(False)
        self.ID_CTRL.ChangeValue(self.id)
        self.ID_CTRL.Enable(False)
        self.phone_CTRL.ChangeValue(self.phone_number)
        self.phone_CTRL.Enable(False)
        self.IC_BUTTON.SetLabel(self.IC)
        self.IC_BUTTON.Enable(False)
        self.techtitle_COMBO.SetValue(self.techtitle)
        self.techtitle_COMBO.Enable(False)
        self.rank_CTRL.SetValue(self.rank)
        self.rank_CTRL.Enable(False)
        self.Onboarding_time_CTRL.SetValue(self.onboarding_time)
        self.Onboarding_time_CTRL.Enable(False)
        self.employment_state_COMBO.SetValue(self.employment_state)
        self.employment_state_COMBO.Enable(False)
        self.hometown_CTRL.ChangeValue(self.hometown)
        self.hometown_CTRL.Enable(False)
        self.province_COMBO.SetValue(self.province)
        self.province_COMBO.Enable(False)
        self.city_COMBO.SetValue(self.city)
        self.city_COMBO.Enable(False)
        self.county_CTRL.ChangeValue(self.county)
        self.county_CTRL.Enable(False)
        self.road_CTRL.ChangeValue(self.road)
        self.road_CTRL.Enable(False)
        self.password_BTN.Show(False)
        self.education_COMBO.SetValue(self.education)
        self.education_COMBO.Enable(False)
        self.education_degree_COMBO.SetValue(self.education_degree)
        self.education_degree_COMBO.Enable(False)
        self.school_name_CTRL.ChangeValue(self.school_name)
        self.school_name_CTRL.Enable(False)
        self.graduate_year_CTRL.SetValue(self.graduate_year)
        self.graduate_year_CTRL.Enable(False)
        self.take_pic_btn.Show(False)
        self.load_pic_btn.Show(False)
        self.pic_file_name=self.ex_pic_file_name
        bmp_common = wx.Image(self.pic_file_name).Scale(width=210, height=285,
                                                        quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.statBmp = wx.StaticBitmap(self.picture_PANEL, wx.ID_ANY, bmp_common)
        # self.picture_PANEL.Layout()
    def OnTakePicBtn(self,event):
        import wx.lib.agw.pybusyinfo as PBI
        busy = PBI.PyBusyInfo("正在打开摄像头，这需要几秒钟的时间，请稍候...", parent=None, title="系统提示：",
                              icon=images.Smiles.GetBitmap())
        wx.Yield()
        dlg=TakePictureDialog(self,self.log)
        del busy
        dlg.CenterOnScreen()
        if (dlg.ShowModal() == wx.ID_OK):
            self.picture_changed=True
            self.pic_file_name = dirName+"\\example.jpg"
            bmp_common = wx.Image(self.pic_file_name).Scale(width=210, height=285,
                                                            quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
            self.statBmp = wx.StaticBitmap(self.picture_PANEL, wx.ID_ANY, bmp_common)
            self.statBmp.Refresh()
        dlg.Destroy()
