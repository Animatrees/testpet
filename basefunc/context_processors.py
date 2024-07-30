def get_context_menu(request):
    menu_items = [{'title': "О сайте", 'url_name': 'about'},
                  {'title': "Добавить статью", 'url_name': 'add_page'},
                  {'title': "Обратная связь", 'url_name': 'contact'},
    ]

    return {'menu': menu_items}
