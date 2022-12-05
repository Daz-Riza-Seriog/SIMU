# Code made by Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# SIMU: Assigment-3

from SIMU_Files_initiate.Entrega_3 import Exchanger, Mixture, Reactor_Estch, Flash_sep, Pumps, Dest_tower

# Para correr aca necesitamos un directorio con lista { ´F´ =[, , , , ], ´T´=} llamado inp -> input
# Orden de los flujos: EB, ST, TO, H2, CH4, WT

line1 = {}
line1['F'] = [9.35624, 0.0518544, 0.0112358, 0, 0, 0]  # kmol
line1['T'] = 37.1787 + 273.15
line1['P'] = 1e5
print("Entradas a la linea 1\n", line1)

[line2, Q_E501] = Exchanger.HeatEx(line1, T=868.15, P=1e5)
print("\nHeat Duty Exchanger E-501\n", Q_E501, "kJ/hr")
print("Salida en linea 2\n", line2)

line4w = {}
line4w['T'] = 25 + 273.15
line4w['P'] = 1e5
line4w['F'] = [0, 0, 0, 0, 0, 666.101]
[line5w, Q_H501] = Exchanger.HeatEx(line4w, P=1e5, T=701.53 + 273.15)
print("\nHeat Duty Exchanger H-501\n", Q_H501, "kJ/hr")
print("Salida en linea 5\n", line5w)

line6 = Mixture.PuntMez([line5w, line2])
print("\nSalida en linea 6\n", line6)

# Definición de reacciones
reac1 = [-1, 1, 0, 1, 0, 0]
reac2 = [-1, 0, 1, -1, 1, 0]
reac = [reac1, reac2]
x1 = 0.7
x2 = 0.2
x = [x1, x2]

[line7, Q_R501] = Reactor_Estch.React_X(line6, reac, x, T=950, P=4e4)
print("\nHeat Duty Reactor R-501\n", Q_R501, "kJ/hr")
print("Salida en linea 7\n", line7)

[line8, Q_E502] = Exchanger.HeatEx(line7, T=77.608 + 273.15, P=4e4)
print("\nHeat Duty Reactor E-502\n", Q_E502, "kJ/hr")
print("Salida en linea 8\n", line8)

[line9, line10, line11] = Flash_sep.Flash(line8, [[0, 0, 0, 1, 1, 0], [1, 1, 1, 0, 0, 0]])
print("\nSalida en linea 9\n", line9)
print("Salida en linea 10\n", line10)
print("Salida en linea 11\n", line11)

line12 = Pumps.Pump(line10, P=1.63e5)
print("\nSalida en linea 12\n", line12)

[line16, line15] = Dest_tower.TorreDest(line12, [0.994, 0.9708], [2, 1], T=[122.305 + 273.15, 171.57 + 273.15],
                                        P=[1.2e5, 1.962e5])
print("\nSalida en linea 15\n", line15)
print("Salida en linea 16\n", line16)

[line24, line28] = Dest_tower.TorreDest(line15, [0.99996, 0.992], [2, 1], T=[117.702 + 273.15, 172.778 + 273.15],
                                        P=[0.6e5, 1.962e5])
print("\nSalida en linea 24\n", line24)
print("Salida en linea 28\n", line28)