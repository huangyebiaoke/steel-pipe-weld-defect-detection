from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec
from matplotlib.gridspec import SubplotSpec
import numpy as np
import json
import cv2
import matplotlib
import matplotlib.pyplot as plt
plt.rc('font',family='Times New Roman')
del matplotlib.font_manager.weight_dict['roman']
matplotlib.font_manager._rebuild()

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

if __name__=='__main__':
    train_list_path='./file-list/train-list0.txt'
    arr=get_json_and_image_path(train_list_path)

    fig=plt.figure(figsize=(18,18))
    gs = GridSpec(1, 2, figure=fig)
    j=-1
    labels=['air-hole','bite-edge','broken-arc','crack','overlap','slag-inclusion','unfused']
    colors=['#00CED1','#DC143C','#00582D','#D8FF00','#D200FF','#0048FF','#759A13']
    coords=[]
    w_list=[]
    h_list=[]

    coords_center=[]
    c_x_list=[]
    c_y_list=[]
    lable_set=set()
    lable_set.add('气孔')
    # num=0
    for row in arr:
        bndboxes,label_names,image=get_bndboxes_and_image(row)
        for i in range(len(bndboxes)):
            # num+=len(bndboxes)
            w=bndboxes[i]['xmax']-bndboxes[i]['xmin']
            h=bndboxes[i]['ymax']-bndboxes[i]['ymin']
            w_list.append(w)
            h_list.append(h)

            c_x=(bndboxes[i]['xmax']+bndboxes[i]['xmin'])/2
            # plot坐标原点在左下角，原图是在左上角，所以要将y轴坐标上下翻转
            c_y=653-1-(bndboxes[i]['ymax']+bndboxes[i]['ymin'])/2
            c_x_list.append(c_x)
            c_y_list.append(c_y)
            if label_names[i] not in lable_set:
                lable_set.add(label_names[i])
                coords.append({"name":label_names[i],"w":w_list.copy(),"h":h_list.copy()})
                w_list.clear()
                h_list.clear()
                coords_center.append({"name":label_names[i],"x":c_x_list.copy(),"y":c_y_list.copy()})
                c_x_list.clear()
                c_y_list.clear()
                j+=1
            # plt.gca().add_patch(plt.Rectangle(xy=(bndboxes[i]['xmin'],653-1-bndboxes[i]['ymin']),
            #                       width=w,
            #                       height=h,
            #                       edgecolor=colors[j],
            #                       fill=False, linewidth=1))

    ax2 = fig.add_subplot(gs[0,1])
    ax2.set_aspect(653/958)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.title('The width & height')
    plt.xlim(0,958)
    plt.ylim(0,653)
    plt.xlabel('W')
    plt.ylabel('H')
    for i in range(len(coords)):
        plt.scatter(coords[i]['w'], coords[i]['h'], s=np.pi*2**2, c=colors[i], alpha=0.4, label=labels[i])
    plt.plot([0,653],[0,653],linewidth = '0.5',color='#000000')
    plt.legend()

    ax3 = fig.add_subplot(gs[0,0])
    ax3.set_aspect(653/958)
    plt.title("The position of boundingbox's center point")
    plt.xlim(0,958)
    plt.ylim(0,653)
    plt.xlabel('X')
    plt.ylabel('Y')
    coords_center=np.array(coords_center)
    for i in range(len(coords_center)):
        plt.scatter(coords_center[i]['x'], coords_center[i]['y'], s=np.pi*2**2, c=colors[i], alpha=0.4, label=labels[i])
    plt.plot([0,958],[653,0],linewidth = '0.5',color='#000000')
    plt.legend()
    # plt.savefig(fname="sample-data-analysis-v2-en.svg",format="svg")      
    plt.show()