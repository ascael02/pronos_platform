from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Bookmaker, ClicAffilie


def liste_bookmakers(request):
    bookmakers = Bookmaker.objects.filter(actif=True).order_by('ordre')
    return render(request, 'bookmakers/liste.html', {'bookmakers': bookmakers})


def detail_bookmaker(request, slug):
    bk = get_object_or_404(Bookmaker, slug=slug, actif=True)
    return render(request, 'bookmakers/detail.html', {'bk': bk})


def redirect_affilie(request, slug):
    bk = get_object_or_404(Bookmaker, slug=slug, actif=True)
    ClicAffilie.objects.create(
        bookmaker=bk,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )
    return HttpResponseRedirect(bk.lien_affilie)
