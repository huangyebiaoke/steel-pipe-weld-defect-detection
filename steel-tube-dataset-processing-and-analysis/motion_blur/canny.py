import cv2
#载入图片
img_original=cv2.imread('overlap052_motion_blur.jpg')
#设置窗口
cv2.namedWindow('Canny')
#定义回调函数
def nothing(x):
    pass
#创建两个滑动条，分别控制threshold1，threshold2
cv2.createTrackbar('threshold1','Canny',50,400,nothing)
cv2.createTrackbar('threshold2','Canny',100,400,nothing)
while(1):
    #返回滑动条所在位置的值
    threshold1=cv2.getTrackbarPos('threshold1','Canny')
    threshold2=cv2.getTrackbarPos('threshold2','Canny')
    #Canny边缘检测
    img_edges=cv2.Canny(img_original,threshold1,threshold2)
    #显示图片
    cv2.imshow('original',img_original)
    cv2.imshow('Canny',img_edges)  
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()