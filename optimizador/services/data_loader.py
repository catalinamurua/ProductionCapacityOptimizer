import pandas as pd

class DataLoader:
    # Columnas que se esperan en el archivo CSV para poder cargar y validar correctamente
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
        # Constructor que recibe el archivo CSV (puede ser path o archivo subido)
        self.csv_file = csv_file
        self.dataframe = None  # Aquí se almacenará el DataFrame después de cargar y validar

    def load_and_validate(self):
        # Lectura del archivo CSV con pandas
        try:
            df = pd.read_csv(self.csv_file)
        except Exception as e:
            # Si ocurre algún error en la lectura, se lanza excepción con mensaje claro
            raise ValueError(f"Error leyendo el archivo CSV: {e}")

        # Verificamos que todas las columnas esperadas estén presentes en el CSV
        missing_cols = [col for col in self.expected_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Faltan columnas obligatorias en CSV: {missing_cols}")

        # Opcionalmente verificamos si hay columnas extras que no esperamos
        extra_cols = [col for col in df.columns if col not in self.expected_columns]
        if extra_cols:
            raise ValueError(f"El CSV contiene columnas no esperadas: {extra_cols}")

        # Validamos que todas las columnas esperadas tengan datos numéricos
        for col in self.expected_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(f"La columna '{col}' debe contener valores numéricos")

        # Verificamos que no existan valores faltantes (NaN) en las columnas esperadas
        if df[self.expected_columns].isnull().any().any():
            raise ValueError("El CSV contiene valores faltantes (NaN)")

        # Finalmente, se guarda el DataFrame con solo las columnas esperadas y validadas
        self.dataframe = df[self.expected_columns]

        # Retornamos el DataFrame validado para ser usado en el proceso
        return self.dataframe
