# Code made by Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# SIMU: Assigment-2

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


Pc_s = {'Ethylbenzene':36.06e5,'Toluene':41.06e5,'Styrene':38.40e5}
Tc_s = {'Ethylbenzene':617.2,'Toluene':591.8,'Styrene':636.0}
Vc_s = {'Ethylbenzene':374e-3,'Toluene':316e-3,'Styrene':352e-3}
data = pd.DataFrame(data=(Pc_s,Tc_s,Vc_s))
data['Data'] = ['Pc Pas','Tc K','Vc m3/Kmol']


# Esta función entrega los valores de a y b dadas P,T,Pc,Tc y w

def PRab(P, T, Pc, Tc, w):
    Pr = P / Pc
    Tr = T / Tc
    ep = 1 - np.sqrt(2)
    sig = 1 + np.sqrt(2)
    R = 8.314462 # m^3* Pas / Kmol * K
    ohm = 0.07780
    psi = 0.45724
    alpha = (1 + (0.37464 + 1.54226 * w - 0.26992 * w ** 2) * (1 - Tr ** (0.5))) ** 2
    b = ohm * R * Tc / Pc
    a = psi * alpha * R ** 2. * Tc ** 2. / Pc
    return a, b


# Definición de función de Peng-Robinson dadas Pc, Tc y w para sustancia pura
def PR(P, T, Pc, Tc, w):
    Pr = P / Pc
    Tr = T / Tc
    ep = 1 - np.sqrt(2)
    sig = 1 + np.sqrt(2)
    R = 8.314462
    ohm = 0.07780
    psi = 0.45724
    alpha = (1 + (0.37464 + 1.54226 * w - 0.26992 * w ** 2) * (1 - Tr ** (0.5))) ** 2
    b = ohm * R * Tc / Pc
    a = psi * alpha * R ** 2. * Tc ** 2. / Pc
    beta = ohm * Pr / Tr
    q = a / (b * R * T)

    Zv = 1
    e1 = 1e5
    mit = 1e3
    i = 1
    while e1 > 1e-8 and i < mit:
        Zv2 = 1 + beta - q * beta * (Zv - beta) / ((Zv + ep * beta) * (Zv + sig * beta))
        e1 = abs(Zv2 - Zv)
        Zv = Zv2
        i = i + 1

    Zl = beta
    e2 = 1e5
    j = 1
    while e2 > 1e-8 and j < mit:
        Zl2 = beta + (Zl + ep * beta) * (Zl + sig * beta) * ((1 + beta - Zl) / (q * beta))
        e2 = abs(Zl2 - Zl)
        Zl = Zl2
        j = j + 1

    vl = Zl * R * T / P
    vv = Zv * R * T / P
    return Zl, Zv, vl, vv
