from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('add-to-cart/', views.addToCart, name="addToCart"),
    path('update-cart-item/', views.updateCartItem, name="updateCartItem"),
    path('remove-from-cart/', views.removeFromCart, name="removeFromCart"),
]

