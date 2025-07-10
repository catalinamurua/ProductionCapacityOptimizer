import pandas as pd
from optimizador.services.optimization import OptimizationModel

def test_optimization_finds_solution():
    df = pd.DataFrame([{
        "Product_A_Production_Time_Machine_1": 2,
        "Product_A_Production_Time_Machine_2": 3,
        "Product_B_Production_Time_Machine_1": 4,
        "Product_B_Production_Time_Machine_2": 5,
        "Machine_1_Available_Hours": 100,
        "Machine_2_Available_Hours": 100,
        "Price_Product_A": 10,
        "Price_Product_B": 15
    }])

    model = OptimizationModel(df)
    result = model.solve()

    assert result['Product_A_units'] >= 0
    assert result['Product_B_units'] >= 0
    assert result['Total_Revenue'] > 0
