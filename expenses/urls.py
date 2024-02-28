from django.urls import path
from expenses import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('chart', views.chart, name='chart_expenses'),
    path('get_chart_data', views.get_chart_data, name='get_chart_data_expenses'),
    path('create_pdf', views.create_pdf, name='create_pdf_expenses'),
    path('import_excel', views.import_excel, name='import_excel_expenses'),
    path('add', views.add, name='add_expenses'),
    path('edit/<int:id>', views.edit, name='edit_expenses'),
    path('delete/<int:id>', views.delete, name='delete_expenses'),
]



