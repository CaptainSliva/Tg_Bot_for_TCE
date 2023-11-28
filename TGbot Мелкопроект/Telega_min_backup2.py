
# Импортируем нужные библиотеки для работы с aiogram
import time
import os
import logging as log
from apscheduler.schedulers.blocking import BlockingScheduler
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
import Buttons as btn
import CotInfo as ci
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# Мои файлы
import Buttons as btn
import CotInfo as ci
import Create_new_table as New_table

# # Начинаем создавать бота


TOKEN = '5897237424:AAE3IRCOrP474qARfVWRU9UfnxIPJeq92XI' # Ваш токен бота
#Создаем telegram бота
log.basicConfig(level = log.INFO) # Включаем логирование чтобы не пропустить важные сообщения
bot = Bot(token = TOKEN) # Создаем обьект бота
dp = Dispatcher(bot) # Диспетчер

subscribe_adres = str()
adress = str()
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
#
def normal(nstr): # Функция ля удаления айдишника из адреса    nstr - строка с айдишником
    return nstr.split('_')[0]

@dp.message_handler(commands = ['start', 's', 'старт'])
async def cmd_start(message: types.Message):
    await message.answer('Hello {0.first_name}'.format(message.from_user), reply_markup=btn.MainMenu) 


# С подпиской

@dp.message_handler() # Обработчик сообщений
async def bot_message(message: types.Message):
    global subscribe_adres
    if message.text == 'Мои подписки':
        var1, var2, var3, var4, var5 = ci.parse_table()
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
                await callback.message.answer(f'{var1[var1.index(callback_answer)]}:\nT1 = {var2[var1.index(callback_answer)]}\nT2 = {var3[var1.index(callback_answer)]}\nP1 = {var4[var1.index(callback_answer)]}\nP2 = {var5[var1.index(callback_answer)]}', reply_markup = btn.Delete_from_Subscribe) # Выводит информацию о котельной
                # await message.answer()
                # await bot.send_message(message.from_user.id, callback.data)
                # await callback.message.answer(f'{callback_answer}')
                subscribe_adres = callback_answer

    if message.text == 'Интервал сообщений 5 минут(в разработке)':
        print(message.text)
        await message.answer('Информация о котельной будет присылаться раз в 5 минут', reply_markup = btn.MainNext)
        ci.send_message_interval_5(subscribe_adres, message.from_user.id)

    if message.text == 'Интервал сообщений 10 минут(в разработке)':
        print(message.text)
        await message.answer('Информация о котельной будет присылаться раз в 10 минут', reply_markup = btn.MainNext)
        ci.send_message_interval_10(subscribe_adres, message.from_user.id)

    if message.text == 'Отписаться': 
        print(message.text)
        if subscribe_adres != '':
            ci.subscribe_del(subscribe_adres, message.from_user.id)
            await message.answer(f'Вы отписались от {subscribe_adres}', reply_markup = btn.MainNext)
        else: 
            await message.answer(f'Повторите попытку')
            


# Переход в главное меню

    if message.text == 'Главное меню':
        var1, var2, var3, var4, var5 = ci.parse_table()
        await message.answer('Главное меню', reply_markup = btn.MainMenu)
    


# Без подписки

    if message.text == 'Получить список котельных':
        var1, var2, var3, var4, var5 = ci.parse_table()
        print('В иф для подписки вошел')
        await message.answer('Получить список котельных', reply_markup = btn.MainNext,)
        await message.answer('Список котельных:', reply_markup = btn.AllListCotel)
        @dp.callback_query_handler(text = btn.AllListCotel_t) # Обработчик нажатия инлайн кнопок
        async def msg_answer(callback: types.CallbackQuery): # Ответ на нажатие на кнопку 
            global adress
            
            print('отработала подписка')
            print(callback.message.from_user.id)
            callback_answer=normal(callback.data) # Переменная для сохранения адреса
            
            if ci.file_check_copy(callback_answer, callback.from_user.id):
                await callback.message.answer(f'{var1[var1.index(callback_answer)]}:\nT1 = {var2[var1.index(callback_answer)]}\nT2 = {var3[var1.index(callback_answer)]}\nP1 = {var4[var1.index(callback_answer)]}\nP2 = {var5[var1.index(callback_answer)]}', reply_markup = btn.MainNext) # Выводит информацию о котельной  
                # await message.answer()
            else:
                await callback.message.answer(f'{var1[var1.index(callback_answer)]}:\nT1 = {var2[var1.index(callback_answer)]}\nT2 = {var3[var1.index(callback_answer)]}\nP1 = {var4[var1.index(callback_answer)]}\nP2 = {var5[var1.index(callback_answer)]}', reply_markup = btn.Add_to_Subscribe) # Выводит информацию о котельной  
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
    var1, var2, var3, var4, var5 = ci.parse_table()

    for i in ci.adding_msg(): # Ключи словаря
        print(i)
        try: # Проверка на то запущен или остановлен бот у пользователя (надо для того что бы бот не лёг)
            for j in ci.adding_msg()[i]: # Значения для ключа
                print(j)
                await bot.send_message(i, f'{var1[var1.index(j)]}:\nT1 = {var2[var1.index(j)]}\nT2 = {var3[var1.index(j)]}\nP1 = {var4[var1.index(j)]}\nP2 = {var5[var1.index(j)]}') # Выводит информацию о котельной
        except:
            pass

scheduler.add_job(New_table.new_table, trigger='interval', seconds=60*22) 
time.sleep(1)
scheduler.add_job(send_message_interval, trigger='interval', seconds=58*5) # Создание сообщения на рассылку
time.sleep(1)
scheduler.add_job(New_table.new_table, trigger='interval', seconds=60*2) 
scheduler.start() # Рассылка



# Запускаем бота и включаем его на бесконечную работу

# if __name__ == '__main':
executor.start_polling(dp, skip_updates=True)









