#импорты - реквексты для загрузок веб-странци, csv для .csv файлов,
#Pool из multiprocessing дял многоядерки и sys для системной всякой хуеты
import requests
import csv
from multiprocessing import Pool
import sys

#функция для загрузки вакансии по id. Блок try пытается загрузить страницу и проверяет,
#подходит ли она под заданные параметры(годы спеки). Если да - следующая функция, нет-печатаем id чтобы знать где трабл
def load(vac_id):
    try:
        vac_id = str(vac_id)
        while len(vac_id) < 8: #проверка на длину id и если что дописываем 0 до нужного количесва цифра (8)
            vac_id = '0' + vac_id
        vac = requests.get(f'https://api.hh.ru/vacancies/{vac_id}')#грузим страницу по id
        if vac.status_code == 200:#если загрузили то
            vac = vac.json() # конверт в json чтобы дальше в массив
            if vac['published_at'][:4] in ('2016', '2017', '2018', '2019', '2020', '2021'):#чек на нужные года
                if vac['area']['id'] in ('2', '1'):#чек на мск спб
                    parse(vac)#некст функция если всё удачно
                    return
            return
        return
    except Exception:
        print(vac_id)#если в страе что то пошло по пизде тупо печатаем id шоб знать где ошибка


def parse(vac):#функция которая парсит полученный в прошлой функции json в строку для .csv файла
    skills = ''
    for skill in vac['key_skills']:
        skills += f"{skill['name']} | "
    code = ''
    name = ''
    for spec in vac['specializations']:
        code += spec['id'] + ' '
        name += spec['name'] + ', '
    if vac['salary'] is None:#тут интересный чек на зарплату. Иногда её не пишут или пишут не полностью.
        vac['salary'] = {'from': '-', 'to': '-'}
    else:
        if vac['salary']['from'] is None:
            vac['salary']['from'] = '-'
        if vac['salary']['to'] is None:
            vac['salary']['to'] = '-'
    info = {'id': vac['id'], 'name': vac['name'], 'publication_date': vac['published_at'][:10],
            'city': vac['area']['name'], 'experience': vac['experience']['name'], 'skills': skills.rstrip('| '),
            'spec.code': code.rstrip(' '), 'spec.name': name.rstrip(', ').strip('"'),
            'salary.from': vac['salary']['from'], 'salary.to': vac['salary']['to']}# с 44 по 47 строку - одна строка.
#запихиваем все нужные данные в словарь(dict) для записи в .csv
    write_data(info)#функция для записи полученного dict в .csv файл
    return
#тут рил по факту работа с массивами (json). Просто нужный элемент массива в нужный момент строки пихаем.


def write_data(data):#пишем в .csv (тут скучно, просто юзаем метод из библы csv для записи словаря в строку .csv)
    with open('data.csv', 'a', encoding='utf8') as f:
        wr = csv.DictWriter(f, fieldnames=['id', 'name', 'publication_date', 'city', 'experience', 'skills',
                                           'spec.code', 'spec.name', 'salary.from', 'salary.to'])
        wr.writerow(data)


if __name__ == '__main__':#мэйн, прога запускается тут изначально
    params = sys.argv#чекаем параметры запуска, они же id с которого начинаем и id которым заканчиваем
    if len(params) == 3:#если 2 параметра (да я знаю что написано 3 но по факту чек на 2 приколы программирования такие)
        print(f'{params[1]}-{params[2]} in process')
        with Pool() as p:#запускаем процессы на стольких ядрах, сколько есть
            p.map(load, range(int(params[1]), int(params[2])))#вызываем САМУЮ 1 ФУНКЦИЮ СВЕРХУ для каждого id
    else:
        print('Wrong parameters! Please input lower and upper boundaries of the vacancies ID interval.')#мало ли не 2
