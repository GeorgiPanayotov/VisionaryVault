from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Report
from .forms import ReportForm
from django.shortcuts import get_object_or_404, redirect

from ..art.models import ArtPiece


class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reporting/report.html'
    success_url = reverse_lazy('art_gallery_list')

    def form_valid(self, form):
        form.instance.user = self.request.user

        if form.instance.art_piece:
            # Set the art piece to reported
            form.instance.art_piece.status = 'reported'
            form.instance.art_piece.save()
        elif form.instance.comment:
            # Set the comment to reported
            form.instance.comment.status = 'reported'
            form.instance.comment.save()

        return super().form_valid(form)


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