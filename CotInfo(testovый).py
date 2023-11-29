import os
import datetime as dt
import pandas as pd
# # Парсинг таблицы
# def parse_table(adres, id):
#     temp = dict()
#     for f_name in os.listdir(os.getcwd()+'\FilesForBot'):
#         with open(f'{os.getcwd()}\\FilesForBot\{f_name}', 'r') as fol:
#             file = fol.readlines()
#             ad = list()
#             for i in file:

#                 if 'нет данных' not in i:
#                     # print(i)
#                     ad.append(i.replace('\n', ''))
#             temp[f_name.split('.')[0]] = ad
#     # return temp
#     try:
#         with open(f'{os.getcwd()}\Settings\Settings_{id}.txt', 'r', encoding='utf-8') as fol:
#             if 'separate' in fol.read():
#                 return ''.join([i.split(',')[0]+','+i.split(',')[1][0:2]+'/\\' if ',' in i else f'{i}/\\' for i in temp[adres]]).replace('/\\','\n')
#             else:
#                 return ''.join([f'{i}/\\' for i in temp[adres]]).replace('/\\','\n')
#     except:
#         return ''.join([f'{i}/\\' for i in temp[adres]]).replace('/\\','\n')
    
def parse_table():
    temp = dict()
    for f_name in os.listdir(os.getcwd()+'\FilesForBot'):
        with open(f'{os.getcwd()}\\FilesForBot\{f_name}', 'r') as fol:
            file = fol.readlines()
            ad = list()
            for i in file:

                if 'нет данных' not in i:
                    # print(i)
                    ad.append(i.replace('\n', ''))
            temp[f_name.split('.')[0]] = ad
    return temp

# print(parse_table('14-Линия74(3)', 5288656086))

# cotelnaya_l=''.join([i.split(',')[0]+','+i.split(',')[1][0:2]+'/\\' if ',' in i else f'{i}/\\' for i in parse_table()['14-Линия74(3)']]).replace('/\\','\n')
cotelnaya_r = ''

# '14-Линия74(3)'
# Шеболдаева4Д(1)
for i in parse_table()['Шеболдаева4Д(1)']:
    if ',' in i:

        a = i.split(',')[0]+','+i.split(',')[1][0:2]

    else:
        a = i
    cotelnaya_r += ''.join(f'{a}\n')

# print(cotelnaya_l)
print(cotelnaya_r)
# with open(f'{os.getcwd()}\Settings\Settings_5288656086.txt', 'w', encoding='utf-8') as fol:
#     fol.write('separate')









