# -*- coding: utf-8 -*-
"""
Created on Wed May 14 13:05:48 2025

@author: TongtongStudioa
"""

class EconomicHypothesis: 
    """Container for configuration parameters"""
    def __init__(self, investment_return_rate = 0.05, saving_return_rate = 0.025, expense_uncertainty = 0.2, income_uncertainty = 0.05, saving_loss_prob = 0.01, investment_loss_prob = 0.15):
        self.investment_return_rate = investment_return_rate
        self.saving_return_rate = saving_return_rate
        self.expense_uncertainty = expense_uncertainty
        self.income_uncertainty = income_uncertainty
        self.saving_loss_prob = saving_loss_prob
        self.investment_loss_prob = investment_loss_prob
        self.inflation = 0.03
        
        
    def __str__(self):
        string = "\n*** Hypothesis ***"
        string += f"\nTaux retour sur investissement annuel: {self.investment_return_rate * 100}%"
        string += f"\nTaux retour sur épargne annuel: {self.saving_return_rate * 100}%\n"
        return string
    
    