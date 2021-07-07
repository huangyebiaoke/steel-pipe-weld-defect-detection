import os
import cv2
import json

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
        # with 会自动close文件https://blog.csdn.net/u011280778/article/details/104283319?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param
        # f.close()
    objects=json_data['outputs']['object']
    for obj in objects:
        bndboxes.append(obj['bndbox'])
        label_names.append(obj['name'])
    return bndboxes,label_names,cv2.imread(image_path)

if __name__=='__main__':
    train_list_path='./file-list/train-list.txt'
    arr=get_json_and_image_path(train_list_path)
    i=1000
    while True:
        bndboxes,label_names,image=get_bndboxes_and_image(arr[i])
        print(str(i)+' '+arr[i][1]+' '+label_names[0]+' w:'+str(image.shape[0])+',h:'+str(image.shape[1])+' ')
        for box in bndboxes:
            cv2.rectangle(image,(box['xmin'],box['ymin']),(box['xmax'],box['ymax']),(0,255,0),2)
            print("xmin:"+str(box['xmin'])+" ymin:"+str(box['ymin'])+ " xmax:"+str(box['xmax'])+" ymax:"+str(box['ymax'])+"\n")
        cv2.namedWindow('tube flaw', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('tube flaw',int(image.shape[1]/2), int(image.shape[0]/2))
        cv2.imshow('tube flaw',image)
        key=cv2.waitKey(0)
        if key==ord('d'):
            i+=1
        elif key==ord('a'):
            i-=1
        elif key==ord('q'):
            break
    cv2.destroyAllWindows()