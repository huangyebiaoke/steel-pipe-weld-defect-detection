import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

price = [39.5, 39.9, 45.4, 38.9, 33.34]
"""
绘制水平条形图方法barh
参数一：y轴
参数二：x轴
"""
plt.barh(range(5), price, height=0.7, color='steelblue', alpha=0.8)      # 从下往上画
plt.yticks(range(5), ['亚马逊', '当当网', '中国图书网', '京东', '天猫'])
plt.xlim(30,47)
plt.xlabel("价格")
plt.title("不同平台图书价格")
for x, y in enumerate(price):
    plt.text(y + 0.2, x - 0.1, '%s' % y)
plt.show()