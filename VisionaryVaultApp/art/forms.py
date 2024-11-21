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

    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Enter a description"}),
        error_messages={'required': 'Selecting Art Category is mandatory'}  # Empty string removes the default message
    )

    price = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter price'}),
        min_value=0.01,  # You can adjust the minimum value if needed
        decimal_places=2
    )

    class Meta:
        model = ArtPiece
        fields = ['art_image', 'description', 'categories', 'price']


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
