# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 18:42:09 2025

@author: La famille tong
"""

from account_modilzation_balance import BankAccount 

account1 = BankAccount()
print(account1)
account1.n_months_simulations(12*5)
account1.show_simulations_infos(False,0.025, 0.05)
account1.show_graph(12*5)