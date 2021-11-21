import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import voyageur_de_commerce
import utils

df_cities = pd.read_csv("data\cities.csv", sep=";")
df_factors = pd.read_csv("data\\factors.csv")
df_orders = pd.read_csv("data\orders.csv", sep=";")
df_packages = pd.read_csv("data\packages.csv")
df_pricing = pd.read_csv("data\pricing.csv")
df_routes = pd.read_csv("data\\routes_v2.csv")
df_trucks = pd.read_csv("data\\trucks.csv", sep=";")
df_warehouses = pd.read_csv("data\warehouses.csv", sep=";")


def execute(list_of_cities):
    """
    Execute le code de voyageur de commerce
    :param list_of_cities:
    :return: - ancienne liste de ville
             - ancienne distance
             - nouvelle liste de ville
             - nouvelle distance
    """
    gc = voyageur_de_commerce.GestionnaireCircuit()

    for k in range(len(list_of_cities)):
        ville = voyageur_de_commerce.Ville(list_of_cities[k][1], list_of_cities[k][2], list_of_cities[k][0])
        gc.ajouterVille(ville)

    # on initialise la population avec 50 circuits
    pop = voyageur_de_commerce.Population(gc, 50, True)

    # On fait evoluer notre population sur 100 generations
    ga = voyageur_de_commerce.GA(gc)
    pop = ga.evoluerPopulation(pop)
    for i in range(0, 100):
        pop = ga.evoluerPopulation(pop)

    meilleurePopulation = pop.getFittest()
    list_of_new_cities = []
    for ville in meilleurePopulation.circuit:
        list_of_new_cities.append(ville.nom)

    # ordinner la nouvelle liste
    list_of_new_cities = utils.ordonner_une_liste(list_of_new_cities, list_of_cities[0][0])

    # on ajoute le trajet retour à l'ancienne distance
    trajet_retour = utils.distance(list_of_cities[0], list_of_cities[-1])
    ancienne_distance = df_routes.loc[1]['total_distance'] + trajet_retour

    # list of ancienne cities
    list_of_only_old_cities = [list_of_cities[k][0] for k in range(len(list_of_cities))]

    return list_of_only_old_cities, ancienne_distance, list_of_new_cities, pop.getFittest().getDistance()


if __name__ == "__main__":

    database = []
    # for k in range(len(df_routes)):
    for k in range(0, 5):  # Ici exemple seulement avec 5 trajets

        # je recupere les trajets
        stops = df_routes.loc[k]['stops'].split(' > ')
        list_of_cities = []
        for i in range(len(stops)):  # Pour chaque arrêt je récupere les données de lontitude et latitude de la ville
            coord = utils.donnees_cities(stops[i], df_cities)
            list_of_cities.append([stops[i], coord[0], coord[1]])

        print("Liste de l'ancien trajet: " + str(stops))
        test = execute(list_of_cities)

        print("Liste du nouveau trajet:" + str(test[2]))

        print("")

        # TODO  Problème : à chaque fois que je lance execute : il calcule le plus court trajet avec les villes que je lui donne plus les villes des anciennes fois où j'ai executé le code
        database.append(execute(list_of_cities))
