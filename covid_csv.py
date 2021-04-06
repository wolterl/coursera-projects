import csv

with open("owid-covid-data.csv") as stuff:
    rows = csv.reader(stuff)
#res (results) will include all data in stuff and 
#res.pop(0) creates the column headers (cols) from the first line of the csv file, but 
#not include the first line as data results (pop deletes and returns the cloumn headers)
    res = list(rows)
#    print(res[0])
    cols = res.pop(0)
#dictionary comprehension -- for each column name creating dictionary where key is the name of the column and value is its index, assigned to an object 
#maps the column name to the index number   
    info = {col_name: cols.index(col_name) for col_name in cols}

month_sums = {}
    
for row in res:
#    print(row[info['date']])
#create date so chart can be by year_month
    date = row[info['date']]
    year_month = date[:7]
    if year_month in ['2020-01', '2021-04']:
        continue
       
    if year_month not in month_sums:
        month_sums[year_month] = {}       
        
#    print(year_month)
    location = row[info['location']]
    try:
        total_cases = float(row[info['total_cases']])
    except:
        total_cases = 0
    try:
        total_deaths = float(row[info['total_deaths']])
    except:
        total_deaths = 0
    try:
        new_cases = float(row[info['new_cases']])
    except:
        new_cases = 0
    try:
        new_deaths = float(row[info['new_deaths']])
    except:
        new_deaths = 0
 
    if location not in month_sums[year_month]:
        month_sums[year_month][location] = {}
        month_sums[year_month][location]['total_cases']=total_cases + new_cases
        month_sums[year_month][location]['total_deaths']=total_deaths + new_deaths
#        month_sums[year_month][location]['new_cases']=new_cases
#        month_sums[year_month][location]['new_deaths']=new_deaths
    else:
        month_sums[year_month][location]['total_cases']+=new_cases
        month_sums[year_month][location]['total_deaths']+=new_deaths
#        month_sums[year_month][location]['new_cases']+=new_cases
#        month_sums[year_month][location]['new_deaths']+=new_deaths
        
#print(month_sums)    
countries = []

fhand = open('covid.js','w')
fhand.write("covid_cases_data = [ ['date'")
for location in month_sums['2020-02']:
    if location not in ['World', 'Asia', 'Europe', 'European Union', 'South America', 'Africa', 'North America', 'International', 'Oceania']:
        fhand.write(",'"+location+"'")
        countries.append(location)
fhand.write("]")

for date in month_sums:
    fhand.write(",\n['"+date+"'")
    for location in countries:
        total_cases = month_sums[date][location]['total_cases']
        fhand.write(","+str(total_cases))

    fhand.write("]");

fhand.write("\n];\n")

fhand.write("covid_deaths_data = [ ['date'")
for location in countries:
    fhand.write(",'"+location+"'")
fhand.write("]")

for date in month_sums:
    fhand.write(",\n['"+date+"'")
    for location in countries:
        total_deaths = month_sums[date][location]['total_deaths']
        fhand.write(","+str(total_deaths))

    fhand.write("]");

fhand.write("\n];\n")
fhand.close()