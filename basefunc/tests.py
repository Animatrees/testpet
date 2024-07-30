import math
from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from basefunc.models import Post
from basefunc.utils import PaginateMixin


class GetPagesTestCase(TestCase):

    def setUp(self):
        cache.clear()

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'basefunc/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)


class DataTestCase(TestCase):
    fixtures = ['fixtures/testdata.json']

    def setUp(self):
        cache.clear()

    def test_paginate_pages(self):
        path = reverse('home')
        posts = Post.published.all()
        paginate_by = PaginateMixin.paginate_by
        pages = math.ceil(len(posts) / paginate_by)
        for page in range(1, pages + 1):
            response = self.client.get(path + f'?page={page}')
            self.assertQuerySetEqual(response.context_data['posts'], posts[(page - 1) * paginate_by:page * paginate_by])

    def test_check_posts_content(self):
        posts = Post.published.all()
        for p in posts:
            path = reverse('post', args=[p.slug])
            response = self.client.get(path)
            self.assertEqual(p.content, response.context_data['post'].content)
