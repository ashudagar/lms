from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from library.serializers import (UserSerializer, BookSerializer, BooksIssuedSerializer, DepartmentSerializer,
                                 AuthorSerializers
                                 )
from library.models import User, Book, BooksIssued, Department, Author
from library.filters import BooksIssuedFilter


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.active_objects.all().order_by('-created_on')

    def destroy(self, request, pk=None):
        """
        function to delete a book,
        """
        instance = self.get_queryset().filter(id=pk)
        if instance:
            instance.is_deleted = True
            instance.deleted_on = timezone.now()
            instance.save()
        return Response({'result': 'success'})


class BooksissuedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows issued books to be viewed or edited.
    """
    serializer_class = BooksIssuedSerializer
    filter_class = BooksIssuedFilter

    def get_queryset(self):
        """
        override the get_queryset method
        :return: queryset
        """
        qs = BooksIssued.objects.all().order_by('-issued_on')
        return qs

    def list(self, request, *args, **kwargs):
        """
        override list method to get all issued books to the given user using filter class
        """
        filtered_qs = self.filter_queryset(self.get_queryset().order_by('-issued_on'))
        data = BooksIssuedSerializer(filtered_qs, many=True).data
        return Response({'result': data})


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows departments to be viewed or edited.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers