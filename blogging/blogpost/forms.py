from django.forms import ModelForm
from django import forms
from .models import Comment, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'created_date']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'mb-3 form-control'})


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }
