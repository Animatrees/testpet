from django.core.files.base import ContentFile
from django.views.generic.base import ContextMixin
from django.views.generic.list import MultipleObjectMixin
import requests


class DataMixin(ContextMixin):
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.page_title is not None:
            context['title'] = self.page_title
        return context


class PaginateMixin(MultipleObjectMixin):
    paginate_by = 3

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        page_kwarg = self.page_kwarg
        page_number = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        page = paginator.get_page(page_number)
        return paginator, page, page.object_list, page.has_other_pages()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_range"] = context["paginator"].get_elided_page_range(context["page_obj"].number, on_each_side=2,
                                                                           on_ends=1)
        return context


# def get_photo(form):
#     print(form.cleaned_data)
#     photo_url = form.cleaned_data.get('photo_url')
#     photo = form.cleaned_data.get('photo')
#     photo_content = None
#
#     if photo_url:
#         try:
#             image_response = requests.get(photo_url)
#             image_response.raise_for_status()
#             photo_content = ContentFile(image_response.content)
#         except requests.exceptions.RequestException:
#             pass
#     elif photo:
#         photo_content = photo
#
#     return photo_content
