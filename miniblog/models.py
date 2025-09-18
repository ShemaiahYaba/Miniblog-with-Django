# Import Django's database models and utilities
from django.db import models
from django.contrib.auth.models import User  # Django's built-in User model
from django.urls import reverse              # For generating URLs
from django.utils import timezone            # For timezone-aware datetime

# Database Models - These define the structure of our database tables

class Post(models.Model):
    """
    Blog Post model - represents a single blog post
    Each post has a title, content, publication date, and author
    """
    # CharField for short text with a maximum length
    title = models.CharField(max_length=200)
    
    # TextField for long text content (no length limit)
    content = models.TextField()
    
    # DateTimeField that automatically sets to current time when post is created
    date_posted = models.DateTimeField(default=timezone.now)
    
    # ForeignKey creates a relationship to the User model
    # on_delete=CASCADE means if user is deleted, delete their posts too
    # null=True allows posts without an author (for data migration)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        """
        String representation of the Post object
        This is what shows up in Django admin and when printing the object
        """
        return self.title
    
    def get_absolute_url(self):
        """
        Returns the URL for this post's detail page
        Django will redirect here after creating/updating a post
        """
        return reverse('post-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    """
    Comment model - represents a comment on a blog post
    Each comment belongs to a post and has an author
    """
    # ForeignKey to Post model with related_name for reverse lookups
    # related_name='comments' means we can access post.comments.all()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    
    # ForeignKey to User model for the comment author
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    # The actual comment text
    content = models.TextField()
    
    # When the comment was posted
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        """
        String representation showing who commented on which post
        """
        return f'Comment by {self.author.username} on {self.post.title}'