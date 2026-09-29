#Contains all tax functions
import numpy as np
#Phase 4 - Tax systems - calculating net wealth after tax

#global variables to store frozen thresholds
piketty_wealth_threshold_900 = None
piketty_wealth_threshold_990 = None

piketty_income_threshold_900 = None
piketty_income_threshold_990 = None
piketty_income_threshold_999 = None

uk_income_threshold_100 = None
uk_income_threshold_600 = None
uk_income_threshold_900 = None

uk_ni_threshold_100 = None
uk_ni_threshold_800 = None

last_update_year = -1  #keeps track of when thresholds were last updated

def update_thresholds(year, household_array, r):
    # update thresholds every 5 years, otherwise keep them frozen
    global piketty_wealth_threshold_900, piketty_wealth_threshold_990
    global piketty_income_threshold_900, piketty_income_threshold_990, piketty_income_threshold_999
    global uk_income_threshold_100, uk_income_threshold_600, uk_income_threshold_900
    global uk_ni_threshold_100, uk_ni_threshold_800
    global last_update_year

    if last_update_year == -1 or (year - last_update_year) % 5 == 0:
        wealth = household_array[:, 0]
        gross_income = household_array[:, 1] + (r * household_array[:, 0])
        labour = household_array[:, 1]

        # thresholds for Piketty wealth tax
        piketty_wealth_threshold_900 = np.percentile(wealth, 90)
        piketty_wealth_threshold_990 = np.percentile(wealth, 99)

        # thresholds for Piketty income tax
        piketty_income_threshold_900 = np.percentile(gross_income, 90)
        piketty_income_threshold_990 = np.percentile(gross_income, 99)
        piketty_income_threshold_999 = np.percentile(gross_income, 99.9)

        # thresholds for UK income tax
        uk_income_threshold_100 = np.percentile(gross_income, 10)
        uk_income_threshold_600 = np.percentile(gross_income, 60)
        uk_income_threshold_900 = np.percentile(gross_income, 90)

        # thresholds for UK NI tax
        uk_ni_threshold_100 = np.percentile(labour, 10)
        uk_ni_threshold_800 = np.percentile(labour, 80)

        last_update_year = year  # update marker


def no_tax(household_array,r):
    for i in range(len(household_array)):
        household_array[i,0]=household_array[i,0]*(1+r)+household_array[i,1]
        #W(t+1)=W(t)*(1+r)+Y(t)
    return household_array


def piketty_wealth_tax(household_array, year):
    #houses 0-900 pay 0%, 901-990 pay 1% and 991-1000 pay 2% of flat tax of their total wealth
    global piketty_wealth_threshold_900, piketty_wealth_threshold_990

    wealth = household_array[:, 0]

    for i in range(len(household_array)):
        if wealth[i] > piketty_wealth_threshold_990:
            household_array[i, 0] *= 0.98 #pay 2%
        elif wealth[i] > piketty_wealth_threshold_900:
            household_array[i, 0] *= 0.99 #pay 1%
        else:
            pass #pay 0%
    return household_array


def piketty_income_tax(household_array, r, year):
    #0% for bottom 90%, 50% for 90-99%, 60% for 99-99.9%, 70% for 100% of marginal tax of gross income
    global piketty_income_threshold_900, piketty_income_threshold_990, piketty_income_threshold_999

    gross_income = household_array[:, 1] + (r * household_array[:, 0]) #gross income=labour income+capital income

    #applying marginal tax rates
    for i in range(len(household_array)):
        income = gross_income[i]
        tax = 0
        if income > piketty_income_threshold_999:
            tax += 0.7 * (income - piketty_income_threshold_999)
            income = piketty_income_threshold_999
        if income > piketty_income_threshold_990:
            tax += 0.6 * (income - piketty_income_threshold_990)
            income = piketty_income_threshold_990
        if income > piketty_income_threshold_900:
            tax += 0.5 * (income - piketty_income_threshold_900)
        # Bottom 90% pay 0%
        net_income = gross_income[i] - tax
        household_array[i, 0] += net_income

    return household_array


def uk_income_tax(household_array, r, ni_tax, year):
    #0% on first 10%, 20% on next 50%, 40% on next 30%, 45% on the last 10% - on gross income
    global uk_income_threshold_100, uk_income_threshold_600, uk_income_threshold_900

    gross_income = household_array[:, 1] + (r * household_array[:, 0])  # gross income=labour income+capital income

    #applying marginal tax rates
    for i in range(len(household_array)):
        income = gross_income[i]
        tax = 0
        if income > uk_income_threshold_900:
            tax += 0.45 * (income - uk_income_threshold_900)
            income = uk_income_threshold_900
        if income > uk_income_threshold_600:
            tax += 0.4 * (income - uk_income_threshold_600)
            income = uk_income_threshold_600
        if income > uk_income_threshold_100:
            tax += 0.2 * (income - uk_income_threshold_100)
        # Bottom 10% pay 0%
        net_income = gross_income[i] - tax - ni_tax[i]
        household_array[i, 0] += net_income

    return household_array


def uk_ni_tax(household_array, year):
    #0% on first 10%, 8% on next 70% and 2 more% on the last 20% - on LABOUR INCOME ONLY
    global uk_ni_threshold_100, uk_ni_threshold_800

    labour = household_array[:, 1]
    ni_tax = np.zeros(len(household_array))

    #applying marginal tax rates
    for i in range(len(household_array)):
        labour_val = household_array[i, 1]
        tax = 0
        if labour_val > uk_ni_threshold_800:
            tax += 0.02 * (labour_val - uk_ni_threshold_800)
            labour_val = uk_ni_threshold_800
        if labour_val > uk_ni_threshold_100:
            tax += 0.08 * (labour_val - uk_ni_threshold_100)
            labour_val = uk_ni_threshold_100
        #bottom 10% pay nothing

        ni_tax[i] = tax

    return ni_tax
