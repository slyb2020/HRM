#!/usr/bin/env python3
import datetime
data='1'
length = len(data)
for i in range(5 - length):
    data='0'+data
today = datetime.datetime.now()
year = str(today.year)[2:4]
print("year=",year)
result=year+data
print("result=",result)
# import numpy as np
# import cv2
# from matplotlib import pyplot as plt
#
# img = cv2.imread('test.jpg', 0)
# plt.imshow(img, cmap='gray', interpolation='bicubic')
# plt.xticks([]), plt.yticks([])  # 隐藏x和y坐标上的刻度值
# plt.show()
