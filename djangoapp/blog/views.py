from typing import Any
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
# from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
# from django.shortcuts import render
from blog.models import Post, Page
from django.http import Http404, HttpRequest, HttpResponse

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
        context.update(
            {'page_title': 'HOME - ', }
        )
        return context


# def index(request):

#     posts = Post.objManager.get_published()

#     paginator = Paginator(posts, 9)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'HOME - ',
#         }
#     )

# view que filtra por criador:


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context = {}
    # Usamos o get para previnir erros caso eu queira redirecionar para pagina

    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:

        author_pk = self.kwargs.get('id')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404

        self._temp_context.update(
            {
                'author_pk': author_pk,
                'user': user,

            }
        )

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['author_pk'])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self._temp_context['user']

        page_title = user.username + ' posts - '

        context.update(
            {'page_title': page_title, }
        )
        return context


# def created_by(request, id):
#     user = User.objects.filter(pk=id).first()

#     if user is None:
#         raise Http404

#     page_title = user.username + ' posts - '

#     posts = Post.objManager.get_published().filter(created_by__pk=id)

#     paginator = Paginator(posts, 9)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


class CategoryListView(PostListView):
    # erro 404 para categorias vazias:
    allow_empty = False

    def get_queryset(self):
        # self.kwargs.get() -> Coleta argumentos da URL
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - '  # type: ignore
        context.update(
            {'page_title': page_title, }
        )
        return context


# def category(request, slug):

#     posts = Post.objManager.get_published().filter(category__slug=slug)

#     paginator = Paginator(posts, 9)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f'{page_obj[0].category.name} - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = (
            f'{self.object_list[0].tags.first().name} - '  # type: ignore
        )
        context.update(
            {'page_title': page_title, }
        )
        return context


# def tag(request, slug):

#     posts = Post.objManager.get_published().filter(tags__slug=slug)

#     paginator = Paginator(posts, 9)
#     page_number = request.GET.get("page", '').strip()
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f'{page_obj[0].tags.first().name} - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


class SearchListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._search_value = ''

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:

        if self._search_value == '':
            return redirect('blog:index')

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(title__icontains=self._search_value) |
            Q(excerpt__icontains=self._search_value) |
            Q(content__icontains=self._search_value)
        )[:9]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = (
            f'{self._search_value[:20]} - '  # type: ignore
        )
        context.update({
            'search_value': self._search_value,
            'page_title': page_title,
        })
        return context


# def search(request):
#     # GET -> http
#     # get -> python -> obter valor
#     search_value = request.GET.get('search')
#     posts = Post.objManager.get_published().filter(
#         Q(title__icontains=search_value) |
#         Q(excerpt__icontains=search_value) |
#         Q(content__icontains=search_value)
#     )[:9]

#     page_title = f'{search_value[:20]} - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': posts,
#             'search_value': search_value,
#             'page_title': page_title,
#         }
#     )


class PageDetailView(DetailView):
    template_name = 'blog/pages/page.html'
    model = Page
    slug_field = 'slug'
    context_object_name = 'page'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'{page.title} - '  # type:ignore
        context.update({
            'page_title': page_title,
        })
        return context


# def page(request, slug):
#     page_obj = (
#         Page.objects.filter(is_published=True).filter(slug=slug).first()
#     )

# #     if page_obj is None:
# #         raise Http404()

# #     page_title = f'{page_obj.title} - '

# #     return render(
# #         request,
# #         'blog/pages/page.html',
# #         {
# #             'page': page_obj,
# #             'page_title': page_title,
# #         }
# #     )


class PostDetailView(DetailView):
    template_name = 'blog/pages/post.html'
    model = Post
    slug_field = 'slug'
    context_object_name = 'post'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        post_title = f'{post.title} - '  # type:ignore
        context.update({
            'post_title': post_title,
        })
        return context


# def post(request, slug):
#     post_obj = Post.objManager.get_published().filter(slug=slug).first()

#     if post_obj is None:
#         raise Http404()

#     page_title = f'{post_obj.title} - '

#     return render(
#         request,
#         'blog/pages/post.html',
#         {
#             'post': post_obj,
#             'page_title': page_title,
#         }
#     )
