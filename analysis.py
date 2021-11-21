import json
import matplotlib.pyplot as plt

with open("output.json", "r") as json_data:
    data = json.load(json_data)

sum_of_total_new_traject, sum_of_total_old_traject = 0, 0
for traject in data:
    sum_of_total_new_traject += traject[3]
    sum_of_total_old_traject += traject[1]

print("Nous avons économisé : " + str(int(sum_of_total_old_traject - sum_of_total_new_traject)) + " km")
print("Ce qui représente : " + str(int(((
                                                sum_of_total_old_traject - sum_of_total_new_traject) / sum_of_total_old_traject) * 100)) + "% de CO2 économisé")
print("\n")

sum_of_total_new_traject_5, sum_of_total_old_traject_5 = 0, 0
for traject in data:
    if len(traject[0]) > 4:
        sum_of_total_new_traject_5 += traject[3]
        sum_of_total_old_traject_5 += traject[1]
    else:
        pass

print("Nous avons économisé : " + str(
    int(sum_of_total_old_traject_5 - sum_of_total_new_traject_5)) + " km sur les trajets d'au moins 4 arrêts")
print("Ce qui représente : " + str(int(((
                                                sum_of_total_old_traject_5 - sum_of_total_new_traject_5) / sum_of_total_old_traject_5) * 100)) + "% de CO2 économisé sur les trajets d'au moins 4 arrêts")
