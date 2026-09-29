

Readme · MD
Wealth Inequality Simulation
📖 Read the full write-up on Medium: [link]

Overview
An independent research problem using a Monte Carlo simulation to model how different tax systems affect wealth inequality and distribution over time. The simulation tracks 1000 households over a century under three tax regimes - UK's current system, no tax, Piketty-style progressive wealth tax - to compare long-term distributional outcomes. 

Methodology
Population modelling: Household wealth and income are generated using Pareto and lognormal distributions, chosen to reflect the real-world skew of wealth concentration (a small number of households holding a disproportionate share of total wealth).
Simulation engine: A Monte Carlo approach runs the model across many iterations to account for randomness in income growth, investment returns, and other variables, producing a distribution of plausible outcomes rather than a single deterministic result.
Inequality measurement: Results are evaluated using Lorenz curves (visualising the gap between actual and perfectly equal wealth distribution) and Gini coefficients (a single summary statistic of inequality, from 0 = perfect equality to 1 = maximum inequality).

Key Findings
Over a simulated 100-year period, Piketty's progressive income and wealth tax system reduced wealth concentration far more effectively than the current UK system. The top 10%'s share of total wealth started at 72% (matching real UK data) and fell to around 20% under the UK system, but dropped much further to roughly 11.25% under Piketty's system. This was reflected in both the Gini coefficient (which stayed far lower under Piketty's system) and the Lorenz curve, which sat much closer to the line of perfect equality.

To sense-check these results, I compared them against a Tax Foundation macroeconomic analysis of the same Piketty proposal (using a dynamic scoring model of the wider US economy). That report found the wealth tax could shrink capital stock, GDP, and employment, and that dynamic revenue losses could significantly undercut the static tax take — suggesting that while a wealth tax can flatten wealth distribution, it may come with real economic trade-offs that a purely distributional (household-level) simulation like mine doesn't capture.

Context
Findings were compared against real-world data from the Tax Foundation and the LSE Spatial Inequality Report, to sense-check the model against existing macroeconomic research on inequality and tax policy.

How to Run
Clone the repository and install the required dependencies (see below).
Run the simulation:
   python main.py
   
The script generates a series of interactive graphs one at a time. Each graph supports zooming and panning to explore the data more closely.
Close the current graph window to move on to the next one in the sequence.

Project Structure
main.py — runs the simulation: generates the initial population, applies each tax system year by year, and calls the plotting functions
taxes.py — implements the UK and Piketty-style tax systems (income tax, National Insurance, wealth tax), with thresholds recalculated every 5 years
graphs.py — computes inequality metrics (Gini coefficient, Lorenz curve, top 10% wealth share) and plots them
test_values.py — sample output values for a 10-household, 1-year test run, used to sanity-check the model

Tools Used
Python · NumPy · Matplotlib · QuantEcon 


