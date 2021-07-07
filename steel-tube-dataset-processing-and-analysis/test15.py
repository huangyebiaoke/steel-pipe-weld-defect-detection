import matplotlib.pyplot as plt
import math
import random

x_arr=[]
y_arr=[]
r_arr=[]
x_arr.append(random.uniform(0.,150.))
y_arr.append(random.uniform(0.,150.))
r_arr.append(random.uniform(1.,20.))
while True:
    x=random.uniform(0.,150.)
    y=random.uniform(0.,150.)
    r=random.uniform(1.,20.)
    can_add=True
    # 循环集合，把新生成的圆和集合中的每个圆作比较
    for i in range(x_arr.__len__()):
        if math.pow((x-x_arr[i]),2)+math.pow((y-y_arr[i]),2)-math.pow((r-r_arr[i]),2)<=0:
            # 只要新生成的圆和集合中任意一个重合，can_add设为False，不能被加入集合
            can_add=False
            break
    # 为True意味着新生成的圆和集合中任意的圆都不重合，才能加入集合
    if(can_add):
        x_arr.append(x)
        y_arr.append(y)
        r_arr.append(r)
        # 设置圆的个数
        if(x_arr.__len__()==1000):
            break

# # 打印集合中的圆，比1000要少，因为去掉了很多重合的圆
# print(x_arr.__len__())
##########以下是绘图API和matlab相似#################
plt.plot(x,y)
plt.scatter(x_arr,y_arr, s=r_arr, c='r', alpha=1)
plt.xlim(0,150)
plt.ylim(0,150)
plt.title('test')
plt.xlabel('x')
plt.ylabel('y')
plt.show()