import os
import cv2
import matplotlib.pyplot as plt
import json
plt.rcParams['font.sans-serif'] = ['FangSong']

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
    print(image_path)
    return bndboxes,label_names,cv2.imread(image_path)

if __name__=='__main__':
    train_list_path='./file-list/train-list.txt'
    arr=get_json_and_image_path(train_list_path)
    # for i in arr:
    #     print("json_path:"+i[0]+" image_path:"+i[1])
    bndboxes,label_names,image=get_bndboxes_and_image(arr[9])
    print(image)
    for box in bndboxes:
        cv2.rectangle(image,(box['xmin'],box['ymin']),(box['xmax'],box['ymax']),(0,255,0),1)
        print("xmin:"+str(box['xmin'])+" ymin:"+str(box['ymin'])+ " xmax:"+str(box['xmax'])+" ymax:"+str(box['ymax'])+"\n")
    cv2.imshow(label_names[0],image)
    cv2.waitKey(0)
    
    # plt.figure(figsize=(10,10))
    # plt.imshow(image)
    # plt.title(label_names[0])
    # plt.show()