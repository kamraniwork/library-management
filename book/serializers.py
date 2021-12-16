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
            'jpublish',
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
        ]


class BookIssueListSerializers(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='book:book-detail', lookup_field='slug')

    class Meta:
        model = Book
        fields = [
            'url',
            'name',
            'slug',
        ]


class IssueListSerializers(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='book:issue-detail')
    book = BookIssueListSerializers()

    class Meta:
        model = Issue
        fields = [
            'url',
            'book',
            'user',
            'renewCount',
            'is_on_time',
        ]


class IssueDetailSerializers(ModelSerializer):
    book = BookDetailSerializers()

    class Meta:
        model = Issue
        fields = [
            'book',
            'user',
            'jpublish',
            'renewCount',
            'status',
            'is_on_time',
        ]


class IssueInputSerializers(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'book',
            'user',
            'renewCount',
        ]
