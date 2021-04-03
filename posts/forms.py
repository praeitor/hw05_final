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
        fields = ('post', 'author', 'text')
        labels = {
            'text': _('Текст')
        }
        help_texts = {
            'text': _('Текст поста который планируется к публикации')
        }