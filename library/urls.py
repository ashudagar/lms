from django.conf.urls import url
from rest_framework import routers
from library import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='users')
router.register(r'books', views.BookViewSet, base_name='books')
router.register(r'books-issued', views.BooksIssuedViewSet, base_name='books-issued')
router.register(r'author', views.AuthorViewSet, base_name='author')
router.register(r'department', views.DepartmentViewSet, base_name='department')
urlpatterns = router.urls
