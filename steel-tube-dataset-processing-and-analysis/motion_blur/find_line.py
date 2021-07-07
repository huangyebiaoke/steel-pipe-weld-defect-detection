import cv2
import numpy as np

image=cv2.imread('overlap052_motion_blur.jpg')
cv2.imshow('image',image)
image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow('image_gray',image_gray)

image_gray_canny = cv2.Canny(image_gray, 1, 50)
cv2.imshow('image_gray_canny',image_gray_canny)

lines = cv2.HoughLinesP(image_gray_canny, 1, np.pi / 90, 100, minLineLength=100, maxLineGap=40)
lines1 = lines[:, 0, :]
for x1, y1, x2, y2 in lines1[:]:
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
cv2.imshow('line',image)

cv2.waitKey(0)