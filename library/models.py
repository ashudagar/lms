from __future__ import unicode_literals
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(_('username'), unique=True,
                                 error_messages={
        'unique': _("A user with that email address already exists."),
    })
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now)

    phone_number = models.CharField(max_length=15, null=True)
    address = models.TextField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name='book_author')
    department = models.ForeignKey(Department, related_name='book_department')
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name='book_created_by')

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class BooksIssued(models.Model):
    user = models.ForeignKey(User, related_name='book_issued')
    book = models.ForeignKey(Book, related_name='book_issued')
    issued_on = models.DateTimeField(default=timezone.now)
    due_on = models.DateTimeField(null=True)
    returned_on = models.DateTimeField(null=True)
    fine_charge = models.FloatField(null=True)
    issued_by = models.ForeignKey(User, related_name='book_issued_by')

    def __str__(self):
        return self.user + self.book
