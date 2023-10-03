from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.shopHome, name="shopHome"),
    path('checkout/', views.checkout, name="checkout"),
    path('thank-you/tracking-id=<int:pk>', views.thank_you, name="thankYou"),
]
