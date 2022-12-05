# Code made by Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# SIMU: Assigment-3


import numpy as np
import pandas as pd


def React_X(input, coef, X, rl='H', T=0, P=0):
    # Temperatura debe ser en K
    # Considera por defecto el sistema
    out = {}
    Q = 0
    F0 = input['F']
    # Manejo de errores
    if type(coef[0]) in [float, int]:
        coef = [coef]
    if type(X) in [float, int]:
        X = [X]
    if len(coef) != len(X):
        raise Exception('Error en la cantidad de reacciones y conversiones')
    for i in coef:
        if len(i) != len(F0):
            raise Exception('Error en coeficientes de reacciones o cantidad de flujos de entrada')
    if rl == 'H':
        rl = [0 for i in X]

    cpl = [282.012, 262.82, 235.65, 301.714, 512.885, 81.5015]  # kJ/kmolK
    cpv = [306.9, 278.49, 255.61, 30.02, 53.57, 39.6761]  # kJ/kmolK
    Tb = [136.2, 145.16, 110.63, -252.76, 161.49, 100]  # C
    Tb = [i + 273.15 for i in Tb]  # K
    Hvap = [35615.3, 36722.1, 33277.8, 896.542, 8171.28, 40693.7]  # kJ/kmol
    Hrxn = [117760.27805856, -54286.279074]
    # Codigo per se
    F = [i for i in F0]
    for i in range(len(X)):
        for j in range(len(F0)):
            F[j] = F[j] + X[i] * coef[i][j] * F0[rl[i]]
    for i in F:
        if i < 0:
            raise Exception('Flujos menores que 0')
    out['F'] = F
    if T == 0 or P == 0:
        print('Temperatura o presión no especificadas. No se realiza el cálculo energético')
        return [out, Q]
    try:
        T_in = input['T']
    except:
        print('Temperatura de la corriente de entrada no definida. No se realiza el cálculo energético')
        return [out, Q]
    out['T'] = T
    out['P'] = P
    Q += sum([F0[rl[k]] * X[k] * Hrxn[k] for k in range(len(X))])
    for i in range(len(F)):
        if T > Tb[i]:
            if T_in > Tb[i]:
                Q += F0[i] * cpv[i] * (T - T_in)
            else:
                Q += F0[i] * (cpv[i] * (Tb[i] - T_in) + Hvap[i] + cpl[i] * (T - Tb[i]))
        else:
            if T_in < Tb[i]:
                Q += F0[i] * cpl[i] * (T - T_in)
            else:
                Q += F0[i] * (cpv[i] * (Tb[i] - T_in) - Hvap[i] + cpl[i] * (T - Tb[i]))
    Q = round(Q, 2)
    return [out, Q]
