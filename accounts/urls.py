from django.urls import path
from .views import AccountView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('accounts/', AccountView.as_view()),
    path('login/', jwt_views.TokenObtainPairView.as_view()),
]