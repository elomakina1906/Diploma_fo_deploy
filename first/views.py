from django.http import HttpResponse
from django.shortcuts import render


posts = [
    {
        'author': 'Author 1',
        'title': 'Post 1',
        'date': 'date 1'
    },
    {
        'author': 'Author 2',
        'title': 'Post 2',
        'date': 'date 2'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'first/home.html', context)

def about(request):
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    m = {
        'city': request.GET['city'],
        'month': request.GET['month']
    }
    return render(request, 'first/about.html', m)

#def about(request):
 #   return render(request, 'first/about.html', {'title': 'About'})
