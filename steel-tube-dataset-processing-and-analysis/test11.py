import matplotlib.pyplot as plt
import matplotlib
import matplotlib.image as cv2
# import cv2
# from pylab import mpl
# mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
# mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
plt.rc('font',family='Times New Roman')
del matplotlib.font_manager.weight_dict['roman']
matplotlib.font_manager._rebuild()

# plt.figure(figsize=(24,24))

label_names=['Blowhole','Undercut','Broken arc','Crack','Overlap','Slag inclusion','Lack of fusion','Hollow bead']

for i in range(8):
    image=cv2.imread('./exp6/'+str(i+1)+'.png')
    plt.subplot(2,4,i+1)
    plt.title(label_names[i],fontdict={'weight':'normal','size':14})
    plt.imshow(image)
plt.tight_layout()
plt.savefig("q.svg",dpi=300)
plt.show()