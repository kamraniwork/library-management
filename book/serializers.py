from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField
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
            'description',
            'author',
            'created',
            'status',
        ]


class BookListSerializers(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='book:book-detail', lookup_field='slug')
    category = CategoryListSerializers(many=True)

    class Meta:
        model = Book
        fields = [
            'url',
            'name',
            'slug',
            'category',
            'status',
        ]


class BookInputSerializers(ModelSerializer):

    class Meta:
        model = Book
        fields = [
            'name',
            'slug',
            'category',
            'description',
            'author',
            'created',
        ]
