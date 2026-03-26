from django.urls import path
from .views import UploadView, JobDetailView, download_output

app_name = 'transform'

urlpatterns = [
    path('', UploadView.as_view(), name='upload'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('jobs/<int:pk>/download/', download_output, name='download'),
]
