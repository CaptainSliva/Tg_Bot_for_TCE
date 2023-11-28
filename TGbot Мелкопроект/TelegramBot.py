# Импортируем нужные библиотеки для работы с aiogram
import logging as log
from aiogram import Bot, Dispatcher, executor, types
from aiogram import types
import datetime as dt
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Мои файлы
import Buttons as btn
import CotInfo as ci
import bot_config as bc

# # Начинаем создавать бота

# 5897237424:AAE3IRCOrP474qARfVWRU9UfnxIPJeq92XI Основной
# 5994728533:AAGbpqR_nWnBG-XdwDmbHLgMDITpSvqODGg Для тестов

TOKEN = bc.Config['Token'] # Ваш токен бота
#Создаем telegram бота
log.basicConfig(level = log.INFO) # Включаем логирование чтобы не пропустить важные сообщения
bot = Bot(token = TOKEN) # Создаем обьект бота
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage) # Диспетчер
Admin_id = bc.Config['Admin']

subscribe_adres = str()
adress = str()
mes_id = str()
cotelnaya = str()
number = str()
fav_adres = str()
distribut = str()
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
#

ci.create_subscribers()
ci.create_dir_for_admin()


# async def choose_buttons_vars(cotl, cal, cal_ans, var1, var2, var3, var4):
#     if ci.file_check_copy(f'{cal_ans}(1)', cal.from_user.id, 'sub') and ci.file_check_copy(f'{cal_ans}(1)', cal.from_user.id, 'fav'):
#         await cal.message.answer(cotl, reply_markup = btn.var1) # Выводит информацию о котельной
#         await cal.answer()
#         adress = cal_ans
#         fav_adres = f'{cal_ans}(1)'

#     elif ci.file_check_copy(f'{cal_ans}(1)', cal.from_user.id, 'sub'):
#         print(f'{cal_ans}(1)')
#         print(cotl)
#         await cal.message.answer(f'{cotl}', reply_markup = btn.var2) # Выводит информацию о котельной
#         await cal.answer()
#         adress = cal_ans
#         fav_adres = f'{cal_ans}(1)'
#     elif ci.file_check_copy(f'{cal_ans}(1)', cal.from_user.id, 'fav'):
#         print(f'{cal_ans}(1)')
#         print(cotl)
#         await cal.message.answer(f'{cotl}', reply_markup = btn.var3) # Выводит информацию о котельной
#         await cal.answer()
#         adress = cal_ans
#         fav_adres = f'{cal_ans}(1)'
#     else:
#         print(f'{cal_ans}(1)')
#         print(cotl)
#         await cal.message.answer(f'{cotl}', reply_markup = btn.var4) # Выводит информацию о котельной
#         await cal.answer()
#         adress = cal_ans
#         fav_adres = f'{cal_ans}(1)'


def normal(nstr): # Функция ля удаления айдишника из адреса    nstr - строка с айдишником
    return nstr.split('/')[0]


# Установление времени после перезапуска бота
for i in ci.adding_msg(): # Ключи словаря
    print(i)
    try: # Проверка на то запущен или остановлен бот у пользователя (надо для того что бы бот не лёг)
        for j in ci.adding_msg()[i]: # Значения для ключа
            print(i); print(j)
            ci.add_newtime(str(j).split(', ')[0], i)
    except:
        pass



class UserState(StatesGroup):
    firstname = State()
    name = State()
    lastname = State()
    phonenumber = State()
    anytime = State()


# class Admin(StatesGroup):
#     requests = State()
#     subscribers = State()
    

@dp.message_handler(commands = ['start', 's', 'старт'])
async def cmd_start(message: types.Message):
    global Admin_id
    Admin_id = bc.Config['Admin']
    if ci.bot_check_sub(str(message.from_user.id), 'Subscribers'):
        await message.answer(f'Здравствуйте! {message.from_user.full_name}', reply_markup=btn.MainMenu)
    
    elif str(message.from_user.id) == Admin_id:
        await message.answer(f'Здравствуйте! {message.from_user.full_name}', reply_markup=btn.Admin_Main)

        
# Процесс регистрации
    elif not ci.bot_check_sub(str(message.from_user.id), 'SubscribersNo'):

        await message.answer(f'Здравствуйте! {message.from_user.full_name}\nВы не зарегестрированны в данном боте. Пожалйста, введите свои имя, фамилию, отчество и номер телефона.')
        await message.answer('Введите свою фамилию')
        # if all(i.isalpha() for i in message.text):
        await UserState.firstname.set()

        @dp.message_handler(state=UserState.firstname)
        async def get_username(message: types.Message, state: FSMContext):
            await state.update_data(firstname=message.text.capitalize())
            await message.answer("Введите своё имя")
            await UserState.next()
            
            
        @dp.message_handler(state=UserState.name)
        async def get_username(message: types.Message, state: FSMContext):
            await state.update_data(name=message.text.capitalize())
            await message.answer("Введите своё отчество")
            # if all(i.isalpha() for i in message.text):
            await UserState.next()
            

        @dp.message_handler(state=UserState.lastname)
        async def get_username(message: types.Message, state: FSMContext):
            await state.update_data(lastname=message.text.capitalize())
            await state.update_data(userid=message.from_user.id)
            await message.answer("Введите ваш номер телефона")
            # if all(i.isdigit() or i in ['+', '-'] for i in message.text):
            await UserState.next()

        @dp.message_handler(state=UserState.phonenumber)
        async def get_username(message: types.Message, state: FSMContext):
            await state.update_data(phonenumber=message.text)
            data = await state.get_data()
            if all(i.isalpha() for i in data['firstname']) and all(i.isalpha() for i in data['name']) and all(i.isalpha() for i in data['lastname']) and all(i.isdigit() or i in ['+', '-'] for i in data['phonenumber']):
                # await message.answer(f"Фамилия: {data['firstname']}\n"
                #                     f"Имя: {data['name']}\n"
                #                     f"Отчество: {data['lastname']}\n"
                #                     f"Телефон: {data['phonenumber']}\n")
                # nameuser = f"{data['firstname']} {data['name']} {data['lastname']} {data['phonenumber']}"
                # userid = data['userid']
                await message.answer('Регистрация пройдена, ожидайте получения прав для пользования ботом')
                ci.bot_nosubscribers(f"{data['firstname']} {data['name']} {data['lastname']} {data['phonenumber']}", data['userid'])
            else:
                if not all(i.isalpha() for i in data['firstname']):
                    await message.answer('При вводе фамилии была допущена ошибка. Пожалйста, нажмите на /s для повторной регистрации')
                if not all(i.isalpha() for i in data['name']):
                    await message.answer('При вводе имени была допущена ошибка. Пожалйста, нажмите на /s для повторной регистрации')
                if not all(i.isalpha() for i in data['lastname']):
                    await message.answer('При вводе отчества была допущена ошибка. Пожалйста, нажмите на /s для повторной регистрации')
                if not all(i.isdigit() or i in ['+', '-'] for i in data['phonenumber']):
                    await message.answer('При вводе номера телефона была допущена ошибка. Пожалйста, нажмите на /s для повторной регистрации')
            await UserState.next()
    else:
        await message.answer(f'Здравствуйте! {message.from_user.full_name}. Вашу заявку ещё не приняли')


# Admin_id = ci.parse_config('Admin')
# @dp.message_handler(commands = 'Вы стали подписчиком бота')
# async def cmd_start(message: types.Message):
#     await message.answer('Вы стали подписчиком бота'.format(message.from_user), reply_markup=btn.MainMenu) 


@dp.message_handler() # Обработчик сообщений
async def bot_message(message: types.Message):
    global cotelnaya
    global number
    global subscribe_adres
    global fav_adres
    global distribut
    global Admin_id
    global mes_id

    if ci.bot_check_sub(str(message.from_user.id), 'Subscribers') or str(message.from_user.id) == Admin_id:
        


    #Администрирование
        
        if message.text == 'Админка' and str(message.from_user.id) == Admin_id:
            await message.answer('Админка', reply_markup=btn.Admin_Second)
            print('Админка')

        if message.text == 'Заявки' and str(message.from_user.id) == Admin_id:
            btn.Nosubs()
            print('Заявки')
            await message.answer('Заявки на пользование ботом', reply_markup=btn.SubscribersNo)
            # print(btn.SubscribersNo_t)
            # await Admin.requests.set()
            
        @dp.callback_query_handler(text = btn.SubscribersNo_t) 
        async def msg_answer_p(callback: types.CallbackQuery): 
            # await Admin.requests.set()
            global distribut
            callback_answer = normal(callback.data)
            # print(callback_answer)
            user_l = ''.join([f'{i}/\\' for i in ci.parse_user_info(str(callback_answer), 'SubscribersNo')]).replace('/\\','\n')
            await callback.message.answer(user_l, reply_markup=btn.Admin_Distributor)
            await callback.answer()
            # print(callback_answer)
            distribut = callback_answer
            # await state.finish()
        if message.text == 'Пользователи' and str(message.from_user.id) == Admin_id:
            btn.Subs()
            print('Пользоатели')
            await message.answer('Пользователи бота', reply_markup=btn.Subscribers)
            # print(btn.Subscribers_t)
            
        @dp.callback_query_handler(text = btn.Subscribers_t) 
        async def msg_answer_g(callback: types.CallbackQuery): 
            global distribut
            # await Admin.subscribers.set()   
            callback_answer = normal(callback.data)
            # print(callback_answer)
            user_l = ''.join([f'{i}/\\' for i in ci.parse_user_info(str(callback_answer), 'Subscribers')]).replace('/\\','\n')
            await callback.message.answer(user_l, reply_markup=btn.Admin_Del_From_Bot_Subs)
            await callback.answer()
            # print(callback_answer)
            distribut = callback_answer
            # await state.finish()
        if message.text == 'Принять' and str(message.from_user.id) == Admin_id:
            await message.answer(f'Вы приняли {distribut}', reply_markup=btn.MainNext)
            ci.bot_subscribers_ac(distribut)
            try: 
                await bot.send_message(distribut, 'Теперь вы являетесь подписчиком бота. Нажмите - /s для начала работы')
            except: pass

        if message.text == 'Отклонить' and str(message.from_user.id) == Admin_id:
            await message.answer(f'Вы отклонили {distribut}', reply_markup=btn.MainNext)
            ci.del_from(distribut, 'SubscribersNo')

        if message.text == 'Удалить' and str(message.from_user.id) == Admin_id:
            await message.answer(f'Вы удалили {distribut}', reply_markup=btn.MainNext)
            ci.del_from(distribut, 'Subscribers')



    # Настройки


        # if message.text == 'Настройки':
        #     async with aiofiles.open(f'{os.getcwd()}\Subscribers\Settings_{message.from_user.id}.txt', 'r', encoding='utf-8') as fol:
        #         if 'separate' in await fol.read():
        #             await message.answer('Настройки вывода данных', reply_markup = btn.All_data)

        #         else:
        #             await message.answer('Настройки вывода данных', reply_markup = btn.Sep_data)

        # if message.text == 'Полный вывод':
        #     # функция для добавления полного вывода
        #     await ci.settings_file('separate', message.from_user.id)
        #     await message.answer('Данные будут выводться в полном виде') 
        # if message.text == 'Сокращённый вывод':
        #     # функция для добавления сокращённого вывода
        #     await ci.settings_file('separate', message.from_user.id)
        #     await message.answer('Данные будут выводться в сокращённом виде')

            # тут надо добавить что если в файле есть separate, то выводить сообщения в сокращённом варанте. АКАК? Типо функцию вывода дополнить надо, что если в файле обнаружено separate, то 
            # выводить информацию в сокращённом виде
            # ну и соответственно незабыть добавить separate в файл -3 элементом.


    # Переход в главное меню

        
        if message.text == 'Главное меню' and str(message.from_user.id) == Admin_id:
            await message.answer('Главное меню', reply_markup = btn.Admin_Main)

        elif message.text == 'Главное меню':
            await message.answer('Главное меню', reply_markup = btn.MainMenu)





    # С подпиской
        if message.text == 'Мои подписки':

            print('В иф для отписки вошел')
            print(message.from_user.id)
            await message.answer('Подписки', reply_markup = btn.MainNext)
            if len([i for i in ci.file_read(message.from_user.id) if 'sub' in i]) == 0:
                await message.answer('У вас нет подписок', reply_markup = btn.MainNext)
            else:
                btn.AddToSubscribeCotel(str(message.from_user.id))
                await message.answer('Список котельных:', reply_markup = btn.AllListSubscribeCotel)
                mes_id = message.from_user.id

                        
        @dp.callback_query_handler(text = btn.AllListSubscribeCotel_t) # Обработчик нажатия инлайн кнопок
        async def msg_answer(callback: types.CallbackQuery):
            global subscribe_adres
            global fav_adres
            global mes_id
            print('отработала отписка')
            print(mes_id)
            callback_answer=normal(callback.data) # Переменная для сохранения адреса
            await btn.screening_generate(callback_answer, mes_id)
            # cotelnaya_l=''.join([f'{i}/\\' for i in ci.parse_table()[f'{callback_answer}']]).replace('/\\','\n')
            # if ci.check_param('Settings', 'separate', message.from_user.id):
            cotelnaya_l=''.join([i.split(',')[0]+','+i.split(',')[1][0:2]+'\n' if ',' in i else f'{i}\n' for i in ci.parse_table()[f'{callback_answer}']])
            # else:
            #     cotelnaya_l=''.join([f'{i}\n' for i in ci.parse_table()[f'{callback_answer}']])



            if ci.file_check_copy(f'{callback_answer}', callback.from_user.id, 'sub') and ci.file_check_copy(f'{callback_answer}', callback.from_user.id, 'fav'): # Если котельная в избранном и подписках
                await callback.message.answer(cotelnaya_l, reply_markup = btn.Delete_from_Subscribe.add(btn.FromSubscribe)) # Выводит информацию о котельной
                await callback.answer()
                subscribe_adres = callback_answer
                # fav_adres = callback_answer

            else: 
                await callback.message.answer(f'{cotelnaya_l}', reply_markup = btn.Delete_from_Subscribe.row(btn.FromSubscribe, btn.ToFav)) # Выводит информацию о котельной
                await callback.answer()
                subscribe_adres = callback_answer
                # fav_adres = callback_answer


            subscribe_adres = callback_answer
            fav_adres = callback_answer
            print(subscribe_adres, 'it is subscribe adress', callback_answer)


        # if message.text == 'Интервал сообщений 5 минут': Мб понадобится, и если понадобится, то тут штука с экранированием времнеи должна быть./-/*\-\
        #     print(message.text)
        #     await message.answer('Информация о котельной будет присылаться раз в 5 минут', reply_markup = btn.MainNext)
        #     ci.send_message_interval_5(subscribe_adres, message.from_user.id)
        #     ci.add_newtime(subscribe_adres, message.from_user.id)

        if message.text == 'Задать произвольный интервал сообщений':
            print(message.text)
            print(subscribe_adres)
            print(mes_id)
            await message.answer('Введите интервал сообщений. От 5 до 1440 минут', reply_markup = btn.MainNext)
            await UserState.anytime.set()
            @dp.message_handler(state = UserState.anytime)
            async def msg_answer(message: types.Message, state = FSMContext):
                global subscribe_adres, mes_id
                print(subscribe_adres)
                print(mes_id)
                await state.update_data(anytime=message.text)
                data = await state.get_data()
                print(type(message.text), message.text)
                if message.text.isdigit() and 1441 > int(message.text) > 4:
                    ci.send_message_interval(subscribe_adres, mes_id, data['anytime'])
                    ci.add_newtime(subscribe_adres, mes_id)
                    await message.answer(f'Новый интервал сообщений - {message.text} мин', reply_markup = btn.MainNext)
                    await state.finish()

                elif message.text == 'Главное меню':
                    await state.finish()
                else:
                    await message.answer('Неверный ввод')
                

                




                



    # Избранные

        if message.text == 'Избранное':
            print('В иф с избранным вошел')
            # btn.AddToFavsCotel(str(message.from_user.id))
            await message.answer('Избранное', reply_markup = btn.MainNext)
            if len([i for i in ci.file_read(message.from_user.id) if 'fav' in i]) == 0:
                await message.answer('У вас нет избранных котельных', reply_markup = btn.MainNext)
            else:
                btn.AddToFavsCotel(str(message.from_user.id))
                print(message.text)
                await message.answer('Список котельных:', reply_markup = btn.Favourites)
        
        @dp.callback_query_handler(text = btn.Favourites_t) # Обработчик нажатия инлайн кнопок         
        async def msg_answer(callback: types.CallbackQuery):    

            global fav_adres, subscribe_adres
            print('отработала избранное')
            callback_answer=normal(callback.data) # Переменная для сохранения адреса
            # cotelnaya_l=''.join([f'{i}/\\' for i in ci.parse_table()[f'{callback_answer}']]).replace('/\\','\n')
            # if ci.check_param('Settings', 'separate', message.from_user.id):
            cotelnaya_l=''.join([i.split(',')[0]+','+i.split(',')[1][0:2]+'\n' if ',' in i else f'{i}\n' for i in ci.parse_table()[f'{callback_answer}']])
            # else:
            #     cotelnaya_l=''.join([f'{i}\n' for i in ci.parse_table()[f'{callback_answer}']])
            # print(callback_answer)

            if ci.file_check_copy(f'{callback_answer}', callback.from_user.id, 'sub') and ci.file_check_copy(f'{callback_answer}', callback.from_user.id, 'fav'):
                await callback.message.answer(cotelnaya_l, reply_markup = btn.Del_From_Fav) # Выводит информацию о котельной
                await callback.answer()
                # adress = callback_answer
                # fav_adres = callback_answer

            else:
                await callback.message.answer(f'{cotelnaya_l}', reply_markup = btn.Add_to_Fav_with_Sub) # Выводит информацию о котельной
                await callback.answer()
                # adress = callback_answer
                # fav_adres = callback_answer
                

            fav_adres = callback_answer
            subscribe_adres = callback_answer
            # await state.finish()
            print(fav_adres, 'it is fav adress')






    




    # Без подписки

        if message.text == 'Получить список районов':

            print('В иф для подписки вошел')
            # await message.answer('Получить список районов', reply_markup = btn.MainNext)
            await message.answer('Список районов:', reply_markup = btn.Cotels_Districts)
        @dp.callback_query_handler(text = btn.Cotels_Districts_t) # Обработчик нажатия инлайн кнопок 1 ур
        async def msg_answer_1(callback: types.CallbackQuery): # Вывод районов в инлайн кнопках
            print('я в 1 ур')
            back = normal(callback.data)
            btn.CotsInDistrict(back)
            await callback.message.answer(f'{back}', reply_markup = btn.Cotels_in_District)
            await callback.answer()
            print(back, 'Остановилось')

            @dp.callback_query_handler(text = btn.Cotels_in_District_t) # Обработчик нажатия инлайн кнопок 2 ур
            async def msg_answer_2(callback: types.CallbackQuery): # Вывод котельных для выбранного района
                global adress
                global subscribe_adres
                global fav_adres
                # await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id) # Штука для удаления сообщения(если надо будет)
                print('я во 2 ур')
                print(message.from_user.id)
                print(callback.data)
                print(message.message_id)
                callback_answer=normal(callback.data) # Переменная для сохранения адреса
                if len(ci.parse_file_district()[callback_answer]) < 2:

                    # if ci.check_param('Settings', 'separate', message.from_user.id):
                    cotelnaya_l=''.join([i.split(',')[0]+','+i.split(',')[1][0:2]+'\n' if ',' in i else f'{i}\n' for i in ci.parse_table()[f'{callback_answer}(1)']])
                    # else:
                    #     cotelnaya_l=''.join([f'{i}\n' for i in ci.parse_table()[f'{callback_answer}']])

                    if ci.file_check_copy(f'{callback_answer}(1)', callback.from_user.id, 'sub') and ci.file_check_copy(f'{callback_answer}(1)', callback.from_user.id, 'fav'):
                        await callback.message.answer(cotelnaya_l, reply_markup = btn.MainNext) # Выводит информацию о котельной
                        await callback.answer()
                        adress = callback_answer
                        fav_adres = f'{callback_answer}(1)'
                        subscribe_adres = f'{callback_answer}(1)'

                    elif ci.file_check_copy(f'{callback_answer}(1)', callback.from_user.id, 'sub'):
                        print(f'{callback_answer}(1)')

                        print(cotelnaya_l)
                        await callback.message.answer(f'{cotelnaya_l}', reply_markup = btn.AddToFav) # Выводит информацию о котельной
                        await callback.answer()
                        adress = callback_answer
                        fav_adres = f'{callback_answer}(1)'
                        subscribe_adres = f'{callback_answer}(1)'

                    elif ci.file_check_copy(f'{callback_answer}(1)', callback.from_user.id, 'fav'):
                        await callback.message.answer(f'{cotelnaya_l}', reply_markup = btn.AddToSub) # Выводит информацию о котельной
                        await callback.answer()
                        adress = callback_answer
                        fav_adres = f'{callback_answer}(1)'
                        subscribe_adres = f'{callback_answer}(1)'

                    else:
                        await callback.message.answer(f'{cotelnaya_l}', reply_markup = btn.Add_to_Subscribe_with_Fav) # Выводит информацию о котельной
                        await callback.answer()
                        adress = callback_answer
                        fav_adres = f'{callback_answer}(1)'
                        subscribe_adres = f'{callback_answer}(1)'

                else:
                    adress = callback_answer
                    btn.Teplosystems_Cotel_test(callback_answer)
                    
                    await callback.message.answer(f'Теплосистемы {callback_answer}:', reply_markup = btn.TS_cotel_test)



            print(message.text, '+++++++++++++++++++++++++++++++++++++', adress)



        if 'Теплосистема' in message.text:
            
            print(message.text,'---------------------------------------')
            number = message.text.split('Теплосистема ')[1]
            cotelnaya=f'{adress}({number})'
            print(cotelnaya)
            # if ci.check_param('Settings', 'separate', message.from_user.id):
            cotelnaya_l=''.join([i.split(',')[0]+','+i.split(',')[1][0:2]+'\n' if ',' in i else f'{i}\n' for i in ci.parse_table()[f'{cotelnaya}']])
            # else:
            #     cotelnaya_l=''.join([f'{i}\n' for i in ci.parse_table()[f'{cotelnaya}']])
            # cotelnaya_l=''.join([f'{i}/\\' for i in ci.parse_table()[f'{adress}({number})']]).replace('/\\','\n') 

            if ci.file_check_copy(cotelnaya, message.from_user.id, 'sub') and ci.file_check_copy(cotelnaya, message.from_user.id, 'fav'):
                await message.answer(f'{cotelnaya_l}', reply_markup = btn.MainNext) # Выводит информацию о котельной
                
            elif ci.file_check_copy(cotelnaya, message.from_user.id, 'fav'):
                await message.answer(f'{cotelnaya_l}', reply_markup = btn.AddToSub) # Выводит информацию о котельной

            elif ci.file_check_copy(cotelnaya, message.from_user.id, 'sub'):
                await message.answer(f'{cotelnaya_l}', reply_markup = btn.AddToFav) # Выводит информацию о котельной

            else:
                await message.answer(f'{cotelnaya_l}', reply_markup = btn.Add_to_Subscribe_with_Fav) # Выводит информацию о котельной
            
            fav_adres = cotelnaya
            subscribe_adres = cotelnaya
            print(cotelnaya_l)
        try:
            if adress in [str(j).split('(')[0] for j in ci.parse_table() if len(ci.parse_file_district()[adress]) < 2]:
                cotelnaya=f'{adress}(1)'
        except: pass



    # Подписки/отписки и прочая мешура
        if message.text == 'Подписаться': 
            print(cotelnaya)
            if subscribe_adres in [j for j in ci.parse_table()]:
                subscribe_adres_for_message = subscribe_adres.split('(')[0]
                await message.answer(f'Вы подписались на {subscribe_adres_for_message}', reply_markup = btn.MainNext)
                ci.subscribe_add(subscribe_adres, message.from_user.id)
                ci.send_message_interval(subscribe_adres, message.from_user.id, 5)
                ci.add_newtime(subscribe_adres, message.from_user.id)
                

            elif fav_adres in [j for j in ci.parse_table()]:      
                subscribe_adres_for_message = fav_adres.split('(')[0] 
                await message.answer(f'Вы подписались на {subscribe_adres_for_message}', reply_markup = btn.MainNext)         
                ci.subscribe_add(fav_adres, message.from_user.id)
                ci.send_message_interval(fav_adres, message.from_user.id, 5)
                ci.add_newtime(fav_adres, message.from_user.id)

            else: 
                await message.answer(f'Повторите попытку')

        if message.text == 'Отписаться':
            print(message.text)
            if subscribe_adres != '':
                ci.subscribe_del(subscribe_adres, message.from_user.id)
                subscribe_adres_for_message = subscribe_adres.split('(')[0]
                await message.answer(f'Вы отписались от {subscribe_adres_for_message}', reply_markup = btn.MainNext)

            else: 
                await message.answer(f'Повторите попытку')


        if message.text == 'Добавить в избранное':
            print(message.text)
            if fav_adres in [j for j in ci.parse_table()]:
                ci.favourite_add(fav_adres, message.from_user.id)
                fav_adres_for_message = fav_adres.split('(')[0]
                await message.answer(f'Вы добавили в избранное {fav_adres_for_message}', reply_markup = btn.MainNext)


            elif subscribe_adres in [j for j in ci.parse_table()]:
                ci.favourite_add(subscribe_adres, message.from_user.id)
                fav_adres_for_message = subscribe_adres.split('(')[0]
                await message.answer(f'Вы подписались на {fav_adres_for_message}', reply_markup = btn.MainNext)
        
            else: 
                await message.answer(f'Повторите попытку')

        if message.text == 'Удалить из избранного':
            print(message.text)
            if fav_adres != '':
                ci.favourite_del(fav_adres, message.from_user.id)
                fav_adres_for_message = fav_adres.split('(')[0]
                await message.answer(f'Вы удалили из избранного {fav_adres_for_message}', reply_markup = btn.MainNext)

            else: 
                await message.answer(f'Повторите попытку')




    elif 'Интервал' not in message.text:
        pass
        


# Рассылка



async def send_message_interval(): # Функция для создания сообщений для рассылки

    for i in ci.adding_msg(): # Ключи словаря
        print(i)
        try: # Проверка на то запущен или остановлен бот у пользователя (надо для того что бы бот не лёг)
            for j in ci.adding_msg()[i]: # Значения для ключа
                if '=' not in j:
                    
                    # print(ci.adding_msg()[i])
                    

                    now_time = int(str(dt.datetime.now().strftime('%H:%M:00')).split(':')[0])*60+int(str(dt.datetime.now().strftime('%H:%M:00')).split(':')[1])
                    # try: 
                    j_time = int((str(j).split(', ')[-1]).split(':')[0])*60+int((str(j).split(', ')[-1]).split(':')[1])
                    # except: pass
                    j_adres = str(j).split(', ')[0].replace('\ufeff', '')
                    print(j)
                    print( str(dt.datetime.now().strftime('%H:%M:00')), j_time, now_time)
                    if j_time == int(str(dt.datetime.now().strftime('%H:%M:00')).split(':')[0])*60+int(str(dt.datetime.now().strftime('%H:%M:00')).split(':')[1]):
                        # print(i); print(j)
                        # if ci.check_param('Settings', 'separate', i):
                        cotelnaya_l=''.join([i.split(',')[0]+','+i.split(',')[1][0:2]+'\n' if ',' in i else f'{i}\n' for i in ci.parse_table()[str(j.split(', ')[0])]])
                        # else:
                        #     cotelnaya_l=''.join([f'{i}\n' for i in ci.parse_table()[str(j.split(', ')[0])]])
                        # cotelnaya_l=''.join([f'{i}/\\' for i in ci.parse_table()[str(j.split(', ')[0]).replace('\ufeff', '')]]).replace('/\\','\n')
                        print(cotelnaya_l)
                        await bot.send_message(i, f'{cotelnaya_l}') # Выводит информацию о котельной
                        ci.file_new_time(j_adres, i)
                    
        except:
            await bot.send_message('ОШИБКА!')

    

scheduler.add_job(send_message_interval, trigger='interval', seconds=1) # Создание сообщения 276693613 на рассылку 5288656086
scheduler.start() # Рассылка



# Запускаем бота и включаем его на бесконечную работу

# if __name__ == '__main':
executor.start_polling(dp, skip_updates=False)



