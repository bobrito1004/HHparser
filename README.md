# HHparser
Проект по поиску вакансий на hh.ru
Проект по поиску вакансий на hh.ru Задача - найти нужные вакансии со всего hh по заданным заказчиком критериям, после чего вывести необходимые в csv файл для дальнейшей обработки. К сожалению, на прямую через API найти нужные вакансии не вышло, поэтому пришлось брать каждую вакансию по id, начиная с 0 и заканчивая 43846426. Для ускорения алгоритма я поделил id на интервалы и запускал алгоритм на 16 вирутальных машинах на Google Cloud одновременно, а также использова многопоточность.
