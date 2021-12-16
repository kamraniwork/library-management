from rest_framework.viewsets import ViewSet, ModelViewSet
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Book, Issue
from .serializers import BookListSerializers, BookDetailSerializers
from django.shortcuts import get_object_or_404


class BookView(ViewSet):
    lookup_field = 'slug'

    def list(self, request):
        book_list = Book.objects.filter(status='p')
        serializer = BookListSerializers(instance=book_list, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        book_obj = get_object_or_404(Book, status='p', slug=slug)
        serializer = BookDetailSerializers(instance=book_obj, context={'request': request})
        return Response(serializer.data)
