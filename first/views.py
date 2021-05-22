from django.shortcuts import render
import pandas


def home(request):
    return render(request, 'first/home.html')


def about(request):
    data = pandas.read_csv('k3_csv_2.csv')
    city = request.GET['city'].lower().strip()
    month = request.GET['month'].lower().strip()
    top = request.GET['top']
    if top == "":
        top = 5
    if not month_is_correct(month):
        rating = {'rating': "Такого месяца не существует"}
        return render(request, 'first/error.html', rating)
    if city != "":
        if month != "":
            r = rating_city_month(city, month, data)
            if r != 0:
                rating = {'rating': r}
                return render(request, 'first/about.html', rating)
            else:
                rating = {'rating': "В базе данных нет такого города"}
                return render(request, 'first/error.html', rating)
        else:
            r = rating_city(city, data)
            if len(r) != 0:
                rating = {'rating': rating_city(city, data)}
                return render(request,
                              'first/month_to_top_of_cities.html', rating)
            else:
                rating = {'rating': "В базе данных нет такого города"}
                return render(request, 'first/error.html', rating)
    else:
        if month != "":
            rating = {'rating':
                      month_to_top_of_cities(month, data)[:int(top)]}
            return render(request, 'first/month_to_top_of_cities.html', rating)
        else:
            rating = {'rating': "Данные не введены"}
            return render(request, 'first/error.html', rating)


def month_is_correct(month):
    months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
              'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь', '']
    res = False
    for m in months:
        if m == month:
            res = True
    return res


def rating_city_month(city, month, data):
    mark_cnt = 0
    mark_sum = 0
    month_we_need = month[0:len(month) - 1]
    for value in data.iloc:
        if value['город'].lower().strip() == city:
            month = value['дата'].split(' ')[3]
            if month.startswith(month_we_need):
                mark_sum += value['оценка']
                mark_cnt += 1
    if mark_cnt != 0:
        return mark_sum / mark_cnt
    else:
        return 0


def rating_city(city, data):
    d = {}  # Ключ: месяц; Значение list(сумма оценок, количество оценок)
    for value in data.iloc:
        if value['город'].lower().strip() == city:
            month = value['дата'].split(' ')[3]
            if d.get(month) is not None:
                d[month][0] += value['оценка']
                d[month][1] += 1
            else:
                d[month] = [value['оценка'], 1]
    lst = []
    for x in d:
        new_x = x.title()[0:len(x) - 2]
        if not (new_x.startswith('Март') | new_x.startswith('Август')):
            if new_x.startswith('Ма'):
                new_x += 'й'
            else:
                new_x += 'ь'
        lst.append([new_x, d[x][0] / d[x][1]])
    lst = sorted(lst, key=lambda rec: rec[1]*(-1))
    return lst


def month_to_top_of_cities(month, data):
    month_we_need = month[0:len(month) - 1]
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
        lst.append([x, d[x][0] / d[x][1]])
    lst = sorted(lst, key=lambda rec: rec[1]*(-1))
    return lst
