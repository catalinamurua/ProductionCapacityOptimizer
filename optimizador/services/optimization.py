from pulp import LpProblem, LpMaximize, LpVariable, LpStatus, value, LpInteger

class OptimizationModel:
    def __init__(self, data):
        """
        data: pd.DataFrame con las columnas validadas,
            asumiendo solo UNA fila con los parámetros.
        """
        self.data = data.iloc[0]  # Tomamos la fila con los parámetros
        self.model = None
        self.result = {}

    def build_model(self):
        # Crea problema de maximización
        prob = LpProblem("Maximize_Revenue", LpMaximize)

        # Variables: cantidad a producir de A y B (enteras o continuas, según contexto)
        x_a = LpVariable('x_a', lowBound=0,cat=LpInteger)  # Cantidad producto A
        x_b = LpVariable('x_b', lowBound=0,cat=LpInteger)  # Cantidad producto B

        # Coeficientes (tiempos de producción por producto y máquina)
        # Extraemos de la fila de datos
        t_a1 = self.data['Product_A_Production_Time_Machine_1']
        t_a2 = self.data['Product_A_Production_Time_Machine_2']
        t_b1 = self.data['Product_B_Production_Time_Machine_1']
        t_b2 = self.data['Product_B_Production_Time_Machine_2']

        # Horas disponibles máquinas
        t_m1 = self.data['Machine_1_Available_Hours']
        t_m2 = self.data['Machine_2_Available_Hours']

        # Precios de productos
        p_a = self.data['Price_Product_A']
        p_b = self.data['Price_Product_B']

        # Función objetivo: maximizar ingresos
        prob += p_a * x_a + p_b * x_b, "Maximizacion_Ingresos"

        # Restricciones de capacidad de máquinas
        prob += t_a1 * x_a + t_b1 * x_b <= t_m1, "Tiempo_disponible_Maq1"
        prob += t_a2 * x_a + t_b2 * x_b <= t_m2, "Tiempo_disponible_Maq2"

        self.model = prob
        self.variables = (x_a, x_b)

    def solve(self):
        if self.model is None:
            self.build_model()

        # Resuelve el modelo
        status = self.model.solve()

        if LpStatus[self.model.status] != 'Optimal':
            raise Exception(f"No se encontró solución óptima. Status: {LpStatus[self.model.status]}")

        x_a, x_b = self.variables

        # Guarda resultados
        self.result = {
            'Product_A_units': x_a.varValue,
            'Product_B_units': x_b.varValue,
            'Total_Revenue': value(self.model.objective)
        }

        return self.result
