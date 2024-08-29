from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

from . import views 

app_name = "repository"

urlpatterns = [
    path("", views.IndexView.as_view(), name="repository"),
    path("<int:owner_id>/upload_file/", views.upload_file , name="upload_file"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
