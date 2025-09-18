# Import Django admin and our models
from django.contrib import admin
from . import models

# Alternative simple registration (commented out)
# admin.site.register(models.Post)
# admin.site.register(models.Comment)
# Note: User model is already registered by Django

# Advanced admin configuration using decorators and ModelAdmin classes
# This provides more control over how models appear in the admin interface

@admin.register(models.Post)  # Decorator to register Post model with custom admin
class PostAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Post model
    Provides enhanced functionality for managing blog posts
    """
    # Fields to display in the admin list view
    list_display = ('title', 'author', 'date_posted')
    
    # Add filter sidebar for these fields
    list_filter = ('date_posted', 'author')
    
    # Enable search functionality on these fields
    search_fields = ('title', 'content')
    
    # Add date-based drill-down navigation
    date_hierarchy = 'date_posted'
    
    # Default ordering (newest first)
    ordering = ('-date_posted',)

@admin.register(models.Comment)  # Decorator to register Comment model with custom admin
class CommentAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Comment model
    Provides enhanced functionality for managing comments
    """
    # Fields to display in the admin list view
    list_display = ('post', 'author', 'date_posted')
    
    # Add filter sidebar
    list_filter = ('date_posted', 'author')
    
    # Enable search on post title (post__title) and comment content
    # post__title uses Django's double underscore notation for related field lookup
    search_fields = ('post__title', 'content')
    
    # Date-based navigation
    date_hierarchy = 'date_posted'
    
    # Default ordering (newest first)
    ordering = ('-date_posted',)