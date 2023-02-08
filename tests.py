import pytest
import pandas as pd
from package import obrobka_danych as od


def test_clean():
    df1 = {"Country Name": ["Poland", "USA", "Mexico"], "Country Code": ["1", "2", "3"], "col3": ["1", "2", "3"],
           "col4": ["1", "2", "3"], "1960": [3, 4, 5], "1961": [4, 5, 6]}
    df1 = pd.DataFrame(df1)
    df1 = od.clean(df1)
    assert list(df1["Country"]) == ["POLAND", "USA", "MEXICO"]
