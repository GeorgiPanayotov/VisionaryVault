
from django.urls import path, include
from .views import (
    ArtGalleryListView,
    ArtPieceDetailView,
    ArtPieceCreateView,
    ArtPieceDeleteView,
    ArtPieceUpdateView,
    CategoryListView, MyArtListView,

)


urlpatterns = [
    path('gallery/', ArtGalleryListView.as_view(), name='art_gallery_list'),
    path('my_art/', MyArtListView.as_view(), name='my_art'),
    path('upload/', ArtPieceCreateView.as_view(), name='upload_art'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('<int:pk>/', include([
        path('details/', ArtPieceDetailView.as_view(), name='art_piece_detail'),
        path('art/edit/', ArtPieceUpdateView.as_view(), name='edit_art_piece'),
        path('art/delete/', ArtPieceDeleteView.as_view(), name='delete_art_piece'),
    ])),
]

