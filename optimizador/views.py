# optimizador/views.py

from django.shortcuts import render
from .forms import UploadCSVForm
from .services.data_loader import DataLoader
from .services.optimization import OptimizationModel
from .services.results_handler import ResultsHandler
from .services.validation import ValidacionParametros  # <-- Importa tu clase de validación
import os
from django.conf import settings
import pandas as pd

def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['csv_file']
            loader = DataLoader(file)
            data = loader.load_and_validate()
            
            row = data.iloc[0].copy()  # Copiamos la fila para modificar

            # Sobrescribir con valores opcionales si vienen
            if form.cleaned_data.get('override_machine_1_hours') is not None:
                row['Machine_1_Available_Hours'] = form.cleaned_data['override_machine_1_hours']

            if form.cleaned_data.get('override_machine_2_hours') is not None:
                row['Machine_2_Available_Hours'] = form.cleaned_data['override_machine_2_hours']

            if form.cleaned_data.get('override_price_a') is not None:
                row['Price_Product_A'] = form.cleaned_data['override_price_a']

            if form.cleaned_data.get('override_price_b') is not None:
                row['Price_Product_B'] = form.cleaned_data['override_price_b']

            if form.cleaned_data.get('override_prod_a_time_m1') is not None:
                row['Product_A_Production_Time_Machine_1'] = form.cleaned_data['override_prod_a_time_m1']

            if form.cleaned_data.get('override_prod_a_time_m2') is not None:
                row['Product_A_Production_Time_Machine_2'] = form.cleaned_data['override_prod_a_time_m2']

            if form.cleaned_data.get('override_prod_b_time_m1') is not None:
                row['Product_B_Production_Time_Machine_1'] = form.cleaned_data['override_prod_b_time_m1']

            if form.cleaned_data.get('override_prod_b_time_m2') is not None:
                row['Product_B_Production_Time_Machine_2'] = form.cleaned_data['override_prod_b_time_m2']

            # Validacion de Parametros del modelo
            try:
                validator = ValidacionParametros(row)
                validator.ejecutar_validaciones()
            except ValueError as e:
                # Si falla, mostrar el error en upload.html junto al form
                return render(request, 'upload.html', {
                    'form': form,
                    'error_message': str(e),
                })

            # Si pasa validación, construir modelo y resolver
            model = OptimizationModel(data=pd.DataFrame([row]))
            model.build_model()
            solution = model.solve()

            handler = ResultsHandler(solution, row)
            formatted = handler.format_results()

            # Guarda los gráficos
            image_path = os.path.join(settings.BASE_DIR, 'Optimizador/static', 'Cantidad_Producto.png')
            handler.generate_bar_chart(image_path)
            capacity_image_path = os.path.join(settings.BASE_DIR, 'Optimizador/static', 'Capacidad.png')
            handler.generate_capacity_usage_chart(capacity_image_path)

            # Diccionario explícito con parámetros usados
            final_params = {
                'Horas disponibles Máquina 1': row['Machine_1_Available_Hours'],
                'Horas disponibles Máquina 2': row['Machine_2_Available_Hours'],
                'Precio Producto A': row['Price_Product_A'],
                'Precio Producto B': row['Price_Product_B'],
                'Tiempo Producción A - Máquina 1': row['Product_A_Production_Time_Machine_1'],
                'Tiempo Producción A - Máquina 2': row['Product_A_Production_Time_Machine_2'],
                'Tiempo Producción B - Máquina 1': row['Product_B_Production_Time_Machine_1'],
                'Tiempo Producción B - Máquina 2': row['Product_B_Production_Time_Machine_2'],
            }

            return render(request, 'results.html', {
                'results': formatted,
                'chart_url': 'static/Cantidad_Producto.png',
                'capacity_chart_url': 'static/Capacidad.png',
                'data_row': final_params,
            })
    else:
        form = UploadCSVForm()
    return render(request, 'upload.html', {'form': form})
