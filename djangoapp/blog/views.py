from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from blog.models import Post, Page
from django.http import Http404

posts = list(range(1000))


class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'post'
    ordering = '-pk',
    paginate_by = 9
    queryset = Post.objManager.get_published()

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context.update(
            {'page_title': 'HOME - ', }
        )
        return context


def index(request):

    posts = Post.objManager.get_published()

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': 'HOME - ',
        }
    )

# view que filtra por criador:


def created_by(request, id):
    user = User.objects.filter(pk=id).first()

    if user is None:
        raise Http404

    page_title = user.username + ' posts - '

    posts = Post.objManager.get_published().filter(created_by__pk=id)

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def category(request, slug):

    posts = Post.objManager.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()

    page_title = f'{page_obj[0].category.name} - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def tag(request, slug):

    posts = Post.objManager.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page", '').strip()
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()

    page_title = f'{page_obj[0].tags.first().name} - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def search(request):
    # GET -> http
    # get -> python -> obter valor
    search_value = request.GET.get('search')
    posts = Post.objManager.get_published().filter(
        Q(title__icontains=search_value) |
        Q(excerpt__icontains=search_value) |
        Q(content__icontains=search_value)
    )[:9]

    page_title = f'{search_value[:20]} - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        }
    )


def page(request, slug):
    page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first()

    if page_obj is None:
        raise Http404()

    page_title = f'{page_obj.title} - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )


def post(request, slug):
    post_obj = Post.objManager.get_published().filter(slug=slug).first()

    if post_obj is None:
        raise Http404()

    page_title = f'{post_obj.title} - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )
