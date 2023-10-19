from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.shop_home, name="shop_home"),
    path('product/<str:name>/', views.product_page, name="product_page"),
    path('product-category/<str:slug>/', views.category_page, name="category_page"),
    path('checkout/', views.checkout, name="checkout"),
    path('thank-you/', views.thank_you_page, name="thank_you_page"),
]
