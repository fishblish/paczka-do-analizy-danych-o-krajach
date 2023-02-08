import argparse
import pandas as pd
import obrobka_danych as od


#sciezka_bazowa='/home/students/mat/j/jb417512/python/'
sciezka_bazowa='/home/julia/Documents/python/projekt/'

parser = argparse.ArgumentParser()
parser.add_argument("sciezka_gdp", type=str, nargs="?", default= sciezka_bazowa + 'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv', help="Ścieżka do danych o GDP")
parser.add_argument("sciezka_populacja", type=str, nargs="?", default= sciezka_bazowa + 'API_SP.POP.TOTL_DS2_en_csv_v2_4751604/API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv', help="Ścieżka do danych o populacji")
parser.add_argument("sciezka_co2", type=str, nargs="?", default= sciezka_bazowa + 'co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv', help="Ścieżka do danych o emisji co2")
parser.add_argument("--sd", type=int, default=0, help="Data początkowa")
parser.add_argument("--ed", type=int, default=0, help="Data końcowa")

args = parser.parse_args()

gdp = pd.read_csv(args.sciezka_gdp, skiprows=3)
populacja = pd.read_csv(args.sciezka_populacja, skiprows=3)
co2 = pd.read_csv(args.sciezka_co2, skiprows=0)

#usunięcie ostatniej kolumny jeśli jest pusta
if gdp.iloc[:,len(gdp.columns)-1].isna().sum() == len(gdp.iloc[:,len(gdp.columns)-1]):
    gdp=gdp.drop(gdp.columns[len(gdp.columns)-1], axis=1)

if populacja.iloc[:,len(populacja.columns)-1].isna().sum() == len(populacja.iloc[:,len(populacja.columns)-1]):
    populacja=populacja.drop(populacja.columns[len(populacja.columns)-1], axis=1)

[int(s) for s in gdp.columns if s.isnumeric()]
gdp_lata = [eval(i) for i in list(gdp.columns) if i.isnumeric()]
populacja_lata = [eval(i) for i in list(populacja.columns) if i.isnumeric()]

rok_start=max(min(gdp_lata), min(populacja_lata), min(co2.Year))
rok_koniec=min(max(gdp_lata), max(populacja_lata), max(co2.Year))
print('\nDostępny zakres lat to od', rok_start, 'do', rok_koniec)

start_user=args.sd
end_user=args.ed

#zrobić z tego funkcję wyboru dat
if(start_user==0):
    print('Ustawienie domyślnej daty startu:', rok_start)
if(end_user==0):
    print('Ustawienie domyślnej daty końcowej:', rok_koniec)
if((start_user>end_user) & (start_user!=0) & (end_user!=0)):
    print('Data startu późniejsza niż data końcowa.\nUstawienie domyślnego przedziału czasu: od', rok_start, 'do', rok_koniec)
if(start_user!=0):
    if(start_user>=rok_start):
        rok_start = start_user
        print('Ustawienie daty startu na', start_user)
    else:
        print('Brak danych dla podanej daty startowej.\nUstawienie domyślej daty startu:', rok_start)
if(end_user!=0):
    if(end_user>=rok_koniec):
        rok_koniec = end_user
        print('Ustawienie daty startu na', start_user)
    else:
        print('Brak danych dla podanej daty startowej.\nUstawienie domyślej daty startu:', rok_koniec)


merged = od.wstepna_obrobka_danych(gdp, populacja, co2)
od.max_gdp(merged)
od.max_co2(merged)
od.differences(merged)
