# -*- coding: utf-8 -*-
"""
Created on Wed May 14 13:26:45 2025

@author: Axel
"""

class Strategy:
    
    def __init__(self, saving_ratio = 0.2, investment_ratio = 0.1):
        self.saving_ratio = saving_ratio
        self.investment_ratio = investment_ratio
        if (saving_ratio + investment_ratio >= 1):
            print("*** Attention ! ***\nL'addition des ratios est plus grand que 1 !")