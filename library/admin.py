from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from library.models import User, Book, Author, Department, BooksIssued


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Department)
admin.site.register(BooksIssued)


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
            ('User Profile', {'fields': ('username', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name', 'email')},),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')},),
            ('Important dates', {'fields': ('last_login', 'date_joined')},),
    )
    list_display = ('username', 'is_superuser', 'is_active', 'activate')
    search_fields = ['username']
    list_filter = ['groups']

    def activate(self, obj):
        if obj.groups.filter(name='officer').exists():
            return '<button class="request-activate" data-id="%s">%s</button>' % (obj.id, 'Request activate')
        else:
            return ''

    activate.allow_tags = True
    activate.short_description = 'Activate'
    save_on_top = True
