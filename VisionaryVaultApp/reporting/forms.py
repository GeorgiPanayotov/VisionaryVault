from django import forms
from .models import Report, ArtPiece, Comment


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['art_piece', 'comment', 'reason']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['reason'].widget = forms.Textarea(attrs={
            'placeholder': 'Provide a reason for reporting...',
            'rows': 4
        })

