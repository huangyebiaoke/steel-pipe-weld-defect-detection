import random
from skimage import exposure
import numpy as np
import math
import skimage
from PIL import Image,ImageEnhance,ImageOps,ImageFile,ImageChops
import copy

def change_light(image,bndboxes):
    # todo:可以加一个步长使明暗变化更明显
    flag=random.uniform(0.4,2.5)
    while(flag==1):
        flag=random.uniform(0.4,2.5)
    image=exposure.adjust_gamma(image,flag)
    for box in bndboxes:
        cv2.rectangle(image,(box['xmin'],box['ymin']),(box['xmax'],box['ymax']),(255,0,0),2)
    return image

def rotate(image,bndboxes,angle=5,scale=1.):
    w=image.shape[1]
    h=image.shape[0]

    rangle=np.deg2rad(angle)
    nw=(abs(np.sin(rangle)*h)+abs(np.cos(rangle)*w))*scale
    nh=(abs(np.cos(rangle)*h)+abs(np.sin(rangle)*w))*scale

    rot_mat=cv2.getRotationMatrix2D((nw*.5,nh*.5),angle,scale)
    rot_move=np.dot(rot_mat,np.array([(nw-w)*.5,(nh-h)*.5,0]))
    rot_mat[0,2]+=rot_move[0]
    rot_mat[1,2]+=rot_move[1]

    rot_img=cv2.warpAffine(image,rot_mat,(int(math.ceil(nw)),int(math.ceil(nh))),flags=cv2.INTER_LANCZOS4)

    rot_boxes=list()
    for box in bndboxes:
        p1=np.dot(rot_mat,np.array([(box['xmin']+box['xmax'])/2,box['ymin'],1]))
        p2=np.dot(rot_mat,np.array([box['xmax'],(box['ymin']+box['ymax'])/2,1]))
        p3=np.dot(rot_mat,np.array([(box['xmin']+box['xmax'])/2,box['ymax'],1]))
        p4=np.dot(rot_mat,np.array([box['xmin'],(box['ymin']+box['ymax'])/2,1]))
        concat=np.vstack((p1,p2,p3,p4))
        concat=concat.astype(np.int32)
        rx,ry,rw,rh=cv2.boundingRect(concat)
        rx_min=rx
        ry_min=ry
        rx_max=rx+rw
        ry_max=ry+rw
        rot_boxes.append({'xmin':rx_min,'ymin':ry_min,'xmax':rx_max,'ymax':ry_max})

    for box in rot_boxes:
        cv2.rectangle(rot_img,(box['xmin'],box['ymin']),(box['xmax'],box['ymax']),(255,0,0),2)
    return rot_img

# todo:fix the bug of zero after mask operation;adjust the position of hole
def cutout(image,bndboxes,length=20,hole_num=1,threshold=.5):
    if image.ndim==3:
        h,w,c=image.shape
    else:
        _,h,w,c=image.shape
    mask=np.ones((h,w,c),np.int32)
    for i in range(hole_num):
        y=np.random.randint(h)
        x=np.random.randint(w)
        y1=np.clip(y-length//2,0,h)
        y2=np.clip(y+length//2,0,h)
        x1=np.clip(x-length//2,0,w)
        x2=np.clip(x+length//2,0,w)

        mask[y1:y2,x1:x2]=0
    image=image*mask
    for box in bndboxes:
        cv2.rectangle(image,(box['xmin'],box['ymin']),(box['xmax'],box['ymax']),(255,0,0),2)
    return image

# !!!!the reture image format is skimage package
def gaussian_noise(image):
    return skimage.util.random_noise(image,mode='gaussian',var=.004)

def flip(image,bndboxes):
    h=image.shape[0]
    w=image.shape[1]
    image=cv2.warpAffine(image,cv2.getRotationMatrix2D((w*.5,h*.5),0,1),(w,h))
    # 1水平翻转；2垂直翻转
    image=cv2.flip(image,1)
    for box in bndboxes:
        box['xmin']=w-1-box['xmin']
        box['xmax']=w-1-box['xmax']
        cv2.rectangle(image,(box['xmin'],box['ymin']),(box['xmax'],box['ymax']),(255,0,0),2)
    return image

# !!!!the return format of iamge is Image in PIL package
def color(image):
    image=Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
    # 饱和度
    ran=np.random.randint(0, 31) / 10.
    image=ImageEnhance.Color(image).enhance(ran)
    # 对比度
    ran=np.random.randint(10, 21) / 10.
    image=ImageEnhance.Contrast(image).enhance(ran)
    # 锐度
    ran=np.random.randint(0, 31) / 10.
    image=ImageEnhance.Sharpness(image).enhance(ran)
    return image

def resize(image,bndboxes):
    h=image.shape[0]
    w=image.shape[1]
    ran_h=np.random.randint(h*.5,h)
    ran_w=np.random.randint(w*.5,w)
    image=cv2.resize(image,(ran_w,ran_h),interpolation=cv2.INTER_LINEAR)
    for box in bndboxes:
        box['xmin']=int((ran_w/w)*box['xmin'])
        box['xmax']=int((ran_w/w)*box['xmax'])
        box['ymin']=int(box['ymin']*(ran_h/h))
        box['ymax']=int(box['ymax']*(ran_h/h))
        cv2.rectangle(image,(box['xmin'],box['ymin']),(box['xmax'],box['ymax']),(255,0,0),2)
    return image

def crop(image,bndboxes):
    w=image.shape[1]
    h=image.shape[0]
    xmin=w
    xmax=0
    ymin=h
    ymax=0
    for box in bndboxes:
        xmin=min(xmin,box['xmin'])
        xmax=max(xmax,box['xmax'])
        ymin=min(ymin,box['ymin'])
        ymax=max(ymax,box['ymax'])
    crop_left=random.randint(0,xmin)
    crop_right=random.randint(xmax,w)
    crop_top=random.randint(0,ymin)
    crop_bottom=random.randint(ymax,h)
    crop_image=image[crop_top:crop_bottom,crop_left:crop_right]
    for box in bndboxes:
        box['xmin']-=crop_left
        box['xmax']-=crop_left
        box['ymin']-=crop_top
        box['ymax']-=crop_top
        cv2.rectangle(crop_image,(box['xmin'],box['ymin']),(box['xmax'],box['ymax']),(255,0,0),2)
    return crop_image


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
    # for i in arr:
    #     print("json_path:"+i[0]+" image_path:"+i[1])

    plt.figure(figsize=(24,24))

    bndboxes,label_names,image=get_bndboxes_and_image(arr[700])
    label_names=['Blowhole','Undercut','Broken arc','Crack','Overlap','Slag inclusion','Lack of fusion']

    plt.subplot(331)
    plt.title(label_names[4]+": original",fontdict={'weight':'normal','size':14})
    plt.imshow(image)

    image2=change_light(image,bndboxes)
    plt.subplot(332)
    plt.title(label_names[4]+": after change light",fontdict={'weight':'normal','size':14})
    plt.imshow(image2)

    image3=rotate(image=copy.deepcopy(image),bndboxes=copy.deepcopy(bndboxes),angle=random.uniform(-15,15))
    plt.subplot(333)
    plt.title(label_names[4]+": after rotate",fontdict={'weight':'normal','size':14})
    plt.imshow(image3)

    image4=cutout(image=image,bndboxes=bndboxes)
    plt.subplot(334)
    plt.title(label_names[4]+": after cutout",fontdict={'weight':'normal','size':14})
    plt.imshow(image4)

    image5=gaussian_noise(image)
    plt.subplot(335)
    plt.title(label_names[4]+": after gaussian noise",fontdict={'weight':'normal','size':14})
    plt.imshow(image5)

    # 数组在python中是引用传递所以要用deepcopy拷贝一个新对象
    image6=flip(copy.deepcopy(image),copy.deepcopy(bndboxes))
    plt.subplot(336)
    plt.title(label_names[4]+": after horizontal flip",fontdict={'weight':'normal','size':14})
    plt.imshow(image6)

    image7=color(image)
    plt.subplot(337)
    plt.title(label_names[4]+": after adjust color,contrast & sharpness",fontdict={'weight':'normal','size':14})
    plt.imshow(image7)

    # image8=shift(image,bndboxes)
    # plt.subplot(335)
    # plt.title(label_names[0]+"：随机平移后",fontdict={'weight':'normal','size':14})
    # plt.imshow(image8)

    image9=resize(copy.deepcopy(image),copy.deepcopy(bndboxes))
    plt.subplot(338)
    plt.title(label_names[4]+": after resize width & height",fontdict={'weight':'normal','size':14})
    plt.imshow(image9)

    image10=crop(copy.deepcopy(image),copy.deepcopy(bndboxes))
    plt.subplot(339)
    plt.title(label_names[4]+": after crop image",fontdict={'weight':'normal','size':14})
    plt.imshow(image10)
    # plt.savefig(fname="data-augmentation-en.svg",format="svg") 
    plt.tight_layout()
    plt.show()