import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib import rcParams
config = {
    "font.family":'Times New Roman',  # 设置字体类型
    # "font.size": 80,
#     "mathtext.fontset":'stix',
}
rcParams.update(config)
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec
from matplotlib.gridspec import SubplotSpec

import pandas as pd
import numpy as np

def get_data(path,col):
    data=pd.read_csv(path,usecols=[col])
    data_np=np.array(data)
    return data_np[:,0]


if __name__=='__main__':
    yolo_presicion=100*get_data(r'E:\Yangdingming\Downloads\wandb_export_2021-04-01T09_20_21.721+08_00.csv','exp2 - metrics/precision')
    yolo_presicion=yolo_presicion[:224]
    faster_presicion=100*get_data(r'E:\Yangdingming\vs-code-projects\faster-rcnn-tf2\tensorboard\run-.-tag-mean_detection_acc.csv','Value')
    yolo_loss=get_data(r'E:\Yangdingming\Downloads\wandb_export_2021-04-01T09_22_02.817+08_00.csv','exp2 - train/box_loss')+get_data(r'E:\Yangdingming\Downloads\wandb_export_2021-04-01T09_21_52.882+08_00.csv','exp2 - train/obj_loss')+get_data(r'E:\Yangdingming\Downloads\wandb_export_2021-04-01T09_21_34.538+08_00.csv','exp2 - train/cls_loss')
    yolo_loss=yolo_loss[:224]
    faster_loss=get_data(r'E:\Yangdingming\vs-code-projects\faster-rcnn-tf2\tensorboard\run-.-tag-total_loss.csv','Value')
    x=np.arange(0,len(yolo_presicion),1)
    x2=np.arange(0,len(faster_presicion),1)
    # plt.subplot(1,2,1)
    # plt.title('a:compare persicion')
    # plt.xlim(0,len(yolo_presicion))
    # plt.ylim(0,100)
    # plt.xlabel('epoch')
    # plt.ylabel('persicion')
    # # plt.plot(x,yolo_presicion,linewidth=2,color='g',label='yolov5')
    # plt.plot(x2,faster_presicion,linewidth=2,color='r',label='faster r-cnn')
    # plt.legend(loc='best')

    # plt.subplot(1,2,2)
    # plt.title('b:compare total loss')
    # plt.xlim(0,len(yolo_presicion))
    # plt.xlabel('epoch')
    # plt.ylabel('total loss')
    # plt.plot(x,yolo_loss,linewidth=1,color='g',label='yolov5')
    # # plt.plot(x2,faster_loss,linewidth=1,color='r',label='faster r-cnn')
    # plt.legend(loc='best')

    # plt.show()

    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.5, 0.8, 0.4],xticklabels=[],ylim=(np.min(faster_presicion), np.max(faster_presicion)))
    ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.4],ylim=(np.min(yolo_presicion), np.max(yolo_presicion)))
    ax1.set_title('a: compare precision')
    plt.xlabel('epoch')
    plt.ylabel('precision')
    ax1.plot(x,faster_presicion,linewidth=1,color='r',label='faster r-cnn')
    ax2.plot(x2,yolo_presicion,linewidth=1,color='g',label='yolov5')
    # ax2.yaxis.set_major_locator(MultipleLocator(20))
    ax1.legend(loc='best')
    ax2.legend(loc='best')
    plt.show()
