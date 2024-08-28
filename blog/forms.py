from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(
                attrs={
                    'placeholder': 'Share your thoughts in the comments...',
                    'class': 'form-control mt-2',
                    'rows': 4
                }
            )
        }

        labels = {
            'body': 'Add you comment:'
        }
