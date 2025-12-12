from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Author, Post, TeamMember

# Register your models here.

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_at',)
    list_filter_submit = True
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    ordering = ['-created_at']

@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_at',)
    list_filter_submit = True
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    ordering = ['name']

@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('title', 'author', 'category', 'will_be_in_hero', 'created_at', 'updated_at')
    list_select_related = ('author', 'category')
    search_fields = ('title', 'description')
    list_filter_submit = True
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    ordering = ['-created_at']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['author', 'category']
    date_hierarchy = 'created_at'

    fieldsets = (
        ("General Information", {
            "fields": ("title", "slug", "description", "will_be_in_hero"),
        }),
        ("Content", {
            "fields": ("post_text", "post_image", "post_image_alt"),
        }),
        ("Relations", {
            "fields": ("author", "category"),
        }),
        ("Timestamps", {
             "fields": ("created_at", "updated_at"),
             "classes": ("collapse",),
        })
    )

    class Media:
        css = {
            'all': ('css/admin_overrides.css',)
        }

@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_at',)
    list_filter_submit = True
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    ordering = ['name']
