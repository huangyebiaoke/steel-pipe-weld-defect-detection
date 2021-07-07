import numpy as np
import matplotlib.pyplot as plt
import cv2


# opencv的颜色通道顺序为[B,G,R]，而matplotlib的颜色通道顺序为[R,G,B]。
def plotImg(img):
    if len(img.shape) == 3:
        img = img[:, :, (2, 1, 0)]
        plt.imshow(img)
    else:
        plt.imshow(img, cmap='gray')
    plt.show()


image = cv2.imread('overlap052_motion_blur.jpg')
plotImg(image)


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 0, 40)
    return canny


lane_image = np.copy(image)
canny = canny(lane_image)
plotImg(canny)


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            if np.abs(x1-x2)>30:
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return line_image


lines = cv2.HoughLinesP(canny, rho=1.0, theta=np.pi / 180,threshold=100, minLineLength=2, maxLineGap=200)
line_image = display_lines(image, lines)
plotImg(line_image)

combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
cv2.imwrite('overlap052_motion_blur_line.jpg',combo_image)
plotImg(combo_image)