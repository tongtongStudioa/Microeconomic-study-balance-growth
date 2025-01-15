# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 13:54:14 2025

@author: La famille tong
"""

import numpy as np
from numpy.random import choice
import matplotlib.pyplot as plt

#Constantes 
months = ["January","February","March","April","May","June","July","August","September","October","November", "December"]

class BalancingSimulation:
    def __init__(self, months_number = 12 * 5, inflation = 0.03, investment_return_rate = 0.05, saving_loss_prob = 0.01, investment_loss_prob = 0.15):
        self.months_n = months_number
        self.inflation = inflation
        self.investment_return_rate = investment_return_rate
        self.investment_loss_prob = investment_loss_prob
        self.saving_loss_prob = saving_loss_prob
        
    def analyse_simulations(self):
        #todo : tests multiple scenarios to compare investment ratio and saving ratio etc
        return
class BankAccount:
    """ Create life bank account for particular personn with all parameters you want."""
    
    def __init__(self,initial_balance = 1500,initial_saving = 2250, initial_investment = 1100,monthly_income = 2500):
        self.initial_balance = initial_balance
        self.initial_saving = initial_saving
        self.initial_investment = initial_investment
        self.monthly_income = monthly_income
        self.initial_capital = initial_balance + initial_investment + initial_saving
        self.monthly_expenses_ratio = 0.85
        self.monthly_expenses = self.monthly_expenses_ratio * self.monthly_income   # Dépenses fixes mensuelles ($)
        self.saving_ratio = 0.2
        self.investment_ratio = 0.3
        self.init_user_param = False
        self.init_bank_account()
        
    def init_manual_parameters(self):
        monthly_expenses_ratio = float(input("Taux de dépenses mensuel (en %) :"))/100 # Propension marginale à consommer
        monthly_expenses = monthly_expenses_ratio *self.monthly_income   # Dépenses fixes mensuelles ($)
        saving_ratio =  float(input("Taux d'épargne mensuel (en %) :"))/100 # (0.1 % de chance de perte)
        investment_ratio = float(input("Taux d'investissement mensuel (en %) :"))/100
        self.monthly_expenses_ratio = monthly_expenses_ratio
        self.monthly_expenses = monthly_expenses
        self.saving_ratio = saving_ratio
        self.investment_ratio = investment_ratio
        # Signaler que les paramètres essentiels sont mis à jour par l'utilisateur
        self.init_user_param = True
        
    def __str__(self):
        # Afficher le captial total
        infos = f">>> Capital financier : {self.capital:.1f} $ <<<\n"
        infos += f"-> sous forme d'investissement : {self.total_investments:.1f} $  ({(self.total_investments/self.capital * 100):.1f}%)\n"
        infos += f"-> épargne : {self.total_savings:.1f} $  ({(self.total_savings/self.capital * 100):.1f}%)\n"
        infos += f"-> en cash disponible : {self.balances[-1]:.1f} $\n"
        return infos
    
    def init_bank_account(self):
        self.balances = [self.initial_balance]  # Liste pour stocker le solde à chaque mois
        self.income_history = [self.monthly_income]           # Historique des revenus mensuels
        self.expense_history = [self.monthly_expenses]          # Historique des dépenses mensuelles
        self.investments = [self.initial_investment]            # Historique des investissements 
        self.savings = [self.initial_saving]               # Historique de l'épargne mensuel 
        
        self.total_investments = self.investments[-1]
        self.total_savings = self.savings[-1]
        self.capital = self.total_investments + self.total_savings + self.balances[-1]
        self.wealthy_financial_assets = -1
        
    def n_months_simulations(self,months_n,investment_return_rate = 0.05,saving_return_rate = 0.025, expense_uncertainty = 0.2, income_uncertainty = 0.05,saving_loss_prob = 0.01,investment_loss_prob = 0.15):
        """Simulation for a number of months"""
                
        for i in range(months_n):
            self.month_simulation(i, investment_return_rate,saving_return_rate, expense_uncertainty, income_uncertainty,saving_loss_prob,investment_loss_prob)
            
            # Suivre la progression du capital
            if (self.capital >= 3000000 and self.wealthy_financial_assets == -1):
                self.wealthy_financial_assets = i
                
        # todo : maybe return essential information !
        
    def month_simulation(self,i, investment_return_rate,saving_return_rate, expense_uncertainty, income_uncertainty,saving_loss_prob,investment_loss_prob):
        
        current_balance = self.balances[-1]
        
        # Ajouter revenu et déduire dépenses
        rate = np.random.uniform(-income_uncertainty, income_uncertainty) # Ajoute l'incertitude aux revenus et dépenses
        income = self.monthly_income * (1 + rate)
        rate = np.random.uniform(-expense_uncertainty, expense_uncertainty)
        expense = self.monthly_expenses * (1 + rate)
        
        # Ajouter les gains réinvestis
        if (i >= 12 and self.investments[i-12] > 0):
            income += self.investments[i-12] * investment_return_rate
        if (i >= 12 and self.savings[i-12] > 0):
            income += self.savings[i-12] * saving_return_rate
            
        new_balance = current_balance + income - expense
        
        # Remettre de l'argent dans le compte courant si à découvert
        if (new_balance < 0 and self.savings[-1] > 0):
            new_balance += self.savings[-1]
            self.savings[-1] = 0
            
        # Vérifier si pas de découvert sur plus de 2 mois
        if (self.balances[-1] <0 and new_balance < 0):
            return
        
        # Epargner et investir si possible
        monthly_saving = 0
        if (new_balance > 0):
            monthly_saving = new_balance * self.saving_ratio * choice([0,1], 1, p=[saving_loss_prob ,1 - saving_loss_prob])[0] #1 % de chance de perte 
            #print(f"Epargne mensuel : {monthly_saving:.1f} $")
            new_balance -= monthly_saving
            
        monthly_investment = 0
        if (new_balance > 0 and new_balance * self.investment_ratio > 100):
            monthly_investment = new_balance * self.investment_ratio * choice([0,1], 1, p=[investment_loss_prob ,1 - investment_loss_prob])[0] #15 % de chance de perte 
            new_balance -= monthly_investment
            #print(f"Investissement mensuel : {monthly_investment:.1f} $")
            #print(f"Balance after investments/savings on {months[i%12]}: {new_balance:.1f} $")
            
        # Mettre à jour les historiques
        self.balances.append(new_balance)
        self.investments.append(monthly_investment)
        self.savings.append(monthly_saving)
        self.income_history.append(income)
        self.expense_history.append(expense)
        self.total_investments = sum(self.investments)
        self.total_savings = sum(self.savings)
        self.capital = self.total_investments + self.total_savings + self.balances[-1]
        
    def show_simulations_infos(self,show_details, saving_return_rate, investment_return_rate):
        months_n = len(self.balances)
                
        for i in range(months_n):
            if (not show_details):
                break
            
            if (i%12 == 0):
                print(f"\nWealth at the end of the year : {self.capital:.1f}")
                print("***********************")
                print(f"\n\nYear {int(i/12+1)}\n")
                
            if (i >= 12 and self.investments[i-12] > 0):
                print(f"{self.investments[i-12]:.1f} $ was invested one year ago at {investment_return_rate * 100}%")
            if (i >= 12 and self.savings[i-12] > 0):
                print(f"{self.savings[i-12]:.1f} $ save at {saving_return_rate * 100}%")
            if (self.income_history[i] - self.expense_history[i] < 0 and self.savings[i] > 0):
                print(f"Using savings ({self.savings[-1]:.1f} $) to help main account !")
            print(f"Final balance on {months[i%12]}: {self.balances[i]:.1f} $\n")
            # Vérifier si pas de découvert sur plus de 2 mois
            if (self.balances[i-1] < 0 and self.income_history[i] - self.expense_history[i] < 0):
                print("Attention au défault de paiement")
                return
        
        print(f"****** Analyse des comptes (après {int(i/12)} ans) ******\n")
        print(f"Moyenne des dépenses mensuels : {np.average(self.expense_history):.1f} $")
        print(f"Moyenne des revenus mensuels : {np.average(self.income_history):.1f} $\n")
        
        print(self)
        
        if (self.wealthy_financial_assets != -1):
            print(f"Capital de riche en {self.wealthy_financial_assets} mois (ou {self.wealthy_financial_assets/12:.1f} années) !")
    
    def show_graph(self,months_n):
        plt.figure(figsize=(10, 6))
        plt.plot(range(months_n + 1), self.balances, label="Balance (€)", color="blue", linewidth=2)
        plt.axhline(0, color="black", linestyle="--", linewidth=0.8)  # Ligne de référence à 0

        # Ajouter les revenus et dépenses pour comparaison
        plt.bar(range(months_n + 1), self.income_history, label="Revenus mensuels (€)", color="green", alpha=0.5)
        plt.bar(range(months_n + 1), [-e for e in self.expense_history], label="Dépenses mensuelles (€)", color="red", alpha=0.5)

        # Mise en forme du graphique
        plt.xlabel("Mois")
        plt.ylabel("Montant (€)")
        plt.title("Évolution de la Balance avec Revenus et Dépenses")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()