from django.contrib.messages import success
from django.core.validators import validate_slug
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from help_app.models import Article


@require_GET
def list_articles(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.all()
    return render(
        request,
        f"{__package__}/{list_articles.__name__}.html",
        {
            "articles": articles,
        },
    )


@require_http_methods(["GET", "POST"])
def create_article(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        validate_slug(request.POST["slug"])
        article = Article.objects.create(
            title=request.POST["title"],
            slug=request.POST["slug"],
            description=request.POST["description"] or None,
            text=request.POST["text"],
        )
        success(request, f"Created {article}.")
        return redirect(article)
    return render(request, f"{__package__}/{create_article.__name__}.html", {})


@require_GET
def view_article(request: HttpRequest, slug: str) -> HttpResponse:
    article = get_object_or_404(Article, slug=slug)
    return render(
        request,
        f"{__package__}/{view_article.__name__}.html",
        {
            "article": article,
        },
    )


@require_http_methods(["GET", "POST"])
def edit_article(request: HttpRequest, slug: str) -> HttpResponse:
    article = get_object_or_404(Article, slug=slug)
    if request.method == "POST":
        article.title = request.POST["title"]
        article.slug = request.POST["slug"]
        article.description = request.POST["description"] or article.description
        article.text = request.POST["text"]
        article.save()
        success(request, f"Saved changes to {article}.")
        return redirect(article)
    return render(
        request,
        f"{__package__}/{edit_article.__name__}.html",
        {
            "article": article,
        },
    )


@require_POST
def delete_article(request: HttpRequest, slug: str) -> HttpResponse:
    article = get_object_or_404(Article, slug=slug)
    title = article.title
    article.delete()
    success(request, f"Deleted {title}.")
    return redirect("list_articles")
