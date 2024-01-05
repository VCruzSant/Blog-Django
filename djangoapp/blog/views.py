from django.shortcuts import render

# Create your views here.


def index(request):
    return render(
        request,
        'blog/pages/index.html',
        {
            'name': 'Vini Sant'
        }
    )


def post(request):
    return render(
        request,
        'blog/pages/post.html',
        {
            'name': 'Esse é o POST'
        }
    )


def page(request):
    return render(
        request,
        'blog/pages/page.html',
        {
            'name': 'Essa é a PAGE'
        }
    )
