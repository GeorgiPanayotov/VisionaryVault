from django import forms
from .models import Report
from ..art.models import ArtPiece, Comment


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['comment', 'reason',]

    def __init__(self, *args, art_piece_id=None, **kwargs):
        super().__init__(*args, **kwargs)

        if art_piece_id:
            self.fields['comment'].queryset = Comment.objects.filter(art_piece_id=art_piece_id)
        else:
            self.fields['comment'].queryset = Comment.objects.none()

        self.fields['reason'].widget = forms.Textarea(attrs={
            'placeholder': 'Provide a reason for reporting...',
            'rows': 4
        })
