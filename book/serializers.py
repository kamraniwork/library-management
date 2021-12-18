from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField
)
from .models import (
    Book,
    Category,
    Issue
)

User = get_user_model()


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


class BookInputSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(max_length=256)
    category = serializers.ListField()
    description = serializers.CharField(max_length=3000)
    author = serializers.CharField()

    def create(self, validated_data):
        name = validated_data.get('name')
        slug = validated_data.get('slug')
        category = validated_data.get('category')
        description = validated_data.get('description')
        author = validated_data.get('author')

        category_list = list()
        for slug_cat in category:
            category_obj = get_object_or_404(Category, slug=slug_cat, status=True)
            category_list.append(category_obj)

        book = Book.objects.create(name=name, slug=slug, description=description, author=author, status='p')
        book.category.set(category_list)
        return book

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        category = validated_data.get('category')
        description = validated_data.get('description')
        author = validated_data.get('author')

        category_list = list()
        for slug_cat in category:
            category_obj = get_object_or_404(Category, slug=slug_cat, status=True)
            category_list.append(category_obj)

        instance.name = name
        instance.category = category_list
        instance.description = description
        instance.author = author
        instance.save()
        return instance


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
            'is_not_time',
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
            'is_not_time',
        ]


class IssueInputSerializers(serializers.Serializer):
    user = serializers.CharField(max_length=256, required=True)
    book = serializers.CharField(max_length=256, required=True)
    renewCount = serializers.IntegerField(required=False)
    status = serializers.CharField(max_length=1, required=False)

    def create(self, validated_data):
        username = validated_data.get('user')
        book_id = validated_data.get('book')

        user = get_object_or_404(User, username=username)
        book = get_object_or_404(Book, slug=book_id, status='p')
        if user is not None or book is not None:
            issue = Issue.objects.create(user=user, book=book, renewCount=0, status='p')
        else:
            return Response('user or book not Available')
        return issue

    def update(self, instance, validated_data):
        renew_count = validated_data.get('renewCount', instance.renewCount)
        status = validated_data.get('status', 'p')

        instance.renewCount = renew_count
        instance.status = status
        instance.save()
        return instance
