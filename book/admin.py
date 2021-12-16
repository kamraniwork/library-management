from django.contrib import admin
from .models import Category, Book, Issue


def make_published(modeladmin, request, queryset):
    row_updated = queryset.update(status='p')
    if row_updated == 1:
        message_bit = "منتشر شد"
    else:
        message_bit = "منتشر شدند"

    modeladmin.message_user(request, "{} مقاله {}".format(row_updated, message_bit))


make_published.short_description = "انتشار مقاله"


def make_Draft(modeladmin, request, queryset):
    row_updated = queryset.update(status='d')
    if row_updated == 1:
        message_bit = "پیش نویس شد"
    else:
        message_bit = "پیش نویس شدند"

    modeladmin.message_user(request, "{} مقاله {}".format(row_updated, message_bit))


make_Draft.short_description = "پیش نویس مقاله"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')


admin.site.register(Category, CategoryAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'description', 'author', 'status', 'jpublish', 'category_to_string')
    list_filter = ('status', 'created')
    search_fields = ('name', 'description')

    actions = [make_published, make_Draft]


admin.site.register(Book, BookAdmin)


class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'is_not_time',
        'jpublish',
        'renewCount',
        'status',
    )
    list_filter = ('status', 'created')

    actions = [make_published, make_Draft]


admin.site.register(Issue, IssueAdmin)
