
'''
getSeismicData.py: Extract all data from Centro Sismologico Nacional, UCH,
    and save it into multiple folders sorted by year and month, and finally into a daily csv.

For further research in AI using ML to hopefully predict eathquakes and save lives.

2020 Sebastian Salazar

'''

import csv
import requests
import re
import time
import os
import datetime

now = datetime.datetime.now()

#To get all data available since 2008 (the first record) until today
years = [*range(2008, now.year + 1)]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]


for year in years:
    for month in months:
        for day in days:
            try:
                url = 'http://sismologia.cl/events/listados/' + str(year) + '/' + str(month).zfill(2) \
                    + '/' +  str(year) + str(month).zfill(2) + str(day).zfill(2)  + '.html'

                r = requests.get(url)

                #to check the status of the request
                print(r)

                if '<table>' in r.text:

                    #to get table header 
                    headerRe = re.findall(('<th>'
                                            '(.*?)</th></tr>'),
                                                r.text, re.DOTALL
                                                )

                    header = headerRe[0].split("</th><th>")

                    #to get daily seismic data
                    dailySeismsRe = re.findall(('target="centro">'
                                            '(.*?)</td></tr>'),
                                                r.text, re.DOTALL
                                                )

                    #for using multiple splits
                    dailySeisms = [re.split('</a></td><td>|</td><td>', line) for line in dailySeismsRe]

                    #...path to where to store the data

                    pathToDataFolder = ""
                    pathToSave = pathToDataFolder + '/' + str(year) +'/'+ str(month) 

                    if os.path.exists(pathToSave):
                        fileName = 'day_' + str(day) + '.csv'
                        with open(pathToSave + '/' + fileName, 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(header)
                            for seism in dailySeisms:
                                    writer.writerows(dailySeisms)
                    else:
                        #makedirs make all intermediate directories
                        os.makedirs(pathToSave)
                        fileName = 'day_' + str(day) + '.csv'
                        with open(pathToSave + '/' + fileName, 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(header)
                            for seism in dailySeisms:
                                    writer.writerows(dailySeisms)
            except:
                print("Error: No data for date " + str(day) + '/' + str(month) + '/' + str(year))
                #Date format used is day/month/year


