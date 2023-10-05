from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.shop_home, name="shop_home"),
    path('product/', views.product_page, name="product_page"),
    path('checkout/', views.checkout, name="checkout"),
    path('thank-you/tracking-id=<int:pk>', views.thank_you, name="thank_you"),
]
