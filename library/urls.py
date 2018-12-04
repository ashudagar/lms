from django.conf.urls import url
from rest_framework import routers
from library import views
from django.apps import apps

router = routers.DefaultRouter()
app = apps.get_app_config('library')
for model_name, model in app.models.items():
    viewset = views.__dict__.get(model_name.title() + "ViewSet")
    if viewset:
        router.register(model_name, viewset=viewset, base_name="'" + model_name + "'")

# router.register(r'users', views.UserViewSet, base_name='users')
# router.register(r'books', views.BookViewSet, base_name='books')
# router.register(r'books-issued', views.BooksIssuedViewSet, base_name='books-issued')
# router.register(r'author', views.AuthorViewSet, base_name='author')
# router.register(r'department', views.DepartmentViewSet, base_name='department')
urlpatterns = router.urls
