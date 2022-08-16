import cv2
import numpy as np


def nothing(x):
    pass


radius_t = 1
bt, gt, rt = 255, 255, 255


def draw_circle(event, x, y, radius, b=255, g=255, r=255):
    global radius_t, bt, gt, rt
    radius = radius_t
    b, g, r = bt, gt, rt
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), radius, (b, g, r), -1)


img = np.zeros((1366, 768, 3), np.uint8)
cv2.namedWindow("image")

# --------- 画笔颜色
cv2.createTrackbar('brush_radius', 'image', 1, 10, nothing)
cv2.createTrackbar('pen_B', 'image', 0, 255, nothing)
cv2.createTrackbar('pen_G', 'image', 0, 255, nothing)
cv2.createTrackbar('pen_R', 'image', 0, 255, nothing)

# 创建鼠标回调函数，绑定功能函数
cv2.setMouseCallback("image", draw_circle)

while (1):
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    brush_radius = cv2.getTrackbarPos('brush_radius', 'image')
    pen_B = cv2.getTrackbarPos('pen_B', 'image')
    pen_G = cv2.getTrackbarPos('pen_G', 'image')
    pen_R = cv2.getTrackbarPos('pen_R', 'image')

    # 对鼠标函数参数进行赋值
    radius_t = brush_radius
    bt, gt, rt = pen_B, pen_G, pen_R

cv2.destroyAllWindows()