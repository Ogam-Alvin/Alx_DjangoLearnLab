from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Add tags separated by commas"
    )

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]

    def save(self, commit=True):
        post = super().save(commit=False)

        if commit:
            post.save()

            tag_names = self.cleaned_data["tags"].split(",")
            for name in tag_names:
                name = name.strip()
                if name:
                    tag, created = Tag.objects.get_or_create(name=name)
                    post.tags.add(tag)

        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
