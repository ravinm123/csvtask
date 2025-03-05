# core/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .serializers import CSVUploadSerializer,ProductSearchSerializer
from .tasks import process_csv
from .models import CSVFile, ProcessedData
import pandas as pd
from rest_framework import status

class CSVUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = CSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.save()
            process_csv.delay(csv_file.id)
            return Response({'message': 'File uploaded successfully.', 'file_id': csv_file.id}, status=201)
        return Response(serializer.errors, status=400)


class ProcessedDataView(APIView):
    def get(self, request, file_id, *args, **kwargs):
        try:
            csv_file = CSVFile.objects.get(id=file_id)
            processed_data = getattr(csv_file, 'processed_data', None)

            if not processed_data:
                return Response({'message': 'File is still being processed.'}, status=202)

            return Response({
                'total_revenue': processed_data.total_revenue,
                'avg_discount': processed_data.avg_discount,
                'best_selling_product': processed_data.best_selling_product,
                'most_profitable_product': processed_data.most_profitable_product,
                'max_discount_product': processed_data.max_discount_product,
            }, status=200)
        except CSVFile.DoesNotExist:
            return Response({'message': 'File not found.'}, status=404)


class ProductSearchView(APIView):
    def get(self, request, *args, **kwargs):
        # Step 1: Get and validate the query parameter
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'message': 'Query parameter "q" is required.'}, status=400)

        results = []

        
        for processed_data in ProcessedData.objects.all():
            try:
                
                file_path = processed_data.csv_file.file.path
                print(f"Loading file: {file_path}")  # Debugging: Print the file path
                df = pd.read_csv(file_path, skip_blank_lines=True)

                
                df.columns = df.columns.str.strip()  
                if 'Product Name' not in df.columns:
                    print(f"Missing 'Product Name' column in file: {file_path}")
                    continue  
                df['Product Name'] = df['Product Name'].str.strip() 
                
                filtered_data = df[df['Product Name'].str.contains(query, case=False, na=False)]
                print(f"Filtered data for query '{query}': {filtered_data}")  

                
                results.extend(filtered_data.to_dict(orient='records'))
            except Exception as e:
                print(f"Error processing file {file_path}: {e}") 

        
        serializer = ProductSearchSerializer(results, many=True)
        return Response(serializer.data, status=200)
