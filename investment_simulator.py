# -*- coding: utf-8 -*-
"""
Created on Sun May 11 13:55:13 2025

@author: Axel
"""

import numpy as np
import pandas as pd
from itertools import product
from collections import defaultdict

class InvestmentSimulator:
    def __init__(self, initial_capital=10000, years=20, inflation_rate=0.02):
        """
        Initialize the investment simulator with basic parameters.
        
        Args:
            initial_capital (float): Starting amount of money
            years (int): Number of years to simulate
            inflation_rate (float): Annual inflation rate
        """
        self.initial_capital = initial_capital
        self.years = years
        self.inflation_rate = inflation_rate
        self.strategies = []
        self.results = []
        
    def add_strategy(self, name, savings_rate, investment_allocation, annual_fees=0.005):
        """
        Add an investment strategy to consider.
        
        Args:
            name (str): Name of the strategy
            savings_rate (float): Percentage of salary saved annually (0-1)
            investment_allocation (dict): Allocation to different asset classes (must sum to 1)
                                          Example: {'stocks': 0.7, 'bonds': 0.3}
            annual_fees (float): Annual management fees (0-1)
        """
        if abs(sum(investment_allocation.values()) - 1.0) > 0.01:
            raise ValueError("Investment allocations must sum to 1.0")
            
        self.strategies.append({
            'name': name,
            'savings_rate': savings_rate,
            'allocation': investment_allocation,
            'fees': annual_fees
        })
    
    def generate_default_strategies(self, salary_growth=0.03, initial_salary=50000):
        """
        Generate a set of common default strategies to test.
        """
        # Common asset classes with their expected returns and volatility
        asset_classes = {
            'stocks': {'return': 0.07, 'volatility': 0.15},
            'bonds': {'return': 0.03, 'volatility': 0.05},
            'real_estate': {'return': 0.05, 'volatility': 0.10},
            'cash': {'return': 0.01, 'volatility': 0.01}
        }
        
        # Generate common allocation strategies
        allocations = [
            {'name': 'Aggressive', 'stocks': 0.9, 'bonds': 0.1},
            {'name': 'Moderate', 'stocks': 0.7, 'bonds': 0.3},
            {'name': 'Conservative', 'stocks': 0.5, 'bonds': 0.5},
            {'name': 'Balanced', 'stocks': 0.6, 'bonds': 0.3, 'real_estate': 0.1},
            {'name': 'Real Estate Heavy', 'stocks': 0.4, 'real_estate': 0.5, 'bonds': 0.1},
            {'name': 'All Stocks', 'stocks': 1.0},
            {'name': 'All Bonds', 'bonds': 1.0},
            {'name': 'Retirement Mix', 'stocks': 0.5, 'bonds': 0.4, 'cash': 0.1}
        ]
        
        # Savings rates to test
        savings_rates = [0.1, 0.15, 0.2, 0.25, 0.3]
        
        # Generate all combinations
        for alloc in allocations:
            for rate in savings_rates:
                name = f"{alloc['name']} - {int(rate*100)}% Savings"
                self.add_strategy(
                    name=name,
                    savings_rate=rate,
                    investment_allocation={k: v for k, v in alloc.items() if k != 'name'},
                    annual_fees=0.005
                )
    
    def simulate_strategy(self, strategy, salary_growth=0.03, initial_salary=50000):
        """
        Simulate a single strategy over time with random market returns.
        
        Returns:
            dict: Final capital and annual details
        """
        capital = self.initial_capital
        salary = initial_salary
        annual_details = []
        
        asset_classes = {
            'stocks': {'return': 0.07, 'volatility': 0.15},
            'bonds': {'return': 0.03, 'volatility': 0.05},
            'real_estate': {'return': 0.05, 'volatility': 0.10},
            'cash': {'return': 0.01, 'volatility': 0.01}
        }
        
        for year in range(1, self.years + 1):
            # Calculate annual savings
            savings = salary * strategy['savings_rate']
            
            # Calculate investment returns for each asset class
            total_return = 0
            for asset, allocation in strategy['allocation'].items():
                if asset in asset_classes:
                    # Random return based on normal distribution
                    annual_return = np.random.normal(
                        asset_classes[asset]['return'],
                        asset_classes[asset]['volatility']
                    )
                    total_return += allocation * annual_return
            
            # Apply fees
            total_return -= strategy['fees']
            
            # Apply inflation adjustment to returns
            real_return = (1 + total_return) / (1 + self.inflation_rate) - 1
            
            # Update capital
            capital = capital * (1 + real_return) + savings
            
            # Salary growth
            salary *= (1 + salary_growth)
            
            # Record annual details
            annual_details.append({
                'year': year,
                'capital': capital,
                'salary': salary,
                'savings': savings,
                'return': total_return,
                'real_return': real_return
            })
        
        return {
            'strategy': strategy['name'],
            'final_capital': capital,
            'annual_details': annual_details
        }
    
    def run_simulations(self, num_runs=1000, salary_growth=0.03, initial_salary=50000):
        """
        Run Monte Carlo simulations for all strategies.
        
        Args:
            num_runs (int): Number of simulations to run for each strategy
            salary_growth (float): Expected annual salary growth rate
            initial_salary (float): Starting salary
        """
        self.results = []
        
        for strategy in self.strategies:
            print(f"Simulating strategy: {strategy['name']}")
            final_capitals = []
            
            for _ in range(num_runs):
                result = self.simulate_strategy(strategy, salary_growth, initial_salary)
                final_capitals.append(result['final_capital'])
            
            # Store aggregate results
            self.results.append({
                'strategy': strategy['name'],
                'savings_rate': strategy['savings_rate'],
                'allocation': strategy['allocation'],
                'median_capital': np.median(final_capitals),
                'mean_capital': np.mean(final_capitals),
                'min_capital': np.min(final_capitals),
                'max_capital': np.max(final_capitals),
                'std_capital': np.std(final_capitals),
                'all_simulations': final_capitals
            })
    
    def get_top_strategies(self, n=10, metric='median_capital'):
        """
        Get the top n strategies based on the specified metric.
        
        Args:
            n (int): Number of top strategies to return
            metric (str): Metric to sort by ('median_capital', 'mean_capital', etc.)
            
        Returns:
            list: Sorted list of top strategies
        """
        if not self.results:
            raise ValueError("No simulation results available. Run simulations first.")
            
        # Sort strategies by the selected metric
        sorted_results = sorted(self.results, key=lambda x: x[metric], reverse=True)
        
        return sorted_results[:n]
    
    def plot_strategy_results(self, top_strategies=None):
        """
        Plot the results of the top strategies.
        Requires matplotlib to be installed.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Matplotlib is required for plotting. Please install it first.")
            return
        
        if top_strategies is None:
            top_strategies = self.get_top_strategies()
        
        plt.figure(figsize=(12, 8))
        
        for result in top_strategies:
            # Plot distribution of final capitals
            plt.hist(
                result['all_simulations'],
                bins=30,
                alpha=0.5,
                label=f"{result['strategy']} (Median: ${result['median_capital']/1000:.1f}k)"
            )
        
        plt.title('Distribution of Final Capital for Top Strategies')
        plt.xlabel('Final Capital ($)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)
        plt.show()

# Example usage
if __name__ == "__main__":
    # Create simulator
    simulator = InvestmentSimulator(initial_capital=10000, years=5, inflation_rate=0.02)
    
    # Generate default strategies
    simulator.generate_default_strategies()
    
    # Add some custom strategies
    simulator.add_strategy(
        name="Tech Heavy - 20% Savings",
        savings_rate=0.2,
        investment_allocation={'stocks': 0.8, 'bonds': 0.1, 'real_estate': 0.1},
        annual_fees=0.005
    )
    
    simulator.add_strategy(
        name="Safe Growth - 25% Savings",
        savings_rate=0.25,
        investment_allocation={'stocks': 0.6, 'bonds': 0.3, 'cash': 0.1},
        annual_fees=0.003
    )
    
    # Run simulations
    print("Running simulations...")
    simulator.run_simulations(num_runs=1000)
    
    # Get top 10 strategies
    top_strategies = simulator.get_top_strategies(n=3)
    
    # Display results
    print("\nTop 10 Strategies by Median Final Capital:")
    print("-" * 70)
    for i, strategy in enumerate(top_strategies, 1):
        print(f"{i}. {strategy['strategy']}")
        print(f"   Savings Rate: {strategy['savings_rate']*100:.0f}%")
        print(f"   Allocation: {strategy['allocation']}")
        print(f"   Median Final Capital: ${strategy['median_capital']:,.2f}")
        print(f"   Range: ${strategy['min_capital']/1000:.1f}k - ${strategy['max_capital']/1000:.1f}k")
        print("-" * 70)
    
    # Plot results
    simulator.plot_strategy_results()