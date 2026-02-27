from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rescue/', views.rescue_request_view, name='rescue_request'),
    path('adoptions/', views.adoptions_view, name='adoptions'),
    path('adopt/<int:animal_id>/', views.adopt_animal, name='adopt_animal'),
    path('products/', views.products_view, name='products'),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('services/', views.services_view, name='services'),
    path('book/<int:plan_id>/', views.book_service, name='book_service'),
    path('about/', views.about_view, name='about'),
]
