from django import forms

from .models import PostModel, Comment

class PostModelForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = [
            'kind',
            'title',
            'content'
        ]

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author',None)
        self.post = kwargs.pop('post',None)
        super().__init__(*args, **kwargs)

    def save(self, commit= True):
        comment = super().save(commit=False)
        comment.author = self.author
        comment.post = self.post
        comment.save()

    class Meta:
        model = Comment
        fields = ["body"]
