# Code made by Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# SIMU: Assigment-3

def HeatEx(input, T, P):
    F0 = input['F']
    T_in = input['T']
    out = {}
    Q = 0

    cpl = [282.012, 262.82, 235.65, 301.714, 512.885, 81.5015]  # kJ/kmolK
    cpv = [306.9, 278.49, 255.61, 30.02, 53.57, 39.6761]  # kJ/kmolK
    Tb = [136.2, 145.16, 110.63, -252.76, 161.49, 100]  # C
    Tb = [i + 273.15 for i in Tb]  # K
    Hvap = [35615.3, 36722.1, 33277.8, 896.542, 8171.28, 40693.7]  # kJ/kmol
    Hrxn = [117760.27805856, -54286.279074]

    # Calculo de Flujos
    out['F'] = F0
    out['P'] = P
    out['T'] = T

    # Calculo energetico
    for i in range(len(F0)):
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


# Para correr aca necesitamos un directorio con lista { ´F´ =[, , , , ], ´T´=} llamado inp -> input

