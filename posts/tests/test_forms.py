from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.forms import PostForm
from posts.models import Group, Post

from. import constants as c


User = get_user_model()


class PostsCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create(username=c.AUTHOR)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title=c.GROUP_TITLE,
            slug=c.GROUP_SLUG,
            description=c.GROUP_DESC,
        )
        cls.post = Post.objects.create(
            text=c.POST_TEXT,
            pub_date=c.POST_PUBDATE,
            author=PostsCreateFormTests.user,
            group=PostsCreateFormTests.group,
            image=c.POST_IMAGE,
        )
        cls.form = PostForm()

    def test_create_post(self):
        '''Тест создания нового поста и проверки корректности ввода данных'''
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый тест 2',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            c.NEW_URL,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, c.INDEX_URL)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(text='Тестовый тест 2').exists())

    def test_edit_post(self):
        '''Тест редактирования существующего поста и корректность данных'''
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Запись после редактирования',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            '/user_test/1/edit/',
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count == posts_count)
        self.assertTrue(Post.objects.filter(
            text='Запись после редактирования').exists()
        )
        self.assertRedirects(response, c.POST_URL)
