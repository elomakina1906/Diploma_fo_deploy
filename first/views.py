from django.http import HttpResponse
from django.shortcuts import render
import pandas


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
    city = request.GET['city']
    month = request.GET['month']
    top = request.GET['top']
    if top == "":
        top = 5
    if city != "":
        rating = {
            'rating': rating_city_month(city, month)
        }
        return render(request, 'first/about.html', rating)
    else:

        rating = {
            'rating': month_to_top_of_cities(month)[:int(top)]
        }
        return render(request, 'first/month_to_top_of_cities.html', rating)


def rating_city_month(city, month):
    data = pandas.read_csv('k3_csv.csv')
    mark_sum = 0
    mark_cnt = 0
    city_we_need = city  # "Краснодар"
    month_we_need = month  # "январь"
    month_we_need = month_we_need[0:len(month_we_need) - 1]
    for value in data.iloc:
        if value['город'] == city_we_need:
            month = value['дата'].split(' ')[2]
            if month.startswith(month_we_need):
                mark_sum += value['оценка']
                mark_cnt += 1
    return mark_sum / mark_cnt


def month_to_top_of_cities(month):
    data = pandas.read_csv('k3_csv_2.csv')
    month_we_need = month
    month_we_need = month_we_need[0:len(month_we_need) - 1]
    d = {}  # Ключ: город; Значение: list(сумма оценок, количество оценок)
    for value in data.iloc:
        month_split = value['дата'].split(' ')
        month = month_split[3]
        if month.startswith(month_we_need):
            city = value['город']
            if d.get(city) is not None:
                d[city][0] += value['оценка']  # Увеличиваем сумму оценок
                d[city][1] += 1  # Увеличиваем количество оценок
            else:
                d[city] = [value['оценка'], 1]
    lst = []
    for x in d:
        lst.append([x, d[x][0]/d[x][1]])
    # print(lst)
    lst = sorted(lst, key=lambda rec: rec[1]*(-1))
    # print(lst)
    return lst
