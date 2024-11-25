from django import forms
from .models import ArtPiece, Category, Comment
from .choices import CategoryType


class ArtPieceForm(forms.ModelForm):
    categories = forms.ModelChoiceField(
        queryset=Category.objects.all(),  # Get all categories from the database
        widget=forms.Select(),  # You can change this to Select if you want a dropdown
        required=True,
        label="Select Art Category"
    )

    class Meta:
        model = ArtPiece
        fields = ['title', 'art_image', 'description', 'categories', 'price']

        error_messages = {
            'art_image': {
                'required': 'Please upload an image for your artwork.',  # Custom error for art_image
            },
            'description': {
                'required': 'Please provide a description for your artwork.',  # Custom error for description
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

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Comment cannot be empty')
        return content


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']  # Use correct field names

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_name'].widget.attrs.update({'placeholder': 'Category Name'})
        self.fields['description'].widget = forms.Textarea(attrs={'placeholder': 'Optional description...'})
