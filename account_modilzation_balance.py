# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 13:54:14 2025

@author: La famille tong
"""

import numpy as np
from numpy.random import choice

#Cobstantes 
months = ["January","February","March","April","May","June","July","August","September","October","November", "December"]

# Paramètres
initial_balance = 500  # Solde initial (€)
monthly_income = 2500    # Revenu mensuel (€)
monthly_expenses_ratio = float(input("Taux de dépenses mensuel (en %) :"))/100 # Propension marginale à consommer
monthly_expenses = monthly_expenses_ratio * monthly_income   # Dépenses fixes mensuelles ($)
saving_ratio =  float(input("Taux d'épargne mensuel (en %) :"))/100 # (0.1 % de chance de perte)
investment_ratio = float(input("Taux d'investissement mensuel (en %) :"))/100

investment_return_rate = 0.05  # Taux de rendement annuel des investissements (15 % de chance de perte)
months_number = 12 * 3           # Nombre de mois (8 ans)

# Simulation
balances = [initial_balance]  # Liste pour stocker le solde à chaque mois
income_history = []           # Historique des revenus mensuels
expense_history = []          # Historique des dépenses mensuelles
investments = [100]            # Historique des investissements 
savings = [250]               # Historique de l'épargne mensuel 

total_investments = investments[-1]
total_savings = savings[-1]
capital = total_investments + total_savings + balances[-1]
initial_capital = capital
date_decuple_capital = -1

print(f"\nMonthly income : {monthly_income} $")
print(f"Monthly expenses : {monthly_expenses} $")
print(f">>> Capital initial : {capital:.1f} $ <<<\n\n")



for i in range(months_number):

    if (i > 0 and i % 12 == 0):
        print(f">>> Capital financier = {capital:.1f} $ <<<\n")
        print("*************")
        print(f"\n\nYear {i/12}")

    current_balance = balances[-1]
    
    # Ajouter revenu et déduire dépenses
    uncertainty = np.random.uniform(-0.2,0.2) # Ajoute l'incertitude aux revenus et dépenses
    income = monthly_income * (1 + uncertainty)
    uncertainty = np.random.uniform(-0.2,0.2)
    expense = monthly_expenses * (1 + uncertainty)
    
    # Ajouter les gains réinvestis
    if (i >= 12 and investments[i-12] > 0):
        print(f"{investments[i-12]:.1f} $ was invested one year ago at {investment_return_rate * 100}%")
        income += investments[i-12] * investment_return_rate
    
    new_balance = current_balance + income - expense
    print(f"Balance on {months[i%12]}: {new_balance:.1f} $")
    
    # Remettre de l'argent dans le compte courant si à découvert
    if (new_balance < 0 and savings[-1] > 0):
        print(f"Utilisation de l'épargne ({savings[-1]:.1f} $) pour diminuer le déficit")
        new_balance += savings[-1]
        savings[-1] = 0
        
    # Vérifier si pas de découvert sur plus de 2 mois
    if (balances[-1] <0 and new_balance < 0):
        print("Attention au défault de paiement")
        break
    
    # Epargner et investir si possible
    monthly_saving = 0
    if (new_balance > 0):
        # Interet de 3% par ans
        monthly_saving = new_balance * saving_ratio * choice([0,1], 1, p=[0.01,0.99])[0] #1 % de chance de perte 
        #print(f"Epargne mensuel : {monthly_saving:.1f} $")
        new_balance -= monthly_saving
        
    monthly_investment = 0
    if (new_balance > 0 and new_balance * investment_ratio > 100):
        monthly_investment = new_balance * investment_ratio * choice([0,1], 1, p=[0.15,0.85])[0] #15 % de chance de perte 
        new_balance -= monthly_investment
        #print(f"Investissement mensuel : {monthly_investment:.1f} $")
        #print(f"Balance after investments/savings on {months[i%12]}: {new_balance:.1f} $")
        
    # Mettre à jour les historiques
    balances.append(new_balance)
    investments.append(monthly_investment)
    savings.append(monthly_saving + savings[-1])
    income_history.append(income)
    expense_history.append(expense)
    total_investments = sum(investments)
    total_savings = savings[-1]
    capital = total_investments + total_savings + balances[-1]
    
    # Suivre la progression du capital
    if (capital >= 10 * initial_capital and date_decuple_capital == -1):
        date_decuple_capital = i

    print()
        
print("****** Analyse des comptes ******")
print(f"Moyenne des dépenses mensuels : {np.average(expense_history):.1f} $")
print(f"Moyenne des revenus mensuels : {np.average(income_history):.1f} $")

# Afficher le captial total
print(f"Capital financier : {capital:.1f} $ (au bout de {months_number/12:.0f} ans)")
print(f"-> sous forme d'investissement : {total_investments:.1f} $  ({(total_investments/capital * 100):.1f}%)")
print(f"-> épargne : {total_savings:.1f} $  ({(total_savings/capital * 100):.1f}%)")
print(f"-> en cash disponible : {balances[-1]:.1f} $")
if (date_decuple_capital != -1):
    print(f"Capital décuplé en {date_decuple_capital} mois (ou {date_decuple_capital/12:.1f} années) !")