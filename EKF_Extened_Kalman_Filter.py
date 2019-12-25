import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt
from math import atan, pi

def EFK(x_k, P_k, u_k, y_kp1, deltaT):
    ##x_k 是上一时刻best estimate
    ##u_k 是control vector
    ##y_k 是测量值
    ##deltaT 是时间单位

    ##Define parameters
    [S,D] = [20,40]
    F_k = np.mat([[1, deltaT],[0,1]])
    L_k = np.identity(2)
    M_kp1 = 1

    ##calculation(prediction part)
    xp_kp1 = F_k.dot(x_k)+np.mat([[0],[deltaT]]).dot(u_k)
    Pp_kp1 = F_k.dot(P_k).dot(F_k.T)+L_k.dot(0.1*np.identity(2)).dot(L_k.T)
    H_kp1 = np.mat([S/((D-xp_kp1[0].item())**2+S**2),0])
    ##Optimal gain
    K_kp1 = Pp_kp1.dot(H_kp1.T)/(H_kp1.dot(Pp_kp1).dot(H_kp1.T)\
                                        +M_kp1*0.01*M_kp1)

    ##Correction part
    h_xp1 = atan(S/(D-xp_kp1[0]))*180/pi
    print(h_xp1)
    x_kp1 = xp_kp1+K_kp1*(y_kp1-h_xp1)
    P_kp1 = (np.identity(2)-K_kp1.dot(H_kp1)).dot(Pp_kp1)
    return x_kp1

if __name__=="__main__":
    ##Define initial conditions:
    [u0, y1] = [-2, 30]
    x_k = np.mat([[0],[5]])
    P_k = np.mat([[0.01,0],[0,1]])
    u_k = -2
    deltaT = 0.5
    y_kp1 = 30
    x_kp1 = EFK(x_k, P_k, u_k, y_kp1, deltaT)
    print(x_kp1)
