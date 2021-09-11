from django.contrib import admin


# Register your models here.
from django.contrib import admin
from .models import Blog


# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_date', 'is_active')


admin.site.register(Blog, BlogAdmin)



