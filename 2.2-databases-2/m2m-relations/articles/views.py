from django.shortcuts import render
from .models import Article


def articles_list(request):
    template = 'articles/news.html'

    # Получаем все статьи, сортируем по дате публикации (свежие сверху)
    articles = Article.objects.all().order_by('-published_at')

    # Передаем статьи в контекст под именем object_list (как требует шаблон)
    context = {
        'object_list': articles
    }

    return render(request, template, context)