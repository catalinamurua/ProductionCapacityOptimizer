from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadViewTests(TestCase):
    def setUp(self):
        # Se instancia el cliente de pruebas para hacer peticiones a la app
        self.client = Client()

    def test_upload_page_loads(self):
        # Se hace una petición GET a la url 'upload_csv'
        response = self.client.get(reverse('upload_csv'))
        # Se verifica que el estado HTTP sea 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Se verifica que la plantilla usada sea 'upload.html'
        self.assertTemplateUsed(response, 'upload.html')

    def test_upload_valid_csv_returns_result(self):
        # Se crea un archivo CSV válido como bytes
        content = b"""Product_A_Production_Time_Machine_1,Product_A_Production_Time_Machine_2,Product_B_Production_Time_Machine_1,Product_B_Production_Time_Machine_2,Machine_1_Available_Hours,Machine_2_Available_Hours,Price_Product_A,Price_Product_B
1.5,2,1,1.5,8,10,100,80
"""
        # Se crea un archivo simulado para subirlo en la prueba
        uploaded_file = SimpleUploadedFile("data.csv", content, content_type="text/csv")
        # Se hace una petición POST enviando el archivo CSV
        response = self.client.post(reverse('upload_csv'), {'csv_file': uploaded_file})

        # Se verifica que el estado HTTP sea 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Se verifica que la plantilla usada sea 'results.html'
        self.assertTemplateUsed(response, 'results.html')
        # Se comprueba que el contenido de la respuesta incluye el texto "Ingresos Totales"
        self.assertIn(b"Ingresos Totales", response.content)
