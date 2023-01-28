import argparse
import pandas as pd
#from morse import morse

sciezka_bazowa='/home/students/mat/j/jb417512/python/'
#sciezka_bazowa='/home/julia/PycharmProjects/projekt-zaliczeniowy/'

parser = argparse.ArgumentParser()
parser.add_argument("sciezka_dane1", type=str, nargs="?", default= sciezka_bazowa + 'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv', help="Ścieżka do pierwszych danych")
parser.add_argument("sciezka_dane2", type=str, nargs="?", default= sciezka_bazowa + 'API_SP.POP.TOTL_DS2_en_csv_v2_4751604/API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv', help="Ścieżka do drugich danych")
parser.add_argument("sciezka_dane3", type=str, nargs="?", default= sciezka_bazowa + 'co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv', help="Ścieżka do trzecich danych")

#parser.add_argument("ścieżka_dane2", help="Ścieżka do drugich danych")

args = parser.parse_args()

print(args.sciezka_dane1)
dane1 = pd.read_csv(args.sciezka_dane1, skiprows=3)
print(dane1.head(5))
dane2 = pd.read_csv(args.sciezka_dane2, skiprows=3)
print(dane2.head(5))
dane3 = pd.read_csv(args.sciezka_dane3, skiprows=0)
print(dane3.head(5))

