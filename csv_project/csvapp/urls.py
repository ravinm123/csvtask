# core/urls.py
from django.urls import path
from .views import CSVUploadView, ProcessedDataView, ProductSearchView

urlpatterns = [
    path('upload/', CSVUploadView.as_view(), name='csv_upload'),
    path('processed/<int:file_id>/', ProcessedDataView.as_view(), name='processed_data'),
    path('search/', ProductSearchView.as_view(), name='product_search'),
]