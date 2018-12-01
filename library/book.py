
@python_2_unicode_compatible
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name='book_author')
    department = models.ForeignKey(Department, related_name='book_department')
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name='book_created_by')
    active_objects = BookManager()
    objects = models.Manager()

    def __str__(self):
        return self.title
