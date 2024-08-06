from captcha.fields import CaptchaField
from django import forms
from .models import *


class AddPostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), widget=forms.CheckboxSelectMultiple, label='Страна')
    photo_url = forms.URLField(required=False, label='URL изображения')

    class Meta:
        model = Post
        fields = ['title', 'content', 'photo', 'photo_url', 'is_published', 'cat', 'tags']


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(required=False, label='E-mail',
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    content = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ContactForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['name'].initial = user.username
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['email'].initial = user.email
            self.fields['email'].widget.attrs['readonly'] = True
        else:
            self.fields['captcha'] = CaptchaField()
