import numpy as np
import taxes,graphs

#Phase 1 - Constants
population=1000
wealth_total=1_000_000
years=100
r=0.043
wealth_min=1
wealth_floor=0

#Phase 2 - Initial Wealth Generation
rng_wealth=np.random.default_rng(1) #same seed for consistency
raw_wealth=rng_wealth.pareto(1.1126449, population)+1 #+1 so no one has wealth of 0
#trial and error with alpha till top 10% of wealth=72% of the wealth to replicate the UK's wealth distribution
scaled_wealth=raw_wealth/np.sum(raw_wealth) * wealth_total
initial_wealth=np.sort(scaled_wealth)

#checks for alpha (top 10% has 72% of wealth)
#print(round(0.72*np.sum(initial_wealth),2))
#print(round(np.sum(initial_wealth[-100:]),2))


#Phase 3 - Assigning Labour Income
rng_labour=np.random.default_rng(2) #same seed for consistency
raw_labour=rng_labour.lognormal(0,0.5,population) #The variance (sigma = 0.5) was chosen to produce a moderate spread: most households earn near the average, while a few earn higher wages, mimicking real-world wage inequality in the UK
total_labour_target = 86_000
scaled_labour = raw_labour/ np.sum(raw_labour) * total_labour_target
labour=np.sort(scaled_labour)
labour=np.round(labour,2)

households=np.column_stack((initial_wealth,labour))

# Phase 5 - Annual Wealth Update Loop
households_piketty = households.copy()
households_uk = households.copy()

# arrays of the distribution of wealth over time
wealth_piketty = np.zeros((years+1, population)) #2D array: rows=years+1, columns=population
wealth_uk = np.zeros((years+1, population))

# initial wealth
wealth_piketty[0] = households_piketty[:, 0]
wealth_uk[0] = households_uk[:, 0]

for year in range(1, years+1):
    # update thresholds every 5 years (or use last frozen thresholds)
    taxes.update_thresholds(year, households_piketty, r)  # thresholds are frozen for 5-year periods

    #PIKETTY TAX
    households_piketty = taxes.piketty_wealth_tax(taxes.piketty_income_tax(households_piketty, r, year), year)
    households_piketty[:, 0] = np.maximum(households_piketty[:, 0], wealth_floor)
    wealth_piketty[year] = households_piketty[:, 0]

    #UK TAX
    ni_tax = taxes.uk_ni_tax(households_uk, year)
    households_uk = taxes.uk_income_tax(households_uk, r, ni_tax, year)
    households_uk[:, 0] = np.maximum(households_uk[:, 0], wealth_floor)
    wealth_uk[year] = households_uk[:, 0]

#Phase 7 - Plotting and Visualisation

#calculating all the gini coefficients per year of the tax systems
gini_piketty=graphs.find_gini_coefficient(wealth_piketty)
gini_uk=graphs.find_gini_coefficient(wealth_uk)

#plotting gini coefficient against years now
graphs.plot_gini(gini_piketty, gini_uk)

#calculating lorenz curve calculations (cumulative population/cumulative income)
lorenz_piketty=graphs.find_lorenz_curve(wealth_piketty)
lorenz_uk=graphs.find_lorenz_curve(wealth_uk)

#plotting lorenz curves now
graphs.plot_lorenz_curve(lorenz_piketty[0],lorenz_piketty[1], lorenz_uk[1]) #parameters should be lorenz_pikettey_0, lorenz_piketty_100, lorenz_uk_100
#index 0 of lorenz_piketty is initial lorenz curve values for all tax systems

#calculating percentile wealth shares for 10%
percentile10_piketty=graphs.find_percentile_wealth_shares_10(wealth_piketty)
percentile10_uk=graphs.find_percentile_wealth_shares_10(wealth_uk)

#plotting bar chart for top 10% wealth share
graphs.plot_bar_chart_top10(percentile10_piketty, percentile10_uk)