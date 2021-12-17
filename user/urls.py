from rest_framework import routers
from django.urls import path, include
from .views import (
    RegisterUser,
    ConfirmEmailView,
    LoginView,
    ForgotPassword,
    GoogleLogin,
    ResetPassword,
    ProfileViewSet,
    AddEmailPhoneProfile,
)

router = routers.SimpleRouter()
router.register(r'', RegisterUser, basename='register')
router.register(r'confirm', ConfirmEmailView, basename='confirm')
router.register(r'login', LoginView, basename='login')
router.register(r'forget_password', ForgotPassword, basename='forget_password')
router.register(r'reset_password', ResetPassword, basename='reset_password')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'add_field', AddEmailPhoneProfile, basename='add_field')

app_name = 'auth'
urlpatterns = [
    path('', include(router.urls)),
    path('google/', GoogleLogin.as_view(), name='google'),
]
