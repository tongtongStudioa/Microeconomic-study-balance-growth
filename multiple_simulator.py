# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 18:47:14 2025

@author: TongtongStudioa
"""

from account_modelisation import BankAccount
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from strategy_class import Strategy

class MultipleBalancingSimulator:
    """Simulates multiple strategies to find optimal saving/investment ratios"""
    def __init__(self,hypothesis, initial_bank_account, years_number = 5):
        self.years = years_number
        self.months_n = years_number * 12
        self.saving_ratios = np.linspace(0,0.4,4)
        self.investment_ratios = np.linspace(0,0.5,5)
        self.initial_bank_account = initial_bank_account
        self.strategies = []
        self.results = []
        
        
    def define_saving_investment_ratios(self, saving_ratios, investment_ratios):
        self.saving_ratios = saving_ratios
        self.investment_ratios = investment_ratios
        
    def add_strategy(self, savings_rate, investment_rate):
        """
        Add an investment strategy to consider.
        
        Args:
            name (str): Name of the strategy
            savings_rate (float): Percentage of salary saved annually (0-1)
            investment_rate (float): Percentage of salary invest annually (0-1) (better return rate but greater volatility)
        """
        
        if investment_rate + savings_rate > 1:
            raise ValueError("Investment allocations must sum to 1.0")
            
        self.strategies.append(Strategy(savings_rate,investment_rate))
    
    def generate_strategies(self):
        """
        Generate a set of strategies.
        """
        
        # Generate all combinations
        for s_rate in self.saving_ratios:
            for i_rate in self.investment_ratios:
                self.add_strategy(
                    savings_rate = s_rate,
                    investment_rate = i_rate
                )
                
    def run_simulations(self, num_runs = 20):
        """Run Monte Carlo simulations for all strategies"""
        self.generate_strategies()
        self.simulations_list = []
        #todo : tests multiple scenarios to compare investment ratio and saving ratio 
        id_simulation = 0
        for new_strategy in self.strategies:
            bank_account = self.initial_bank_account
            bank_account.strategy = new_strategy
            final_capitals = []
            bankruptcies = 0
            
            for _ in range(num_runs):
                bank_account.reset_account()
                result = bank_account.simulate_for_years(self.years)
                final_capitals.append(result['capital'])
                bankruptcies += result['bankruptcy']
                
                if (bank_account.bankruptcy):
                    continue
            self.results.append(
                        {"id" : id_simulation,
                        "saving_ratio" : new_strategy.saving_ratio,
                        "investment_ratio" : new_strategy.investment_ratio,
                        'median_capital': np.median(final_capitals),
                        'mean_capital': np.mean(final_capitals),
                        'min_capital': np.min(final_capitals),
                        'max_capital': np.max(final_capitals),
                        'std_capital': np.std(final_capitals),
                        'mean_investments': np.mean(result["total_investments"]),
                        'mean_savings': np.mean(result["total_savings"]),
                        'mean_av_cash': np.mean(result["available_cash"]),
                        'bankruptcy_rate': bankruptcies / num_runs})
    
    def find_optimal_strategies(self, n: int = 5, metric: str = 'median_capital'):
        """Find top n strategies based on selected metric"""
        sorted_results = sorted(self.results, key=lambda x: x[metric], reverse=True)
        return sorted_results[:n]
    
    def show_graph(self):
        
        fig = plt.figure(figsize=(10, 15))
        axes = fig.add_subplot(projection='3d')
        for simulation in self.simulations_list:
            axes.scatter(
                simulation["investment_ratio"],
                simulation["saving_ratio"],
                simulation["final_capital"],
                c=simulation["id"],  # Couleur différente par point
                cmap='viridis',
                s=100,  # Taille des points
                alpha=0.7
                )
    
        axes.set_xlabel("Taux d'investissement (%)", labelpad=15)
        axes.set_ylabel("Taux d'épargne (%)", labelpad=15)
        axes.set_zlabel("Capital (€)", labelpad=15)
    
        plt.title("Simulations de stratégies d'enrichissement : richesse au bout de 5 ans")
        plt.show()
        
    def plot_3d_results(self, metric: str = 'median_capital'):
        """Create 3D visualization of strategy performance"""
        if not self.results:
            raise ValueError("No results to plot. Run simulations first.")
            
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Prepare data
        x = [r['saving_ratio'] for r in self.results]
        y = [r['investment_ratio'] for r in self.results]
        z = [r[metric] for r in self.results]
        
        # Create surface plot
        ax.scatter(x, y, z, c=z, cmap='viridis', s=50)
        
        # Highlight top strategies
        top_strategies = self.find_optimal_strategies(3, metric)
        for strategy in top_strategies:
            ax.scatter(
                strategy['saving_ratio'], 
                strategy['investment_ratio'], 
                strategy[metric],
                color='red', s=200, marker='*'
            )
        
        # Labels and title
        ax.set_xlabel('Saving Ratio')
        ax.set_ylabel('Investment Ratio')
        ax.set_zlabel(metric.replace('_', ' ').title())
        ax.set_title(f'Strategy Performance by {metric.replace("_", " ").title()}')
        
        plt.tight_layout()
        plt.show()
    
    def plot_heatmap(self, metric: str = 'median_capital'):
        """Create 2D heatmap of strategy performance"""
        if not self.results:
            raise ValueError("No results to plot. Run simulations first.")
            
        # Create pivot table for heatmap
        df = pd.DataFrame(self.results)
        pivot = df.pivot(index='saving_ratio', columns='investment_ratio', values=metric)
        
        plt.figure(figsize=(12, 8))
        plt.imshow(pivot, cmap='viridis', aspect='auto', origin='lower')
        plt.colorbar(label=metric.replace('_', ' ').title())
        
        # Annotations
        for i in range(len(pivot.index)):
            for j in range(len(pivot.columns)):
                plt.text(j, i, f"{pivot.iloc[i, j]/1000:.1f}k",
                        ha="center", va="center", color="w")
        
        # Labels
        plt.xticks(range(len(pivot.columns)), pivot.columns.round(2))
        plt.yticks(range(len(pivot.index)), pivot.index.round(2))
        plt.xlabel('Investment Ratio')
        plt.ylabel('Saving Ratio')
        plt.title(f'Strategy Performance Heatmap ({metric.replace("_", " ").title()})')
        
        plt.tight_layout()
        plt.show()