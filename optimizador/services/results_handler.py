# optimizador/services/results_handler.py

import matplotlib.pyplot as plt
import os

class ResultsHandler:
    def __init__(self, solution, data=None):
        """
        solution_dict debe tener claves como:
        {
            'Product_A_units': 50,
            'Product_B_units': 30,
            'Total_Revenue': 5000
        }
        """
        self.solution = solution
        self.data = data

    def format_results(self):
        """Retorna los resultados en formato listo para mostrar en el template"""
        return {
            "product_a_units": self.solution.get("Product_A_units", 0),
            "product_b_units": self.solution.get("Product_B_units", 0),
            "total_revenue": self.solution.get("Total_Revenue", 0),
        }

    def generate_bar_chart(self, output_path):
        """Genera un gráfico simple de unidades producidas"""
        labels = ['Producto A', 'Producto B']
        values = [self.solution.get("Product_A_units", 0), self.solution.get("Product_B_units", 0)]

        plt.figure(figsize=(6, 4))
        plt.bar(labels, values, color=['#4CAF50', '#2196F3'])
        plt.title('Unidades producidas')
        plt.ylabel('Cantidad')
        plt.tight_layout()

        # Asegúrate de que la carpeta existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        plt.savefig(output_path)
        plt.close()

    def generate_capacity_usage_chart(self, output_path):
        """Genera un gráfico del uso de capacidad por máquina"""


        x_a = self.solution.get('Product_A_units', 0)
        x_b = self.solution.get('Product_B_units', 0)
        # Horas usadas máquina 1 y 2
        uso_m1 = self.data['Product_A_Production_Time_Machine_1'] * x_a + \
                 self.data['Product_B_Production_Time_Machine_1'] * x_b

        uso_m2 = self.data['Product_A_Production_Time_Machine_2'] * x_a + \
                 self.data['Product_B_Production_Time_Machine_2'] * x_b

        disponible_m1 = self.data['Machine_1_Available_Hours']
        disponible_m2 = self.data['Machine_2_Available_Hours']

        labels = ['Máquina 1', 'Máquina 2']
        usados = [uso_m1, uso_m2]
        disponibles = [disponible_m1, disponible_m2]

        x = range(len(labels))

        plt.figure(figsize=(6, 4))
        plt.bar(x, usados, width=0.4, label='Usado', color='#FF5722')
        plt.bar([i + 0.4 for i in x], disponibles, width=0.4, label='Disponible', color='#B0BEC5')
        plt.xticks([i + 0.2 for i in x], labels)
        plt.title('Uso de capacidad por máquina (horas)')
        plt.ylabel('Horas')
        plt.legend()
        plt.tight_layout()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close()