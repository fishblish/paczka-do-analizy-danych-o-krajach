import pytest
import pandas as pd
from src.package import obrobka_danych as od



@pytest.mark.parametrize("num1, num2, num3, num4, res1, res2", [(1960, 2014, 0, 0, 1960, 2014),
                                                                (2000, 2010, -3, 2020, 2000, 2010),
                                                                (1990, 2001, 0, 2000, 1990, 2000),
                                                                (1990, 2001, 1990, 2001, 1990, 2001)])
def test_wybor_daty1(num1: int, num2: int, num3: int, num4: int, res1: int, res2: int):
    assert od.wybor_dat(num1, num2, num3, num4) == [res1, res2]

@pytest.mark.parametrize(
