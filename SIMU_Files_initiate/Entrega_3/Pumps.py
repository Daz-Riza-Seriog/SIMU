# Code made by Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# SIMU: Assigment-3

def Pump(input, P):
    out = {}
    out['F'] = input['F']
    out['P'] = P
    try:
        out['T'] = input['T']
    except:
        pass
    return out
