import pandas as pd
import numpy as np
import re
pd.options.mode.chained_assignment = None

#sciezka_bazowa='/home/students/mat/j/jb417512/python/'
sciezka_bazowa='/home/julia/Documents/python/projekt/'
sciezka_dane1 = sciezka_bazowa + 'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv'
sciezka_dane2 = sciezka_bazowa + 'API_SP.POP.TOTL_DS2_en_csv_v2_4751604/API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv'
sciezka_dane3 = sciezka_bazowa + 'co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv'


gdp = pd.read_csv(sciezka_dane1, skiprows=3)
populacja = pd.read_csv(sciezka_dane2, skiprows=3)
co2 = pd.read_csv(sciezka_dane3, skiprows=0)

#usunięcie ostatniej kolumny jeśli jest pusta
if gdp.iloc[:,len(gdp.columns)-1].isna().sum() == len(gdp.iloc[:,len(gdp.columns)-1]):
    gdp=gdp.drop(gdp.columns[len(gdp.columns)-1], axis=1)

if populacja.iloc[:,len(populacja.columns)-1].isna().sum() == len(populacja.iloc[:,len(populacja.columns)-1]):
    populacja=populacja.drop(populacja.columns[len(populacja.columns)-1], axis=1)




print(gdp.isna().sum().sum())
print(populacja.isna().sum().sum())
print(co2.isna().sum().sum())

print(range(gdp.shape[0]))

#sprawdzenie które wiersze nie mają żadnych danych o gdp
print('\nkraje o których GDP nie ma żadnych danych')
for row in range(gdp.shape[0]):
    if(gdp.iloc[row,4:].isna().sum() == len(gdp.iloc[row,4:])):
        print(gdp.iloc[row,0])

#sprawdzenie które wiersze nie mają żadnych danych o populacji
print('\nkraje o których populacji nie ma żadnych danych')
for row in range(populacja.shape[0]):
    if(populacja.iloc[row,4:].isna().sum() == len(populacja.iloc[row,4:])):
        print(populacja.iloc[row,0])
print(list(populacja.columns))


gdp_lata = [eval(i) for i in list(gdp.columns)[4:]]

populacja_lata = [eval(i) for i in list(populacja.columns)[4:]]

rok_start=max(min(gdp_lata), min(populacja_lata), min(co2.Year))
rok_koniec=min(max(gdp_lata), max(populacja_lata), max(co2.Year))
print('\nzakres lat to od', rok_start, 'do', rok_koniec)

gdp_index_start=gdp.columns.get_loc(str(rok_start))
gdp_index_koniec=gdp.columns.get_loc(str(rok_koniec))
print(gdp_index_start, gdp_index_koniec)

a=list(range(0,4)) + list(range(gdp_index_start,gdp_index_koniec+1))
gdp=gdp.iloc[:, a]

populacja_index_start=populacja.columns.get_loc(str(rok_start))
populacja_index_koniec=populacja.columns.get_loc(str(rok_koniec))
print(populacja_index_start, populacja_index_koniec)

a=list(range(0,4)) + list(range(populacja_index_start,populacja_index_koniec+1))
populacja=populacja.iloc[:, a]
print(populacja)

co2=co2[(co2.Year>=rok_start) & (co2.Year<=rok_koniec)]

#zmienianie nazw krajów na wielkie litery
for index, row in gdp.iterrows():
    gdp['Country Name'].iloc[index]=gdp['Country Name'].iloc[index].upper()
print(list(gdp['Country Name']))

for index, row in populacja.iterrows():
    populacja['Country Name'].iloc[index]=populacja['Country Name'].iloc[index].upper()
print(list(populacja['Country Name']))

print('\nTUTAJ\n')
kraje1=pd.DataFrame(list(set(gdp['Country Name'].copy())))
kraje1.columns=['kraje1']
kraje2=pd.DataFrame(list(set(co2['Country'].copy())))
kraje2.columns=['kraje2']
print(kraje1, '\n\n')
kraje1.kraje1=[re.sub('.\(.*\)', '', i) for i in kraje1.kraje1]
kraje2.kraje2=[re.sub('.\(.*\)', '', i) for i in kraje2.kraje2]
kraje2.kraje2=[re.sub('VIET NAM', 'VIETNAM', i) for i in kraje2.kraje2]
kraje1.kraje1=[re.sub(',.*', '', i) for i in kraje1.kraje1]
kraje2.kraje2=[re.sub('.\(.*\)', '', i) for i in kraje2.kraje2]
kraje1.kraje1=[re.sub('&', 'AND', i) for i in kraje1.kraje1]
kraje2.kraje2=[re.sub('&', 'AND', i) for i in kraje2.kraje2]
kraje1=kraje1.sort_values('kraje1')
kraje2=kraje2.sort_values('kraje2')
print('')
kraje_tabela=kraje1.merge(kraje2, left_on='kraje1', right_on='kraje2', how='outer')
#352, 349 po usunieciu nawiasow w kraje1, 342 po zmianie wietnam i usunięciu rzeczy po przecinku, 338 po zamianie and

#co się powtarza po zmianach
print(pd.concat(g for _, g in kraje1.groupby("kraje1") if len(g) > 1))
#Congo i Korea (w kongo zamienić na kongo i demokratyczne kongo) z koreą tak samo
print(pd.concat(g for _, g in kraje2.groupby("kraje2") if len(g) > 1))
#Yugoslavia - zmieniła się w 1990 roku - ok

#Decyzje projektowe:
#-usunąć ZSRR
#- połączyć Francję i Monako z Francją
# z Czechosłowacji zrobić Czechy i SŁowację pół na pół
print(gdp.columns)
gdp_melt=pd.melt(gdp, id_vars=['Country Name'], value_vars=gdp.columns[4:])
gdp_melt.columns=['Country', 'Year', 'GDP']
populacja_melt=pd.melt(populacja, id_vars=['Country Name'], value_vars=gdp.columns[4:])
populacja_melt.columns=['Country', 'Year', 'Population']

merge1=pd.merge(gdp_melt,populacja_melt, how='outer')
merge1.Year=[int(i) for i in merge1.Year]
merged_all=pd.merge(merge1,co2,how='outer')
#co2['nowe'] = np.ones(co2.shape[0])

#for rok in [int(s) for s in gdp.columns if s.isnumeric()]:
#    for index, row in gdp.iterrows():
#        print(row['Country Name'], rok)
#        co2[(co2.Year==rok) & (co2.Country==row['Country Name'])].nowe=2
#        print(co2[(co2.Year==rok) & (co2.Country==row['Country Name'])].nowe)
print(co2.dtypes)
print(merge1.dtypes)
print('cos')
#print(co2[co2.Year==1960])
#print(co2.loc[(co2.Year==1960) & (co2.Country=='URUGUAY')])

