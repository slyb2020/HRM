#!/usr/bin/env python
# encoding: utf-8
'''
@author: slyb
@license: (C) Copyright 2017-2020, 天津定智科技有限公司.
@contact: slyb@tju.edu.cn
@file: Function.py
@time: 2019/9/1 17:18
@desc:
'''
import wx
import pymysql as MySQLdb
from ID_DEFINE import *
# import face_recognition

def GetDepartmentInfo(log,whichDB=0):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `部门名称列表` from `系统参数` WHERE 1"""
    cursor.execute(sql)
    data = cursor.fetchone()  # 获得压条信息
    data=data[0]
    db.close()
    return 0,data
def GetStaffBriefInfo(log,field,data,whichDB=0):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if(field=="厂"):
        sql = """SELECT `姓名`,`性别`,`员工编号`,`IC卡编号`,`工位编号`,`处`,`科`,`工位名`,`电话`,`密码`,`工作状态`,`职别`,`职别名`,出生日期,民族,身份证号码,职称,籍贯,入职时间,离职时间,学历,学位,毕业学校,毕业时间,婚姻状况,省,市,区,街道 from `info_staff` WHERE 姓名<>'新建员工'"""
    elif(field=="处"):
        sql = """SELECT `姓名`,`性别`,`员工编号`,`IC卡编号`,`工位编号`,`处`,`科`,`工位名`,`电话`,`密码`,`工作状态`,`职别`,`职别名`,出生日期,民族,身份证号码,职称,籍贯,入职时间,离职时间,学历,学位,毕业学校,毕业时间,婚姻状况,省,市,区,街道 from `info_staff` WHERE `处`='%s' AND 姓名<>'新建员工'"""%(data)
    elif(field=="科"):
        sql = """SELECT `姓名`,`性别`,`员工编号`,`IC卡编号`,`工位编号`,`处`,`科`,`工位名`,`电话`,`密码`,`工作状态`,`职别`,`职别名`,出生日期,民族,身份证号码,职称,籍贯,入职时间,离职时间,学历,学位,毕业学校,毕业时间,婚姻状况,省,市,区,街道 from `info_staff` WHERE `科`='%s' AND 姓名<>'新建员工'"""%(data)
    elif(field=="工位名"):
        sql = """SELECT `姓名`,`性别`,`员工编号`,`IC卡编号`,`工位编号`,`处`,`科`,`工位名`,`电话`,`密码`,`工作状态`,`职别`,`职别名`,出生日期,民族,身份证号码,职称,籍贯,入职时间,离职时间,学历,学位,毕业学校,毕业时间,婚姻状况,省,市,区,街道 from `info_staff` WHERE `工位名`='%s' AND 姓名<>'新建员工'"""%(data)
    cursor.execute(sql)
    data = cursor.fetchall()  # 获得压条信息
    data=list(data)
    db.close()
    return 0,data
def GetPicture(log,id,whichDB=0):
    data=[]
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT 照片 from `info_staff` WHERE `员工编号`='%s'"""%(id)
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    if data!=None:
        if len(data)>0:
            data=data[0]
            return 0,data
    return -1,""

def GetFaceCharacter(log,id):
    data=[]
    try:
        db = MySQLdb.connect(host="%s" % host_name, user='%s' % user_name, passwd='%s' % passwd_name, db='%s' %DATABASE_NAME[5],charset='utf8')
    except:
        wx.MessageBox("无法连接management数据库","错误信息")
        log.WriteText("无法连接management数据库" ,colour=wx.RED)
        return -1,[]
    cursor = db.cursor()
    sql = """SELECT 人脸特征 from `info_staff` WHERE `员工编号`='%s'"""%(id)
    cursor.execute(sql)
    data = cursor.fetchone()  # 获得1条信息
    data=data[0]
    db.close()
    return 0,data
def UpdateIndividualFaceCharactor(job_id,encoding):
    DB = MySQLdb.connect(host="%s" % host_name, user='%s' % user_name, passwd='%s' % passwd_name, db='%s' %DATABASE_NAME[5],charset='utf8')
    cursor = DB.cursor()
    cursor.execute(
        "UPDATE `info_staff` set `人脸特征`='%s' WHERE `员工编号`='%s'" %(encoding,job_id))
    DB.commit()
    DB.close()
def GetAllIDWithPicture(log=None):
    data=[]
    try:
        db = MySQLdb.connect(host="%s" % host_name, user='%s' % user_name, passwd='%s' % passwd_name, db='%s' %DATABASE_NAME[5],charset='utf8')
    except:
        wx.MessageBox("无法连接management数据库","错误信息")
        log.WriteText("无法连接management数据库" ,colour=wx.RED)
        return -1,[]
    cursor = db.cursor()
    sql = """SELECT `员工编号` from `info_staff` WHERE `照片`<>''"""
    cursor.execute(sql)
    ls = cursor.fetchall()  # 获得压条信息
    for i in ls:
        data.append(i[0])
    db.close()
    return 0,data
def GetAllIDWithFaceCharactor(log=None):
    data=[]
    try:
        db = MySQLdb.connect(host="%s" % host_name, user='%s' % user_name, passwd='%s' % passwd_name, db='%s' %DATABASE_NAME[5],charset='utf8')
    except:
        wx.MessageBox("无法连接management数据库","错误信息")
        log.WriteText("无法连接management数据库" ,colour=wx.RED)
        return -1,[]
    cursor = db.cursor()
    sql = """SELECT `员工编号` from `info_staff` WHERE `人脸特征`<>''"""
    cursor.execute(sql)
    ls = cursor.fetchall()  # 获得压条信息
    for i in ls:
        data.append(i[0])
    db.close()
    return 0,data
