# Code made for Sergio Andrés Díaz Ariza
# 30 September 2022
# License MIT
# IRQ: Python Program-Assigment 1


# This program simulates the steady-state profile
# in a Packed Bed Reactor (PBR) of the reaction
# A <==> B + C, occuring on a solid catalyst in
# contact with a gas stream of A, B, C, and a
# non-reactive dilutent gas G. The reactor is assumed
# to be isothermal and there are no mass transfer
# limitations. Surface reaction is assumed to be
# rate limiting with adsorption/desorption in
# equilibrium.


import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
import timeit

start = timeit.default_timer()
sns.set()


class set_Rate:
    # set reaction rate law parameters
    # moles of active sites per Kg of catalyst
    c_t = 1e-3
    # adsorption equilibrium constant for A
    Ka_A = 4.2e-5  # in 1 / Pa
    # adsorption equilibrium constant for B
    Ka_B = 2.5e-5  # in 1 / Pa
    # forward surface reaction rate constant
    k_s = 30  # in 1 / s
    # equilibrium constant for surface reaction
    Keq_s = 9.12e5  # in Pa


class set_Reactor:
    # diameter of catalyst particles
    D_p = 0.005  # in m
    # void fraction of bed
    phi = 0.64
    # cross sectional area of bed
    A_c = 0.0079  # in m ^ 2
    # density of solid catalyst phase
    rho_s = 900  # in Kg / m ^ 3
    # set inlet gas properties
    # total pressure of inlet stream
    P_0 = 1.2  # in Bar
    p_A0 = 1.75
    # inlet volumetric flow rate
    vflow_0 = 0.001  # in m ^ 3 / s
    # inlet temperature
    T_0 = 373  # in K
    # molar flow rate of A in feed stream
    F_A0 = (p_A0 * vflow_0 / 8.314) / T_0  # in mol / s
    # molar flow rate of dilutent gas in feed stream
    F_G0 = ((P_0 - p_A0) * vflow_0 / 8.314) / T_0  # in mol / s
    # total molar flow rate of feed stream in mol/s
    F_tot0 = F_A0 + F_G0
    # density of gas phase at inlet conditions
    rho_0 = 2.9  # in Kg / m ^ 3
    # viscosity of gas pahse
    mu = 2e-5  # in Pa * s
    # superficial mass velocity
    gamma = (rho_0 * vflow_0) / A_c
    # Ergun constant beta_0 for model of pressure
    # drop across packed bed, assumed constant viscosity
    var1 = (150 * (1 - phi) * mu) / D_p
    var2 = (gamma * (1 - phi)) / (rho_0*D_p * (phi ** 3)) #Here the Value from matlab is different var2=34.7669
    beta_0 = var2 * (var1 + 1.75 * gamma )


Rate = set_Rate()
Reactor = set_Reactor()


class set_initial_state:
    __metaclass__ = Rate
    __metaclass__ = Reactor
    x_0 = np.empty(7)  # allocate memory
    R = 8.314  # ideal gas constant in SI units
    x_0[0] = Reactor.F_A0
    x_0[1] = 0  # molar flow rate of B
    x_0[2] = 0  # molar flow rate of C
    x_0[3] = Reactor.P_0  # pressure
    # following values from isotherm of A
    c_v = Rate.c_t / (1 + Rate.Ka_A * Reactor.p_A0)
    c_AS = Rate.Ka_A * Reactor.p_A0 * c_v
    x_0[4] = c_AS  # conc. of absorbed A
    x_0[5] = 0  # conc. of absorbed B
    x_0[6] = c_v  # conc. of vacant sites


# % set initial state vector
initial = set_initial_state()

# set mass matrix
Mass = np.zeros((7, 7))
Mass[0:4, 0:4] = np.eye(4)

# ask user to input mass of catalyst in reactor
W_tot = float(input('Enter tot. cat. mass in PBR : '))


# PBR_calc_f function
def PBR_calc_f(W, x, Rate, Reactor):
    f = np.zeros((7, 1))
    # extract state variables
    F_A = x[0]  # molar flow rate of A
    F_B = x[1]  # molar flow rate of B
    F_C = x[2]  # molar flow rate of C
    P = x[3]  # total pressure
    c_AS = x[4]  # conc. of absorbed A
    c_BS = x[5]  # conc. of absorbed B
    c_v = x[6]  # conc. of vacant sites

    # compute total molar flow rate
    F_tot = F_A + F_B + F_C + Reactor.F_G0

    # compute partial pressures in gas phase
    p_A = (P * F_A) / F_tot
    p_B = (P * F_B) / F_tot
    p_C = (P * F_C) / F_tot

    # compute volumetric flow rate in m^3/s
    R = 8.314  # ideal gas constant in SI units
    T = Reactor.T_0  # isothermal operation
    vflow = (F_tot * R * T) / P  # volumetric flow rate

    # compute surface reaction rate
    r_R = Rate.k_s * (c_AS - (c_BS * p_C / Rate.Keq_s))  # Another issue

    # Next, evaluate derivative functions.

    # mole balance on A
    f0 = -r_R
    # mole balance on B
    f1 = r_R
    # mole balance on C
    f2 = r_R
    # pressure drop across packed bed
    var1 = Reactor.beta_0 / (Reactor.A_c * (1 - Reactor.phi) * Reactor.rho_s)  ## maybe here is the issue
    f3 = -var1 * (Reactor.P_0 / P) * (F_tot / Reactor.F_tot0)
    # adsorption equilibrium of A
    f4 = Rate.Ka_A * p_A * (c_v - c_AS)
    # adsorption equilibrium of B
    f5 = Rate.Ka_B * p_B * (c_v - c_BS)
    # site balance
    f6 = Rate.c_t - c_v - c_AS - c_BS

    f = [f0, f1, f2, f3, f4, f5, f6]

    return f


t_eval = np.arange(0, W_tot, 0.001)
sol = solve_ivp(PBR_calc_f, [0, W_tot], initial.x_0, args=(Rate, Reactor), method='RK45', t_eval=t_eval)


class plot_results:
    __metaclass__ = Rate
    __metaclass__ = Reactor
    __metaclass__ = sol
    # first plot is of molar flow rates
    plt.figure(1)
    plt.plot(sol.t, sol.y[0], 'r')  # F_A & F_B
    plt.plot(sol.t, sol.y[1], 'g')  # F_A & F_C
    plt.plot(sol.t, sol.y[2])  # F_A & F_C
    plt.show()


# plot results
plot = plot_results()

stop = timeit.default_timer()
print('Time: ', stop - start)
