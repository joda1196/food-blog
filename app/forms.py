from django import forms
from app.models import *


##this will be connecting to the 'comment view'
class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = "content"
