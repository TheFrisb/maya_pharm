from django.urls import path
from shop_manager import views

app_name='shop_manager'
urlpatterns = [
    path('', views.redirect_to_dashboard, name="redirect"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
