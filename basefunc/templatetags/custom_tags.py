from django import template
from django.db.models import Count

import basefunc.views as views
from basefunc.models import Category, Tags

register = template.Library()


@register.inclusion_tag('basefunc/cats_menu.html', takes_context=True)
def cats_menu(context, cat_id):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_id': cat_id, 'title': context['title']}


@register.inclusion_tag('basefunc/tags_menu.html')
def tags_menu(tag_id):
    sorted_tags = Tags.objects.annotate(num_posts=Count('women')).filter(num_posts__gt=0).order_by('title')
    return {'tags': sorted_tags, 'tag_id': tag_id}
