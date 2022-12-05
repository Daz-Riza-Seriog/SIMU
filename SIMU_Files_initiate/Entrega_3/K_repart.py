# Code made by Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# SIMU: Assigment-2


import numpy as np
import pandas as pd


# Esta función entrega los valores de a y b dadas P,T,Pc,Tc y w

def PRab(P, T, Pc, Tc, w):
    Tr = T / Tc
    R = 8.314462  # Pas*m^3/mol*K
    ohm = 0.07780
    psi = 0.45724
    fw = 0.37464 + 1.54226 * w - 0.26992 * w ** 2
    alpha = (1 + fw * (1 - (Tr ** 0.5))) ** 2
    b = ohm * R * Tc / Pc
    a = psi * alpha * (R ** 2) * (Tc ** 2) / Pc
    return a, b

#TODO hacer un input for add to dataframe new components

Pc_s = {'Ethylbenzene': 36.06e5, 'Toluene': 41.06e5, 'Styrene': 38.40e5}
Tc_s = {'Ethylbenzene': 617.2, 'Toluene': 591.8, 'Styrene': 636.0}
w_s = {'Ethylbenzene': 0.303, 'Toluene': 0.262, 'Styrene': 0.297}
data = pd.DataFrame(data=(Pc_s, Tc_s, w_s))
data['Data'] = ['Pc Pas', 'Tc K', 'w']

# Función que calcula los ab de mezcla de separación

def PRabmez(P, T, x):
    ab = []

    ab.append(PRab(P, T, data['Toluene'][0], data['Toluene'][1], data['Toluene'][2]))  # Toluene
    ab.append(PRab(P, T, data['Ethylbenzene'][0], data['Ethylbenzene'][1], data['Ethylbenzene'][2]))  # Ethylbenceno
    ab.append(PRab(P, T, data['Styrene'][0], data['Styrene'][1], data['Styrene'][2]))  # Estireno

    a = 0
    b = 0
    for i in range(len(ab)):
        for j in range(len(ab)):
            a = a + x[i] * x[j] * ab[i][0] ** 0.5 * ab[j][0] ** 0.5

        b = b + x[i] * ab[i][1]
    return a, b, ab


# Definición de función de cálculo de Z
def PRZ(A, B):
    pol = np.poly1d([1, -1, A - B - B ** 2, -A * B])
    rt = np.roots(pol)
    Zl = min(rt)
    Zv = max(rt)
    return Zl, Zv


def cr_AB(ab, P, T, R):
    a = []
    b = []
    for i in ab:
        a.append(i[0])
        b.append(i[1])
    c1 = P / (R ** 2 * T ** 2)
    c2 = P / (R * T)
    A = [item * c1 for item in a]
    B = [item * c2 for item in b]
    return A, B


# Definición de función de cálculo de coeficientes de fugacidades parciales

def fug_vap(AB, A, B, Zv):
    A_i = AB[0]
    B_i = AB[1]
    FIV = []
    for i in range(len(A_i)):
        FIV.append(np.exp(
            (Zv - 1) * B_i[i] / B - np.log(Zv - B) - A / B * (2 * np.sqrt(A_i[i] / A) - B_i[i]) * np.log(1 + B / Zv)))
    return FIV


# Definición de función de cálculo del coeficiente de fugacidad del vapor
def fug_vap_tot(A, B, Zv):
    return np.exp(Zv - 1 - np.log(Zv - B) - A / B * np.log(1 + B / Zv))


# Definición de funciones de presión de saturación
def Psat_TO(T):
    return 1e3 * np.exp(13.9320 - 3056.96 / (T - 273.15 + 217.625))


def Psat_EB(T):
    return 1e3 * np.exp(13.9726 - 3259.93 / (T - 273.15 + 212.3))


def Psat_ST(T):
    return 1e5 * 10 ** (4.21948 - 1525.059 / (T - 56.379))


def Psat(T):
    return [Psat_TO(T), Psat_EB(T), Psat_ST(T)]


# Definición de función de volumen del liquido
def v_i(P, T, R):
    ab = []
    ab.append(PRab(P, T, 41.06e5, 591.8, 0.262))
    ab.append(PRab(P, T, 36.06e5, 617.2, 0.303))
    ab.append(PRab(P, T, 36.40e5, 636.0, 0.297))
    AB = cr_AB(ab, P, T, R)
    A = AB[0]
    B = AB[1]
    v = []
    for i in range(len(A)):
        Z = PRZ(A[i], B[i])
        v.append(Z[0] * R * T / P)
    return v


# Definición de función de fugacidad de vapor saturado
def fug_vap_sat(T, R):
    Pi = Psat(T)
    ab = []
    ab.append(PRab(Pi[0], T, 41.06e5, 591.8, 0.262))
    ab.append(PRab(Pi[1], T, 36.06e5, 617.2, 0.303))
    ab.append(PRab(Pi[2], T, 36.40e5, 636.0, 0.297))
    A = [item * 0 for item in Pi]
    B = [item * 0 for item in A]
    for i in range(len(Pi)):
        buf = cr_AB(ab, Pi[i], T, R)
        A[i] = buf[0][i]
        B[i] = buf[1][i]
    Zv = []
    FVS = [item * 0 for item in B]
    for i in range(len(A)):
        Z = PRZ(A[i], B[i])
        Zv.append(Z[1])
        FVS[i] = fug_vap_tot(A[i], B[i], Zv[i])
    return FVS


# Definición de función de fugacidad de líquido
def fug_liq(P, T, R):
    Pi = Psat(T)
    vi = v_i(P, T, R)
    fivs = fug_vap_sat(T, R)
    FIL = []
    for i in range(len(Pi)):
        FIL.append(fivs[i] * Pi[i] / P * np.exp(vi[i] * (P - Pi[i]) / (R * T)))
    return FIL


def Evap():
    return [33.2778, 35.6153, 36.7221]


def act(vi, x, T, R):
    gamma = []
    PHI = []
    delta = []
    for i in range(len(vi)):
        PHI.append(x[i] * vi[i])
        delta.append((Evap()[i] / vi[i]) ** 0.5)
    PHI = PHI / sum(PHI)
    sum2 = 0
    for i in range(len(vi)):
        sum2 = sum2 + PHI[i] * delta[i]
    for i in range(len(vi)):
        gamma.append(np.exp((vi[i] * (delta[i] - sum2) ** 2) / (R * T)))
    return gamma


def Kr(gamma, FIL, FIV):
    k = []
    for i in range(len(gamma)):
        k.append(gamma[i] * FIL[i] / FIV[i])
    return k


def Krep(P, T, x, R):
    temp = [x[1], x[2], x[0]]
    x = temp
    coef = PRabmez(P, T, x)
    ab_i = coef[2]
    A = coef[0] * P / (R ** 2 * T ** 2)
    B = coef[1] * P / (R * T)

    Z = PRZ(A, B)
    Zl = Z[0]
    Zv = Z[1]

    AB_i = cr_AB(ab_i, P, T, R)

    FVI = fug_vap(AB_i, A, B, Zv)

    fv = fug_vap_tot(A, B, Zv)

    vi = v_i(P, T, R)

    fvs = fug_vap_sat(T, R)
    FLI = fug_liq(P, T, R)
    gamma = act(vi, x, T, R)
    k = Kr(gamma, FLI, FVI)
    return [k[1], k[2], k[0]]


# R = 8.314462
# P = 1.28e5  # Pa
# T = 500  # K
# xTO = 0.2  # x tolueno
# xEB = 0.1  # x etilbenceno
# xST = 0.7  # x estireno
# x = [xTO, xEB, xST]
# coef = PRabmez(P, T, x)
# ab_i = coef[2]
# A = coef[0] * P / (R ** 2 * T ** 2)
# B = coef[1] * P / (R * T)
# Z = PRZ(A, B)
# Zl = Z[0]
# Zv = Z[1]
#
#
# AB_i = cr_AB(ab_i, P, T, R)
#
# FVI = fug_vap(AB_i, A, B, Zv)
#
# fv = fug_vap_tot(A, B, Zv)
#
# vi = v_i(P, T, R)
#
# fvs = fug_vap_sat(T, R)
# FLI = fug_liq(P, T, R)
# gamma = act(vi, x, T, R)
# k = Krep(P,T,x, 8.314)

