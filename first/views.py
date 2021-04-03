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
    return render(request, 'first/about.html', {'title': 'About'})
