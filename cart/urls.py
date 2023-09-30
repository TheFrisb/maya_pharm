from django.urls import path
from . import views  # Django rest framework views

from . import views_without_DjangoRestFramework
urlpatterns = [
    path('add-to-cart/', views_without_DjangoRestFramework.addToCart, name="addToCart"),
    path('update-cart-item/', views_without_DjangoRestFramework.updateCartItem, name="updateCartItem"),
    path('remove-from-cart/', views_without_DjangoRestFramework.removeFromCart, name="removeFromCart"),
]

# urlpatterns = [
#     path('actions/', views.CartView.as_view(), name='cartActions'),
# ]
