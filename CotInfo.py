import fitz
from typing import Tuple
import os
import datetime as dt
# Парсинг папки
def parse_table():
    temp = dict()
    for f_name in os.listdir(os.getcwd()+'\FilesForBot'):
        
        if f_name not in ['P_reports', 'T_reports']:
            # print(f_name)
            with open(f'{os.getcwd()}\\FilesForBot\{f_name}', 'r') as fol:
                file = fol.readlines()
                ad = list()
                for i in file:

                    if 'нет данных' not in i:
                        # print(i)
                        ad.append(i.replace('\n', ''))
                temp[f_name.split('.')[0]] = ad
        else:
            print(-1)
    return temp

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
#         with open(f'{os.getcwd()}\Subscribers\Settings_{id}.txt', 'r', encoding='utf-8') as fol:
#             if 'separate' in fol.read():
#                 return ''.join([i.split(',')[0]+','+i.split(',')[1][0:2]+'/\\' if ',' in i else f'{i}/\\' for i in temp[adres]]).replace('/\\','\n')
#             else:
#                 return ''.join([f'{i}/\\' for i in temp[adres]]).replace('/\\','\n')
#     except:
#         return ''.join([f'{i}/\\' for i in temp[adres]]).replace('/\\','\n')


def create_subscribers(): # Создание файла для подписок
    if not os.path.isdir("Subscribers"):
        os.mkdir("Subscribers")



def create_dir_for_admin(): # Создание файла для администрирования подписчиков
    if not os.path.isdir("FilesForAdmin"):
        os.mkdir("FilesForAdmin")
        open(f'{os.getcwd()}\FilesForAdmin\Subscribers.txt', 'w', encoding='utf-8').close()
        open(f'{os.getcwd()}\FilesForAdmin\SubscribersNo.txt', 'w', encoding='utf-8').close()


def bot_nosubscribers(name, id): # Добавление пользователя в файл с ожидающими подписку пользователями
    id_list_n = list()
    if len(name.split(' ')) == 4:
        with open(f'{os.getcwd()}\FilesForAdmin\SubscribersNo.txt', 'r', encoding='utf-8') as fol:
            file = fol.read().split('\n')
            id_list_n = [i for i in file if i != '']
            if id not in [i.split(' = ')[1] for i in file if i != '']:
                id_list_n.append(f'{name} = {id}')
        with open(f'{os.getcwd()}\FilesForAdmin\SubscribersNo.txt', 'w', encoding='utf-8') as fol:
            id_list_n.sort()
            for i in id_list_n:
                fol.write(f'{i}\n')

# bot_nosubscribers('Ка Кв1 Ка2 23567', '25sad6a5')
def bot_subscribers_ac(id): # Принятие пользователя в ряды подписчиков бота
    id_list_n = list()
    id_list_y = list()
    with open(f'{os.getcwd()}\FilesForAdmin\SubscribersNo.txt', 'r', encoding='utf-8') as fol:
        file = fol.read().split('\n')
        # id_list_n = [i for i in file if i != '']
        id_list_n = [i for i in [i for i in file if i != ''] if i.split(' = ')[1] != id]
        id_list_y = [i for i in [i for i in file if i != ''] if i.split(' = ')[1] == id]

    with open(f'{os.getcwd()}\FilesForAdmin\SubscribersNo.txt', 'w', encoding='utf-8') as fol:
        for i in id_list_n:
            print(id_list_n)
            fol.write(f'{i}\n')

    with open(f'{os.getcwd()}\FilesForAdmin\Subscribers.txt', 'r', encoding='utf-8') as fol:
        file = fol.read().split('\n')
        for i in file:
            id_list_y.append(f'{i}')

    with open(f'{os.getcwd()}\FilesForAdmin\Subscribers.txt', 'w', encoding='utf-8') as fol:
        id_list_y.sort()
        for i in id_list_y[1:]:
            fol.write(f'{i}\n')


def list_FileSub_or_No(filename): # Список пользователей которые хранятся в файле 
    SubNo = list()
    with open(f'{os.getcwd()}\FilesForAdmin\{filename}.txt', 'r', encoding='utf-8') as fol:
        file = fol.read().split('\n')
        if len(file) == 0:
            SubNo = ['Людей нет']
        else:
            SubNo = [i for i in file]
    return SubNo


def del_from(id, filename): # Удаление человека из желающих подписаться
    SubNo = list()
    with open(f'{os.getcwd()}\FilesForAdmin\{filename}.txt', 'r', encoding='utf-8') as fol:
        file = fol.read().split('\n')
        SubNo = [i for i in [i for i in file if i != ''] if i.split(' = ')[1] != id]
    with open(f'{os.getcwd()}\FilesForAdmin\{filename}.txt', 'w', encoding='utf-8') as fol:
        for i in SubNo:
            fol.write(f'{i}\n')


def bot_check_sub(id, filename): # Проверка пользователя на принадлежность к подписчикам бота
    with open(f'{os.getcwd()}\FilesForAdmin\{filename}.txt', 'r', encoding='utf-8') as fol:
        file = fol.read().split('\n')
        if id in [i.split(' = ')[1] for i in file if i != '']:
            return True
        else:
            return False


def parse_user_info(id, filename):
    user_info = list()
    with open(f'{os.getcwd()}\FilesForAdmin\{filename}.txt', 'r', encoding='utf-8') as fol:
        file = fol.read().split('\n')
        info = [i.split(' ') for i in file if i != ' ']
        for i in info:
            if id in i:
                for j, k in enumerate(i):
                
                    if j == 0:
                        user_info.append(f'Фамилия - {k}')
                    if j == 1:
                        user_info.append(f'Имя - {k}')
                    if j == 2:
                        user_info.append(f'Отчество - {k}')
                    if j == 3:
                        user_info.append(f'тел - {k}')
                    if j == 5:
                        user_info.append(f'id - {k}')

        # ''.join([f'{i}/\\' for i in ci.parse_table()[f'{id})']]).replace('/\\','\n') 
    return user_info
# dadada=''.join([f'{i}/\\' for i in parse_user_info(str(276693613), 'SubscribersNo')]).replace('/\\','\n')
# print(dadada)

# def del_trash(txt, repl):
#     for i, j in repl.items():
#         txt = txt.replace(i, j)
#     return txt
# r={"'" : "" , '"' : "" , "[" : "" , "]" : "" , "{" : "" , "}" : "" }

# async def settings_file(arg, id): # Функция для добавления / удаления настройки
#     async with aiofiles.open(f'{os.getcwd()}\Settings\Settings_{id}.txt', 'r', encoding='utf-8') as fol:
#         f = await fol.read()
#         if arg in f:
#             async with aiofiles.open(f'{os.getcwd()}\Settings\Settings_{id}.txt', 'w', encoding='utf-8') as fol:
#                 for i in f.split(', '):
#                     if i != arg:
#                         await fol.write(i)
#         else:
#             async with aiofiles.open(f'{os.getcwd()}\Settings\Settings_{id}.txt', 'a', encoding='utf-8') as fol:
#                 await fol.write(f'{arg}, ')


# async def check_param(filefrom, param, id): # Проверяет наличие параметра в файле
#     async with aiofiles.open(f'{os.getcwd()}\Settings\{filefrom}_{id}.txt', 'r', encoding='utf-8') as fol:
#         if param in await fol.read():
#             return True
#         else:
#             return False



def parse_file_district(): # Для создания словаря с принадлежностью котельной к теплосистемам с районом:  {'Евдокимова 35': {'Евдокимова 35(1)': ['Северный'], 'Евдокимова 35(2)': ['Северный'], 'Евдокимова 35(3)': ['Северный']}} 
    temp = dict()
    last_name = list()

    for f_name in os.listdir(os.getcwd()+'\FilesForBot'):
        last_name.append(f_name.split('.')[0])
        if f_name not in ['P_reports', 'T_reports']:
            with open(f'{os.getcwd()}\\FilesForBot\{f_name}', 'r') as fol:
                file = fol.readlines()
                ad = list()

                for i in file:
                    if 'РТС' in i:
                        ad.append(i.split(' : ')[1].replace('\n', ''))
                        break
                temp[f_name.split('(')[0]]=ad
                if len(last_name)>1:
                    indexses = [j for j in range(1,int(f_name.split('(')[1].split(')')[0])+1)]
                    temp[f_name.split('(')[0]]={str(last_name[-max(indexses)]) : ad}

                    for j in range(1, int(indexses[-1])+1):
                        if (last_name[-2]!=f_name.split('.')[0]) and (str(last_name[-2]).split('(')[0] == f_name.split('(')[0]):      
                            name = f_name.split('(')[0]
                            temp[name][f'{name}({j})']=ad
                        else:
                            pass        
                else:
                    temp[f_name.split('(')[0]]={f_name.split('.')[0] : ad}
    return temp


def parse_file_TP_district_t(val, interval): # Создаёт список файлов удоволетворяющих условию времени.
    temp = dict()
    last_name = list()
    name = list()
    for f_name in os.listdir(os.getcwd()+f'\FilesForBot\{val}_reports'):
        if f_name.split(f'_{val}')[1].split('h')[0] == str(interval):
            name.append(f_name.split(f'_{val}')[0])

            
    return name

def parse_file_TP_district(cotel, val, interval): # Создаёт список файлов удоволетворяющих условию времени.
    name = str()
    for f_name in os.listdir(os.getcwd()+f'\FilesForBot\{val}_reports'):
        if f_name.split(f'_{val}')[1].split('h')[0] == str(interval):
            # name.append(f_name.split(f'_{val}')[0])
            if cotel[:3:] in f_name and cotel[-3::] in f_name:
                name = f_name
                print(name)
                break

    return name
# print(parse_file_district())


def districts():
    ur2 = parse_file_district().values()
    trash_list_with_districts = list() # Районы всех котельных
    for j in ur2:
        for k in j.values():
            trash_list_with_districts.append(str(k).replace('[','').replace(']','').replace("'",''))
    districts = sorted(list(set([i for i in trash_list_with_districts]))) #Список районов
    return districts

# print(districts())

print('----------------')



# def file_check_id(id): # Чтение интересующего файла по его id
#     try:
#         with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'r', encoding='utf-8') as fol:
#             ad =  [line.split(',')[0] for line in fol.read().split('\n') if line != '']  
#         return ad
#     except:
#         return True
# print(check(6288656086))



# def parse_file():
#     temp = list()
#     with open(f'{os.getcwd()}\Информация о котельных.txt', 'r', encoding='utf-8') as fol:
#         file = fol
#         for i in file:
#             if i == 'температура':
#                 temp+=i
#     return(temp)
# print(parse_file)


def file_read(id): # Чтение интересующего файла по его id
    ad = list()
    try:
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'r', encoding='utf-8') as fol:
            ad =  [line.split(',')[0] for line in fol.read().split('\n') if line != '']   
        return ad
    except:
        return []


def file_check_copy(adres, id, copyadres): # Проверяет есть ли котельная в файле
    ad = list()

    try:
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'r', encoding='utf-8') as fol:
            file = fol.read().replace(f'{copyadres} = ', '')
            ad =  [line.split(', ')[0] for line in file.split('\n') if line != '' or copyadres in line]  
            print(adres, ad, id)
            if adres in ad:
                return True
            else:
                return False 
    except:
        print(adres, ad, id)
        return False


def adding_msg(): # Функция для формирования словаря id:adres (используется в рассылке)
    Unsubscribe=dict()
    ad = list()
    for i in os.listdir(os.getcwd()+'\Subscribers'):
        Filename=i.split('_')[-1].split('.')[0]
        try:
            with open(f'{os.getcwd()}\Subscribers\Subscribe_{Filename}.txt', 'r', encoding='utf-8') as fol:
                file = fol.read()
                ad =  [line.replace('sub = ', '') for line in file.split('\n') if line != '']    
            Unsubscribe[i.split('_')[-1].split('.')[0]] = ad # Фармирование словаря: ключ - айди пользователя, значенеие - писок котельных на которые он подписан
            
        except:
            return 'error', Filename

    return Unsubscribe
# print(adding_msg())
# for i in adding_msg():
#     print(i)


def subscribe_add(adres, id):  # Добавление котельной в подписки # adres - adres # id - message.from_user.id
    subscribe = list()
    try:
        print('try')
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'r', encoding='utf-8') as fol:  

            file = fol.read().replace('sub = ', '')
            a=[line for line in file.split('\n') if line != '']     # Сортировка котельных по алфавиту должна быть
            if adres not in a: a.append(adres)
            print(a)
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'w', encoding='utf-8') as new_fol: # Добавление котельной в файл с подписками
            subscribe = a
            subscribe.sort()
            # print(a.sort())
            print(subscribe)
            for i in subscribe:
                if 'fav' not in i:
                    new_fol.write(f'sub = {i}\n')
                else:
                    new_fol.write(f'{i}\n')

    except:
        print('except')
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'a', encoding='utf-8') as new_fol:
            new_fol.write(f'sub = {adres}\n')
    return subscribe


def subscribe_del(adres, id):  # Удаление котельной из подписок # adres - adres # id - message.from_user.id
    subscribe = list()
    try:
        print('try')
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'r', encoding='utf-8') as fol:  
            file = fol.read().replace('sub = ', '')
            # print(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt') 
            # print([line for line in fol.read().split('\n') if line != adres])
            a=[line for line in file.split('\n') if line.split(', ')[0] != adres and line != '']     # Сортировка котельных по алфавиту должна быть
            print(a)
            print(adres)
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'w', encoding='utf-8') as new_fol: # Добавление котельной в файл с подписками
            subscribe = a
            subscribe.sort()
            # print(a.sort())
            print(subscribe)
            for i in subscribe:
                if 'fav' not in i:
                    new_fol.write(f'sub = {i}\n')
                else:
                    new_fol.write(f'{i}\n')

    except:
        print('except')
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'a', encoding='utf-8') as new_fol:
            new_fol.write(f'sub = {adres}\n')
    return subscribe



def send_message_interval(adres, id, t): # Добавление интервала между сообщениями в 10 минут
    subscribe = list()
    try:
        print('try')
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'r', encoding='utf-8') as fol:  
            file = fol.read().replace('sub = ', '')
            a=[line for line in file.split('\n') if line != '']     # Сортировка котельных по алфавиту должна быть
            # full_adres = [line for line in a if line.split(', ')[0] == adres] # Добавление всей строки для данной котельной
            # print(full_adres, 'full')
            print(a)
            print(adres)
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'w', encoding='utf-8') as new_fol: # Добавление котельной в файл с подписками
            # subscribe = [line.replace(', 5', ', 10') if (line.split(',')[0] == adres) and (', 10' not in str(full_adres)) else line for line in a ] # Добавление цифры 10 - интервал в минутах по присыланию сообщения
            subscribe = list()
            for line in a:

                if (line == adres):
                    subscribe.append(f'{line}, 5')

                elif (line.split(', ')[0] == adres) and (f', {t}' not in line) and (', ') in line: # Проверка на наличие этого промежутка времени
                    a = line.split(', ')[0]; tm = line.split(', ')[-1]
                    subscribe.append(f'{a}, {t}, {tm}')
                    # print(line)
                    # print(line.split(', '))
                    # print(line.split(', ')[-2])     
                    # print(line.split(', ')[0]+', '+t+', '+line.split(', ')[-1])
                    # print(line.replace(line.split(', ')[-2], f'{t}'))
                
                else:
                    subscribe.append(line) 
            
            # print([print(line, adres) for line in a ])
            subscribe.sort()
            # print(a.sort())
            print(subscribe)
            for i in subscribe:
                new_fol.write(f'sub = {i}\n')
    except:
        print('except')
    return subscribe



def screening_time(adres, id): # Добавление интервала между сообщениями в 10 минут
    time = int()
    try:
        print('try')
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'r', encoding='utf-8') as fol:  
            file = fol.read().replace('sub = ', '')
            a=[line for line in file.split('\n') if line != '']     # Сортировка котельных по алфавиту должна быть
            # full_adres = [line for line in a if line.split(', ')[0] == adres] # Добавление всей строки для данной котельной
            # print(full_adres, 'full')
            print(a)
            print(adres)
            for line in a:
                if line.split(', ')[0] == adres: # Проверка на наличие этого промежутка времени
                    time = line.split(', ')[-2]
                    break
    except:
        print('except')
    return time

        

def add_newtime(adres, id): # Добавление времени для отправки сообщения
    subscribe = list() 
    with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'r', encoding='utf-8') as vremia:
        tm = vremia.read().replace('sub = ', '').split('\n')
        AlTime = [line for line in tm if line.split(', ')[0] != adres]
        # AdTime = [line for line in tm if line.split(', ')[0] == adres]
        subscribe = AlTime
        for line in tm:
            if ':' in line and line.split(', ')[0] == adres:
                subscribe.append(line.replace(line.split(', ')[-1],dt.datetime.now().strftime('%H:%M:00')))
            elif ':' not in line and line.split(', ')[0] == adres and len(line.split(', ')) == 2:
                subscribe.append(line+dt.datetime.now().strftime(', %H:%M:00'))
            elif line.split(', ')[0] == adres:
                subscribe.append(line)
            
        print(subscribe)
    with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'w', encoding='utf-8') as newtime:
        subscribe.sort()
        print(subscribe[0])
        for i in subscribe[1:]:
            if 'fav' not in i:
                print(i)
                newtime.write(f'sub = {i}\n')
            else:
                print(i)
                newtime.write(f'{i}\n')

# send_message_interval('Республиканская 136(2)', 5288656086, 17)
# print(screening_time('Республиканская 136(2)', 5288656086))
# print(add_newtime('Республиканская 136(2)', 5288656086))
#

def file_new_time(adres, id): # Изменение времени отправки сообщения
    subscribe = list()
    with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'r', encoding='utf-8') as vremia:
        tm = vremia.read().replace('sub = ', '').replace('\ufeff', '').split('\n')
        subscribe = [line for line in tm if line.split(', ')[0] != adres]
        for line in tm:
            if line.split(', ')[0] == adres:
                new_time = line.split(', ')
                index_for_times = line.split(', ')[-1].split(':')
                print(index_for_times)
                if len(index_for_times) == 3:
                    min = dt.timedelta(hours = int(index_for_times[0]), minutes = int(index_for_times[1]) + int(line.split(', ')[1]))
                    if len(str(min).split(', ')) == 2:
                        print(str(min).split(', ')[1])
                        new_min = str(min).split(', ')[1]
                        subscribe.append(f'{new_time[0]}, {new_time[1]}, {new_min}')
                    else:
                        print(min)
                        subscribe.append(f'{new_time[0]}, {new_time[1]}, {min}')
                else:
                    subscribe.append(line)
    with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'w', encoding='utf-8') as newtime:
        subscribe.sort()
        # print(subscribe)
        for i in subscribe[1:]:
            if 'fav' not in i:
                newtime.write(f'sub = {i}\n')
            else:
                newtime.write(f'{i}\n')
    return subscribe


# send_message_interval('Евдокимова 35(2)', 5288656086, 17)
# print(screening_time('Евдокимова 35(2)', 5288656086))
# print(add_newtime('Евдокимова 35(2)', 5288656086))
# print(file_new_time('Евдокимова 35(2)', 5288656086))


def favourite_add(adres, id):  # Добавление котельной в подписки # adres - adres # id - message.from_user.id
    subscribe = list()
    try:
        print('try')
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'r', encoding='utf-8') as fol:  

            file = fol.read().replace('fav = ', '')
            a=[line for line in file.split('\n') if line != '']     # Сортировка котельных по алфавиту должна быть
            if adres not in a: a.append(adres)
            print(a)
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'w', encoding='utf-8') as new_fol: # Добавление котельной в файл с подписками
            subscribe = a
            subscribe.sort()
            # print(a.sort())
            print(subscribe)
            for i in subscribe:
                if 'sub' not in i:
                    new_fol.write(f'fav = {i}\n')
                else:
                    new_fol.write(f'{i}\n')

    except:
        print('except')
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'a', encoding='utf-8') as new_fol:
            new_fol.write(f'fav = {adres}\n')
    return subscribe


def favourite_del(adres, id):  # Удаление котельной из подписок # adres - adres # id - message.from_user.id
    subscribe = list()
    try:
        print('try')
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'r', encoding='utf-8') as fol:  
            file = fol.read().replace('fav = ', '')
            # print(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt') 
            # print([line for line in fol.read().split('\n') if line != adres])
            a=[line for line in file.split('\n') if line.split(', ')[0] != adres and line != '']     # Сортировка котельных по алфавиту должна быть
            print(a)
            print(adres)
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'w', encoding='utf-8') as new_fol: # Добавление котельной в файл с подписками
            subscribe = a
            subscribe.sort()
            # print(a.sort())
            print(subscribe)
            for i in subscribe:
                if 'sub' not in i:
                    new_fol.write(f'fav = {i}\n')
                else:
                    new_fol.write(f'{i}\n')

    except:
        print('except')
        with open(f'{os.getcwd()}\Subscribers\Subscribe_{id}.txt', 'a', encoding='utf-8') as new_fol:
            new_fol.write(f'fav = {adres}\n')
    return subscribe


# follow_add('Суздальский 15(1)',5288656086)



def convert_pdf2img(input_file: str, pages: Tuple = None): # переводит pdf в png для отправки в чат.
    """Converts pdf to image and generates a file by page"""
    # Open the document
    pdfIn = fitz.open(input_file)
    output_files = []
    # Iterate throughout the pages
    for pg in range(pdfIn.pageCount):
        if str(pages) != str(None):
            if str(pg) not in str(pages):
                continue
        # Select a page
        page = pdfIn[pg]
        rotate = int(0)
        # PDF Page is converted into a whole picture 1056*816 and then for each picture a screenshot is taken.
        # zoom = 1.33333333 -----> Image size = 1056*816
        # zoom = 2 ---> 2 * Default Resolution (text is clear, image text is hard to read)    = filesize small / Image size = 1584*1224
        # zoom = 4 ---> 4 * Default Resolution (text is clear, image text is barely readable) = filesize large
        # zoom = 8 ---> 8 * Default Resolution (text is clear, image text is readable) = filesize large
        zoom_x = 1.33333333
        zoom_y = 1.33333333
        # The zoom factor is equal to 2 in order to make text clear
        # Pre-rotate is to rotate if needed.
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        output_file = f"{os.path.splitext(os.path.basename(input_file))[0]}.png"
        pix.writePNG(output_file)
        output_files.append(output_file)
    pdfIn.close()
    summary = {
        "File": input_file, "Pages": str(pages), "Output File(s)": str(output_files)
    }
    
    # Printing Summary
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return output_files
    