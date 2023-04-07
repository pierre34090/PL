from pyomo.environ import *
import random

def generate_knapsack_instance(num_items, capacity):
    """
    Génère une instance aléatoire du problème de sac à dos avec le nombre
    d'objets et la capacité du sac à dos donnés.
    
    Retourne un tuple contenant deux dictionnaires :
    - weights : un dictionnaire qui associe à chaque objet son poids
    - profits : un dictionnaire qui associe à chaque objet son profit
    """
    weights = {}
    profits = {}
    
    for i in range(1, num_items+1):
        weight = random.randint(1, 10)
        profit = random.randint(1, 20)
        weights[i] = weight
        profits[i] = profit
        
    return (weights, profits, capacity)

# Données du problème
capacité = 100
nbObjet = 30

# Génération de l'instance

instance = generate_knapsack_instance(nbObjet, capacité)

weights = instance[0]
profits = instance[1]
capacity = instance[2]


# Créer un modèle d'optimisation
model = ConcreteModel()

# Définir les ensembles d'objets et de variables
model.ITEMS = Set(initialize=weights.keys())
model.x = Var(model.ITEMS, within=Binary)

# Définir la fonction objective
model.obj = Objective(expr=sum(profits[i] * model.x[i] for i in model.ITEMS), sense=maximize)

# Définir les contraintes
model.con1 = Constraint(expr=sum(weights[i] * model.x[i] for i in model.ITEMS) <= capacity)

# Créer un solveur et résoudre le problème
solver = SolverFactory('glpk')
results = solver.solve(model)

# Afficher les résultats
print("Status : ", results.solver.status)
print("Termination Condition : ", results.solver.termination_condition)
print("Capacité : ", capacity)
print("Poids et profit des objets : (",weights,",",profits,")" )
print("Valeur de la fonction objective : ", model.obj())
print("Valeurs des variables de décision : ", {i: model.x[i]() for i in model.ITEMS})