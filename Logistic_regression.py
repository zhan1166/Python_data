import numpy as np
import matplotlib.pyplot as plt
import math
import random

#entropy
#throw a die
##p = np.arange(0.01,1,0.01)
##def Entropy(p):
##    return -p*math.log2(p)-(1-p)*math.log2(1-p) #log base 2
##H = np.zeros(len(p))
##for i in range(0,len(p)):
##    H[i] = Entropy(p[i])
##
##plt.plot(p,H)
##plt.xlabel("p")
##plt.ylabel("H")
##plt.grid(True)
##plt.show()

## logistic regression
def LR(x,y):
    det_theta = 1
    det_v = 1
    theta = 3
    v = 1
    alpha = 0.1 #learning rate
    m = len(x)
    while ((abs(det_theta)>0.01)|(abs(det_v)>0.01)):
        det_theta = dJdt(theta,v,x,y,m)
        det_v = dJdv(theta,v,x,y,m)
        theta = theta-alpha*det_theta
        v = v-alpha*det_v
    return theta,v

def h(theta, v, xi):
    return 1/(1+math.exp(-theta*xi+v))
    
def dJdt(theta,v,x,y,m):
    output = 0
    for i in range(0,len(x)):
              output += 1/m*(h(theta,v,x[i])-y[i])*x[i]
    return output
    
def dJdv(theta,v,x,y,m):
    output = 0
    for i in range(0,len(x)):
              output += 1/m*(-h(theta,v,x[i])+y[i])

    return output

def Regression_ouput(theta,v,x):
    H = np.zeros(len(x))
    for i in range(0,len(x)):
        temp = 1/(1+math.exp(-theta*x[i]+v))
        ##决策边界
        if temp>0.5: H[i]=1
        else: H[i] = 0
    return H



if __name__ == "__main__":
    x = np.array([-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,3,4,5,6,7,8,9,10,11,12])
    y = np.array([0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1])
    theta,v = LR(x,y)
    H = Regression_ouput(theta,v,x)
    print("The theta and v are %f and %f respectively" %(theta, v))
    
    plt.scatter(x,y,color='red',marker='o')

    plt.scatter(x,H,color='blue',marker='x')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()



