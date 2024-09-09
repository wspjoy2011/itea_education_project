from django import forms

from .models import Comment, Post


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


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status', 'image_url', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'





















