from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Book, Issue
from .serializers import (
    BookListSerializers,
    BookDetailSerializers,
    BookInputSerializers,
    IssueListSerializers,
    IssueDetailSerializers,
    IssueInputSerializers,

)
from django.shortcuts import get_object_or_404


class BookView(ViewSet):
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = ()

        return [permission() for permission in permission_classes]

    def list(self, request):
        if request.user.is_superuser:
            book_list = Book.objects.all()
        else:
            book_list = Book.objects.filter(status='p')

        serializer = BookListSerializers(instance=book_list, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        if request.user.is_superuser:
            book_obj = get_object_or_404(Book, slug=slug)
        else:
            book_obj = get_object_or_404(Book, status='p', slug=slug)

        serializer = BookDetailSerializers(instance=book_obj, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = BookInputSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'create book object successfully'})
        else:
            return Response(serializer.errors)

    def update(self, request, slug=None):
        book = get_object_or_404(Book, slug=slug)
        serializer = BookInputSerializers(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def destroy(self, request, slug=None):
        book = get_object_or_404(Book, slug=slug)
        book.delete()
        return Response({'status': 'deleted object'}, status=200)


class IssueView(ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'retrieve', 'list']:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = ()

        return [permission() for permission in permission_classes]

    def list(self, request):
        issue_book = Issue.objects.filter(~Q(status='k'))
        serializer = IssueListSerializers(instance=issue_book, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        issue_obj = get_object_or_404(Issue, ~Q(status='k'), pk=pk)
        serializer = IssueDetailSerializers(instance=issue_obj, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = IssueInputSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 'create issue object successfully'})
        else:
            return Response(serializer.errors)

    def update(self, request, pk=None):
        issue_obj = get_object_or_404(Issue, pk=pk)
        serializer = IssueInputSerializers(issue_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def destroy(self, request, pk=None):
        issue_obj = get_object_or_404(Issue, pk=pk)
        issue_obj.delete()
        return Response({'status': 'deleted object'}, status=200)

    @action(detail=False, methods=['get'], permission_classes=(IsAuthenticated,), name='self user issue list')
    def user_issue_list_book(self, request):
        issue_book_user = Issue.objects.filter(~Q(status='k'), user=request.user)
        serializer = IssueListSerializers(instance=issue_book_user, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=(IsAuthenticated,), name='renew book request')
    def user_issue_renew_request(self, request, pk):
        issue_book = get_object_or_404(Issue, ~Q(status='k'), user=request.user, pk=pk)
        issue_book.status = 'o'
        issue_book.save()
        return Response({'status': 'please waite for accept request...'})

    @action(detail=True, methods=['get'], permission_classes=(IsAdminUser,), name='renew book')
    def user_issue_accept_renew(self, request, pk):
        issue_book = get_object_or_404(Issue, status='o', pk=pk)
        issue_book.status = 'p'
        issue_book.save()
        return Response({'status': 'you accept issue user '})

    @action(detail=True, methods=['get'], permission_classes=(IsAdminUser,), name='reject renew book')
    def user_issue_reject_renew(self, request, pk):
        issue_book = get_object_or_404(Issue, status='o', pk=pk)
        issue_book.status = 'd'
        issue_book.save()
        return Response({'status': 'you reject issue user '})

    @action(detail=True, methods=['post'], permission_classes=(IsAuthenticated,), name='return book')
    def user_issue_return(self, request, pk):
        issue_book = get_object_or_404(Issue, ~Q(status='k'), user=request.user, pk=pk)
        issue_book.status = 'k'
        issue_book.book.status = 'p'
        issue_book.book.save()
        issue_book.save()
        return Response({'status': 'book return to library'})

    @action(detail=False, methods=['get'], permission_classes=(IsAdminUser,), name='list is_on_time==True user ')
    def user_issue_delay_list_return(self, request):
        issue_delay_user = Issue.objects.filter(~Q(status='k'), user=request.user, delay=True)
        serializer = IssueListSerializers(instance=issue_delay_user, context={'request': request}, many=True)
        return Response(serializer.data)
