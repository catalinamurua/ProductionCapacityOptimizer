import pandas as pd
import pytest
from optimizador.services.data_loader import DataLoader

def test_valid_csv_loads_correctly(tmp_path):
    content = """Product_A_Production_Time_Machine_1,Product_A_Production_Time_Machine_2,Product_B_Production_Time_Machine_1,Product_B_Production_Time_Machine_2,Machine_1_Available_Hours,Machine_2_Available_Hours,Price_Product_A,Price_Product_B
2,3,4,5,100,100,10,15
"""
    file = tmp_path / "test.csv"
    file.write_text(content)

    loader = DataLoader()
    df = loader.load(file)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 8)
