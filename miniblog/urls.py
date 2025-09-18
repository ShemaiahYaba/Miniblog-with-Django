# Import Django URL utilities
from django.urls import path
from . import views  # Import our views module

# Import class-based views for cleaner organization
from .views import (
    PostListView,     # Homepage showing all posts
    PostDetailView,   # Individual post page
    PostCreateView,   # Create new post page
    PostUpdateView,   # Edit existing post page
    PostDeleteView,   # Delete post confirmation page
    UserPostListView  # Posts by specific user page
)

# URL patterns for the miniblog app
# Each path() maps a URL pattern to a view
# The 'name' parameter allows us to reference URLs in templates and views
urlpatterns = [
    # Homepage - shows list of all posts
    path('', PostListView.as_view(), name='post-list'),
    
    # User posts - shows posts by a specific user
    # <str:username> captures the username from the URL
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    
    # Post detail - shows a single post with comments
    # <int:pk> captures the post ID as an integer
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # Create new post
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    
    # Update existing post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    
    # Delete post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Add comment to a post
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    
    # User authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Static pages
    path('about/', views.about, name='about'),
]