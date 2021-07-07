# -*- coding:utf-8 -*-
# 用于将labelme的标注结果可视化查看效果

"""
使用方法
    1. 执行脚本命令
    "python 8_label_check.py \
    --input_dir=/media/cjs/TRUNK_8T/TRUNK/1-Datasets/1-detection/TRUNK-highway/Shandong/seme-label/1455208684196280416 \
    --out_dir=/media/cjs/TRUNK_8T/TRUNK/1-Datasets/1-detection/TRUNK-highway/Shandong/seme-label/1455208684196280416\
    --check_overlap \
    --show_color_meaning
    "
    其中
    input_dir是输入的路径，其中包括原始图像和对应的json文件
    out_dir表示输出路径，如果保存video的话存放在这个out_dir 路径中
    --check_overlap用于筛查是不是对同一个物体有多个labels，比如把卡车识别成了car和tuck两个类别，完全覆盖，不方便从labelme中进行查找。
    --show_color_meaning 设置的话会在图像的右侧显示每种颜色所对应的label类别，方便进行查看。

    脚本运行起来后会出现一个小的图像显示框，此时可以双击图像顶部放大为全屏显示，方便查看。

    2. 图像筛选操作：
    2.1 按空格键在内的任何按键会跳到下一帧；
    2.2 按'B'键回退到上一张图片；
    2.3 按‘esc’键退出；

    3. 建议使用方法
    运行两遍本脚本：
    第一遍 在命令行中设置 '--check_overlap' 参数，可以随机对bbox进行偏移，用于查找重叠的框框。
    第二遍 在命令行中去掉 '--check_overlap' 参数，此时的bbox为真实标注的bbox，可用于查看标注的bbox的位置精确度。
"""

import json
import sys
if "/opt/ros/kinetic/lib/python2.7/dist-packages" in sys.path:
    sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")
import cv2
import numpy as np
import argparse
import os
import random

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str,
                        default=r"F:\test",
                        help="the data path ")
    parser.add_argument("--start_id", type=int, default=0,
                        help="the folder of the imgs and json files")
    parser.add_argument("--end_id", type=int, default=2000,
                        help="the end point of the frames")
    parser.add_argument("--out_dir", type=str,
                        default=r"F:\review",
                        help="the reulst folder")
    parser.add_argument("--img_height", type=int, default=720,
                        help="the image height")
    parser.add_argument("--img_width", type=int, default=1280,
                        help="the image width")
    parser.add_argument("--check_overlap", action="store_true",
                        help="if use to check overlap bboxes")
    parser.add_argument("--show_color_meaning", action="store_true",
                        help="if show every color meaning")
    parser.add_argument("--save", action="store_true",
                        help="if saving the result as a video files in the out_dir path")
    return parser.parse_args()


class labelme2show(object):
    def __init__(self, input_dir, out_dir, classes, start_show_id, stop_show_id,
                 img_height, img_width):
        self.input_dir = input_dir
        self.out_dir = out_dir
        os.makedirs(out_dir, exist_ok=True)
        self.classes = classes
        self.start_show_id = start_show_id
        self.stop_show_id = stop_show_id
        self.colors = [
            (0, 0, 255),
            (0, 255, 0),
            (255, 0, 0),
            (0, 255, 255),
            (255, 0, 255),
            (255, 255, 0),
            (125, 0, 0),
            (0, 125, 0),
            (0, 0, 125),
            (125, 125, 0),
            (125, 0, 125),
            (0, 125, 125),
            (125, 125, 125)
        ]
        self.img_height = img_height
        self.img_width = img_width
        self.fps = 15
        self.size = (self.img_width, self.img_height)

    def show_one(self, img_path, label_path, check_overlap = False):
        """
        单张图像的显示
        :param img_path:
        :param label_path:
        :param check_overlap: 用于检查是不是与overlap的bbox，随机添加一个位置噪声实现
        :return:
        """
        img = cv2.imread(img_path)
        with open(label_path, 'r') as fp:
            data = json.load(fp)  # 加载json文件
            for shape in data['shapes']:
                if shape["label"] not in self.classes:
                    continue
                if shape["shape_type"] != "rectangle":
                    continue
                cls = shape["label"]
                bbox = shape["points"]
                if check_overlap:
                    # add random noise on every bbox
                    noise_x1 = random.randint(2, 5)
                    noise_y1 = random.randint(2, 5)
                    noise_x2 = random.randint(2, 5)
                    noise_y2 = random.randint(2, 5)
                    cv2.rectangle(img, (int(bbox[0][0])+noise_x1, int(bbox[0][1])+noise_y1),
                                  (int(bbox[1][0])+noise_x2, int(bbox[1][1])+noise_y2),
                              self.colors[self.classes.index(cls)],
                              2)
                else:
                    cv2.rectangle(img, (int(bbox[0][0]), int(bbox[0][1])), (int(bbox[1][0]), int(bbox[1][1])),
                              self.colors[self.classes.index(cls)],
                              2)
        return img

    def encode_all(self, save=True, check_overlap=False, img_with_color=False):
        """
        对所有的数据进行可视化
        :param save:  是不是要进行存储
        :param check_overlap:  是不是检查重叠的框框，如果True的话会随机给每个框框坐标一个便宜量，来让重和的bbox错开便于检查
        :param img_with_color:  是不是需要显示每个label所对应的color的颜色。
        :return: 
        """
        out_video_path = os.path.join(self.out_dir, "out.avi")
        if save:
            videowriter = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc('M', 'P', '4', '2'), self.fps, self.size)
        # for frame_id in range(self.start_show_id, self.stop_show_id, 1):
        frame_id = self.start_show_id
        while frame_id < self.stop_show_id:
            img_path = os.path.join(self.input_dir, str(frame_id) + ".jpg")
            label_path = os.path.join(self.input_dir, str(frame_id) + ".json")
            if not os.path.exists(label_path):
                if os.path.exists(img_path):
                    img = cv2.imread(img_path)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, "NO LABEL ~", (int(self.img_width / 2), int(self.img_height / 2)),
                                        font, 2, self.colors[0], 5)
                    cv2.imshow("label", img)
                    delay = 2 if save else 0
                    keyboard_res = cv2.waitKey(delay)
                    if keyboard_res== 98: # 想要回退的话
                        frame_id -= 2
                        if frame_id < 0:
                            frame_id = 0
                        print("back one frame")
                    elif keyboard_res == 27:
                        print("exiting checking and the end frame id is {}".format(frame_id))
                        break
                    if save:
                        videowriter.write(img)
                else:
                    print("there is no image named {}~~~~".format(frame_id))
            else:
                img = self.show_one(img_path, label_path, check_overlap=check_overlap)
                if img_with_color:
                    print ("show color meanings")
                    img = self.show_color_meanings(img)
                cv2.namedWindow("label", cv2.WINDOW_FREERATIO)
                cv2.imshow("label", img)
                cv2.waitKey(2)
                if not save:
                    keyboard_res = cv2.waitKey(0)
                    if keyboard_res == 98: # 想要回退的话
                        frame_id -= 2
                        if frame_id < 0:
                            frame_id = 0
                        print("back one frame")
                    elif keyboard_res == 27:
                        print("exiting checking and the end frame id is {}".format(frame_id))
                        break
                print ("finished one named {}".format(frame_id))
                if save:
                    videowriter.write(img)

            frame_id += 1
        if save:
            videowriter.release()
            print("finished generating the video!!")

    def show_color_meanings(self, img):
        img_with_color = np.zeros((self.img_height, self.img_width + 300, 3), dtype=np.uint8)
        img_with_color[0:self.img_height, 0:self.img_width, :] = img
        for i in range(len(self.classes)):
            color = self.colors[i]
            label_class = self.classes[i]
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img_with_color, str(label_class), (self.img_width + 10, 100+ i * 40 + 50),
                        font, 1.5, color, 3)
        return img_with_color


if __name__ == "__main__":
    args = argparser()
    classes = ["person", "truck", "car", "motorbike", "road_sign",
               "bus", "traffic_cone", "bicycle", "tricycle", "traffic_light"]
    m_labelme2show = labelme2show(args.input_dir, args.out_dir, classes, args.start_id, args.end_id,
                                  args.img_height, args.img_width)
    # m_labelme2show.encode_all()
    m_labelme2show.encode_all(save=args.save, check_overlap = args.check_overlap, img_with_color = args.show_color_meaning)
