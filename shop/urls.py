from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopHome, name="shopHome"),
    path('flush-cart/', views.flushCart),
    path('checkout/', views.checkout, name="checkout"),
    path('shopmanager', views.shopmanager),
    path('thank-you/tracking-id=<int:pk>', views.thank_you, name="thankYou"),
]
