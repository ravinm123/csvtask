import pandas as pd
from celery import shared_task
from .models import CSVFile

@shared_task
def process_csv(file_id):
    csv_file = CSVFile.objects.get(id=file_id)
    df = pd.read_csv(csv_file.file.path)

    required_columns = ['Product Name', 'Sales', 'Quantity', 'Discount', 'Profit']
    if not all(col in df.columns for col in required_columns):
        return {'error': 'Invalid CSV format'}

    # Convert numeric columns
    for col in ['Sales', 'Quantity', 'Discount', 'Profit']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Perform calculations
    total_revenue = df['Sales'].sum()
    avg_discount = df['Discount'].mean()
    best_selling_product = df.groupby('Product Name')['Quantity'].sum().idxmax()
    most_profitable_product = df.groupby('Product Name')['Profit'].sum().idxmax()
    max_discount_product = df.groupby('Product Name')['Discount'].max().idxmax()

    result = {
        'total_revenue': total_revenue,
        'avg_discount': avg_discount,
        'best_selling_product': best_selling_product,
        'most_profitable_product': most_profitable_product,
        'max_discount_product': max_discount_product
    }

    csv_file.result = result
    csv_file.processed = True
    csv_file.save()
    return result
