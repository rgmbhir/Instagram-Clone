from .models import Post
from django import forms


class NewPostForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Caption'}), required=True)
    tag = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tags - Separate tag with comma'}),
        required=True)

    class Meta:
        model = Post
        fields = ['picture', 'caption', 'tag']
