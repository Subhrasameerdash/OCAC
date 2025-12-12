from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Form for creating and updating blog posts."""

    class Meta:
        model = Post
        fields = ['title', 'content', 'hero_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 12, 'placeholder': 'Write your story...'}),
            'hero_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
