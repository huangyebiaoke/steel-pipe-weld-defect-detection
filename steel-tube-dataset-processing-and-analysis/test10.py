
import json
import matplotlib.pylab as plt
import cv2

def get_json_and_image_path(file_path):
    with open(file_path,'r') as f:
        arr=f.readlines()
    arr=[i.strip().split(' ') for i in arr]
    return arr

def get_bndboxes_and_image(json_and_image_path):
    json_path=json_and_image_path[0]
    image_path=json_and_image_path[1]
    bndboxes=[]
    label_names=[]
    with open(json_path,'r',encoding='utf-8') as f:
        json_data=json.load(f)
    objects=json_data['outputs']['object']
    for obj in objects:
        bndboxes.append(obj['bndbox'])
        label_names.append(obj['name'])
    return bndboxes,label_names,cv2.imread(image_path)
images=list()
train_list_path='./file-list/train-list0.txt'
arr=get_json_and_image_path(train_list_path)
for row in arr:
    bndboxes,label_names,image=get_bndboxes_and_image(row)
    images.append(image)
# plt.title('sample data show')
# fig.subplots_adjust(left=0.0,bottom=0.0,top=0.1,right=0.1)
fig=plt.figure(figsize=(18,18))
for i in range(len(images)):
    ax=plt.subplot(26,int(len(images)/26)+1,i+1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.imshow(images[i])
    plt.xticks([])
    plt.yticks([])
# plt.subplots_adjust(wspace=0,hspace=0)
# plt.savefig(fname="samples-data-show.svg",format="svg")  
plt.show()