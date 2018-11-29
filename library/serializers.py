from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from library.models import User, Book, BooksIssued, Department, Author


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book


class BooksIssuedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksIssued

    @transaction.atomic
    def create(self, validated_data):
        validated_data['issued_by'] = self.context.get('request').user
        instance = super(BooksIssuedSerializer, self).create(validated_data)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data['returned_on'] = timezone.now()
        instance = super(BooksIssuedSerializer, self).update(
            instance, validated_data)
        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
