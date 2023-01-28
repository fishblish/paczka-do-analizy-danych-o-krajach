import pandas as pd


sciezka_dane1 = '/home/julia/PycharmProjects/projekt-zaliczeniowy/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv'
sciezka_dane2 = '/home/julia/PycharmProjects/projekt-zaliczeniowy/API_SP.POP.TOTL_DS2_en_csv_v2_4751604/API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv'
sciezka_dane3 = '/home/julia/PycharmProjects/projekt-zaliczeniowy/co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv'


gdp = pd.read_csv(sciezka_dane1, skiprows=3)
print(gdp.head(5))
populacja = pd.read_csv(sciezka_dane2, skiprows=3)
print(populacja.head(5))
co2 = pd.read_csv(sciezka_dane3, skiprows=0)
print(co2.head(5))

print(type[list(is(gdp.columns, int)))

