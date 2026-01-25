from django import forms
from .models import Post,Comment,Tag
from django.forms import modelformset_factory
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
        extra = 5
TagFormSet = modelformset_factory(
    Tag,
    form=TagForm,
    extra=5
)

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)