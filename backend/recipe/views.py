from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Recipe, Tag

# вьюха не сделана
def index(request):
    return render(
        request,
        "index.html",
    )

def page_not_found(request, exception):
    """Функция страницы 404"""
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    """Функция страницы 500"""
    return render(request, "misc/500.html", status=500)
