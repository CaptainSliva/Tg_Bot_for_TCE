import xlrd
import xlwt
from random import randint as rnd

def new_table():
    adr = ['', 'Абаканская', 'Благодатная', 'Врубовая', 'Часовой']
    x=1
    y=0

    workbook = xlwt.Workbook (encoding = 'utf-8') # Создать объект книги
    worksheet = workbook.add_sheet ("класс 1")
    worksheet.write(0, 0, 'Адрес'); worksheet.write(0, 1, 'T1'); worksheet.write(0, 2, 'T2'); worksheet.write(0, 3, 'P1'); worksheet.write(0, 4, 'P2')

    while y<5:
        if y == 0:
            for i in range(1, len(adr)):
                worksheet.write(i, y, adr[i]) # Записать содержимое в таблицу, первую строку параметров, второй столбец параметров и содержимое третьего параметра
            y+=1
        if y == 1 or y == 2:
            for i in range(x, 5):
                worksheet.write(i, y, f'{rnd(0,1000)/10}ºC') # Записать содержимое в таблицу, первую строку параметров, второй столбец параметров и содержимое третьего параметра
            y+=1
        if y == 3 or y == 4:
            for i in range(x, 5):
                worksheet.write(i, y, f'{rnd(0,60)/10}') # Записать содержимое в таблицу, первую строку параметров, второй столбец параметров и содержимое третьего параметра
            y+=1



    workbook.save('Псевдокотельные.xls') # Назовите его и сохраните локально
