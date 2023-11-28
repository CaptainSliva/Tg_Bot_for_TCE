from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import CotInfo as ci
# Создание айдишников происходит только с нижним подчеркиванием после основного названия элемента   пример   -   Ленина_subscribe

BtnMain = KeyboardButton('Главное меню')
#setting
Settings = KeyboardButton('Настройки')
button_for_sep = KeyboardButton('Сокращённый вывод')
button_for_nosep = KeyboardButton('Полный вывод')
# MainMenu
MySubscribes=KeyboardButton('Мои подписки')
ListAll = KeyboardButton('Получить список районов')
MyFavs = KeyboardButton('Избранное')

MainMenu = ReplyKeyboardMarkup(resize_keyboard=True).row(MySubscribes, MyFavs).add(ListAll)
    
MainNext = ReplyKeyboardMarkup(resize_keyboard=True).add(BtnMain)
# Subscribes
ToFav = KeyboardButton('Добавить в избранное')
ToSubscribe = KeyboardButton('Подписаться')

Screen_button = KeyboardButton('anf') # (в разработке)
Button_time_on_few_min = KeyboardButton('Задать произвольный интервал сообщений') # (в разработке)
                          
AllListSubscribeCotel_t = [f'{t}/subscribe_cotel' for t in [j for j in ci.parse_table()]] # Создание айдишников для удалённых котельных
AllListSubscribeCotel = InlineKeyboardMarkup()

def AddToSubscribeCotel(id): # Функция для генерации инлайн кнопок в раздел с подписками # message.from_user.id - id пользователя  # adres - adresa # Создание кнопок на зафоловеные котельные
    AllListSubscribeCotel_copy = InlineKeyboardMarkup()
    global AllListSubscribeCotel
    global AllListSubscribeCotel_t
    # # print(ci.subscribe_del(adres, id), '//////////////////////////////')
    for i in ci.file_read(id): # Создание кнопок для всего списка котельных
        # print(i)
        if 'sub' in i:
            adres = i.replace('sub = ', '')
            AllListSubscribeCotel = AllListSubscribeCotel_copy.add(InlineKeyboardButton(text=i.replace('sub = ', '').split('(')[0], callback_data=f'{adres}/subscribe_cotel'))
    # [f'{t}/subscribe_cotel' for t in [j for j in ci.parse_table()]]
# # print(AddToSubscribeCotel(5288656086))

btninf = KeyboardButton('example')
btninf2 = KeyboardButton('example v2')
FromSubscribe = KeyboardButton('Отписаться')
Delete_from_Subscribe = ReplyKeyboardMarkup(resize_keyboard=True).row(BtnMain)
# Delete_from_Subscribe.row(Button_time_on_5_min, Button_time_on_10_min)
# Delete_from_Subscribe.row(Screen_button, Button_time_on_10_min)


async def screening_generate(adres, id):
    global Delete_from_Subscribe
    Delete_from_Subscribe_copy = ReplyKeyboardMarkup(resize_keyboard=True).row(BtnMain).row((f'Интервал сообщений - {ci.screening_time(adres, id)} мин'), Button_time_on_few_min)
    Delete_from_Subscribe = Delete_from_Subscribe_copy



# NoSubscribes



TS_cotel_test = ReplyKeyboardMarkup(resize_keyboard=True)
def Teplosystems_Cotel_test(cotel_name):
    global TS_cotel_test
    TS_cotel_copy = ReplyKeyboardMarkup(resize_keyboard=True)
    ct_dict = ci.parse_file_district()[cotel_name]
    for i in ct_dict:
        number = i.split('(')[1].split(')')[0]
        TS_cotel_test = TS_cotel_copy.add(KeyboardButton(f'Теплосистема {number}'))
# Teplosystems_Cotel_test('Рыбный34')



AllListCotel_t=[ f'{t}/nosubscribe' for t in [j for j in ci.parse_table()]] # Создание айдишников для всего списка котельных
# print(AllListCotel_t)
AllListCotel = InlineKeyboardMarkup()
for i in [j for j in ci.parse_table()]: # Создание кнопок для всего списка котельных
    AllListCotel.add(InlineKeyboardButton(text=i, callback_data=f'{i}/nosubscribe'))

Add_to_Subscribe = ReplyKeyboardMarkup().row(2)
Add_to_Subscribe = ReplyKeyboardMarkup(resize_keyboard=True).add(BtnMain).row(ToSubscribe)
Add_to_Subscribe_with_Fav = ReplyKeyboardMarkup(resize_keyboard=True).add(BtnMain).row(ToSubscribe, ToFav)


# Add_to_Subscribe = ReplyKeyboardMarkup(resize_keyboard=True).add(BtnMain)


districts = ci.districts()
Cotels_Districts_t = [f'{i}/distr_nosub' for i in districts] # district_nosubscribe
Cotels_Districts = InlineKeyboardMarkup() # Список районов
for i in districts: 
    Cotels_Districts.add(InlineKeyboardButton(text=i, callback_data=f'{i}/distr_nosub')) # district_nosubscribe


Cotels_in_District_t = list()
Cotels_in_District = InlineKeyboardMarkup()
def CotsInDistrict(district): # Функция для вывода котельных выбранного района
    global Cotels_in_District_t
    global Cotels_in_District
    ct_dict = ci.parse_file_district() # Словарь с {котельными {теплосистемами : районами}}
    Cotels_in_District_copy_t = list()
    Cotels_in_district_copy = InlineKeyboardMarkup()
    for i in ct_dict.keys():
        for j in ct_dict[i].values():
            if str(j).replace('[','').replace(']','').replace("'",'') == district:
                if f'{i}/cot_in_distr_nosub' not in Cotels_in_District_copy_t:
                    Cotels_in_District = Cotels_in_district_copy.add(InlineKeyboardButton(text=str(i).split('(')[0], callback_data=f'{i}/cot_in_distr_nosub')) # cotel_in_district_nosubscribe
                    Cotels_in_District_t = Cotels_in_District_copy_t.append(f'{i}/cot_in_distr_nosub') # cotel_in_district_nosubscribe
                    # print(f'{i}/cot_in_distr_nosub')

                    
# print('----------------------------------')
TS_cotel_t = list()
TS_cotel = InlineKeyboardMarkup()
def Teplosystems_Cotel(cotel_name):
    global TS_cotel_t
    global TS_cotel
    TS_cotel_copy_t = list()
    TS_cotel_copy = InlineKeyboardMarkup()
    ct_dict = ci.parse_file_district()[cotel_name]
    for i in ct_dict:
        number = i.split('(')[1].split(')')[0]
        TS_cotel_t = TS_cotel_copy_t.append(f'{i}/cot_ts_nosub') # cotel_ts_nosubscribe
        TS_cotel = TS_cotel_copy.add(InlineKeyboardButton(text=f'Теплосистема {number}', callback_data=f'{i}/cot_ts_nosub')) # cotel_ts_nosubscribe
        # print(TS_cotel_copy_t)



# CotsInDistrict('Восточный')


# Options

AddToSub = ReplyKeyboardMarkup(resize_keyboard=True).row(BtnMain).add(ToSubscribe)
AddToFav = ReplyKeyboardMarkup(resize_keyboard=True).row(BtnMain).add(ToFav)

Del_Fav = KeyboardButton('Удалить из избранного')

Add_to_Fav_with_Sub = ReplyKeyboardMarkup(resize_keyboard=True).row(BtnMain).add(Del_Fav, ToSubscribe)
Del_From_Fav = ReplyKeyboardMarkup(resize_keyboard=True).row(BtnMain).add(Del_Fav)

Favourites_t = list()
Favourites_t = [f'{i}/fav_cotel' for i in [j for j in ci.parse_table()]]
Favourites = InlineKeyboardMarkup()
def AddToFavsCotel(id): # Функция для генерации инлайн кнопок в раздел с подписками # message.from_user.id - id пользователя  # adres - adresa # Создание кнопок на зафоловеные котельные
    Favourites_copy = InlineKeyboardMarkup()
    global Favourites
    # global Favourites_t
    # # print(ci.subscribe_del(adres, id), '//////////////////////////////')
    for i in ci.file_read(id): # Создание кнопок для всего списка котельных
        if 'fav' in i:
            adres = i.replace('fav = ', '')
            Favourites = Favourites_copy.add(InlineKeyboardButton(text=i.replace('fav = ', '').split('(')[0], callback_data=f'{adres}/fav_cotel'))
    # Favourites_t = [f'{i}/fav_cotel' for i in [j for j in ci.parse_table()]]
# print(AddToFavsCotel(5288656086))


# Админ-панель
Amogs = KeyboardButton('Админка')
Admin_Main = ReplyKeyboardMarkup(resize_keyboard=True).row(MySubscribes, MyFavs).row(Amogs, ListAll)
SubscribersNo = KeyboardButton('Заявки')
Subscribers = KeyboardButton('Пользователи')
Admin_Second = ReplyKeyboardMarkup(resize_keyboard=True).add(BtnMain).row(SubscribersNo, Subscribers)
InSub = KeyboardButton('Принять')
OutNosub = KeyboardButton('Отклонить')
Admin_Distributor = ReplyKeyboardMarkup(resize_keyboard=True).add(BtnMain).row(OutNosub, InSub)
OutSub = KeyboardButton('Удалить')
Admin_Del_From_Bot_Subs = ReplyKeyboardMarkup(resize_keyboard=True).row(BtnMain).add(OutSub)


SubscribersNo_t = list()
SubscribersNo = InlineKeyboardMarkup()

def Nosubs():
    global SubscribersNo_t
    global SubscribersNo
    SubscribersNo_copy = InlineKeyboardMarkup()
    
    for i in ci.list_FileSub_or_No('SubscribersNo'):
        if i != '':
            adres = i.split(' = ')[1]
            SubscribersNo = SubscribersNo_copy.add(InlineKeyboardButton(text=i.split(' = ')[1], callback_data=f'{adres}/nosubs'))
            SubscribersNo_t.append(f'{adres}/nosubs')
        else:
            SubscribersNo = SubscribersNo_copy.add(InlineKeyboardButton(text='Заявок нет', callback_data='Заявок нет/nosubs'))
            SubscribersNo_t.append('Заявок нет/nosubs')






Subscribers_t = list()
Subscribers = InlineKeyboardMarkup()

def Subs():
    global Subscribers
    global Subscribers_t
    Subscribers_copy = InlineKeyboardMarkup()

    for i in ci.list_FileSub_or_No('Subscribers'):
        if i != '':
            adres = i.split(' = ')[1]
            Subscribers = Subscribers_copy.add(InlineKeyboardButton(text=i.split(' = ')[1], callback_data=f'{adres}/subs'))
            Subscribers_t.append(f'{adres}/subs')
        else:
            Subscribers = Subscribers_copy.add(InlineKeyboardButton(text='Подписчиков нет', callback_data='Подписчиков нет/subs'))
            Subscribers_t.append('Подписчиков нет/subs')

            
# Настройки

All_data = ReplyKeyboardMarkup(resize_keyboard=True).row(BtnMain).add(button_for_nosep)
Sep_data = ReplyKeyboardMarkup(resize_keyboard=True).row(BtnMain).add(button_for_sep)

