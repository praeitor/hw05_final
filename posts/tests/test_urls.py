from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group

from. import constants as c

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        tuser = User.objects.create(username=c.AUTHOR)
        auser = User.objects.create(username='second_user')
        Post.objects.create(
            text=c.POST_TEXT,
            pub_date=c.POST_PUBDATE,
            author=tuser,
        )
        Post.objects.create(
            text='пост другого автора',
            pub_date=c.POST_PUBDATE,
            author=auser,
        )
        Group.objects.create(
            title=c.GROUP_TITLE,
            slug=c.GROUP_SLUG,
            description=c.GROUP_DESC,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username=c.AUTHOR)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls(self):
        '''Проверка доступности основных url сайта'''

        site_urls = {
            '/': 200,
            '/group/test-slug/': 200,
            '/new/': 200,
            '/user_test/': 200,
            '/about/author/': 200,
            '/about/tech/': 200,
            '/user_test/1/': 200,
            '/user_test/1/edit/': 200,
            '/404/': 404,
        }
        for url_path, status_code in site_urls.items():
            with self.subTest():
                self.assertEqual(
                    self.authorized_client.get(url_path).status_code,
                    status_code
                )

    def test_urls_uses_correct_template_auth(self):
        '''Страницы использует корректный темплейт, с авторизацией.'''
        template = 'newpost.html'
        templates_url_names = {
            '/new/',
            '/user_test/1/edit/',
        }
        for url_path in templates_url_names:
            with self.subTest():
                response = self.authorized_client.get(url_path)
                self.assertTemplateUsed(response, template)

    def test_urls_uses_correct_template_anon(self):
        '''Страницы использует корректный темплейт, без авторизации.'''
        templates_url_names = {
            'index.html': '/',
            'group.html': '/group/test-slug/',
        }
        for template, url_path in templates_url_names.items():
            with self.subTest():
                response = self.guest_client.get(url_path)
                self.assertTemplateUsed(response, template)

    def test_url_redirect_anonymous_edit_to_login(self):
        '''Корректный редирект анонима со страницы edit.'''
        response = self.guest_client.get(
            '/user_test/1/edit/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/user_test/1/edit/')

    def test_url_redirect_anonymous_edit_to_postview(self):
        '''Корректный аторизованного (не автора) со страницы edit.'''
        response = self.authorized_client.get(
            '/second_user/2/edit/', follow=True)
        self.assertRedirects(
            response, '/second_user/2/')
