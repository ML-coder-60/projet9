"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from blog import views
import authentication.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        '',
        LoginView.as_view(
            template_name='authentication/login.html',
            redirect_authenticated_user=True),
        name='flux'),
    path(
        'logout/',
        LogoutView.as_view(next_page='/'),
        name='logout'
    ),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('flux/', views.feed, name='flux'),
    path('posts/', views.feed, name='posts'),
    path('ticket/new', views.new_ticket, name='new_ticket'),
    path('ticket/<int:ticket_id>/edit', views.edit_ticket, name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete', views.delete_ticket, name='delete_ticket'),
    path('review/new', views.new_review, name='new_review'),
    path('review/<int:review_id>/edit', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete', views.delete_review, name='delete_review'),
    path('subscription/', views.subscription, name='subscription')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)