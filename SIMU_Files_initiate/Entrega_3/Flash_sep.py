# Code made by Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# SIMU: Assigment-3

def Flash(input, rest):
    F0 = input[0]
    out = [[] for i in rest]
    
    for i in range(len(rest)):
        out[i] = [F0[k] * rest[i][k] for k in range(len(F0))]
    # out[-1] = [F0[k] - sum([out[i][k] for i in range(len(rest))]) for k in range(len(F0))]
    
    # Creamos las 3 lineas con Flujo, Temperatura, Presion
    result = []
    for i in range(len(out)):
        result.append([out[i],input[1],input[2]])
        
    return result

line1 = [] 
# Propano, Propileno, Cumeno, DIP, Benceno
line1.append([0.83, 0.07, 0.02, 0.03, 0.04])  # Aqui agregamos las composicion 
line1.append([37.1787 + 273.15]) # Esta es la temperatura de los componentes a la entrada al Flash
line1.append([1e5]) # Presion a la que entran los componentes
print("Entradas a la linea 1\n", line1)

line9,line10 = Flash(line1, [[1, 1, 0, 0, 0], [0, 0, 1, 1, 1]]) # Establecemos linea livianos y fondos


print("\nSalida en linea 9\n", line9)
print("Salida en linea 10\n", line10)


