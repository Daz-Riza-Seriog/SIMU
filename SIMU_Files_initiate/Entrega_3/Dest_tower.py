# Code made by Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# SIMU: Assigment-3

from SIMU_Files_initiate.Entrega_3 import K_repart
import numpy as np

def TorreDest(inp, rec, kc, T, P):
    F0 = inp['F']
    Tin = inp['T']
    Pin = inp['P']
    out = [{}, {}]
    for i in out:
        i['F'] = [0 for j in F0]
    out[0]['F'][kc[0]] = F0[kc[0]] * rec[0]
    out[1]['F'][kc[0]] = F0[kc[0]] * (1 - rec[0])
    out[1]['F'][kc[1]] = F0[kc[1]] * rec[1]
    out[0]['F'][kc[1]] = F0[kc[1]] * (1 - rec[1])
    x = [i / sum(F0) for i in F0]
    x = x[0:3]
    k = K_repart.Krep(Pin, Tin, x, 8.314)
    for i in range(len(F0)):
        if out[0]['F'][i] == 0 and out[1]['F'][i] == 0 and F0[i] != 0:
            out[0]['F'][i] = np.real(k[i] / (k[i] + 1) * F0[i])
            out[1]['F'][i] = F0[i] - out[0]['F'][i]
    for i in range(len(out)):
        out[i]['T'] = T[i]
        out[i]['P'] = P[i]

    return out