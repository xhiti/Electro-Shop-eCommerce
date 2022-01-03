from django.db import models
from django.urls import reverse


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, unique=True)
    blog_image = models.ImageField(upload_to='photos/blog/', default='', blank=True)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('admin-edit-post', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('admin-delete-post', args=[str(self.id)])
