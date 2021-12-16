from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookView,
    IssueView
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'book', BookView, basename='book')
router.register(r'issue', IssueView, basename='issue')

app_name = 'book'
urlpatterns = [
    path('', include(router.urls)),
]
