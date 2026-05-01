from django.urls import path
from . import views

app_name = 'femr_export'

urlpatterns = [
    path('', views.index, name='index'),
    path('run/', views.run_job, name='run_job'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/log/', views.log_poll, name='log_poll'),
    path('jobs/<int:pk>/download/<str:filename>/', views.download_file, name='download_file'),
]
