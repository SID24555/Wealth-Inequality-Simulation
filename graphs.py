#Functions for plotting Lorenz curves, Gini coefficients, wealth histograms, and line plots
import matplotlib.pyplot as plt
import numpy as np
from quantecon import gini_coefficient, lorenz_curve

#Phase 6 - Compute Inequality Metrics
def find_gini_coefficient(wealth_array):
    gini_array = np.zeros(len(wealth_array))
    for i in range(len(wealth_array)):
        gini_array[i] = gini_coefficient(wealth_array[i, :])

    return gini_array

def find_lorenz_curve(wealth_array):
    lorenz_curve_0 = lorenz_curve(wealth_array[0, :])
    lorenz_curve_100 = lorenz_curve(wealth_array[-1, :])

    return lorenz_curve_0, lorenz_curve_100
    #lorenz curve functions returns a 2D array of cumulative population and the cumulative income for Year 0 and 100

def find_percentile_wealth_shares_10(wealth_array): #wealth of the top 10% at Year 0 compared to Year 100
    #Year 0
    wealth_yr0 = wealth_array[0]  #all wealth of all households in yr0
    total_wealth_yr0 = np.sum(wealth_yr0)

    top10_threshold_yr0 = np.percentile(np.sort(wealth_yr0), 90)  # top 10%
    top10_array_yr0 = []
    for i in wealth_yr0:
        if i >= top10_threshold_yr0:
            top10_array_yr0.append(i)
    top10_wealth_yr0 = np.sum(top10_array_yr0)
    top10_share_yr0 = (top10_wealth_yr0 / total_wealth_yr0) * 100

    #Year 100
    wealth_yr100 = wealth_array[-1]  #final wealth of all households in yr100
    total_wealth_yr100 = np.sum(wealth_yr100)

    top10_threshold_yr100 = np.percentile(np.sort(wealth_yr100), 90)
    top10_array_yr100 = []
    for i in wealth_yr100:
        if i >= top10_threshold_yr100:
            top10_array_yr100.append(i)
    top10_wealth_yr100 = np.sum(top10_array_yr100)
    top10_share_yr100 = (top10_wealth_yr100 / total_wealth_yr100) * 100

    return top10_share_yr0, top10_share_yr100


#Phase 7 - Plotting and Visualisation
def plot_gini(gini_piketty, gini_uk): #Gini coefficient over time - parameter will be gini arrays of all 3 tax systems
    years = np.arange(0, len(gini_piketty))
    plt.plot(years, gini_piketty, label='Piketty Tax Proposal', color='green')
    plt.plot(years, gini_uk, label='UK Tax Proposal', color='red')
    plt.xlabel('Year')
    plt.ylabel('Gini coefficient')
    plt.title('Gini coefficient over time')
    plt.grid(True) #adds grid lines
    plt.legend() #adds key for the 3 types of taxes
    plt.show() #displays the plot


def plot_lorenz_curve(lorenz_piketty_0, lorenz_piketty_100, lorenz_uk_100): #Lorenz curve
    #parameters are the lorenz curve values for all 3 tax systems
    #only need year 0 once as it would be same for all
    plt.plot([0, 1], [0, 1], label='Line of Equality', color='black', linewidth=2, zorder=5)
    #the line of equality is just a straight 45° line from (0,0) to (1,1) that shows perfect equality (everyone has exact wealth)

    #initial
    cumulative_pop0 = lorenz_piketty_0[0]
    cumulative_income0 = lorenz_piketty_0[1]
    plt.plot(cumulative_pop0, cumulative_income0, label='Initial Curve', color='blue', alpha=0.9)

    #pikettey tax system
    cumulative_pop100 = lorenz_piketty_100[0]
    cumulative_income100 = lorenz_piketty_100[1]
    plt.plot(cumulative_pop100, cumulative_income100, label='Piketty Tax Year 100', color='green', alpha=0.9)

    #uk tax system
    cumulative_pop100 = lorenz_uk_100[0]
    cumulative_income100 = lorenz_uk_100[1]
    plt.plot(cumulative_pop100, cumulative_income100, label='UK Tax Year 100', color='red', alpha=0.9)

    plt.xlabel('Cumulative Population')
    plt.ylabel('Cumulative Income')
    plt.title('Lorenz Curve Comparison Across Tax Systems Over 100 Years')
    plt.tight_layout()
    plt.legend()
    plt.show()


def plot_bar_chart_top10(wealth_piketty_tax, wealth_UK_tax):
    labels = ['Piketty Tax Proposal', 'UK Tax Proposal']
    colours = ['Green', 'Red']

    values_yr0 = [wealth_piketty_tax[0], wealth_UK_tax[0]]
    plt.bar(labels, values_yr0, width=0.5, color=colours)  # bar parameters are labels of bar and heights
    plt.xlabel('Tax Systems')
    plt.ylabel('Top 10% Wealth Share (%) at Year 0')
    plt.show()

    values_yr100 = [wealth_piketty_tax[1], wealth_UK_tax[1]]
    plt.bar(labels, values_yr100, width=0.5, color=colours)
    plt.xlabel('Tax Systems')
    plt.ylabel('Top 10% Wealth Share (%) at Year 100')
    plt.show()











