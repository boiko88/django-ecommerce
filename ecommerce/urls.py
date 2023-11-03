
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
    path('update_item/', views.update_item, name="update_item"),
    path('process_order/', views.process_order, name="process_order"),
    path('faq/', views.faq, name="faq"),
    path('login_registration/', views.login_registration, name="login_registration"),
    path('user_registration/', views.user_registration, name="user_registration"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('description/', views.description, name="description"),
    path('create_comment/', views.create_comment, name="create_comment"),
    path('change_password/', views.change_password, name="change_password"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
