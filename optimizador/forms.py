from django import forms

from django import forms

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(label='Selecciona un archivo CSV * ')

    # Campos opcionales para sobrescribir parámetros existentes
    override_machine_1_hours = forms.FloatField(
        label='Horas disponibles Máquina 1 (opcional)',
        required=False,
        min_value=0
    )
    override_machine_2_hours = forms.FloatField(
        label='Horas disponibles Máquina 2 (opcional)',
        required=False,
        min_value=0
    )
    override_price_a = forms.FloatField(
        label='Precio Producto A (opcional)',
        required=False,
        min_value=0
    )
    override_price_b = forms.FloatField(
        label='Precio Producto B (opcional)',
        required=False,
        min_value=0
    )

    override_prod_a_time_m1 = forms.FloatField(
        label='Product A Production Time Machine 1 (opcional)',
        required=False,
        min_value=0
    )
    override_prod_a_time_m2 = forms.FloatField(
        label='Product A Production Time Machine 2 (opcional)',
        required=False,
        min_value=0
    )
    override_prod_b_time_m1 = forms.FloatField(
        label='Product B Production Time Machine 1 (opcional)',
        required=False,
        min_value=0
    )
    override_prod_b_time_m2 = forms.FloatField(
        label='Product B Production Time Machine 2 (opcional)',
        required=False,
        min_value=0
    )

    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']

        # Validar extensión
        if not file.name.endswith('.csv'):
            raise forms.ValidationError("Solo se permiten archivos CSV.")

        # Validar tipo MIME (opcional, pero ayuda)
        if file.content_type not in ['text/csv', 'application/vnd.ms-excel']:
            raise forms.ValidationError("El archivo no es un CSV válido.")

        # Validar tamaño (máximo 2MB)
        if file.size > 2 * 1024 * 1024:
            raise forms.ValidationError("El archivo es muy grande (máximo 2MB).")

        return file
