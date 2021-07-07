import matplotlib.pyplot as plt
#from matplotlib import pyplot as plt
import numpy as np
from numpy import pi as PI

# # 用于正常显示中文标签
# plt.rcParams["font.sans-serif"]=['SimHei']  
# # 用来正常显示负号
# plt.rcParams['axes.unicode_minus']=False
#再论柱状图
#创建一个画板
plt.figure(figsize=(8,6))

#为画板划分多个Axes
ax = plt.subplot(111)  #假如设置为221，则表示创建两行两列也就是4个子画板,ax为第一个子画板

#数据准备
#y轴数据
nums = [81, 72, 250, 120, 219, 23, 50]
labels=['air-hole','bite-edge','broken-arc','crack','overlap','slag-inclusion','unfused']
colors=['#00CED1','#DC143C','#00582D','#D8FF00','#D200FF','#0048FF','#759A13']

#柱状图的宽度
width = 0.6
#x轴数据
x_bar = np.arange(7)

#绘制柱状图
rects = ax.bar(x_bar,nums,width=width,color=colors)

#为柱状图添加高度值
for rect in rects:
    x = rect.get_x()
    height = rect.get_height()
    ax.text(x+0.2,1.01*height,str(height))
#     print(x,height)

#设置x轴的刻度
ax.set_xticks(x_bar)
ax.set_xticklabels(labels)

#设置y轴的刻标注
ax.set_ylabel("number")
ax.set_xlabel("labels")

# #是否显示网格
# ax.grid(True)

#拉伸y轴
# ax.set_ylim(0,28)

#设置标题
ax.set_title("number of samples")

#显示图表
plt.show()