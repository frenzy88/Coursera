import pandas as pd
import numpy as np
import re
from functools import reduce

df = pd.read_excel('Energy Indicators.xls')
df = (df.drop(df.index[0:17])
        .drop(df.columns[0:2], axis=1)
        .drop(df.index[244:])
        .rename(columns= {'Unnamed: 2':'Country', 'Unnamed: 3':'Energy Supply', 'Unnamed: 4':'Energy Supply per Capita', 'Unnamed: 5':'% Renewable'}))
df = (df.replace('...', np.nan)
        .replace('United States of America', 'United States', regex=True)
        .replace(r'Republic of Korea', 'South Korea', regex=True)
        .replace(r'United States of America', 'United States', regex=True)
        .replace(r'United Kingdom of Great Britain and Northern Ireland', 'United Kingdom', regex=True)
        .replace(r'China, Hong Kong Special Administrative Region', 'Hong Kong', regex=True))
print(df.columns)
df['Country'] = df['Country'].str.replace('\d+', '')
df['Country'] = df['Country'].str.replace(' \(.*\)', '')

df['Energy Supply'] = df['Energy Supply']*1000000
energy = df.reset_index(drop=True)
#print(energy.head())
#print('')


gdp = pd.read_csv('world_bank.csv', header=None)

gdp.columns = gdp.iloc[4]

gdp = (gdp.drop(gdp.index[0:5])
          .sort_values('Country Name', ascending=True)
          .reset_index(drop=True, level=0)
          .rename(columns= {'Country Name':'Country'}))
gdp = (gdp.replace('Korea, Rep.', 'South Korea', regex=True)
          .replace('Iran, Islamic Rep.', 'Iran', regex=True)
          .replace('Hong Kong SAR, China', 'Hong Kong', regex=True))
#print(gdp.head())
#print('')

ScimEn = pd.read_excel('scimagojr-3.xlsx')

#print(ScimEn.head())
#print('')

data_frames = [energy, gdp, ScimEn]
dfm = reduce(lambda left,right: pd.merge(left,right,on=['Country'], how='outer'), data_frames)

dfm = dfm.sort_values('Rank', ascending=True)
dfm = (dfm.drop(dfm.columns[7:53], axis=1)
          .drop(dfm.index[15:])
          .rename(columns = {2006.0:'2006', 2007.0:'2007', 2008.0:'2008', 2009.0:'2009', 2010.0:'2010', 2011.0:'2011', 2012.0:'2012', 2013.0:'2013', 2014.0:'2014', 2015.0:'2015'})
          .set_index('Country')
          .rename_axis(None))
dfm = dfm[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]

#cols = dfm.columns.tolist()
#print('')
#print(cols)
print('')
print(dfm)
