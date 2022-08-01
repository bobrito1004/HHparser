import requests
import csv
from multiprocessing import Pool
import sys


def load(vac_id):
    try:
        vac_id = str(vac_id)
        while len(vac_id) < 8:
            vac_id = '0' + vac_id
        vac = requests.get(f'https://api.hh.ru/vacancies/{vac_id}')
        if vac.status_code == 200:
            vac = vac.json()
            if vac['published_at'][:4] in ('2016', '2017', '2018', '2019', '2020', '2021'):
                if vac['area']['id'] in ('2', '1'):
                    parse(vac)
                    return
            return
        return
    except Exception:
        print(vac_id)


def parse(vac):
    skills = ''
    for skill in vac['key_skills']:
        skills += f"{skill['name']} | "
    code = ''
    name = ''
    for spec in vac['specializations']:
        code += spec['id'] + ' '
        name += spec['name'] + ', '
    if vac['salary'] is None:
        vac['salary'] = {'from': '-', 'to': '-'}
    else:
        if vac['salary']['from'] is None:
            vac['salary']['from'] = '-'
        if vac['salary']['to'] is None:
            vac['salary']['to'] = '-'
    info = {'id': vac['id'], 'name': vac['name'], 'publication_date': vac['published_at'][:10],
            'city': vac['area']['name'], 'experience': vac['experience']['name'], 'skills': skills.rstrip('| '),
            'spec.code': code.rstrip(' '), 'spec.name': name.rstrip(', ').strip('"'),
            'salary.from': vac['salary']['from'], 'salary.to': vac['salary']['to']}
    write_data(info)
    return


def write_data(data):
    with open('data.csv', 'a', encoding='utf8') as f:
        wr = csv.DictWriter(f, fieldnames=['id', 'name', 'publication_date', 'city', 'experience', 'skills',
                                           'spec.code', 'spec.name', 'salary.from', 'salary.to'])
        wr.writerow(data)


if __name__ == '__main__':
    params = sys.argv
    if len(params) == 3:
        print(f'{params[1]}-{params[2]} in process')
        with Pool() as p:
            p.map(load, range(int(params[1]), int(params[2])))
    else:
        print('мудак.')
