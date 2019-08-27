"""
############
Introduction
############
This is the main module of the finanpy library. It contains some basic classes
and functions.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def amortize_month(p,pa,m):
    """
    Calculate the monthly repayment of a loan with fixed interest rate.



    """
    r = pa / 12.
    R = (1 + r) ** m
    c = r * R / (R - 1) * p #Payment
    ci = r * p #Interest Payment
    cp = c - ci #Principal Payment
    debt = p - cp

    return c, cp, ci, debt

def amortize_schedule(p,pa):
    """
    Calculate the monthly repayment schedule of a loan with variable rates. The
    term is fixed, so monthly repayment varies with interest so that debt
    is cleared by end of the term.
    Note: It assumes that there are zero fees.

        Args:
            p (float): Principal
            pa (np.array): p.a. nominal interest rate in decimal.

        Raises:
            Nil

        Returns:
            output (dict) : Contains the following data
                'month' (list): Month
                'c' (list): Monthly Repayment
                'cp' (list): Monthly Principal Payment
                'ci' (list): Monthly Interest Payment
                'debt' (list): Remaining debt
                'ti' (list): Total Interest Paid
    """
    output = dict({'month': [0], 'c': [0], 'cp': [0], 'ci': [0], 'debt':[p], 'ti': [0]})
    tot_m = 12 * len(pa)
    m = 0 #current month
    for r_ind, r in enumerate(pa):
        for i in range(12):
            rm = tot_m - m #Remaining Months
            m += 1
            dat = amortize_month(output['debt'][-1], r, rm) #c, cp, ci, debt
            output['month'].append(m)
            output['c'].append(dat[0])
            output['cp'].append(dat[1])
            output['ci'].append(dat[2])
            output['debt'].append(dat[3])
            output['ti'].append(output['ti'][-1] + dat[2])

    return output

def save_series(c, pa, y=np.NaN):
    """
    Function calculates the total amount of savings for a monthly contribution
    of c, with interests rate over the years as pa.

        Args:
            c (float/int or np.array): principal contribution.
            pa (float/int or np.array): p.a. nominal interest rates in decimal.
            y (int, optional): number of years

        Raises:
            Nil

        Returns:
            s (float): Accumulated/compounded Savings
    """
    if not(isinstance(pa, int) or isinstance(pa, float)):
        y = len(pa)
    elif (isinstance(pa, int) or isinstance(pa, float)):
        pa = np.ones(y) * pa

    if (isinstance(c, int) or isinstance(c, float)):
        c = np.ones(y * 12) * c


    s = [0] # Savings
    m = [0] # Month
    assert len(c) == len(pa)*12, "len(c) should be a multiple of 12"

    for r_ind, r in enumerate(pa):
        for i in range(12):
            s.append(s[-1] * (1 + r / 12) + c[m[-1]])
            m.append(m[-1]+1)

    return s

def mortgage_invest(p, ms, Rr, Hr, Y1, Y2):
    """
    Function calculates the difference in savings between a lower monthly
    mortgage repayment vs a high mortgage repayment. Y1 and Y2 are the
    repayment periods, with Y1 being the shorter one. Once the mortgage is
    repaid in Y1, the full monthly salary will be allocated to savings instead.

        Args:
            p  (float): principal
            ms (float): monthly salary
            Rr (float): low risk savings annual interest
            Hr (float): home loan interest rate
            Y1 (int): Number of years on shorter loan
            Y2 (int): Number of years on longer loan

        Raises:
            Nil

        Returns:
            S1 (float): Accumulated/compounded Savings for Y1
            S2 (float): Accumulated/compounded Savings for Y2
    """

    # %%
    pa1 = np.zeros(Y1) + Hr
    spa1 = np.ones(Y2) * Rr # Savings interest rate
    output1 = amortize_schedule(p, pa1) #month, c, cp, ci, debt, ti
    msav1 = ms - np.array(output1['c'][1:])
    msav1 = np.append(msav1, np.ones((Y2 - Y1) * 12) * ms)
    assert sum(msav1 < 0)==0, 'Error: Monthly saving > Monthly Mortage payment'
    S1 = save_series(msav1, spa1)

    # %%
    pa2 = np.zeros(Y2) + Hr
    spa2 = np.ones(Y2) * Rr # Savings interest rate
    output2 = amortize_schedule(p, pa2) #month, c, cp, ci, debt, ti
    msav2 = ms - np.array(output2['c'][1:])
    S2 = save_series(msav2, spa2)
    return S1, S2

def homevsrent(Y, p, REr, rent, inflation, Rr, fc):
    """
    Function calculates the difference in savings between renting and buying a
    house. Rent is subjected to inflation i.e. it increases over time. Home loan
    rate set at 0.026 (HDB Loan rate).

        Args:
            Y  (float): loan length
            p  (float): principal
            Rer (float): home appreciation
            rent (float): monthly rent
            inflation (float): inflation on rent
            Rr (float): Low Risk Investment Interest Rate
            fc (float): Fixed cost based on a percentage of principal

        Raises:
            Nil

        Returns:
            Profit (np.array): Profit from selling a home - cost
            Savings (np.array): Savings over time
    """
    # Annual interest rates for Y number of years
    pa = np.zeros(Y) + 0.026  # This is the rate for a HDB Loan
    output = amortize_schedule(p, pa)  # Month, c, cp, ci, debt, ti
    Ti = output['ti']  # Total Interest over time
    Tpp = np.cumsum(output['cp'])  # Total Principal Paid

    # Calculating Home Savings
    Hp = [p*(1+REr/12)**y for y in range(Y*12+1)]  # House price
    Hs = np.array(Hp) - fc*p - output['debt'] # Home savings

    # Calculating Rental Savings
    rr = [rent*(1+inflation/12)**y for y in range(Y*12)] # real rent
    Rs = save_series((np.array(output['c'][1:]) - rr), Rr, Y)

    # Plot Profit and Savings
    plt.figure()
    plt.subplot(221)
    plt.ion()
    plt.plot(range((Y*12+1)), Hs, label='Home Savings')
    plt.plot(range((Y*12+1)), Rs, label='Rental Savings')
    plt.xlabel('month')
    plt.ylabel('savings ($)')
    plt.title('Assets over time')
    plt.legend()
    plt.grid()


    # Plot rent vs interest payment
    plt.subplot(222)
    plt.plot(range(Y*12), output['ci'][1:], label='Interest')
    plt.plot(range(Y*12), rr, label='Rent')
    plt.xlabel('month')
    plt.ylabel('savings ($)')
    plt.title('Monthly fixed costs')
    plt.legend()
    plt.grid()


    # Plot rent vs interest payment
    plt.subplot(224)
    plt.plot(range(Y*12), np.cumsum(output['ci'][1:]), label='Interest')
    plt.plot(range(Y*12), np.cumsum(rr), label='Rent')
    plt.xlabel('month')
    plt.ylabel('savings ($)')
    plt.title('Cumulative fixed costs')
    plt.legend()
    plt.grid()







class portfolio:
    """
    Portfolio is created to manage your portfolio with ease. It lets you define
    various future earnings, investment decisions to calculate your
    assets, liabilities, risk, liquidity, cash flow over time and more.
    Each portfolio will map out a unique time series that can be compared
    with other portfolios to maximize returns and minimize risk over time.

    The code architecture behaves as follow:
        Define risk-free interest over time

    """

    def __init__():
        pass

    def earnings():
        pass

def refinance():

    pass
