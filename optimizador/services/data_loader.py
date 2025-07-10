import pandas as pd

class DataLoader:
    expected_columns = [
        "Product_A_Production_Time_Machine_1",
        "Product_A_Production_Time_Machine_2",
        "Product_B_Production_Time_Machine_1",
        "Product_B_Production_Time_Machine_2",
        "Machine_1_Available_Hours",
        "Machine_2_Available_Hours",
        "Price_Product_A",
        "Price_Product_B",
    ]

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.dataframe = None

    def load_and_validate(self):
        # Leer CSV con pandas
        try:
            df = pd.read_csv(self.csv_file)
        except Exception as e:
            raise ValueError(f"Error leyendo el archivo CSV: {e}")

        # Verificar columnas
        missing_cols = [col for col in self.expected_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Faltan columnas obligatorias en CSV: {missing_cols}")

        # Opcional: verificar que no haya columnas extras (si quieres estrictura exacta)
        extra_cols = [col for col in df.columns if col not in self.expected_columns]
        if extra_cols:
            raise ValueError(f"El CSV contiene columnas no esperadas: {extra_cols}")

        # Validar tipos: todas las columnas deben ser numéricas
        for col in self.expected_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(f"La columna '{col}' debe contener valores numéricos")

        # Validar que no haya valores NaN
        if df[self.expected_columns].isnull().any().any():
            raise ValueError("El CSV contiene valores faltantes (NaN)")

        # Guardar dataframe validado
        self.dataframe = df[self.expected_columns]

        return self.dataframe
