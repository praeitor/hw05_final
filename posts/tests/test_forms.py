from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.forms import PostForm
from posts.models import Comment, Group, Post, Follow

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

    def test_create_post_auth(self):
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

    def test_create_comment_auth(self):
        '''Тест создания комментария авторизированным пользователем'''
        comments_count = Comment.objects.count()
        form_data = {
            'text': 'Тестовый коментарий',
        }
        self.authorized_client.post(
            c.COMMENT_URL,
            data=form_data,
            follow=True
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertTrue(
            Comment.objects.filter(text='Тестовый коментарий').exists()
        )

    def test_edit_post(self):
        '''Тест редактирования существующего поста и корректность данных'''
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Запись после редактирования',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            c.EDIT_URL,
            data=form_data,
            follow=True,
        )
        self.assertTrue(Post.objects.filter(
            text='Запись после редактирования').exists()
        )
        self.assertRedirects(response, c.POST_URL)
        self.assertEqual(Post.objects.count(), posts_count)

    def test_follow_and_unfollow_auth_to_author(self):
        '''Тест подписки зарегистрированного пользователя'''
        follows_count = Follow.objects.count()
        second_user = User.objects.create(username=c.AUTHOR2)
        response_follow = self.authorized_client.get(
            c.FOLLOW2,
            follow=True,
        )
        second_user_client = Client()
        second_user_client.force_login(second_user)
        form_data = {
            'text': 'Пост пользователя на которого я подписан',
        }
        second_user_client.post(
            c.NEW_URL,
            data=form_data,
            follow=True
        )
        response_first = self.authorized_client.get(c.FOLLOW_URL)
        self.assertEquals(
            response_first.context['posts'].first().text,
            'Пост пользователя на которого я подписан'
        )
        self.assertRedirects(response_follow, c.PROFILE_URL2)
        self.assertEqual(Follow.objects.count(), follows_count + 1)
        response_unfollow = self.authorized_client.get(
            c.UNFOLLOW2,
            follow=True,
        )
        self.assertEquals(
            response_first.context['posts'].first(),
            None,
        )
        self.assertRedirects(response_unfollow, c.PROFILE_URL2)
        self.assertEqual(Follow.objects.count(), follows_count)
