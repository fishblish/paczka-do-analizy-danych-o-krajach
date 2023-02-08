import argparse
import pandas as pd
from . import obrobka_danych as od

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

#wybór dostępnych lat w danych
gdp_lata = [eval(i) for i in list(gdp.columns) if i.isnumeric()]
populacja_lata = [eval(i) for i in list(populacja.columns) if i.isnumeric()]

rok_start=max(min(gdp_lata), min(populacja_lata), min(co2.Year))
rok_koniec=min(max(gdp_lata), max(populacja_lata), max(co2.Year))

#ustalenie przedziału czasu
start_user=args.sd
end_user=args.ed

przedzial_czasu=od.wybor_dat(rok_start, rok_koniec, start_user, end_user)
rok_start=przedzial_czasu[0]
rok_koniec=przedzial_czasu[1]

#wywołanie odpowiednich funkcji
merged = od.wstepna_obrobka_danych(gdp, populacja, co2, rok_start, rok_koniec)
od.max_co2(merged)
od.max_gdp(merged)
od.differences(merged, rok_koniec)
