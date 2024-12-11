from django import forms
from .models import ArtPiece, Comment


class ArtPieceForm(forms.ModelForm):

    class Meta:
        model = ArtPiece
        fields = ['title', 'art_image', 'description', 'categories', 'price']

        error_messages = {
            'art_image': {
                'required': 'Please upload an image for your artwork.',
            },
            'categories': {
                'required': 'Selecting an Art Category is mandatory.',
            },
            'price': {
                'required': 'Price is required. Please enter the price.',
            },
        }

        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Enter a description'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
            'title': forms.TextInput(attrs={'placeholder': 'Give your piece of art a name'}),
            'categories': forms.Select(attrs={'placeholder': 'Select an Art Category'}),
        }


class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Comment cannot be empty')
        return content


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={'placeholder': 'Enter your comment here...'})

    """Preventing from saving empty comments by overriding the clean_content method"""
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Comment cannot be empty')
        return content

