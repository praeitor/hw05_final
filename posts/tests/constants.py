from django.urls import reverse


AUTHOR = 'user_test'
POST_TEXT = 'Тестовый тест'
POST_PUBDATE = '06.01.2021'
POST_ID = '1'
POST_IMAGE = 'posts/hw.jpg'

AUTHOR2 = 'second_user'
POST_TEXT2 = "Второй текст"
POST_PUBDATE2 = '10.01.2021'
POST_ID2 = '2'

GROUP_TITLE = 'Тестовый заголовок'
GROUP_SLUG = 'test-slug'
GROUP_DESC = 'Описание тестовой группы'

INDEX_URL = reverse('index')
NEW_URL = reverse('new_post')
GROUP_URL = reverse('group', kwargs={'slug': GROUP_SLUG})
POST_URL = reverse('post', kwargs={'username': AUTHOR, 'post_id': POST_ID})
EDIT_URL = reverse(
    'post_edit',
    kwargs={'username': AUTHOR, 'post_id': POST_ID}
)
PROFILE_URL = reverse('profile', args=[AUTHOR])
