import pandas as pd
import voyageur_de_commerce
import utils
from tqdm import tqdm
import json

df_cities = pd.read_csv("data\cities.csv", sep=";")
df_factors = pd.read_csv("data\\factors.csv")
df_orders = pd.read_csv("data\orders.csv", sep=";")
df_packages = pd.read_csv("data\packages.csv")
df_pricing = pd.read_csv("data\pricing.csv")
df_routes = pd.read_csv("data\\routes_v2.csv")
df_trucks = pd.read_csv("data\\trucks.csv", sep=";")
df_warehouses = pd.read_csv("data\warehouses.csv", sep=";")


def execute(list_of_cities, ancienne_distance):
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

    # list of ancienne cities
    list_of_only_old_cities = [list_of_cities[k][0] for k in range(len(list_of_cities))]

    return list_of_only_old_cities, ancienne_distance, list_of_new_cities, pop.getFittest().getDistance()


if __name__ == "__main__":

    output_trajects = []
    # for k in range(len(df_routes)):
    for k in tqdm(range(len(df_routes))):  # Ici exemple seulement avec 5 trajets

        # je recupere les trajets
        stops = df_routes.loc[k]['stops'].split(' > ')
        ancienne_distance = 0
        for j in range(len(stops) - 1):
            ancienne_distance += utils.distance(utils.donnees_cities(stops[j], df_cities),
                                                utils.donnees_cities(stops[j + 1], df_cities))

        # on ajoute le trajet retour à l'ancienne distance
        trajet_retour = utils.distance(utils.donnees_cities(stops[0], df_cities),
                                       utils.donnees_cities(stops[-1], df_cities))
        ancienne_distance += trajet_retour

        if len(stops) < 4:
            output_trajects.append([stops, ancienne_distance, stops, ancienne_distance])
        else:
            list_of_cities = []
            for i in range(
                    len(stops)):  # Pour chaque arrêt je récupere les données de lontitude et latitude de la ville
                coord = utils.donnees_cities(stops[i], df_cities)
                list_of_cities.append(coord)
            results_algo = execute(list_of_cities, ancienne_distance)
            if results_algo[1] < results_algo[3]:
                output_trajects.append([results_algo[0], results_algo[1], results_algo[0], results_algo[1]])
            else:
                output_trajects.append(results_algo)

    with open("output.json", 'w') as file:
        json.dump(output_trajects, file, indent=6)

    sum_of_total_new_traject, sum_of_total_old_traject = 0, 0
    for traject in output_trajects:
        sum_of_total_new_traject += traject[3]
        sum_of_total_old_traject += traject[1]

    print("Nous avons économisé : " + str(int(sum_of_total_old_traject - sum_of_total_new_traject)) + " km")
    print("Ce qui représente : " + str(int(((
                                                        sum_of_total_old_traject - sum_of_total_new_traject) / sum_of_total_old_traject) * 100)) + "% de CO2 économisé")
