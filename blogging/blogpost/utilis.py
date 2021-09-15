from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Post


def paginatepost(request, post, results):
    page = request.GET.get('page')
    paginator = Paginator(post, results)
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        post = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        post = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, post


def searchpost(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    post = Post.objects.distinct().filter(
        # Q(published_date__isnull=False),
        Q(title__icontains=search_query) |
        Q(text__icontains=search_query) |
        Q(author__username__icontains=search_query)
    )

    return post, search_query
