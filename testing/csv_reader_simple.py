import csv

ep_num = []
ep_title = []
ep_air_date = []
ep_guest1 = []
ep_round_t = []
ep_round_h = []
ep_url = []

with open('data.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        ep_num.append(row[0])
        ep_title.append(row[1])
        ep_air_date.append(row[2])
        ep_guest1.append(row[3])
        ep_round_t.append(row[4])
        ep_round_h.append(row[5])
        ep_url.append(row[6])

print(ep_num)
print(ep_title)
print(ep_air_date)
print(ep_guest1)
print(ep_round_t)
print(ep_round_h)
print(ep_url)
