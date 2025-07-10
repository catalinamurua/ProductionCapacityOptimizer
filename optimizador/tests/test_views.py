from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_upload_page_loads(self):
        response = self.client.get(reverse('upload_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload.html')

    def test_upload_valid_csv_returns_result(self):
        content = b"""Product_A_Production_Time_Machine_1,Product_A_Production_Time_Machine_2,Product_B_Production_Time_Machine_1,Product_B_Production_Time_Machine_2,Machine_1_Available_Hours,Machine_2_Available_Hours,Price_Product_A,Price_Product_B
1.5,2,1,1.5,8,10,100,80
"""
        uploaded_file = SimpleUploadedFile("data.csv", content, content_type="text/csv")
        response = self.client.post(reverse('upload_csv'), {'csv_file': uploaded_file})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'results.html')
        self.assertIn(b"Ingresos Totales", response.content)
