import csv


def getemailids(csvfile):
    try:
        csvfile = open(csvfile, 'rt')
    except:
        print("File not found")
    csvReader = csv.reader(csvfile, delimiter=",")
    l = []
    for row in csvReader:
        l.append(row[0])
    print (l[1:])
    return l[1:]
