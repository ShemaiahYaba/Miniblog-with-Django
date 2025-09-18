# Import Django utilities and components
from django.shortcuts import render, redirect, get_object_or_404  # Shortcuts for common operations
from django.contrib.auth import login, logout                     # Authentication functions
from django.contrib.auth.decorators import login_required         # Decorator to require login
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # Class-based views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Mixins for class-based views
from django.contrib import messages                               # Flash messages system
from django.urls import reverse_lazy                              # URL reversal for class-based views
from django.contrib.auth.models import User                       # Django's User model
from .models import Post, Comment                                 # Our custom models
from .forms import UserRegisterForm, UserLoginForm, PostForm, CommentForm  # Our custom forms

# Views - These handle HTTP requests and return HTTP responses
# Views contain the business logic of our application

# =============================================================================
# USER AUTHENTICATION VIEWS
# =============================================================================

def register(request):
    """
    Handle user registration
    GET: Display registration form
    POST: Process registration form and create new user
    """
    if request.method == 'POST':
        # User submitted the registration form
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            # Form data is valid, create the user
            user = form.save()  # This creates and saves the user to database
            
            # Automatically log in the new user
            login(request, user)
            
            # Show success message
            messages.success(request, 'Your account has been created! You are now logged in.')
            
            # Redirect to home page
            return redirect('post-list')
    else:
        # GET request - show empty registration form
        form = UserRegisterForm()
    
    # Render the registration template with the form
    return render(request, 'miniblog/register.html', {'form': form})

def user_login(request):
    """
    Handle user login
    GET: Display login form
    POST: Process login form and authenticate user
    """
    if request.method == 'POST':
        # User submitted login credentials
        form = UserLoginForm(data=request.POST)
        
        if form.is_valid():
            # Credentials are valid, get the authenticated user
            user = form.get_user()
            
            # Log in the user (creates session)
            login(request, user)
            
            # Show welcome message
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to home page
            return redirect('post-list')
    else:
        # GET request - show empty login form
        form = UserLoginForm()
    
    # Render the login template with the form
    return render(request, 'miniblog/login.html', {'form': form})

@login_required  # Decorator ensures only logged-in users can access this view
def user_logout(request):
    """
    Handle user logout
    Logs out the current user and redirects to home page
    """
    # Log out the user (destroys session)
    logout(request)
    
    # Show logout message
    messages.info(request, 'You have been logged out.')
    
    # Redirect to home page
    return redirect('post-list')

# =============================================================================
# BLOG POST VIEWS
# =============================================================================

class PostListView(ListView):
    """
    Display a list of all blog posts
    ListView is a Django class-based view that handles displaying lists of objects
    """
    model = Post  # Which model to display
    template_name = 'miniblog/post_list.html'  # Which template to use
    context_object_name = 'posts'  # Name for the list in the template (default would be 'object_list')
    ordering = ['-date_posted']  # Order by date_posted, newest first (- means descending)
    paginate_by = 5  # Show 5 posts per page

class UserPostListView(ListView):
    """
    Display posts by a specific user
    Similar to PostListView but filtered by author
    """
    model = Post
    template_name = 'miniblog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        """
        Override the default queryset to filter by user
        self.kwargs contains URL parameters (like username from the URL)
        """
        # Get the user from the URL parameter, or return 404 if not found
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        
        # Return only posts by this user, ordered by date
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    """
    Display a single blog post with its comments
    DetailView handles displaying a single object
    """
    model = Post
    
    def get_context_data(self, **kwargs):
        """
        Add extra data to the template context
        In this case, we add a comment form so users can add comments
        """
        # Get the default context from the parent class
        context = super().get_context_data(**kwargs)
        
        # Add an empty comment form to the context
        context['comment_form'] = CommentForm()
        
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allow logged-in users to create new blog posts
    LoginRequiredMixin ensures only authenticated users can access this view
    CreateView handles the form display and processing for creating new objects
    """
    model = Post
    form_class = PostForm  # Use our custom form
    
    def form_valid(self, form):
        """
        Called when the form is valid
        Set the author to the current user before saving
        """
        # Set the author to the currently logged-in user
        form.instance.author = self.request.user
        
        # Call the parent method to save the object
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow users to edit their own blog posts
    LoginRequiredMixin: User must be logged in
    UserPassesTestMixin: User must pass a custom test (defined in test_func)
    UpdateView: Handles form display and processing for updating existing objects
    """
    model = Post
    form_class = PostForm
    
    def form_valid(self, form):
        """
        Called when the form is valid
        Ensure the author remains the current user
        """
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        """
        Test function for UserPassesTestMixin
        Only allow users to edit their own posts
        Returns True if user can access this view, False otherwise
        """
        post = self.get_object()  # Get the post being edited
        return self.request.user == post.author  # Check if current user is the author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow users to delete their own blog posts
    DeleteView handles the confirmation and deletion of objects
    """
    model = Post
    success_url = reverse_lazy('post-list')  # Where to redirect after successful deletion
    
    def test_func(self):
        """
        Only allow users to delete their own posts
        """
        post = self.get_object()
        return self.request.user == post.author

# =============================================================================
# COMMENT VIEWS
# =============================================================================

@login_required  # Only logged-in users can add comments
def add_comment(request, pk):
    """
    Handle adding comments to blog posts
    pk parameter comes from the URL and identifies which post to comment on
    """
    # Get the post or return 404 if not found
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        # User submitted a comment
        form = CommentForm(request.POST)
        
        if form.is_valid():
            # Form is valid, create comment but don't save to database yet
            comment = form.save(commit=False)
            
            # Set the post and author (these aren't in the form)
            comment.post = post
            comment.author = request.user
            
            # Now save to database
            comment.save()
            
            # Show success message
            messages.success(request, 'Your comment has been added!')
            
            # Redirect back to the post detail page
            return redirect('post-detail', pk=post.pk)
    
    # If GET request or form invalid, redirect back to post
    return redirect('post-detail', pk=post.pk)

# =============================================================================
# STATIC PAGES
# =============================================================================

def about(request):
    """
    Display the about page
    Simple view that just renders a template
    """
    return render(request, 'miniblog/about.html', {'title': 'About'})