import random as rand
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from APPSO import APPSO

#读取数据
data = np.array(pd.read_csv('./data.csv'))
#设置离散粒子群参数，并输入数据
ap = APPSO(data,alpha=0.6,bate=0.7)
#记录每次迭代的数据
rv = []
#迭代200次
for t in range(200):
    #输出当前第几代
    print(t,end=':')
    #更新粒子群位置
    ap.Update(t)
    #寻找当前最佳适应值的粒子
    av = ap.AdaptiveValue(ap.gBest['array'])
    #添加入rv中
    rv.append(av)
    #输出当前最佳适应值粒子
    print(av)
#输出最佳结果
print(ap.gBest)
#画图
plt.xlabel("iteration times")
plt.ylabel("adaptive value")
plt.title('fitness')
plt.plot(range(len(rv)),rv)
plt.savefig('fitness.png')
plt.show()