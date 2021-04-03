from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Post, Group

from. import constants as c

User = get_user_model()


class PostsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        tuser = User.objects.create(username=c.AUTHOR)
        Post.objects.create(
            text=c.POST_TEXT,
            pub_date=c.POST_PUBDATE,
            author=tuser,
        )
        cls.uverif = Post.objects.get(pk=1)

    def test_post_verbose(self):
        post = PostsModelTest.uverif
        verbosetext = post._meta.get_field('text').verbose_name
        self.assertEqual(verbosetext, 'текст сообщения')

    def test_post_helptext(self):
        post = PostsModelTest.uverif
        helptext = post._meta.get_field('text').help_text
        self.assertEqual(helptext, 'введите сообщение')

    def test_post_title(self):
        post = PostsModelTest.uverif
        expected = 'Тестовый [...]'
        self.assertEquals(expected, str(post))


class GroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(
            title=c.GROUP_TITLE,
            slug=c.GROUP_SLUG,
            description=c.GROUP_DESC,
        )
        cls.gverif = Group.objects.get(pk=1)

    def test_group_verbose(self):
        group = GroupModelTest.gverif
        verbosetext = group._meta.get_field('title').verbose_name
        self.assertEqual(verbosetext, 'назавание группы')

    def test_group_helptext(self):
        group = GroupModelTest.gverif
        helptext = group._meta.get_field('title').help_text
        self.assertEqual(helptext, 'введите название группы')

    def test_group_title(self):
        group = GroupModelTest.gverif
        expected = 'Тестовый заголовок'
        self.assertEquals(expected, str(group))
