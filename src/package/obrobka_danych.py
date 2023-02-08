import pandas as pd
import re
pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', None)


def wybor_dat(rok_start, rok_koniec, start_user=0, end_user=0):
    if(start_user==0):
        start_user=rok_start
        print('Ustawienie domyślnej daty startu:', rok_start)
    if(end_user==0):
        end_user=rok_koniec
        print('Ustawienie domyślnej daty końcowej:', rok_koniec)
    if(start_user>end_user):
        print('Data startu późniejsza niż data końcowa.\nUstawienie domyślnego przedziału czasu: od', rok_start, 'do', rok_koniec)
        start_user=rok_start
        end_user=rok_koniec
    if(start_user<rok_start):
        print('Za wczesna data startowa, brak danych. Ustawienie domyślnej daty startowej', rok_start)
        start_user=rok_start
    if(end_user>rok_koniec):
        print('Za późna data końcowa, brak danych. Ustawienie domyślnej daty końcowej', rok_koniec)
        end_user=rok_koniec
    return [start_user, end_user]

def wstepna_obrobka_danych(gdp, populacja, co2, rok_start, rok_koniec):
    #usunięcie ostatniej kolumny jeśli jest pusta
    if gdp.iloc[:,len(gdp.columns)-1].isna().sum() == len(gdp.iloc[:,len(gdp.columns)-1]):
        gdp=gdp.drop(gdp.columns[len(gdp.columns)-1], axis=1)

    if populacja.iloc[:,len(populacja.columns)-1].isna().sum() == len(populacja.iloc[:,len(populacja.columns)-1]):
        populacja=populacja.drop(populacja.columns[len(populacja.columns)-1], axis=1)

    #ogarnieczenie danych do wybrych dat
    gdp_index_start=gdp.columns.get_loc(str(rok_start))
    gdp_index_koniec=gdp.columns.get_loc(str(rok_koniec))

    a=list(range(0,4)) + list(range(gdp_index_start,gdp_index_koniec+1))
    gdp=gdp.iloc[:, a]

    populacja_index_start=populacja.columns.get_loc(str(rok_start))
    populacja_index_koniec=populacja.columns.get_loc(str(rok_koniec))

    a=list(range(0,4)) + list(range(populacja_index_start,populacja_index_koniec+1))
    populacja=populacja.iloc[:, a]

    co2=co2[(co2.Year>=rok_start) & (co2.Year<=rok_koniec)]

    #zmienianie nazw krajów na wielkie litery
    gdp['Country Name']=[i.upper() for i in gdp['Country Name']]
    populacja['Country Name']=[i.upper() for i in populacja['Country Name']]

    #poprawki w nazwach krajów
    co2['Country']=[re.sub('VIET NAM', 'VIETNAM', i) for i in co2['Country']]
    gdp['Country Name']=[re.sub('&', 'AND', i) for i in gdp['Country Name']]
    populacja['Country Name']=[re.sub('&', 'AND', i) for i in populacja['Country Name']]
    co2['Country']=[re.sub('&', 'AND', i) for i in co2['Country']]

    #zmiana formatu tabel
    gdp_melt=pd.melt(gdp, id_vars=['Country Name'], value_vars=gdp.columns[4:])
    gdp_melt.columns=['Country', 'Year', 'GDP']
    populacja_melt=pd.melt(populacja, id_vars=['Country Name'], value_vars=gdp.columns[4:])
    populacja_melt.columns=['Country', 'Year', 'Population']

    #połączenie danych
    merge1=pd.merge(gdp_melt,populacja_melt, how='outer')
    merge1.Year=[int(i) for i in merge1.Year]
    merged=pd.merge(merge1,co2,how='outer')
    return merged

#PIERWSZE ZADANIE
def max_co2(merged):
    max_co2=merged.groupby(['Year'], sort=False)['Per Capita'].nlargest(5).droplevel(1)
    max_co2=max_co2.to_frame().reset_index()
    max_co2=pd.merge(max_co2, merged, how='inner')
    max_co2=max_co2[['Year', 'Country', 'Per Capita', 'Total']]
    print("\nWynik pierwszego zadania: maksymalna emisjia co2\n",max_co2)
    return max_co2

#DRUGIE ZADANIE
def max_gdp(merged):
    merged['GDP Per Capita'] = merged.GDP/merged.Population
    max_gdp=merged.groupby(['Year'], sort=False)['GDP Per Capita'].nlargest(5).droplevel(1)
    max_gdp=max_gdp.to_frame().reset_index()
    max_gdp=pd.merge(max_gdp, merged, how='inner')
    max_gdp=max_gdp[['Year', 'Country', 'GDP', 'GDP Per Capita']]
    print("\nWynik drugiego zadania: maksymalne GDP na osobę\n", max_gdp)
    return max_gdp

#TRZECIE ZADANIE
def differences(merged, rok_koniec):
    rok_koniec10=rok_koniec-10
    tab=merged[(merged.Year==rok_koniec10) | (merged.Year==rok_koniec)][['Year', 'Country', 'Per Capita']]
    tab=tab.pivot(index='Country', columns='Year')['Per Capita']
    tab = tab.reset_index()
    tab.columns=[str(i) for i in tab.columns]
    tab['Difference'] = tab.iloc[:,1] - tab.iloc[:,2]
    maks=max(tab.Difference)
    mini=min(tab.Difference)
    wynik_max=tab[tab.Difference==maks]
    wynik_min=tab[tab.Difference==mini]
    print("\nWynik trzeciego zadania: najmniejsza różnica w emisji co2 w ciągu ostatnich 10 lat\n", wynik_min)
    print("\nWynik trzeciego zadania: największa różnica w emisji co2 w ciągu ostatnich 10 lat\n", wynik_max)
    return pd.concat([wynik_min, wynik_max]).reset_index(drop=True)
