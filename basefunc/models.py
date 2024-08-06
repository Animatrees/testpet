import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils.text import slugify
from unidecode import unidecode


def custom_slugify(value):
    return slugify(unidecode(value))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Имя')
    content = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, default=None,
                              verbose_name='Путь к изображению')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.IntegerField(choices=Status.choices, default=Status.PUBLISHED, verbose_name='Опубликовано')
    slug = AutoSlugField(populate_from='title', slugify=custom_slugify, unique=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='women', verbose_name='Категория')
    tags = models.ManyToManyField('Tags', related_name='women', verbose_name='Теги')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True,
                               default=None)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Woman'
        verbose_name_plural = 'Women'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def delete(self, *args, **kwargs):
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        super(Post, self).delete(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Название категории')
    # slug = AutoSlugField(populate_from='title', slugify=custom_slugify, default='')
    slug = models.SlugField(max_length=100, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def generate_slug(self):
        if self.pk is not None:
            old_instance = self.__class__.objects.only('slug').get(pk=self.pk)
            if old_instance.slug != self.slug or old_instance.title == self.title:
                return
        self.slug = custom_slugify(self.title)

    def save(self, *args, **kwargs):
        self.generate_slug()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tags(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['title']


class Husbands(models.Model):
    title = models.CharField(max_length=255)
    age = models.SmallIntegerField(blank=True, null=True)
    m_count = models.SmallIntegerField(blank=True, null=True)
