from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ArtPiece, Category
from .forms import ArtPieceForm
from VisionaryVaultApp.art.choices import CategoryType

"""Art piece functionality"""


class ArtGalleryListView(ListView):
    model = ArtPiece
    template_name = 'art/art_gallery_list.html'
    context_object_name = 'art_pieces'

    def get_queryset(self):
        # Return all art pieces, we'll handle slicing in the template
        return ArtPiece.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            context['can_comment'] = True
            context['art_pieces'] = context['art_pieces']

        return context


class MyArtListView(LoginRequiredMixin, ListView):
    model = ArtPiece
    template_name = 'art/private_gallery.html'  # Your template name
    context_object_name = 'art_pieces'

    def get_queryset(self):
        # Filter art pieces by the logged-in user
        return ArtPiece.objects.filter(user=self.request.user)


class ArtPieceDetailView(DetailView):
    model = ArtPiece
    template_name = 'art/art_piece_detail.html'
    context_object_name = 'art_piece'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        return context


class ArtPieceCreateView(CreateView):
    model = ArtPiece
    form_class = ArtPieceForm
    template_name = 'art/upload_art.html'
    success_url = reverse_lazy('art_gallery_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Passing the categories to the template
        return context

    def form_valid(self, form):
        art_piece = form.save(commit=False)
        art_piece.user = self.request.user
        art_piece.save()
        form.save_m2m()
        return super().form_valid(form)


class ArtPieceUpdateView(UpdateView):
    model = ArtPiece
    fields = ['art_image', 'description', 'categories', 'price']
    template_name = 'art/edit_art_piece.html'
    success_url = reverse_lazy('my_art')

    def get_queryset(self):
        return ArtPiece.objects.filter(user=self.request.user)


class ArtPieceDeleteView(DeleteView):
    model = ArtPiece
    template_name = 'art/delete_art_piece.html'
    success_url = reverse_lazy('my_art')

    def get_queryset(self):
        return ArtPiece.objects.filter(user=self.request.user)


class CategoryListView(ListView):
    model = Category
    template_name = 'art/upload_art.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
