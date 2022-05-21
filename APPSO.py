import random as rand
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

class Edage:
    def __init__(self,route):
        if len(route) == 0:
            self.data = []
            return
        last = route[0]
        border = []
        for i in range(1,len(route)):
            border.append((last,route[i]))
            last = route[i]
        self.data = border

    def ToRoute(self):
        result = []
        for i in self.data:
            result.append(i[0])
        result.append(self.data[-1][1])
        return result

    def __EleEq__(self,e1,e2):
        t1 = e1==e2
        t2 = e1==tuple(reversed(e2))
        return t1 or t2

    def __sub__(self, other):
        result = []
        for i in self.data:
            content = False
            for j in other.data:
                if self.__EleEq__(i,j):
                    content = True
            if not content:
                result.append(i)
        border = Edage([])
        border.data = result
        return border
    
    def __add__(self,other):
        route = self.ToRoute()
        for i in other.data:
            start = route.index(i[0])
            end = route.index(i[1])
            #print(start,end)
            r = list(reversed(route[start+1:end+1]))
            for j in range(end-start):
                route[start+1+j] = r[j]
        return Edage(route)

    def __mul__(self,c):
        if c>1:
            raise('probablity over one!')
        data = self.data.copy()
        d = []
        b = Edage([])
        for i in data:
            if random.random() < c:
                d.append(i)
        b.data = d
        return b

    def __str__(self):
        return self.data.__str__()

def Borders(arr):
    result = []
    for i in arr:
        result.append(Edage(i))
    return result

def Routes(arr):
    result = []
    for i in arr:
        result.append(i.ToRoute())
    return result

def Connect(b1,b2):
    nb = Edage([])
    nb.data = b1.data + b2.data
    return nb
    

def RandomChoose(borders):
    result = Edage([])
    for i in borders:
        result = Connect(result,i*random.random())
    return result



class APPSO:

    #求距离矩阵
    def __Distance__(self):
        dl = self.dataLen
        self.cityDistance = np.zeros((dl,dl))
        xs = self.data[:,0].T
        ys = self.data[:,1].T

        for i in range(dl):
            x,y = self.data[i][0],self.data[i][1]
            self.cityDistance[i] = ((xs-x)**2 + (ys-y)**2)**0.5

    def __SortedEdge__(self):
        cd = self.cityDistance.copy()
        result = [np.argsort(cd[0]).tolist()]
        for i in range(1,self.dataLen):
            result.append(np.argsort(cd[i]).tolist())
        self.sortedEdge = np.array(result)

    #产生pNum个粒子
    def __Assigments__(self):
        pNum = self.pNum
        routes = []
        for i in range(pNum):
            temp = np.random.permutation(self.dataLen)
            temp = temp.tolist()
            while temp in routes:
                temp = np.random.permutation(self.dataLen)
                temp = temp.tolist()
            routes.append(temp)
        self.routes = routes

    def __init__(self,data:np.array,ratedLoad=8,pNum = 100,alpha = 0.8,bate = 0.8):
        self.ratedLoad = ratedLoad#货车额定负载
        self.data = data#地图坐标
        self.dataLen = len(data)#数据长度
        self.gBest = {'index':-1,'value':float('inf'),'array':[]}
        self.pNum = pNum
        self.alpha = alpha
        self.bate = bate
        self.cityDistance = self.data
        self.__Assigments__()
        self.__DefaultPBest__()
        self.__SortedEdge__()

    #求一个粒子的适应度值
    def AdaptiveValue(self,assigment):
        time = 0
        for i in range(self.dataLen):
            time += self.data[i][assigment[i]]
        return time

    def __DefaultPBest__(self):
        pBestRoute = []
        pBestValue = []
        for i,j in zip(self.routes,range(self.pNum)):
            av = self.AdaptiveValue(i)
            if av < self.gBest['value']:
                self.gBest['index'] = j
                self.gBest['value'] = av
                self.gBest['array'] = i
            pBestRoute.append(i)         
            pBestValue.append(av)         
        self.pBestRoute = pBestRoute
        self.pBestValue = pBestValue

    def __GPBest__(self):
        pBestValue = self.pBestValue
        pBestRoute = self.pBestRoute
        for i,j in zip(self.routes,range(self.pNum)):
            av = self.AdaptiveValue(i)
            if av < pBestValue[j]:
                pBestValue[j] = av
                pBestRoute[j] = i
            if av < self.gBest['value']:
                self.gBest['index'] = j
                self.gBest['value'] = av
                self.gBest['array'] = i

    def Update(self,t=1,MaxGen=100):
        N = self.dataLen
        m = int(np.floor((N-1)-(N-5)*t/MaxGen))
        V = self.sortedEdge.copy()[:,1:m].tolist()
        VB = Borders(V)
        RB = Borders(self.routes)
        PBRB = Borders(self.pBestRoute)
        PGB = Edage(self.gBest['array'])
        for i in range(len(RB)):
            r = [random.random() for i in range(5)]
            TVB = RandomChoose(VB)
            if r[2] < self.alpha:
                RB[i] = RB[i]+((PBRB[i]-RB[i])*r[0])
            elif r[3] < self.bate:
                RB[i] = RB[i]+((PGB-RB[i])*r[1])
            else:
                RB[i] = RB[i]+(TVB*r[4])
        self.routes = Routes(RB)
        self.__GPBest__()