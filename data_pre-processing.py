# importinh necessary libraries
from datetime import datetime
import numpy as np
import pandas as pd

olympics=pd.read_csv("Downloads/data/olympic_hosts.csv")

#dropping the unnecessary rows
olympics.drop(olympics[olympics.Type=='youthgames'].index, inplace=True)
olympics.drop(olympics[olympics.Year>=2018].index, inplace=True)
olympics.drop(olympics[olympics.Year<2002].index, inplace=True)

#dropping those treated more than once
olympics = olympics.drop_duplicates(subset=['Country'], keep=False)
countries = olympics['Country'].to_numpy()

#generating ids for countries
def generate_id(country):
    return list(countries).index(country)+1

olympics['id'] = olympics['Country'].apply(generate_id)

#showing the needed columns
olympics["Post"] = [1 for i in range(len(countries))]
olympics["Subtype"] = [1 for i in range(len(countries))]
olympics['Subtype'] = pd.get_dummies(olympics['Type'])

olympics['Date'] = [str(i)+' '+j for i, j in zip(olympics.Year.to_numpy(), olympics.Date.to_numpy())]

# converting date
def date_filter(date):
    new = date.split("-")[0]
    new = new + "10:00:00"
    new = datetime.strptime(new, '%Y %d %b %H:%M:%S')
    
    return int(new.strftime('%j'))

olympics['Days'] = olympics['Date'].apply(date_filter)
olympics = olympics[['Country', 'Year', 'id', 'Subtype', 'Post', 'Days']]

#adding the panel data for different years
years = np.arange(min(olympics['Year'].unique()), max(olympics['Year'].unique())+1, 1)

		
#adding the needed variables 
gdpc = pd.read_csv('Downloads/data/gdpc.csv')
olympics['gdpc'] = [0 for i in range(len(olympics))]

fin = pd.read_csv('Downloads/data/fin_data.csv')
olympics['FinStability'] = [0 for i in range(len(olympics))]

freedom = pd.read_csv('Downloads/data/freedom.csv')
olympics['Freedom'] = [0 for i in range(len(olympics))]

polit = pd.read_csv('Downloads/data/polit.csv')
olympics['PolitStability'] = [0 for i in range(len(olympics))]

# for each country and year adding the other variables
for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['gdpc'][idx] = gdpc[gdpc['Country Name']==country][str(year)].to_numpy()[0]
        
for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['FinStability'][idx] = fin[(fin['country']==country)&(fin['year']==year)]['gfddsi01'].to_numpy()[0]
        
for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['Freedom'][idx] = freedom[(freedom['Name']==country)&(freedom['Index Year']==year)]['Overall Score'].to_numpy()[0]

for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['PolitStability'][idx] = polit[(polit['Country Name']==country)&(polit['Series Name']=='Political Stability and Absence of Violence/Terrorism: Estimate')]['{0} [YR{0}]'.format(year)].to_numpy()[0]
        

olympics = olympics.sort_values(by=['id', 'Year'])

# saving the data 
olympics.to_csv("Downloads/olympics.csv")
