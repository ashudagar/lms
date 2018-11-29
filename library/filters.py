import django_filters
from library.models import BooksIssued


class BooksIssuedFilter(django_filters.FilterSet):
    class Meta:
        model = BooksIssued
        fields = ('user', )
