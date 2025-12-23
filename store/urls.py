from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("checkout/", views.checkout, name="checkout"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
]
