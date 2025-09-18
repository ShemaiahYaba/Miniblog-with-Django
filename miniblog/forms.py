# Import Django forms and authentication forms
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post, Comment

# Forms - These handle user input and validation

class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts
    ModelForm automatically generates form fields based on the Post model
    """
    class Meta:
        # Tell Django which model this form is for
        model = Post
        
        # Which model fields to include in the form
        # Note: author and date_posted are handled automatically
        fields = ['title', 'content']
        
        # Custom widgets to add CSS classes for Bootstrap styling
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    """
    Form for adding comments to blog posts
    """
    class Meta:
        model = Comment
        
        # Only include content field - post and author are set in the view
        fields = ['content']
        
        # Custom textarea with Bootstrap styling and placeholder
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,  # Make textarea smaller than post content
                'placeholder': 'Write your comment here...'
            }),
        }

class UserRegisterForm(UserCreationForm):
    """
    User registration form that extends Django's built-in UserCreationForm
    Adds an email field to the standard username/password fields
    """
    # Add email field (not included in default UserCreationForm)
    email = forms.EmailField()
    
    class Meta:
        model = User
        
        # Fields to include in registration form
        fields = ['username', 'email', 'password1', 'password2']
        
        # Remove the default help text for username
        help_texts = {
            'username': None,
        }

class UserLoginForm(AuthenticationForm):
    """
    Custom login form that adds Bootstrap CSS classes
    Extends Django's built-in AuthenticationForm
    """
    def __init__(self, *args, **kwargs):
        # Call the parent class constructor
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap CSS classes to form fields
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
