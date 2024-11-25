from django.http import JsonResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Report
from .forms import ReportForm
from django.shortcuts import get_object_or_404, redirect, render

from ..art.models import ArtPiece, Comment


class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reporting/report.html'
    success_url = reverse_lazy('art_gallery_list')

    def get_form(self, form_class=None):
        # Capture art_piece from GET request
        form = super().get_form(form_class)
        art_piece_id = self.request.GET.get('art_piece')

        if art_piece_id:
            form.fields['art_piece'].initial = art_piece_id  # Set the initial value for art_piece
            form.filter_comments(art_piece_id)  # Filter comments based on selected art_piece

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Handle status setting for the art piece or comment
        if form.instance.art_piece:
            form.instance.art_piece.status = 'reported'
            form.instance.art_piece.save()
        elif form.instance.comment:
            form.instance.comment.status = 'reported'
            form.instance.comment.save()

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        art_piece_id = request.GET.get('art_piece')
        if art_piece_id:
            comments = Comment.objects.filter(art_piece_id=art_piece_id)
            comments_data = [{"id": comment.id, "text": comment.text} for comment in comments]
            return JsonResponse({"comments": comments_data})

        return super().get(request, *args, **kwargs)


def reinstate_art_piece(request, art_piece_id):
    # Ensure the user is an admin before proceeding
    if not request.user.is_staff:
        return redirect('art_gallery_list')  # Or another appropriate page

    # Get the art piece
    art_piece = get_object_or_404(ArtPiece, id=art_piece_id)

    # Change status to 'active'
    art_piece.status = 'active'
    art_piece.save()

    # Redirect to the art gallery or any other appropriate page
    return redirect('art_gallery_list')
