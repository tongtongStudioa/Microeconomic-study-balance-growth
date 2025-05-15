# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 18:42:09 2025

@author: TongtongStudioa
"""

"""
Todo : 
    ajouter l'inflation
    interet versé le 12eme mois de chaque année et pas par mois
"""

from account_modelisation import BankAccount 
from multiple_simulator import MultipleBalancingSimulator
from hypothesis_class import EconomicHypothesis
from strategy_class import Strategy
import numpy as np

hypothesis = EconomicHypothesis(saving_loss_prob=0.001, investment_return_rate=0.1, investment_loss_prob=0.2)
print(hypothesis)
base_strategy = Strategy()
initial_account = BankAccount(hypothesis, base_strategy, initial_balance=1000, initial_saving=1200, initial_investment=500, monthly_income=2000) 
initial_account.define_expense_ratio(0.8)
print(initial_account)
initial_account.show_hypothesis()

multiple_simu = MultipleBalancingSimulator(hypothesis, initial_account, years_number= 5)
multiple_simu.define_saving_investment_ratios(np.linspace(0,0.4,5), np.linspace(0,0.5,6))

# Run simulations (10 simulations per strategy)
print("Running simulations...")
multiple_simu.run_simulations(num_runs=50)

# Find and display top strategies
top_strategies = multiple_simu.find_optimal_strategies(3, "mean_capital")
print("\nTop 5 Strategies by Mean Final Capital:")
for i, strategy in enumerate(top_strategies, 1):
    print(f"{i}. Saving: {strategy['saving_ratio']:.0%}, Investing: {strategy['investment_ratio']:.0%}")
    print(f"   Mean Capital: ${strategy['mean_capital']:,.2f}")
    print(f"   -> Investments: ${strategy['mean_investments']:,.2f}")
    print(f"   -> Savings : ${strategy['mean_savings']:,.2f}")
    print(f"   -> Cash : ${strategy['mean_av_cash']:,.2f}")
    print(f"   Bankruptcy Rate: {strategy['bankruptcy_rate']:.1%}")
    print(f"   Range: ${strategy['min_capital']/1000:.1f}k - ${strategy['max_capital']/1000:.1f}k\n")

# Visualize results
print("Generating visualizations...")
multiple_simu.plot_3d_results('mean_capital')
multiple_simu.plot_heatmap('median_capital')
print("See above !")
print("Finish !")