from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article, Categorie


def liste_articles(request):
    qs = Article.objects.filter(statut='publie').select_related('auteur', 'categorie')
    categorie_slug = request.GET.get('categorie')
    search = request.GET.get('q')
    if categorie_slug:
        qs = qs.filter(categorie__slug=categorie_slug)
    if search:
        qs = qs.filter(Q(titre__icontains=search) | Q(extrait__icontains=search))
    paginator = Paginator(qs, 9)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/liste.html', {
        'page_obj': page,
        'categories': Categorie.objects.all(),
        'categorie_active': categorie_slug,
        'search': search,
    })


def detail_article(request, slug):
    article = get_object_or_404(Article, slug=slug, statut='publie')
    Article.objects.filter(pk=article.pk).update(vues=article.vues + 1)
    recents = Article.objects.filter(statut='publie').exclude(pk=article.pk)[:4]
    return render(request, 'blog/detail.html', {'article': article, 'recents': recents})
