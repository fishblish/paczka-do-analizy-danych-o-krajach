import pytest
import pandas as pd
import numpy as np
from src.package import obrobka_danych as od



@pytest.mark.parametrize("num1, num2, num3, num4, res1, res2", [(1960, 2014, 0, 0, 1960, 2014),
                                                                (2000, 2010, -3, 2020, 2000, 2010),
                                                                (1990, 2001, 0, 2000, 1990, 2000),
                                                                (1990, 2001, 1990, 2001, 1990, 2001)])
def test_wybor_daty1(num1: int, num2: int, num3: int, num4: int, res1: int, res2: int):
    assert od.wybor_dat(num1, num2, num3, num4) == [res1, res2]


df1 = {"Country": ["Poland", "USA", "Poland", "USA"], "Year": [2014, 2014, 2004, 2004], "Per Capita": [1, 2, 10, 4]}
df1 = pd.DataFrame(df1)
res1 = {"Country": ["USA", "Poland"], "2004": [4, 10], "2014": [2, 1], "Difference": [2, 9]}
res1= pd.DataFrame(res1)

df2 = {"Country": ["Mexico", "Italy", "Mexico", "Italy"], "Year": [2010, 2010, 2000, 2000], "Per Capita": [100, 20, 90, 40]}
df2 = pd.DataFrame(df2)
res2 = {"Country": ["Mexico", "Italy"], "2000": [90, 40], "2010": [100, 20], "Difference": [-10, 20]}
res2= pd.DataFrame(res2)

@pytest.mark.parametrize("merged, rok_koniec, res", [(df1, 2014, res1), (df2, 2010, res2)])
def test_differences(merged, rok_koniec, res):
    assert od.differences(merged, rok_koniec).equals(res)
