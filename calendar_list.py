import calendar
from dateutil import rrule
from datetime import datetime, timedelta
from pprint import pp, pprint
from collections import defaultdict


def generate_month(year: int, month: int) -> list:
    """Первый день месяца"""
    first_day_of_month = datetime(year, month, 1)

    """Последний день месяца"""
    last_day_of_month = first_day_of_month.replace(day=calendar.monthrange(year, month)[1])

    """Сгенерированные календарные дни"""
    range_date = rrule.rrule(rrule.DAILY, dtstart=first_day_of_month, until=last_day_of_month)

    """Последний день предыдущего месяца"""
    last_day_of_last_month = first_day_of_month - timedelta(days=1)

    """Кол-во недель в месяце"""
    max_week = len(calendar.monthcalendar(year, month))

    """Кол-во дней в недели"""
    DAYS_WEEK = 7

    dict_days = defaultdict(lambda: [])
    for i in range(DAYS_WEEK):
        for day in range_date:
            if day.weekday() == i:
                dict_days[i].append(day)

    """Получаем индекс элемента с первым и последним числом"""
    first_day_of_week = 0

    for index, value in dict_days.items():
        for date in value:
            if first_day_of_month.day == date.day:
                first_day_of_week = index
            if last_day_of_month.day == date.day:
                last_day_of_week = index

    month = []  # Список с неделями
    """Заполнием пустую матрицу"""
    for i in range(max_week):
        week = [0 for i in range(DAYS_WEEK)]
        month.append(week)

    index = 0
    """Индекс последнего дня предыдущего месяца"""
    pre_date = first_day_of_week
    while pre_date:
        pre_date -= 1
        month[0][index] = {
                    'date': datetime.strftime(last_day_of_last_month-timedelta(days=pre_date), '%Y-%m-%d'),
                    'count_ticket' : 23 ,
                    'ticket' : ['8:00' for i in range(5) ],
                    'is_weekend' : True if index in [5,6] else False
                }
        index += 1

    index = 0
    """Первого дня следующего месяца"""
    last_index = last_day_of_week
    while last_index < DAYS_WEEK:
        month[-1][last_index] = {
                    'date': datetime.strftime(last_day_of_month + timedelta(days=index), '%Y-%m-%d'),
                    'count_ticket' : 23 ,
                    'ticket' : ['8:00' for i in range(5) ],
                    'is_weekend' : True if index in [5,6] else False
                }
        last_index += 1
        index += 1


    """Формируем календарь с вложенными параметрами"""
    for week_num, weeks in enumerate(month):
        for index, value in enumerate(weeks):
            if first_day_of_week <= index and week_num < len(dict_days[index]):
                month[week_num][index] = {
                    'date': datetime.strftime(dict_days[index][week_num], '%Y-%m-%d'),
                    'count_ticket' : 23 ,
                    'ticket' : ['8:00' for i in range(5) ],
                    'is_weekend' : True if index in [5,6] else False
                }

            if index < first_day_of_week and len(dict_days[index]) > week_num >= 0:
                month[week_num+1][index] = {
                    'date': datetime.strftime(dict_days[index][week_num], '%Y-%m-%d'),
                    'count_ticket' : 23 ,
                    'ticket' : ['8:00' for i in range(5) ],
                    'is_weekend' : True if index in [5,6] else False
                }

    return month


month = generate_month(2021, 9)

pprint(month)