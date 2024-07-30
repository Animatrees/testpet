from django.http import HttpResponseNotFound


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не существует</h1>')
