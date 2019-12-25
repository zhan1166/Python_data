import matplotlib.pyplot as plt
import numpy as np
import math
import random

def Data():
    x = np.arange(0.1,10,0.1)
    y = np.zeros(len(x))
    data = []
    for i in range(0,len(x)):
        y[i] = -0.5*(x[i]-5)**2+12
        for j in range(0,3):
            data.append(np.array([x[i],y[i]+random.uniform(-2,2)]))

    Mom = Momentum(data)
    for i in range(len(data)):
        plt.scatter(data[i][0],data[i][1], color="blue", marker="x")

    plt.plot(x,Mom)
    plt.grid(True)
    plt.show()
    
    return


def Momentum(data):
    Beta = 0.9
    alpha = 0.1
    Mom = []
    v = 0
    for i in range(int(len(data)/3)):
        mean = (data[i*3][1]+data[i*3+1][1]+data[i*3+2][1])/3
        w = mean
        v = (Beta*v+(1-Beta)*(mean))
        w = w-alpha*v
        Mom.append(w)
    
    return Mom

def Gradian(data):
    Beta = 0.9
    alpha = 0.9
    Gra = []
    v = 0
    w = (data[0][1]+data[1][1]+data[2][1])/3
    for i in range(int(len(data)/3)):
        mean = (data[i*3][1]+data[i*3+1][1]+data[i*3+2][1])/3
        w = w-alpha*(w-mean)
        Gra.append(w)
    
    return Gra


if __name__ == "__main__":

    Data()
