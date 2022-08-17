# -*- encoding: utf-8 -*-
import base64
from ID_DEFINE import *
import pymysql as MySQLdb
#impo
def TransformBase64(img_name):
    """
    image -> base64
    :param img_name:
    :return:
    """
    try:
        with open(img_name, 'rb') as file:
            image_data = file.read()
            base64_data = base64.b64encode(image_data)  # 'bytes'型数据
            str_base64_data = base64_data.decode()#str型数据
            return str_base64_data
    except:
        # print"erro"
        return "erro"

def UpdateIndividualPIC(job_id,picture_name,whichDB=0):
    data=TransformBase64(picture_name)
    if data != "erro":
        try:
            db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                                 passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
        except:
            wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
            return -1, []
        cursor = db.cursor()
        cursor.execute(
            "UPDATE `info_staff` set `照片`='%s' WHERE `员工编号`='%s'" %(data,job_id))
        db.commit()
        db.close()
    else:
        print("erro2")

def ReadInfoImage(job_id,whichDB=0):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        return -1, []
    cursor = db.cursor()
    cursor.execute("select `照片`  from `info_staff` where `员工编号`='%s'" %(job_id))
    record=cursor.fetchone()
    db.close()
    return record

def MakeImage(job_id):
    """
    base64 -> image
    :return:
    """
    record=ReadInfoImage(job_id,whichDB=WHICHDB)
    if(record[0]!=""):
        with open(picDir+'\\%s.jpg'%job_id, 'wb') as file:
            image = base64.b64decode(record[0])  # 解码
            file.write(image)
