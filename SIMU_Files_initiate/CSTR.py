# Code made for Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# IRQ: Python Program-Assigment 1


import seaborn as sns
import numpy as np
from scipy.optimize import fsolve
import timeit

start = timeit.default_timer()
sns.set()

# Ask the user for the input parameters
Q = float(input("Enter Vol.flow rate:"))
V = float(input("Enter ractor Volume:"))
k1 = float(input("Enter rate Constant for Rxn #1:"))
k2 = float(input("Enter rate Constant for Rxn #2:"))
CA_in = float(input("Enter inlet A concentration:"))
CB_in = float(input("Enter inlet B concentration:"))
CC_in = float(input("Enter inlet C concentration:"))
CD_in = float(input("Enter inlet D concentration:"))

# Set te initial guess to the inlet values
x0 = np.zeros((4, 1))
x0[0] = CA_in
x0[1] = CB_in
x0[2] = CC_in
x0[3] = CD_in

# Extract the unknows into meaningful names
x = np.zeros((4, 1))


# Call fsolve to obtain the steady-state concentrations

def func(x):
    # extract the unknowns into meaningful names
    CA = x[0]
    CB = x[1]
    CC = x[2]
    CD = x[3]
    # compute the reaction  rates
    r1 = k1 * CA * CB
    r2 = k2 * CB * CC

    f = [Q * (CA_in - CA) + V * (-r1), Q * (CB_in - CB) + V * (-r1 - r2), Q * (CC_in - CC) + V * (r1 - r2),
         Q * (CD_in - CD) + V * r2]
    return f


sol = fsolve(func, x0)

# Report the results
print("[A] :", sol[0])
print("[B] :", sol[1])
print("[C] :", sol[2])
print("[D] :", sol[3])

stop = timeit.default_timer()
print('Time: ', stop - start)
