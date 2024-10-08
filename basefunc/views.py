import os

import requests
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from testpet import settings
from .models import Post, Category, Tags
from .forms import AddPostForm, ContactForm
from .utils import DataMixin, PaginateMixin


class IndexView(DataMixin, PaginateMixin, ListView):
    queryset = Post.published.all()
    page_title = 'Главная страница'
    template_name = 'basefunc/index.html'
    context_object_name = 'posts'

    def get_url(self):
        return reverse('home')


class AboutView(DataMixin, TemplateView):
    template_name = 'basefunc/about.html'
    page_title = 'О сайте'


class PostAddView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'basefunc/addpage.html'
    page_title = 'Добавление новой статьи'
    login_url = 'users:login'

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.author = self.request.user
        photo = form.cleaned_data.get('photo')
        new_post.photo.save(new_post.title, photo, save=True)
        return super().form_valid(form)


class PostUpdateView(PermissionRequiredMixin, DataMixin, UpdateView):
    permission_required = 'post.change_post'
    form_class = AddPostForm
    queryset = Post.published
    template_name = 'basefunc/addpage.html'
    page_title = 'Редактирование статьи'

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'post_slug': self.object.slug})

    def form_valid(self, form):
        old_instance = self.queryset.get(pk=self.object.pk)
        if 'photo' in form.changed_data:
            if old_instance.photo:
                if os.path.isfile(old_instance.photo.path):
                    os.remove(old_instance.photo.path)

        photo = form.cleaned_data.get('photo')

        if photo:
            self.object.photo.save(self.object.title, photo, save=True)
        else:
            self.object.photo = None
            self.object.save()

        return super().form_valid(form)


class PostDeleteView(PermissionRequiredMixin, DataMixin, DeleteView):
    permission_required = 'post.delete_post'
    model = Post
    success_url = reverse_lazy('home')
    page_title = 'Удаление статьи'


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'basefunc/contact.html'
    success_url = reverse_lazy('home')
    page_title = "Обратная связь"

    def get_form_kwargs(self):
        kwargs = super(ContactFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        info = self.request.GET.get('info', '')
        kwargs['initial'] = {'theme': info}
        return kwargs

    def form_valid(self, form):
        # Получение данных формы
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        theme = form.cleaned_data['theme']
        content = form.cleaned_data['content']

        # Формирование данных для письма
        subject = theme
        message = f'Сообщение от {name} ({email}):\n\n{content}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]

        # Использование EmailMessage для установки reply_to
        email_message = EmailMessage(
            subject,
            message,
            from_email,
            recipient_list,
            reply_to=[email]  # Адрес электронной почты пользователя в качестве адреса для ответа
        )

        email_message.send()
        return super().form_valid(form)


class PostDetailView(DetailView):
    queryset = Post.published
    template_name = 'basefunc/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post.published, slug=self.kwargs['post_slug'])
        context.update({'title': post.title})
        return context


class PostCatsView(PaginateMixin, ListView):
    template_name = 'basefunc/index.html'
    context_object_name = 'posts'

    def get_url(self):
        return reverse('category', kwargs={'cat_slug': self.kwargs['cat_slug']})

    def get_queryset(self):
        return Post.published.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        context.update({'title': category.title, 'cat_id': category.pk})
        if not context['posts']:
            context['empty_list_message'] = 'Нет женщин в данной категории.'
        return context


class PostTagsView(PaginateMixin, ListView):
    template_name = 'basefunc/index.html'
    context_object_name = 'posts'

    def get_url(self):
        return reverse('tag', kwargs={'tag_slug': self.kwargs['tag_slug']})

    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tags, slug=self.kwargs['tag_slug'])
        context.update({'title': f'Тег: {tag.title}', 'tag_id': tag.pk})
        if not context['posts']:
            context['empty_list_message'] = 'Женщин из данной страны нет.'
        return context


class ProxyImageView(View):
    def get(self, request):
        # Получаем URL изображения из параметров запроса
        image_url = request.GET.get('url')
        if not image_url:
            return JsonResponse({'error': 'No URL provided'}, status=400)

        try:
            # Запрашиваем изображение с указанного URL
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            # Определяем тип контента (миметип) из заголовков ответа
            content_type = response.headers.get('Content-Type')

            # Возвращаем изображение с правильным типом контента
            return HttpResponse(response.content, content_type=content_type)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
