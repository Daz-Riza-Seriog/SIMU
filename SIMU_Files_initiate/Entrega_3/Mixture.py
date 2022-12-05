# Code made by Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# SIMU: Assigment-3

def PuntMez(input):
    out = {}

    out['F'] = [sum([cor['F'][i] for cor in input]) for i in range(len(input[0]['F']))]

    cpl = [282.012, 262.82, 235.65, 301.714, 512.885, 81.5015]  # kJ/kmolK
    cpv = [306.9, 278.49, 255.61, 30.02, 53.57, 39.6761]  # kJ/kmolK
    Tb = [136.2, 145.16, 110.63, -252.76, 161.49, 100]  # C
    Tb = [i + 273.15 for i in Tb]  # K
    Hvap = [35615.3, 36722.1, 33277.8, 896.542, 8171.28, 40693.7]  # kJ/kmol
    Hrxn = [117760.27805856, -54286.279074]

    T = [cor['T'] for cor in input]
    cp = [[0 for i in cpl] for cor in input]
    for j in range(len(T)):
        for i in range(len(cp[0])):
            if T[j] > Tb[i]:
                cp[j][i] = cpv[i]
            else:
                cp[j][i] = cpl[i]
    H = 0
    for cor in input:
        j = input.index(cor)
        for i in range(len(cor['F'])):
            H += cor['F'][i] * cp[j][i] * cor['T']

    To = H / (sum([out['F'][i] * cp[0][i] for i in range(len(out['F']))]))
    out['T'] = To
    out['P'] = (sum([sum(cor['F']) * cor['P'] for cor in input])) / sum(out['F'])

    return out
