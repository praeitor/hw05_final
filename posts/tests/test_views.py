from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


from posts.models import Post, Group

from. import constants as c

User = get_user_model()


class PostsViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        tuser = User.objects.create(username=c.AUTHOR)
        cls.group = Group.objects.create(
            title=c.GROUP_TITLE,
            slug=c.GROUP_SLUG,
            description=c.GROUP_DESC,
        )
        cls.post = Post.objects.create(
            text=c.POST_TEXT,
            pub_date=c.POST_PUBDATE,
            author=tuser,
            group=cls.group,
            image=c.POST_IMAGE,
        )

    def setUp(self):
        self.user = User.objects.get(username=c.AUTHOR)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_about_page_uses_correct_template(self):
        '''Страница group сформирована с правильным шаблоном.'''
        response = self.authorized_client.get(c.GROUP_URL)
        self.assertTemplateUsed(response, 'group.html')

    def test_pages_uses_core_template_auth(self):
        '''Страницы index/newpost сформированы с правильным шаблоном.'''
        templates_url_names = {
            'index.html': 'index',
            'newpost.html': 'new_post',
        }
        for template, name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse(name))
                self.assertTemplateUsed(response, template)

    def test_index_page_shows_correct_context(self):
        '''Страница index сформирована с правильным контекстом.'''
        response = self.authorized_client.get(c.INDEX_URL)
        first_object = response.context['posts'][0]
        paginator = response.context.get('page')
        post_author = first_object.author
        post_text = first_object.text
        post_image = first_object.image
        self.assertEqual(str(post_author), c.AUTHOR)
        self.assertEqual(post_text, c.POST_TEXT)
        self.assertEqual(post_image, c.POST_IMAGE)
        self.assertEqual(len(paginator), 1)

    def test_group_page_shows_correct_context(self):
        '''Страница group сформирована с правильным контекстом.'''
        response = self.authorized_client.get(c.GROUP_URL)
        self.assertEqual(response.context['posts'][0].image, c.POST_IMAGE)
        self.assertEqual(response.context['group'].title, c.GROUP_TITLE)
        self.assertEqual(response.context['group'].description, c.GROUP_DESC)
        self.assertEqual(response.context['group'].slug, c.GROUP_SLUG)

    def test_newpost_page_shows_correct_context(self):
        '''Страница newpost сформирована с правильным контекстом.'''
        response = self.authorized_client.get(c.NEW_URL)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_editpost_page_shows_correct_context(self):
        '''Страница editpost сформирована с правильным контекстом.'''
        response = self.authorized_client.get(c.EDIT_URL)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_profile_page_shows_correct_context(self):
        '''Страница profiles сформирована с правильным контекстом.'''
        response = self.authorized_client.get(c.PROFILE_URL)
        profile_object = response.context['profile']
        post_object = response.context['posts'][0]
        profile_username = profile_object.username
        post_text = post_object.text
        post_image = post_object.image
        self.assertEqual(str(profile_username), c.AUTHOR)
        self.assertEqual(post_text, c.POST_TEXT)
        self.assertEqual(post_image, c.POST_IMAGE)

    def test_post_page_shows_correct_context(self):
        '''Страница post сформирована с правильным контекстом.'''
        response = self.authorized_client.get(c.POST_URL)
        post_object = response.context['post']
        profile_object = response.context['profile']
        profile_username = profile_object.username
        post_text = post_object.text
        post_image = post_object.image
        self.assertEqual(str(profile_username), c.AUTHOR)
        self.assertEqual(post_text, c.POST_TEXT)
        self.assertEqual(post_image, c.POST_IMAGE)
