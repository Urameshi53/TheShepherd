from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

from . import views 

app_name = "sliders"

urlpatterns = [
    path("", views.IndexView.as_view(), name="sliders"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    #path("<int:pk>/", views.DetailView.as_view(), name="discuss"),
    #path("", views.SearchView.as_view(), name="search"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)