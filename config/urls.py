"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Import necessary modules for URL routing
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# Main URL patterns for the entire project
# Django checks these patterns from top to bottom until it finds a match
urlpatterns = [
    # Django admin interface - accessible at /admin/
    path('admin/', admin.site.urls),
    
    # Include all URLs from the miniblog app
    # This means miniblog.urls handles the root URL ('')
    path('', include('miniblog.urls')),
    
    # Built-in Django authentication views
    # Login view using our custom template
    path('login/', auth_views.LoginView.as_view(template_name='miniblog/login.html'), name='login'),
    
    # Logout view using our custom template
    path('logout/', auth_views.LogoutView.as_view(template_name='miniblog/logout.html'), name='logout'),
]
