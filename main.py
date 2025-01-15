# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 18:42:09 2025

@author: La famille tong
"""

from account_modilzation_balance import BankAccount 

account1 = BankAccount(15000,10000,10000,monthly_income=3000)
print(account1)
account1.init_manual_parameters()
account1.how_long_to_be_rich(wealth_goal=30000000)
print(account1)