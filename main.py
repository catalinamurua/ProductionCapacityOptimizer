import os
import pandas as pd
from optimizador.services.data_loader import DataLoader
from optimizador.services.optimization import OptimizationModel
from optimizador.services.results_handler import ResultsHandler  # Asumo que existe

def main():
    # Ruta al archivo CSV (puedes cambiar a la ruta correcta)
    csv_path = "example_data.csv"

    # Crear instancia del DataLoader y cargar/validar datos
    loader = DataLoader(csv_path)
    data = loader.load_and_validate()  # Método que devuelve un DataFrame validado

    # Para simplificar tomamos la primera fila (o la única) como parámetros
    row = data.iloc[0]

    # Crear y ejecutar el modelo de optimización
    opt_model = OptimizationModel(data=pd.DataFrame([row]))
    opt_model.build_model()
    resultados = opt_model.solve()

    # Crear carpeta output si no existe
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Generar gráficos con ResultsHandler (asumiendo que toma resultados y parámetros)
    handler = ResultsHandler(resultados, row)
    cantidad_path = os.path.join(output_dir, "Cantidad_Producto.png")
    capacity_path = os.path.join(output_dir, "Capacidad.png")
    handler.generate_bar_chart(cantidad_path)
    handler.generate_capacity_usage_chart(capacity_path)

    # Imprimir resultados con formato
    print("=== Parámetros usados para la optimización ===")
    for param, val in row.items():
        print(f"{param}: {val}")

    print("\n=== Resultados de la optimización ===")
    # Suponiendo que resultados es un dict o tiene atributos accesibles
    for key, val in resultados.items():
        print(f"{key}: {val}")

    print(f"\nGráficos guardados en carpeta '{output_dir}':")
    print(f" - Unidades producidas: {cantidad_path}")
    print(f" - Uso de capacidad: {capacity_path}")

if __name__ == "__main__":
    main()

