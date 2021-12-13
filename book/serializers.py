from rest_framework.serializers import (
    ModelSerializer,
)
from .models import (
    Book,
    Category,
    Issue
)


class CategoryListSerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'title',
            'slug',
        ]


class BookDetailSerializers(ModelSerializer):
    category = CategoryListSerializers(many=True)

    class Meta:
        model = Book
        fields = [
            'name',
            'slug',
            'category',
            # 'issue',
            'thumbnail',
            'description',
            'author',
            'created',
            'status',
        ]


class BookListSerializers(ModelSerializer):
    category = CategoryListSerializers(many=True)

    class Meta:
        model = Book
        fields = [
            'name',
            'slug',
            'category',
            'thumbnail',
            'status',
        ]
