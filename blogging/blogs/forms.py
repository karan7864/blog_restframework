from django.forms import ModelForm
from django import forms
from .models import Comment, UserProfile
from .serializers import CommentSerializer, UserProfileSerializer  # Import serializers

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def save(self, blog_post, author):
        comment = Comment(blog_post=blog_post, author=author, text=self.cleaned_data['text'])
        comment.save()
        return comment

class RegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['fname', 'lname', 'password', 'email']

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user_profile.set_password(self.cleaned_data['password'])
        if commit:
            user_profile.save()
        return user_profile
