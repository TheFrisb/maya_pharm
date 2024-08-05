from django.urls import path

from . import views

app_name = "shop"
urlpatterns = [
    path("", views.shop_home, name="shop_home"),
    path("product/<str:name>/", views.product_page, name="product_page"),
    path("product-category/<str:slug>/", views.category_page, name="category_page"),
    path("brand/<str:slug>/", views.brand_view, name="brand_view"),
    path("checkout/", views.checkout, name="checkout"),
    path(
        "thank-you/<str:tracking_number>", views.thank_you_page, name="thank_you_page"
    ),
    path("search-results/", views.search_page, name="search_page"),
    path("api/v1/search-product-titles/", views.product_titles, name="product_titles"),
    path("contact-us/", views.contact_us, name="contact_page"),
]
