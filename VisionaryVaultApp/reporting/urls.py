from django.urls import path

from . import views
from .views import ReportCreateView

urlpatterns = [
    path('report/<int:art_piece_id>/', ReportCreateView.as_view(), name='report'),
    path('admin/reinstate-art-piece/<int:art_piece_id>/', views.reinstate_art_piece, name='admin_unreport'),
]
