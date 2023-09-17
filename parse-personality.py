import json 

f = open("16persons.txt", "r")

data = [line.strip() for line in f]

data2 = []
for d in data:
	if (len(d) > 3):
		data2.append(d)

print(len(data2))
D = {}

for i in range(len(data2) // 2):
	code = data2[i * 2]
	des = data2[i * 2 + 1]
	D[code] = des 

with open("16persons.json", "w") as outfile:
    json.dump(D, outfile)