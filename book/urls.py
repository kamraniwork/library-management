from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookView
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'book', BookView, basename='book')

app_name = 'book'
urlpatterns = [
    path('', include(router.urls)),
]
