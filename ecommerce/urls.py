
from django.contrib import admin
from store import views
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
]
