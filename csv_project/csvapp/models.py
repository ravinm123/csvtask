from django.db import models

class CSVFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    

class ProcessedData(models.Model):
    csv_file = models.OneToOneField(CSVFile, on_delete=models.CASCADE, related_name='processed_data')
    total_revenue = models.FloatField()
    avg_discount = models.FloatField()
    best_selling_product = models.CharField(max_length=255)
    most_profitable_product = models.CharField(max_length=255)
    max_discount_product = models.CharField(max_length=255)

    def __str__(self):
        return f"Processed Data for {self.csv_file.file.name}"