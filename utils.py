import numpy as np

def donnees_cities(name_city, df_cities):
    """
    Fontion qui va recupérer les données de lattitude et longitude
    """
    donnes_city = df_cities[df_cities.city == name_city]
    long, lat = float(donnes_city['lat'].iloc[0].replace(',','.')), float(donnes_city['lng'].iloc[0].replace(',','.'))
    return long, lat


def distance(city1,city2):
    """
    Fonction qui renvoie la distance à vol d'oiseau entre deux villes en fonction de leur nom
    """
    long_city1, lat_city1 = np.pi*city1[1]/180, np.pi*city1[2]/180
    long_city2, lat_city2 = np.pi*city2[1]/180, np.pi*city2[2]/180
    return 6371*np.arccos(np.sin(lat_city1)*np.sin(lat_city2)+np.cos(lat_city1)*np.cos(lat_city2)*np.cos(long_city1-long_city2))


def ordonner_une_liste(list, first_element):
    index = list.index(first_element)
    new_list = []
    for k in range(len(list)):
        new_list.append(list[(index+k)%len(list)])
    return new_list
