import pandas as pd
from optimizador.services.optimization import OptimizationModel

def test_optimization_finds_solution():
    # Define un DataFrame con parámetros de entrada válidos
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

    # Instancia el modelo de optimización con los datos
    model = OptimizationModel(df)
    # Ejecuta la solución del modelo
    result = model.solve()

    # Verifica que la cantidad producida del Producto A sea cero o más
    assert result['Product_A_units'] >= 0
    # Verifica que la cantidad producida del Producto B sea cero o más
    assert result['Product_B_units'] >= 0
    # Verifica que los ingresos totales sean mayores a cero
    assert result['Total_Revenue'] > 0
