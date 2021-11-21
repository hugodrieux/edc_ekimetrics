import json
import matplotlib.pyplot as plt

with open("output.json", "r") as json_data:
    data = json.load(json_data)

percentage = []
for traject in data:
    if len(traject[0]) < 4:
        pass
    else:
        percentage.append(int((traject[1]-traject[3])/traject[1]*100))

print(percentage)

