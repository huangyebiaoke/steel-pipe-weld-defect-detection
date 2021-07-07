import cv2
import matplotlib.pyplot as plt
import json
import numpy as np
import random

def random_color():
    color_arr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += color_arr[random.randint(0,14)]
    return "#"+color

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
        f.close()
    objects=json_data['outputs']['object']
    for obj in objects:
        bndboxes.append(obj['bndbox'])
        label_names.append(obj['name'])
    return bndboxes,label_names,cv2.imread(image_path)

if __name__=='__main__':
    train_list_path='./file-list/train-list.txt'
    arr=get_json_and_image_path(train_list_path)
    plt.figure(figsize=(18,18))
    plt.title('width & height')
    plt.xlim=958
    plt.ylim=653
    plt.xlabel('X')
    plt.ylabel('Y')
    coords=[[]]*7
    j=0
    for row in arr:
        bndboxes,label_names,image=get_bndboxes_and_image(row)
        for i in range(len(bndboxes)):
            w=bndboxes[i]['xmax']-bndboxes[i]['xmin']
            h=bndboxes[i]['ymax']-bndboxes[i]['ymin']
            if label_names[i]!=label_names[i-1]:
                j+=1
            coords[j].append([w,h])
    labels=['air-hole','bite-edge','broken-arc','crack','overlap','slag-inclusion','unfused']
    colors=['#00CED1','#DC143C','#15D9D7','#D8FF00','#D200FF','#0048FF','#759A13']
    coords=np.array(coords)
    for i in range(len(coords)):
        plt.scatter(coords[i,:,0], coords[i,:,1], s=np.pi*4**2, c=random_color(), alpha=0.4, label=labels[i])
        # plt.plot(coords[i,:,0],coords[i,:,1],linewidth='0.5',color=colors[i])
    plt.plot([0,958],[0,653],linewidth = '0.5',color='#000000')
    plt.legend()
    plt.show()