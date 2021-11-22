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
list = [[k] for k in range(1,17)]
for traject in data:
    if traject[1] == 0:
        list[len(traject[0])].append(0)
    else:
        list[len(traject[0])].append(int((traject[1] - traject[3]) / traject[1] * 100))

base = [k for k in range(1, 17)]
value = []
print(list[-1])
for j in range(len(list)):
    mean = 0
    z = 0
    for i in range(len(list[j])-1):
        mean += list[j][i+1]
        z+=1
    if z == 0:
        value.append(0)
    else:
        value.append(int(mean/z))

base.pop(-2)
value.pop(-2)
plt.scatter(base, value)
plt.xlabel('# stops')
plt.ylabel('% of CO2 gained')

plt.show()

old_list = ["Avignon","V\u00e9nissieux","Nice","Mont\u00e9limar","Grenoble","Cannes","B\u00e9ziers","Annecy"]

new_list = ["Avignon","B\u00e9ziers","Mont\u00e9limar","V\u00e9nissieux","Annecy","Grenoble","Nice","Cannes"]
