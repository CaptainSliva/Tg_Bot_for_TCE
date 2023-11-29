
# Импортируем нужные библиотеки для работы с aiogram
import time
import logging as log
from apscheduler.schedulers.blocking import BlockingScheduler
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
import Buttons as btn
import CotInfo as ci
import datetime as dt
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# Мои файлы
import Buttons as btn
import CotInfo as ci
import Create_new_table as New_table

# # Начинаем создавать бота


TOKEN = '23456789' # Ваш токен бота
#Создаем telegram бота
log.basicConfig(level = log.INFO) # Включаем логирование чтобы не пропустить важные сообщения
bot = Bot(token = TOKEN) # Создаем обьект бота
dp = Dispatcher(bot) # Диспетчер

subscribe_adres = str()
adress = str()
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
#



def normal(nstr): # Функция ля удаления айдишника из адреса    nstr - строка с айдишником
    return nstr.split('/')[0]

r={"'" : "" , '"' : "" , "[" : "" , "]" : "" , "{" : "" , "}" : "" }
def del_trash(txt):
    global r
    for i, j in r.items():
        txt = txt.replace(i, j)
    return txt



# Установление времени после перезапуска бота
for i in ci.adding_msg(): # Ключи словаря
    # print(i)
    try: # Проверка на то запущен или остановлен бот у пользователя (надо для того что бы бот не лёг)
        for j in ci.adding_msg()[i]: # Значения для ключа
            print(i); print(j)
            ci.add_newtime(str(j).split(', ')[0], i)
    except:
        pass


@dp.message_handler(commands = ['start', 's', 'старт'])
async def cmd_start(message: types.Message):
    await message.answer('Hello {0.first_name}'.format(message.from_user), reply_markup=btn.MainMenu) 


# С подпиской

@dp.message_handler() # Обработчик сообщений
async def bot_message(message: types.Message):

    global subscribe_adres
    if message.text == 'Мои подписки':
        var1 = ci.var1
        print('В иф для отписки вошел')
        
        await message.answer('Подписки', reply_markup = btn.MainNext)
        if len(ci.file_read(message.from_user.id)) == 0:
            await message.answer('У вас нет подписок', reply_markup = btn.MainNext)
        else:
            btn.AddToSubscribeCotel(str(message.from_user.id))
            await message.answer('Получить список котельных:', reply_markup = btn.AllListSubscribeCotel)
            @dp.callback_query_handler(text = btn.AllListSubscribeCotel_t) # Обработчик нажатия инлайн кнопок
            async def msg_answer(callback: types.CallbackQuery):
                
                global subscribe_adres
                print('отработала отписка')
                callback_answer=normal(callback.data) # Переменная для сохранения адреса
                corelnaya=''.join([f'{i},' for i in ci.parse_table()[callback_answer]]).replace(',','\n')
                await callback.message.answer(f'{corelnaya}', reply_markup = btn.Delete_from_Subscribe) # Выводит информацию о котельной
                # await message.answer()
                # await bot.send_message(message.from_user.id, callback.data)
                # await callback.message.answer(f'{callback_answer}')
                subscribe_adres = callback_answer

    if message.text == 'Интервал сообщений 5 минут':
        print(message.text)
        await message.answer('Информация о котельной будет присылаться раз в 5 минут', reply_markup = btn.MainNext)
        ci.send_message_interval_5(subscribe_adres, message.from_user.id)
        ci.add_newtime(subscribe_adres, message.from_user.id)

    if message.text == 'Интервал сообщений 10 минут':
        print(message.text)
        await message.answer('Информация о котельной будет присылаться раз в 10 минут', reply_markup = btn.MainNext)
        ci.send_message_interval_10(subscribe_adres, message.from_user.id)
        ci.add_newtime(subscribe_adres, message.from_user.id)

    if message.text == 'Отписаться': 
        print(message.text)
        if subscribe_adres != '':
            ci.subscribe_del(subscribe_adres, message.from_user.id)
            await message.answer(f'Вы отписались от {subscribe_adres}', reply_markup = btn.MainNext)
        else: 
            await message.answer(f'Повторите попытку')
            


# Переход в главное меню

    if message.text == 'Главное меню':
        var1 = ci.var1
        await message.answer('Главное меню', reply_markup = btn.MainMenu)
    


# Без подписки

    if message.text == 'Получить список котельных':
        var1 = ci.var1
        print('В иф для подписки вошел')
        await message.answer('Получить список районов', reply_markup = btn.MainNext)
        await message.answer('Список райнонов:', reply_markup = btn.Cotels_Districts)
        @dp.callback_query_handler(text = btn.Cotels_Districts_t) # Обработчик нажатия инлайн кнопок
        async def msg_answer(callback: types.CallbackQuery): # Ответ на нажатие на кнопку
            print('я в первом хендлере')
            back = normal(callback.data)
            btn.CotsInDistrict(back)
            await message.answer(f'{back}', reply_markup = btn.Cotels_in_District)
            print(back, 'Остановилось')
            
            @dp.callback_query_handler(text = btn.Cotels_in_District_t) # Обработчик нажатия инлайн кнопок
            async def msg_answer(callback: types.CallbackQuery): # Ответ на нажатие на кнопку
                global adress
                # await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
                print('отработала подписка')
                print(callback.message.from_user.id)
                callback_answer=normal(callback.data) # Переменная для сохранения адреса
                print(callback_answer)
                cotelnaya=''.join([f'{i},' for i in ci.parse_table()[callback_answer]]).replace(',','\n')
                print([f'{i}\n' for i in (ci.parse_table()[callback_answer])])
                if ci.file_check_copy(callback_answer, callback.from_user.id):
                    await callback.message.answer(f'{cotelnaya}', reply_markup = btn.Add_to_Subscribe) # Выводит информацию о котельной
                    # await message.answer()
                else:
                    await callback.message.answer(f'{cotelnaya}', reply_markup = btn.Add_to_Subscribe) # Выводит информацию о котельной
                    # await bot.send_message(message.from_user.id, callback.data)
                    # await callback.message.answer(f'{callback_answer}', reply_markup = btn.Add_to_Subscribe)
                    adress = callback_answer

    if message.text == 'Подписаться': 
        if adress in ci.var1:
            ci.subscribe_add(adress, message.from_user.id)
            # print(ci.subscribe_add(adres, message.from_user.id))
            await message.answer(f'Вы подписались на {adress}', reply_markup = btn.MainNext)
        else: 
            await message.answer(f'Повторите попытку')
    


# Рассылка



async def send_message_interval(): # Функция для создания сообщений для рассылки
    var1 = ci.var1

    for i in ci.adding_msg(): # Ключи словаря
        # print(i)
        try: # Проверка на то запущен или остановлен бот у пользователя (надо для того что бы бот не лёг)
            for j in ci.adding_msg()[i]: # Значения для ключа
                # print(j)
                j_time = str(j).split(', ')[-1]
                j_adres = str(j).split(', ')[0]
                if j_time == str(dt.datetime.now().strftime('%H:%M:00')):
                    print(i); print(j)
                    ci.file_new_time(i, j_adres)
                    
                    await bot.send_message(i, f'{ci.parse_table()[i]}') # Выводит информацию о котельной
        except:
            pass

    
# scheduler.add_job(New_table.new_table, trigger='interval', seconds=60*22) 
# scheduler.add_job(send_message_interval, trigger='interval', seconds=1) # Создание сообщения на рассылку
# scheduler.add_job(New_table.new_table, trigger='interval', seconds=60*2) 
# scheduler.start() # Рассылка



# Запускаем бота и включаем его на бесконечную работу

# if __name__ == '__main':
executor.start_polling(dp, skip_updates=True)

