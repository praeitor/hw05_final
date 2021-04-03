from django import forms
from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _

from posts.models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        labels = {
            'group': _('Имя'),
            'text': _('Текст')
        }
        help_texts = {
            'group': _('Имя группы'),
            'text': _('Текст поста который планируется к публикации')
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            "text": forms.Textarea(attrs={"cols": 50, "rows": 10})
        }