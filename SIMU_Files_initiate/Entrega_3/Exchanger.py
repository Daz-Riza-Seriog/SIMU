# Code made by Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# SIMU: Assigment-3

def HeatEx(input, T, P):
    F0 = input[0]
    T_in = input[1][0]
    out = []
    Q = 0

    cpl = [282.012, 262.82, 235.65, 301.714, 512.885, 81.5015]  # kJ/kmolK
    cpv = [306.9, 278.49, 255.61, 30.02, 53.57, 39.6761]  # kJ/kmolK
    Tb = [136.2, 145.16, 110.63, -252.76, 161.49, 100]   # C
    Tb = [i + 273.15 for i in Tb]  # K
    Hvap = [35615.3, 36722.1, 33277.8, 896.542, 8171.28, 40693.7]  # kJ/kmol

    # Calculo de Flujos
    out.append(F0)
    out.append(P) 
    out.append(T)

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
line1 = [] 
line1.append([9.35624, 0.0518544, 0.0112358, 0, 0, 0])  # Aqui agregamos las composicion en kmol de las especies en Kmol
line1.append([37.1787 + 273.15]) # Esta es la temperatura de los componentes a la entrada
line1.append([1e5]) # Presion a la que entran los componentes
print("Entradas a la linea 1\n", line1)

[line2, Q_E501] = HeatEx(line1, T=868.15, P=1e5) # Condiciones a las que opera el intercambiador
print("\nHeat Duty Exchanger E-501\n", Q_E501, "kJ/hr")
print("Salida en linea 2\n", line2) 

