import cv2
import numpy as np

img = cv2.imread('overlap052_motion_blur.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur,0,40,apertureSize = 3)
cv2.imshow('aa',edges)
lines = cv2.HoughLines(edges,rho=1,theta=np.pi/180,threshold=200,srn=0,stn=0)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

# cv2.imwrite('houghlines3.jpg',img)
cv2.imshow('ss',img)
cv2.waitKey(0)