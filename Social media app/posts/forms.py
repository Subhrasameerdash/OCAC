from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """
    Handles both media and thought posts.
    If a file is attached → media post; otherwise → thought post.
    """

    class Meta:
        model = Post
        fields = ('caption', 'media')
        widgets = {
            'caption': forms.Textarea(attrs={
                'placeholder': 'What\'s on your mind?',
                'rows': 3,
            }),
        }

    def clean(self):
        cleaned = super().clean()
        caption = cleaned.get('caption', '').strip()
        media = cleaned.get('media')

        if not caption and not media:
            raise forms.ValidationError('A post needs either text or media — don\'t leave it empty.')

        return cleaned
