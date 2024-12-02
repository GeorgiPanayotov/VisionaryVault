from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ArtPiece, Category
from .forms import ArtPieceForm
from VisionaryVaultApp.art.choices import CategoryType

"""Art piece functionality"""


class UserPermissionsService:
    @staticmethod
    def can_comment(user):
        return user.is_authenticated

    @staticmethod
    def is_owner(user, art_piece):
        return art_piece.user == user


class ArtGalleryListView(ListView):
    model = ArtPiece
    template_name = 'art/art_gallery_list.html'
    context_object_name = 'art_pieces'

    def get_queryset(self):
        return ArtPiece.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_comment'] = UserPermissionsService.can_comment(self.request.user)
        return context


class MyArtListView(LoginRequiredMixin, ListView):
    model = ArtPiece
    template_name = 'art/private_gallery.html'
    context_object_name = 'art_pieces'

    def get_queryset(self):
        """Filter art pieces by the logged-in user"""
        return ArtPiece.objects.filter(user=self.request.user)


class ArtPieceDetailView(DetailView):
    model = ArtPiece
    template_name = 'art/art_piece_detail.html'
    context_object_name = 'art_piece'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = UserPermissionsService.is_owner(self.request.user, self.object)
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


"""Ensures that user must be authenticated with method_decorator, 
if not it will be redirected to the login page as specified in settings.py"""


@method_decorator(login_required, name='dispatch')
class ArtPieceDeleteView(DeleteView):
    model = ArtPiece
    template_name = 'art/delete_art_piece.html'
    success_url = reverse_lazy('my_art')

    def get_queryset(self):
        return ArtPiece.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Art piece deleted successfully.")
        return super().delete(request, *args, **kwargs)
