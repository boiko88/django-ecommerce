
from django.contrib import admin
from store import views
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
]
