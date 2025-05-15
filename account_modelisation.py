# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 13:54:14 2025

@author: TongtongStudioa
"""

import numpy as np
from numpy.random import choice
import matplotlib.pyplot as plt

#Constantes 
months = ["January","February","March","April","May","June","July","August","September","October","November", "December"]


class BankAccount:
    """ Create life bank account for particular personn with all parameters you want."""
    
    def __init__(self, hypothesis, strategy, initial_balance = 1500,initial_saving = 2250, initial_investment = 1100,monthly_income = 2500):
        self.initial_balance = initial_balance
        self.initial_saving = initial_saving
        self.initial_investment = initial_investment
        self.monthly_income = monthly_income
        self.initial_capital = self.initial_balance + self.initial_investment + self.initial_saving
        self.hypothesis = hypothesis
        
        # Parameters to play with
        self.monthly_expenses_ratio = 0.85
        self.monthly_expenses = self.monthly_expenses_ratio * self.monthly_income   # Dépenses fixes mensuelles ($)
        self.strategy = strategy
        
        self.bankruptcy = False
        self._init_bank_account()
    
    def _init_bank_account(self):
        """Initialize with parameters"""
        self.balances = [self.initial_balance]  # Liste pour stocker le solde à chaque mois
        self.income_history = [self.monthly_income]           # Historique des revenus mensuels
        self.expense_history = [self.monthly_expenses]          # Historique des dépenses mensuelles
        self.investments = [self.initial_investment]            # Historique des investissements 
        self.savings = [self.initial_saving]               # Historique de l'épargne mensuel 
        
        self.total_investments = self.investments[-1]
        self.total_savings = self.savings[-1]
        self.capital = self.initial_capital
        self.capital_history = [self.capital]
        self.wealthy_financial_assets = -1
        
    def reset_account(self):
        """Reset all account history and state"""
        self.balances = [self.initial_balance]
        self.income_history = [self.monthly_income]
        self.expense_history = [self.monthly_expenses_ratio * self.monthly_income]
        self.investments = [self.initial_investment]
        self.savings = [self.initial_saving]
        
        self.total_investments = self.investments[-1]
        self.total_savings = self.savings[-1]
        self.capital = self.total_investments + self.total_savings + self.balances[-1]
        self.capital_history = [self.capital]
        self.bankruptcy = False
        self.wealthy_financial_assets = -1
        
    def define_expense_ratio(self, monthly_expenses_ratio):
        """ Define monthly expense ratio. Between 0 and 1. (float) """
        monthly_expenses = monthly_expenses_ratio *self.monthly_income   # Dépenses fixes mensuelles ($)
        self.monthly_expenses_ratio = monthly_expenses_ratio
        self.monthly_expenses = monthly_expenses
        
    def __str__(self):
        # Afficher le captial total
        infos = f">>> Capital financier : {self.capital:.1f} $ <<<\n"
        infos += f"-> Investissement(tout types) : {self.total_investments:.1f} $  ({(self.total_investments/self.capital * 100):.1f}%)\n"
        infos += f"-> Epargne : {self.total_savings:.1f} $  ({(self.total_savings/self.capital * 100):.1f}%)\n"
        infos += f"-> Cash disponible : {self.balances[-1]:.1f} $\n"
        return infos
        
    def simulate_for_years(self,years):
        """Simulate account activity and return results"""
        months_n = years * 12
        for i in range(months_n):
            self.month_simulation(i)
            if (self.bankruptcy):
                break
        return {
            "capital": self.capital,
            "total_investments": self.total_investments,
            "total_savings": self.total_savings,
            "available_cash": self.balances[-1],
            "bankruptcy": self.bankruptcy,
            "capital_history": self.capital_history.copy()
        } 
    
    def month_simulation(self,i):
        """Core monthly simulation logic"""
        #print(i)
        #if i%12 == 0:
         #   print()
         #   print(f"Year {i/12+1}")
        #print()
        #print(f"{months[int(i%12)]}")
        # Apply random variations to income and expenses
        income = self._apply_variation(
            self.monthly_income, 
            self.hypothesis.income_uncertainty
        )
        expense = self._apply_variation(
            self.monthly_expenses, 
            self.hypothesis.expense_uncertainty
        )
        
        #print(f"Income before returns : {income} $")
        #print(f"Expenses : {expense} $")
        # Add investment and savings returns from previous periods
        income += self._calculate_returns(i)
        
        # Update balance
        new_balance = self.balances[-1] + income - expense
        #print(f"Balance : {new_balance}$")
        
        # Handle negative balance (potential bankruptcy)
        new_balance = self._handle_negative_balance(new_balance)
        if self.bankruptcy:
            return
        
        # Allocate savings and investments
        monthly_saving, monthly_investment = self._allocate_funds(new_balance)

        new_balance -= (monthly_saving + monthly_investment)
        #if (monthly_saving != 0 or monthly_investment != 0):
            #print(f"Balance after saving and invest : {new_balance} $")
        # Update account state
        self._update_account_state(
            new_balance,
            income,
            expense,
            monthly_saving,
            monthly_investment
        )
    
    def _apply_variation(self, base_value: float, uncertainty: float) -> float:
       """Apply random variation to a base value"""
       rate = np.random.uniform(-uncertainty, uncertainty)
       return base_value * (1 + rate)
   
    def _calculate_returns(self, current_month: int) -> float:
        """Calculate returns from investments and savings"""
        returns = 0
        # Investments typically have annual returns
        if current_month >= 12 and months[current_month%12] == "December" and self.total_investments > 0:
            returns += self.total_investments * self.hypothesis.investment_return_rate
            #print(f"Investment returns : {returns} $")
            
        # Savings might have more frequent returns (here monthly for simplicity)
        if current_month >= 12 and months[current_month%12] == "December" and self.total_savings > 0:
            returns += self.total_savings * (self.hypothesis.saving_return_rate)
            #print(f"Saving returns : {returns} $")

        return returns
    
    def _handle_negative_balance(self, balance: float) -> float:
        """Handle negative balance situations"""
        if balance >= 0:
            return balance
            
        # Use savings to cover negative balance
        if self.total_savings > 0:
            coverage = min(abs(balance), self.total_savings)
            balance += coverage
            self.total_savings -= coverage
            
        # Bankruptcy check (2 consecutive months in negative)
        if balance < 0 and self.balances[-1] < 0:
            self.bankruptcy = True
            
        return balance
    
    def _allocate_funds(self, available_balance: float) -> tuple:
         """Allocate funds to savings and investments"""
         if available_balance <= 0:
             return 0, 0
             
         # Savings allocation with risk of loss
         saving_amount = available_balance * self.strategy.saving_ratio
         saving_amount *= choice(
             [0, 1], 
             p=[self.hypothesis.saving_loss_prob, 1-self.hypothesis.saving_loss_prob]
         )
         #print(f"Monthly saving = {available_balance} * {self.strategy.saving_ratio} * chance = {saving_amount} $")
         
         # Investment allocation with higher risk of loss
         investment_amount = 0
         if available_balance > 100:  # Minimum investment threshold
             investment_amount = available_balance * self.strategy.investment_ratio
             investment_amount *= choice(
                 [0, 1],
                 p=[self.hypothesis.investment_loss_prob, 1-self.hypothesis.investment_loss_prob]
             )
         #print(f"Monthly invest = {available_balance} * {self.strategy.investment_ratio} * chance = {investment_amount} $")

         return saving_amount, investment_amount
    
    def _update_account_state(self, balance, income, expenses, saving, investment):
        """Update all account tracking variables"""
        self.balances.append(balance)
        self.income_history.append(income)
        self.expense_history.append(expenses)
        self.investments.append(investment)
        self.savings.append(saving)
        
        self.total_investments += investment
        self.total_savings += saving
        self.capital = self.total_investments + self.total_savings + self.balances[-1]
        self.capital_history.append(self.capital)
        
    def show_simulations_infos(self,show_details):
        """ Print in the console, informations about simulations for a number of months."""
        self.show_hypothesis()
        months_n = len(self.balances)
                
        for i in range(months_n):
            if (not show_details):
                break
            
            if (i%12 == 0):
                print("*"*8)
                print(f"\nWealth at the end of the year {i/12+1}: {self.capital_history[i]:.1f}")
                print("*"*8)
                print(f"\n\nYear {int(i/12+1)}\n")
                
            if (i >= 12 and self.investments[i-12] > 0):
                print(f"{self.investments[i-12]:.1f} $ was invested one year ago at {self.hypothesis.investment_return_rate * 100}%")
            if (i >= 12 and self.savings[i-12] > 0):
                print(f"{self.savings[i-12]:.1f} $ save at {self.hypothesis.saving_return_rate * 100}%")
            if (self.income_history[i] - self.expense_history[i] < 0 and self.savings[i] > 0):
                print(f"Using savings ({self.savings[-1]:.1f} $) to help main account !")
            print(f"Final balance on {months[i%12]}: {self.balances[i]:.1f} $\n")
            # Vérifier si pas de découvert sur plus de 2 mois
            if (self.balances[i-1] < 0 and self.income_history[i] - self.expense_history[i] < 0):
                print("Attention au défault de paiement")
                return
        
        print(self.result_analyse())
        print(self)
        
        if (self.wealthy_financial_assets != -1):
            print(f"Capital de riche en {self.wealthy_financial_assets} mois (ou {self.wealthy_financial_assets/12:.1f} années) !")
    
        
    def result_analyse(self):
        print("****** Analyse des comptes ******")
        print(f"Moyenne des dépenses mensuels : {np.average(self.expense_history):.1f} $")
        print(f"Moyenne des revenus mensuels : {np.average(self.income_history):.1f} $")
        print()
    
    def show_hypothesis(self):
        print()
        print(f"Dépenses mensuels : {self.monthly_expenses:.1f}  +- {self.hypothesis.expense_uncertainty*self.monthly_expenses:.1f} $")
        print(f"Revenus mensuels (travail) : {self.monthly_income:.1f} +- {self.hypothesis.income_uncertainty*self.monthly_income:.1f} $")
        print(f"Ratio d'investissement : {self.strategy.investment_ratio*100:.1f} %")
        print(f"Ratio d'épargne : {self.strategy.saving_ratio*100:.1f} %")

        
    def show_graph(self,months_n):
        plt.figure(figsize=(10, 6))
        plt.plot(range(months_n + 1), self.balances, label="Balance (€)", color="blue", linewidth=2)
        plt.axhline(0, color="black", linestyle="--", linewidth=0.8)  # Ligne de référence à 0

        # Ajouter les revenus et dépenses pour comparaison
        plt.bar(range(months_n + 1), self.income_history, label="Revenus mensuels (€)", color="green", alpha=0.5)
        plt.bar(range(months_n + 1), [-e for e in self.expense_history], label="Dépenses mensuelles (€)", color="red", alpha=0.5)
        
        # Erreur : Pour afficher la courbe, il faut que x et y aient la même dimension.
        #plt.plot(range(months_n + 1), self.total_savings, label="Epargne totale (€)", color="black", alpha=1)
        #plt.plot(range(months_n + 1), self.total_investments, label="Investissements totale (€)", color="brown", alpha=1)
        #plt.plot(range(months_n + 1), self.capital, label="Capital (€)", color="yellow", alpha=1)

        # Mise en forme du graphique
        plt.xlabel("Mois")
        plt.ylabel("Montant (€)")
        plt.title("Évolution de la Balance avec Revenus et Dépenses")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()
    
    def how_long_to_be_rich(self, wealth_goal = 100000):
        """ Method to know how long it take to be "rich" !"""
        i = 0
        self.show_simulation_hypothesis()
        while (self.capital < wealth_goal):
            self.month_simulation(i)
            if self.bankruptcy:
                print(f">>> Faillite en {int(i/12)} années")
                return
            i += 1
        self.show_graph(i)
        print(f"\nYou are rich (wealth >= {wealth_goal} $) in {int(i/12)} years ...\n")
        return i
