# Code made by Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# SIMU: Assigment-3

def Flash(input, rest):
    F0 = input['F']
    if type(rest[0]) not in [list]:
        rest = [rest]
    out = [{} for i in rest]
    out.append({})
    for i in range(len(rest)):
        out[i]['F'] = [F0[k] * rest[i][k] for k in range(len(F0))]
    out[-1]['F'] = [F0[k] - sum([out[i]['F'][k] for i in range(len(rest))]) for k in range(len(F0))]
    try:
        for i in out:
            i['T'] = input['T']
            i['P'] = input['P']
    except:
        pass
    return out
