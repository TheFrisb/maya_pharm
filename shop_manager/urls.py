from django.urls import path
from shop_manager import views, api_views

app_name='shop_manager'
urlpatterns = [
    path('', views.redirect_to_dashboard, name="redirect"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/orders/<str:status>/", views.order_dashboard, name="orderDashboard"),

    path('api/confirm-order/', api_views.confirmOrder),
    path('api/delete-order/', api_views.deleteOrder),
    path('api/restore-order/', api_views.restoreOrder),
]
