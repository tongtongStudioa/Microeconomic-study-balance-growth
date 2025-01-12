# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 13:54:14 2025

@author: La famille tong
"""

import numpy as np
import matplotlib.pyplot as plt

#Cobstantes 
months = ["January","February","March","April","May","June","July","August","September","October","November", "December"]

# Paramètres
initial_balance = 10  # Solde initial (€)
monthly_income = 2500    # Revenu mensuel (€)
monthly_expenses_ratio = 0.89 #float(input("Ratio de dépenses % :"))
print(f"Taux de dépenses par mois : {monthly_expenses_ratio * 100} %")
monthly_expenses = monthly_expenses_ratio * monthly_income   # Dépenses fixes mensuelles (€)
saving_ratio = 0.1
print(f"Taux d'épargne par mois : {saving_ratio * 100} %")
investment_ratio = 0.2
print(f"Taux d'investissement par mois : {investment_ratio * 100} %")

investment_return_rate = 0.05  # Taux de rendement annuel des investissements
months_number = 12 * 3           # Nombre de mois (8 ans)

# Simulation
balances = [initial_balance]  # Liste pour stocker le solde à chaque mois
income_history = []           # Historique des revenus mensuels
expense_history = []          # Historique des dépenses mensuelles
investments = []            # Historique des investissements (15 % de chance de perte)
savings = []               # Historique de l'épargne mensuel (0.1 % de chance de perte)
print(f"Monthly income : {monthly_income} $")
print(f"Monthly expenses : {monthly_expenses} $\n\n")

for i in range(months_number):

    #if (i > 0 and i % 12 == 0):
        #print(f"\nYear {i/12}")

    current_balance = balances[-1]
    
    # Ajouter revenu et déduire dépenses
    income = monthly_income
    expense = monthly_expenses
    
    # Ajouter les gains réinvestis
    if (i >= 12):
        #print(f"{investments[i-12]:.1f} $ was invested one year ago at {investment_return_rate * 100}%")
        income += investments[i-12] * (investment_return_rate +1)
        
    new_balance = current_balance + income - expense
    #print(f"Balance before investments/savings on {months[i%12]}: {new_balance:.1f} $")

    # Epargner et investir si possible
    monthly_saving = new_balance * saving_ratio
    new_balance -= monthly_saving
    monthly_investment = new_balance * investment_ratio
    #print(f"Month investment : {monthly_investment:.1f} $")
    
    # Mettre à jour les historiques
    balances.append(new_balance)
    investments.append(monthly_investment)
    savings.append(monthly_saving)
    income_history.append(income)
    expense_history.append(expense)
        
# Afficher le captial total
total_investments = np.sum(investments)
total_savings = sum(savings)
capital = total_investments + total_savings + balances[-1]
print(f"Capital financier : {capital:.1f} $ (au bout de {months_number/12:.0f} ans)")
print(f"-> sous forme d'investissement : {total_investments:.1f} $  ({(total_investments/capital * 100):.1f}%)")
print(f"-> épargne : {total_savings:.1f} $  ({(total_savings/capital * 100):.1f}%)")
print(f"-> en cash disponible : {balances[-1]:.1f} $")

# Générer les graphiques
plt.figure(figsize=(10, 6))
plt.plot(range(months_number + 1), balances, label="Balance (€)", color="blue", linewidth=2)
plt.axhline(0, color="black", linestyle="--", linewidth=0.8)  # Ligne de référence à 0

# Ajouter les revenus et dépenses pour comparaison
plt.bar(range(months_number), income_history, label="Revenus mensuels (€)", color="green", alpha=0.5)
plt.bar(range(months_number), [-e for e in expense_history], label="Dépenses mensuelles (€)", color="red", alpha=0.5)

# Mise en forme du graphique
plt.xlabel("Mois")
plt.ylabel("Montant (€)")
plt.title("Évolution de la Balance avec Revenus et Dépenses")
plt.legend()
plt.grid()
plt.tight_layout()
#plt.show()