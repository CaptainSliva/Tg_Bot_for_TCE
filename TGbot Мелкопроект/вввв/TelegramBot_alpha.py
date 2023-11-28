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

# # Начинаем создавать бота


TOKEN = ci.parse_config('TOKEN') # Ваш токен бота
#Создаем telegram бота
log.basicConfig(level = log.INFO) # Включаем логирование чтобы не пропустить важные сообщения
bot = Bot(token = TOKEN) # Создаем обьект бота
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage) # Диспетчер

subscribe_adres = str()
adress = str()
cotelnaya = str()
number = str()
fav_adres = str()
distribut = str()
Admin_id = str()
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
#

ci.create_subscribers()
ci.create_dir_for_admin()

def normal(nstr): # Функция ля удаления айдишника из адреса    nstr - строка с айдишником
    return nstr.split('/')[0]


# Установление времени после перезапуска бота
for i in ci.adding_msg(): # Ключи словаря
    #(i)
    try: # Проверка на то запущен или остановлен бот у пользователя (надо для того что бы бот не лёг)
        for j in ci.adding_msg()[i]: # Значения для ключа
            #(i); #(j)
            ci.add_newtime(str(j).split(', ')[0], i)
    except:
        pass



class UserState(StatesGroup):
    firstname = State()
    name = State()
    lastname = State()
    phonenumber = State()
    # favourites = State()


# class Admin(StatesGroup):
#     requests = State()
#     subscribers = State()
    

Admin_id = ci.parse_config('Admin')
@dp.message_handler(commands = ['start', 's', 'старт'])
async def cmd_start(message: types.Message):
    global Admin_id
    Admin_id = ci.parse_config('Admin')
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
                    await message.answer('При вводе Фамилии была допущена ошибка. Пожалйста, нажмите на /s для повторной регистрации')
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

    if ci.bot_check_sub(str(message.from_user.id), 'Subscribers') or str(message.from_user.id) == Admin_id:
        


    #Администрирование
        
        if message.text == 'Админка' and str(message.from_user.id) == Admin_id:
            await message.answer('Админка', reply_markup=btn.Admin_Second)
            #('Админка')

        if message.text == 'Заявки' and str(message.from_user.id) == Admin_id:
            btn.Nosubs()
            #('Заявки')
            await message.answer('Заявки на пользование ботом', reply_markup=btn.SubscribersNo)
            # #(btn.SubscribersNo_t)
            # await Admin.requests.set()
            
        @dp.callback_query_handler(text = btn.SubscribersNo_t) 
        async def msg_answer_p(callback: types.CallbackQuery): 
            # await Admin.requests.set()
            global distribut
            callback_answer = normal(callback.data)
            # #(callback_answer)
            user_l = ''.join([f'{i}/\\' for i in ci.parse_user_info(str(callback_answer), 'SubscribersNo')]).replace('/\\','\n')
            await callback.message.answer(user_l, reply_markup=btn.Admin_Distributor)
            await callback.answer()
            # #(callback_answer)
            distribut = callback_answer
            # await state.finish()
        if message.text == 'Пользователи' and str(message.from_user.id) == Admin_id:
            btn.Subs()
            #('Пользоатели')
            await message.answer('Пользователи бота', reply_markup=btn.Subscribers)
            # #(btn.Subscribers_t)
            
        @dp.callback_query_handler(text = btn.Subscribers_t) 
        async def msg_answer_g(callback: types.CallbackQuery): 
            global distribut
            # await Admin.subscribers.set()   
            callback_answer = normal(callback.data)
            # #(callback_answer)
            user_l = ''.join([f'{i}/\\' for i in ci.parse_user_info(str(callback_answer), 'Subscribers')]).replace('/\\','\n')
            await callback.message.answer(user_l, reply_markup=btn.Admin_Del_From_Bot_Subs)
            await callback.answer()
            # #(callback_answer)
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






    # Переход в главное меню

        
        if message.text == 'Главное меню' and str(message.from_user.id) == Admin_id:
            await message.answer('Главное меню', reply_markup = btn.Admin_Main)

        elif message.text == 'Главное меню':
            await message.answer('Главное меню', reply_markup = btn.MainMenu)





    # С подпиской
        if message.text == 'Мои подписки':

            #('В иф для отписки вошел')
            
            await message.answer('Подписки', reply_markup = btn.MainNext)
            if len([i for i in ci.file_read(message.from_user.id) if 'sub' in i]) == 0:
                await message.answer('У вас нет подписок', reply_markup = btn.MainNext)
            else:
                btn.AddToSubscribeCotel(str(message.from_user.id))
                await message.answer('Список котельных:', reply_markup = btn.AllListSubscribeCotel)
                        
        @dp.callback_query_handler(text = btn.AllListSubscribeCotel_t) # Обработчик нажатия инлайн кнопок
        async def msg_answer(callback: types.CallbackQuery):

            global subscribe_adres
            #('отработала отписка')
            callback_answer=normal(callback.data) # Переменная для сохранения адреса
            # cotelnaya_l=''.join([f'{i}/\\' for i in ci.parse_table()[f'{callback_answer}']]).replace('/\\','\n')
            cotelnaya=''.join([f'{i}/\\' for i in ci.parse_table()[f'{callback_answer}']]).replace('/\\','\n')
            await callback.message.answer(f'{cotelnaya}', reply_markup = btn.Delete_from_Subscribe) # Выводит информацию о котельной
            await callback.answer()
            # await bot.send_message(message.from_user.id, callback.data)
            # await callback.message.answer(f'{callback_answer}')
            subscribe_adres = callback_answer
            #(subscribe_adres, 'it is subscribe adress')

        if message.text == 'Интервал сообщений 5 минут':
            #(message.text)
            await message.answer('Информация о котельной будет присылаться раз в 5 минут', reply_markup = btn.MainNext)
            ci.send_message_interval_5(subscribe_adres, message.from_user.id)
            ci.add_newtime(subscribe_adres, message.from_user.id)

        if message.text == 'Интервал сообщений 10 минут':
            #(message.text)
            await message.answer('Информация о котельной будет присылаться раз в 10 минут', reply_markup = btn.MainNext)
            ci.send_message_interval_10(subscribe_adres, message.from_user.id)
            ci.add_newtime(subscribe_adres, message.from_user.id)

        if message.text == 'Отписаться': 
            #(message.text)
            if subscribe_adres != '':
                ci.subscribe_del(subscribe_adres, message.from_user.id)
                subscribe_adres_for_message = subscribe_adres.split('(')[0]
                await message.answer(f'Вы отписались от {subscribe_adres_for_message}', reply_markup = btn.MainNext)
            else: 
                await message.answer(f'Повторите попытку')
                



    # Избранные

        if message.text == 'Избранное':
            #('В иф с избранным вошел')
            # btn.AddToFavsCotel(str(message.from_user.id))
            await message.answer('Избранное', reply_markup = btn.MainNext)
            if len([i for i in ci.file_read(message.from_user.id) if 'fav' in i]) == 0:
                await message.answer('У вас нет избранных котельных', reply_markup = btn.MainNext)
            else:
                btn.AddToFavsCotel(str(message.from_user.id))
                #(message.text)
                await message.answer('Список котельных:', reply_markup = btn.Favourites)
        
        @dp.callback_query_handler(text = btn.Favourites_t) # Обработчик нажатия инлайн кнопок         
        async def msg_answer(callback: types.CallbackQuery):    
            # await state.finish()
            # await UserState.favourites.set()
            global fav_adres
            #('отработала избранное')
            callback_answer=normal(callback.data) # Переменная для сохранения адреса
            # cotelnaya_l=''.join([f'{i}/\\' for i in ci.parse_table()[f'{callback_answer}']]).replace('/\\','\n')
            cotelnaya_l=''.join([f'{i}/\\' for i in ci.parse_table()[f'{callback_answer}']]).replace('/\\','\n')
            # #(callback_answer)
            await callback.message.answer(f'{cotelnaya_l}', reply_markup = btn.Del_From_Fav) # Выводит информацию о котельной
            await callback.answer()
            # await bot.send_message(message.from_user.id, callback.data)
            # await callback.message.answer(f'{callback_answer}')
            fav_adres = callback_answer
            # await state.finish()
            #(fav_adres, 'it is fav adress')

        if message.text == 'Добавить в избранное': 
            #(message.text)
            if fav_adres != '':
                ci.favourite_add(fav_adres, message.from_user.id)
                fav_adres_for_message = fav_adres.split('(')[0]
                await message.answer(f'Вы добавили в избранное {fav_adres_for_message}', reply_markup = btn.MainNext)
            else: 
                await message.answer(f'Повторите попытку')

        if message.text == 'Удалить из избранного': 
            #(message.text)
            if fav_adres != '':
                ci.favourite_del(fav_adres, message.from_user.id)
                fav_adres_for_message = fav_adres.split('(')[0]
                await message.answer(f'Вы удалили из избранного {fav_adres_for_message}', reply_markup = btn.MainNext)
            else: 
                await message.answer(f'Повторите попытку')

    




    # Без подписки

        if message.text == 'Получить список районов':

            #('В иф для подписки вошел')
            # await message.answer('Получить список районов', reply_markup = btn.MainNext)
            await message.answer('Список районов:', reply_markup = btn.Cotels_Districts)
        @dp.callback_query_handler(text = btn.Cotels_Districts_t) # Обработчик нажатия инлайн кнопок 1 ур
        async def msg_answer_1(callback: types.CallbackQuery): # Вывод районов в инлайн кнопках
            #('я в 1 ур')
            back = normal(callback.data)
            btn.CotsInDistrict(back)
            await callback.message.answer(f'{back}', reply_markup = btn.Cotels_in_District)
            await callback.answer()
            #(back, 'Остановилось')

            @dp.callback_query_handler(text = btn.Cotels_in_District_t) # Обработчик нажатия инлайн кнопок 2 ур
            async def msg_answer_2(callback: types.CallbackQuery): # Вывод котельных для выбранного района
                global adress
                global fav_adres
                # await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id) # Штука для удаления сообщения(если надо будет)
                #('я во 2 ур')
                #(callback.message.from_user.id)
                #(callback.data)
                #(callback.message.message_id)
                callback_answer=normal(callback.data) # Переменная для сохранения адреса
                if len(ci.parse_file_district()[callback_answer]) < 2:
                    cotelnaya_l=''.join([f'{i}/\\' for i in ci.parse_table()[f'{callback_answer}(1)']]).replace('/\\','\n')

                    if ci.file_check_copy_sub(f'{callback_answer}(1)', callback.from_user.id) and ci.file_check_copy_fav(f'{callback_answer}(1)', callback.from_user.id):
                        await callback.message.answer(cotelnaya_l, reply_markup = btn.MainNext) # Выводит информацию о котельной
                        await callback.answer()
                        adress = callback_answer
                        fav_adres = f'{callback_answer}(1)'

                    elif ci.file_check_copy_sub(f'{callback_answer}(1)', callback.from_user.id):
                        #(f'{callback_answer}(1)')
                        #(btn.AddToFav)
                        #(cotelnaya_l)
                        await callback.message.answer(f'{cotelnaya_l}', reply_markup = btn.AddToFav) # Выводит информацию о котельной
                        await callback.answer()
                        adress = callback_answer
                        fav_adres = f'{callback_answer}(1)'

                    elif ci.file_check_copy_fav(f'{callback_answer}(1)', callback.from_user.id):
                        await callback.message.answer(f'{cotelnaya_l}', reply_markup = btn.AddToSub) # Выводит информацию о котельной
                        await callback.answer()
                        adress = callback_answer
                        fav_adres = f'{callback_answer}(1)'

                    else:
                        await callback.message.answer(f'{cotelnaya_l}', reply_markup = btn.Add_to_Subscribe) # Выводит информацию о котельной
                        await callback.answer()
                        adress = callback_answer
                        fav_adres = f'{callback_answer}(1)'

                else:
                    adress = callback_answer
                    btn.Teplosystems_Cotel_test(callback_answer)
                    
                    await callback.message.answer(f'Теплосистемы {callback_answer}:', reply_markup = btn.TS_cotel_test)



            #(message.text, '+++++++++++++++++++++++++++++++++++++', adress)



        if 'Теплосистема' in message.text:
            
            #(message.text,'---------------------------------------')
            number = message.text.split('Теплосистема ')[1]
            cotelnaya=f'{adress}({number})'
            #(cotelnaya)
            
            cotelnaya_l=''.join([f'{i}/\\' for i in ci.parse_table()[f'{adress}({number})']]).replace('/\\','\n') 

            if ci.file_check_copy_sub(cotelnaya, message.from_user.id) and ci.file_check_copy_fav(cotelnaya, message.from_user.id):
                await message.answer(f'{cotelnaya_l}', reply_markup = btn.MainNext) # Выводит информацию о котельной
                
            elif ci.file_check_copy_fav(cotelnaya, message.from_user.id):
                await message.answer(f'{cotelnaya_l}', reply_markup = btn.AddToSub) # Выводит информацию о котельной

            elif ci.file_check_copy_sub(cotelnaya, message.from_user.id):
                await message.answer(f'{cotelnaya_l}', reply_markup = btn.AddToFav) # Выводит информацию о котельной

            else:
                await message.answer(f'{cotelnaya_l}', reply_markup = btn.Add_to_Subscribe) # Выводит информацию о котельной
            
            fav_adres = cotelnaya
            #(cotelnaya_l)
        try:
            if adress in [str(j).split('(')[0] for j in ci.parse_table() if len(ci.parse_file_district()[adress]) < 2]:
                cotelnaya=f'{adress}(1)'
        except: pass

                # await message.answer(f'Теплосистемы {adress}:', reply_markup = btn.TS_cotel)
                # @dp.callback_query_handler(text = btn.TS_cotel_t) # Обработчик нажатия инлайн кнопок 3 ур
                # async def msg_answer_2(callback: types.CallbackQuery): # Вывод информации о теплосистемах котельной
            
                    
                #     #(callback_answer)
                    
                #     callback_answer=normal(callback.data) # Переменная для сохранения адреса

                #     await message.answer(f'Теплосистемы {callback_answer}:', reply_markup = btn.TS_cotel)
                #     #(callback_answer)
                
                #     #('Попытка войти в 3й')
                    
                    
                #     # global adress
                    
                #     #('я в 3 ур')
                #     callback_answer=normal(callback.data)
                #     cotelnaya=''.join([f'{i},' for i in ci.parse_table()[callback_answer]]).replace(',','\n')
                #     #([f'{i}\n' for i in (ci.parse_table()[callback_answer])])
                #     if ci.file_check_copy(callback_answer, callback.from_user.id):
                #         await callback.message.answer(f'{cotelnaya}', reply_markup = btn.Add_to_Subscribe) # Выводит информацию о котельной
                #         # await message.answer()
                #     else:
                #         await callback.message.answer(f'{cotelnaya}', reply_markup = btn.Add_to_Subscribe) # Выводит информацию о котельной
                #         # await bot.send_message(message.from_user.id, callback.data)
                #         # await callback.message.answer(f'{callback_answer}', reply_markup = btn.Add_to_Subscribe)
                #         adress = callback_answer

        if message.text == 'Подписаться': 
            
            #(cotelnaya)
            #(1, '========================')
            # number = message.text.split('Теплосистема ')[1]
            # cotelnaya=''.join([f'{i},' for i in ci.parse_table()[f'{adress}({number})']]).replace(',','\n')
            if cotelnaya in [j for j in ci.parse_table()]:
                ci.subscribe_add(cotelnaya, message.from_user.id)
                ci.send_message_interval_5(cotelnaya, message.from_user.id)
                ci.add_newtime(cotelnaya, message.from_user.id)
                # #(ci.subscribe_add(adres, message.from_user.id))
                subscribe_adres_for_message = cotelnaya.split('(')[0]
                await message.answer(f'Вы подписались на {subscribe_adres_for_message}', reply_markup = btn.MainNext)
        
            else: 
                await message.answer(f'Повторите попытку')





    elif 'Интервал' not in message.text:
        pass
        


# Рассылка



async def send_message_interval(): # Функция для создания сообщений для рассылки

    for i in ci.adding_msg(): # Ключи словаря
        #(i)
        try: # Проверка на то запущен или остановлен бот у пользователя (надо для того что бы бот не лёг)
            for j in ci.adding_msg()[i]: # Значения для ключа
                if 'fav' not in j:
                    # #(ci.adding_msg()[i])
                    
                    now_time = int(str(dt.datetime.now().strftime('%H:%M:00')).split(':')[0])*60+int(str(dt.datetime.now().strftime('%H:%M:00')).split(':')[1])
                    # try: 
                    j_time = int((str(j).split(', ')[-1]).split(':')[0])*60+int((str(j).split(', ')[-1]).split(':')[1])
                    # except: pass
                    j_adres = str(j).split(', ')[0].replace('\ufeff', '')
                    #(j)
                    #( str(dt.datetime.now().strftime('%H:%M:00')), j_time, now_time)
                    if j_time == int(str(dt.datetime.now().strftime('%H:%M:00')).split(':')[0])*60+int(str(dt.datetime.now().strftime('%H:%M:00')).split(':')[1]):
                        # #(i); #(j)
                        cotelnaya_l=''.join([f'{i}/\\' for i in ci.parse_table()[str(j.split(', ')[0]).replace('\ufeff', '')]]).replace('/\\','\n')
                        #(cotelnaya_l)
                        await bot.send_message(i, f'{cotelnaya_l}') # Выводит информацию о котельной
                        ci.file_new_time(j_adres, i)
                    
        except:
            await bot.send_message('Здравствуйте!')

    

scheduler.add_job(send_message_interval, trigger='interval', seconds=1) # Создание сообщения 276693613 на рассылку 5288656086
scheduler.start() # Рассылка



# Запускаем бота и включаем его на бесконечную работу

# if __name__ == '__main':
executor.start_polling(dp, skip_updates=False)



