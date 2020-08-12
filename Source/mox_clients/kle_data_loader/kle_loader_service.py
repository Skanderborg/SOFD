import csv

with open('kle_klasser.csv', 'r', newline='\r\n', encoding='iso-8859-1') as csvfile:
    line = csvfile.read()
    print(line)
    #was = csv.reader(csvfile, delimiter=';')
    #x = 1
    #for row in reader:
    #    print(row)