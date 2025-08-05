from django import forms
from .models import Post, Blog


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','text', 'image']
        labels = {'title': 'Post title:', 'text': 'Content:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','cover_image','background_image','profile_image']
        labels = {'title': 'Blog title:',
                  'cover_image': 'Cover image:',
                  'profile_image': 'Profile image:',
                  'background_image': 'Background image:'}
