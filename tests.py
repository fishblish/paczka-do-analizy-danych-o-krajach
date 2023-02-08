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


df1 = {"Country": ["Poland", "USA", "Poland", "USA"], "Year": [2014, 2014, 2004, 2004], "Per Capita": [1, 2, 3, 4]}
df1 = pd.DataFrame(df1)
res = {"Country": ["Poland"], 2004: [7], 2014: [5], "Difference": [6]}


@pytest.mark.parametrize(df1, 2013, res)
def test_differences(merged, rok_koniec, res):
    assert od.differences(merged, rok_koniec) == res
