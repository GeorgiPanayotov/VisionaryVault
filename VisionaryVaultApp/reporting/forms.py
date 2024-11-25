from django import forms
from .models import Report
from ..art.models import ArtPiece, Comment


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['art_piece', 'comment', 'reason',]

    def __init__(self, *args, art_piece_id=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['reason'].widget = forms.Textarea(attrs={
            'placeholder': 'Provide a reason for reporting...',
            'rows': 4
        })

        if art_piece_id:
            self.fields['art_piece'].queryset = ArtPiece.objects.filter(id=art_piece_id)
            self.fields['art_piece'].initial = art_piece_id  # Set initial value to the selected art piece
            self.fields['art_piece'].widget.attrs['disabled'] = 'disabled'
        else:
            self.fields['art_piece'].queryset = ArtPiece.objects.all()

        self.fields['art_piece'].label_from_instance = lambda obj: obj.title

        # Filter comments based on the selected art piece
        self.filter_comments(art_piece_id)

    def filter_comments(self, art_piece_id):
        if art_piece_id:
            self.fields['comment'].queryset = Comment.objects.filter(art_piece_id=art_piece_id)
        else:
            self.fields['comment'].queryset = Comment.objects.none()
