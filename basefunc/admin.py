from django import forms
from django.contrib import admin, messages
from django.db.models import Count, Prefetch
from django.utils.safestring import mark_safe

from .models import Post, Category, Tags

admin.site.site_header = 'Панель управления'
admin.site.index_title = ''


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_photo', 'photo', 'show_pub', 'cat')
    list_display_links = ('title',)
    ordering = ('title',)
    fields = ('title', 'content', 'show_photo', 'photo', 'cat', 'tags')
    readonly_fields = ('show_photo',)

    @admin.display(description='Фото')
    def show_photo(self, women:Post):
        if women.photo:
            return mark_safe(f'<img src="{women.photo.url}" alt="Фото для {women.title}" width=70')

    @admin.display(description='Publish', boolean=True)
    def show_pub(self, women: Post):
        return women.is_published

    @admin.action(description='Опубликовать выбранные посты')
    def make_pub(self, request, queryset):
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f'Успешно опубликовано {count} постов', level=messages.INFO)

    @admin.action(description='Снять с публикации выбранные посты')
    def unpub(self, request, queryset):
        count = queryset.update(is_published=Post.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {count} постов', level=messages.WARNING)


class CachingModelChoicesFormSet(forms.BaseInlineFormSet):
    """
    Used to avoid duplicate DB queries by caching choices and passing them all the forms.
    To be used in conjunction with `CachingModelChoicesForm`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sample_form = self._construct_form(0)
        self.cached_choices = {}
        try:
            model_choice_fields = sample_form.model_choice_fields
        except AttributeError:
            pass
        else:
            for field_name in model_choice_fields:
                if field_name in sample_form.fields and not isinstance(
                        sample_form.fields[field_name].widget, forms.HiddenInput):
                    self.cached_choices[field_name] = [c for c in sample_form.fields[field_name].choices]

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['cached_choices'] = self.cached_choices
        return kwargs


class CachingModelChoicesForm(forms.ModelForm):
    """
    Gets cached choices from `CachingModelChoicesFormSet` and uses them in model choice fields in order to reduce
    number of DB queries when used in admin inlines.
    """

    @property
    def model_choice_fields(self):
        return [fn for fn, f in self.fields.items()
                if isinstance(f, (forms.ModelChoiceField, forms.ModelMultipleChoiceField,))]

    def __init__(self, *args, **kwargs):
        cached_choices = kwargs.pop('cached_choices', {})
        super().__init__(*args, **kwargs)
        for field_name, choices in cached_choices.items():
            if choices is not None and field_name in self.fields:
                self.fields[field_name].choices = choices


class PostInlineForm(CachingModelChoicesForm):
    class Meta:
        model = Post
        exclude = ()


class PostInline(admin.TabularInline):
    model = Post
    extra = 0

    form = PostInlineForm
    formset = CachingModelChoicesFormSet

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('tags')
        return queryset


# class PostInline(admin.StackedInline):
#     model = Post
#     extra = 0  # количество дополнительных форм для добавления объектов

#     form = PostInlineForm
#     formset = CachingModelChoicesFormSet
#
# def get_queryset(self, request):
#     queryset = super().get_queryset(request)
#     queryset = queryset.prefetch_related('tags')
#     return queryset


class PostAdminForm(forms.ModelForm):
    women = forms.ModelMultipleChoiceField(queryset=Post.objects.all(),
                                           widget=admin.widgets.FilteredSelectMultiple("women", is_stacked=False))

    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['women'].initial = self.instance.women.all()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'number_of_women')
    list_display_links = ('title',)
    ordering = ('title',)
    form = PostAdminForm
    inlines = (PostInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(_number_of_women=Count('women'))

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.women.set(form.cleaned_data['women'])


    @admin.display(description='Всего женщин в категории', ordering='_number_of_women')
    def number_of_women(self, cat: Category):
        return cat._number_of_women


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


