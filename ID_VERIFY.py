#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
import re
from datetime import datetime
# 身份证前两位代表的省市，作为籍贯
area = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", "23": "黑龙江", "31": "上海",
        "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东", "41": "河南", "42": "湖北", "43": "湖南",
        "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏", "61": "陕西",
        "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}
# 身份证有效性校验
def checkIdcard(idcard):
    Messages = ['验证通过', '身份证号码位数不对', '身份证号码出生日期超出范围或含有非法字符', '身份证号码校验错误', '身份证地区非法']
    idcard = str(idcard)  # 身份证号码转成字符串
    idcard=idcard.upper()
    # print"idcard=",idcard
    idcard = idcard.strip()  # 移除字符串头尾指定的字符（默认为空格）
    idcard_list = list(idcard)  # 转成列表
    # print"idcard_list=",idcard_list
    # 地区校验
    if (not area[(idcard)[0:2]]):
        return Messages[4]
    # 15位身份号码检测
    if (len(idcard) == 15):
        if ((int(idcard[6:8]) + 1900) % 4 == 0 or (
                    (int(idcard[6:8]) + 1900) % 100 == 0 and (int(idcard[6:8]) + 1900) % 4 == 0)):
            ereg = re.compile(
                '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')
        else:
            ereg = re.compile(
                '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')
        # 测试出生日期的合法性
        if (re.match(ereg, idcard)):
            return Messages[0]
        else:
            return Messages[2]
    # 18位身份号码检测
    elif (len(idcard) == 18):
        # 出生日期的合法性检查
        # 闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
        # 平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
        if (int(idcard[6:10]) % 4 == 0 or (int(idcard[6:10]) % 100 == 0 and int(idcard[6:10]) % 4 == 0)):
            ereg = re.compile(
                '[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')  # //闰年出生日期的合法性正则表达式
        else:
            ereg = re.compile(
                '[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')  # //平年出生日期的合法性正则表达式
        # 测试出生日期的合法性
        if (re.match(ereg, idcard)):
            # 计算校验位
            S = (int(idcard_list[0]) + int(idcard_list[10])) * 7 + (int(idcard_list[1]) + int(idcard_list[11])) * 9 +\
                (int(idcard_list[2]) + int(idcard_list[12])) * 10 + (int(idcard_list[3]) + int(idcard_list[13])) * 5 +\
                (int(idcard_list[4]) + int(idcard_list[14])) * 8 + (int(idcard_list[5]) + int(idcard_list[15])) * 4 + \
                (int(idcard_list[6]) + int(idcard_list[16])) * 2 + int(idcard_list[7]) * 1 + int(idcard_list[8]) * 6 + int(idcard_list[9]) * 3
            Y = S % 11
            M = "F"
            JYM = "10X98765432"
            M = JYM[Y]  # 判断校验位
            if (M == idcard_list[17]):  # 检测ID的校验位
                return Messages[0]
            else:
                return Messages[3]
        else:
            return Messages[2]
    else:
        return Messages[1]
# 获取身份证信息
def getIdInfo(idcard):
    idcard = str(idcard)
    idcard=idcard.upper()
    idcard = idcard.strip()
    ID_address = (idcard)[0:2]  # 前两位是籍贯
    ID_sex = idcard[14:17]  # 14位之后表示性别
    if (len(idcard) == 15):
        ID_birth = '19' + idcard[6:12]  # 获取15位身份证出生年月日，补全19
    else:
        ID_birth = idcard[6:14]  # 获取18位身份证出生年月日

    strAddress = area[ID_address]  # 籍贯
    strGender = 'male'  # 性别
    year = ID_birth[0:4]
    moon = ID_birth[4:6]
    day = ID_birth[6:8]
    # strBirthDate = year + '-' + moon + '-' + day  # 出生日期
    strBirthDate = datetime(int(year),int(moon),int(day))# 出生日期
    if int(ID_sex) % 2 == 0:
        strGender = '女'
    else:
        strGender = '男'
    idInfo = [strAddress, strGender, strBirthDate]
    return idInfo
# 测试
getIdInfo('23052219470407227X')