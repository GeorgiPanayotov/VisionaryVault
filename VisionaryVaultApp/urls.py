"""
URL configuration for VisionaryVaultApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include

from VisionaryVaultApp.art.api_views import CommentListCreateView, CommentDetailView, LikeArtPieceView
from VisionaryVaultApp.common.views import HomePageView


urlpatterns = [
    path('admin/', admin.site.urls),  # Admin dashboard
    path('', HomePageView.as_view(), name='home'),  # Homepage
    path('accounts/', include('VisionaryVaultApp.accounts.urls')),
    path('art/', include('VisionaryVaultApp.art.urls')),
    path('art/<int:art_piece_id>/comments/', CommentListCreateView.as_view(), name='comment_add_and_list'),
    path('art/<int:art_piece_id>/comments/<int:comment_id>/', CommentDetailView.as_view(), name='edit_delete_comment'),
    path('art/<int:pk>/like/', LikeArtPieceView.as_view(), name='like_art_piece'),
    path('about/', include('VisionaryVaultApp.common.urls')),
    path('reporting/', include('VisionaryVaultApp.reporting.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
