
from django.contrib import admin
from store import views
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('faq/', views.faq, name="faq"),
    path('login_registration/', views.login_registration, name="login_registration"),
    path('user_registration/', views.user_registration, name="user_registration"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
