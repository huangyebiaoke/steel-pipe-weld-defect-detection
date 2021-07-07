import matplotlib.pyplot as plt
import cv2
import matplotlib
plt.rc('font',family='Times New Roman')
del matplotlib.font_manager.weight_dict['roman']
matplotlib.font_manager._rebuild()

# plt.figure(figsize=(24,24))

label_names=['Air hole','Bite edge']

for i in range(2):
    image=plt.imread('./test13/'+str(i+1)+'.png')
    plt.subplot(1,2,i+1)
    plt.title(label_names[i],fontdict={'weight':'normal','size':14})
    plt.imshow(image)

plt.show()