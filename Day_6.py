import telebot
import requests
from telebot import types


TOKEN = '1886173504:AAFpTy02mhIkVhtIcv6WiAb3dzGlaOiLaf8'
WEATHER_TOKEN = '4ffe0b3ca31d102df5f3b9f5ccacb059'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help','no','film','weather','film','profile','calc'])
def start_bot(message):
    if message.text.lower() == '/start':
        bot.send_message(message.chat.id, "Перед началом работы пожалуйста авторизируйтесь. /profile.")                                          
    
    elif message.text.lower() == '/help':
        bot.send_message(message.chat.id, "Привет! Я новый бот! \nСписок команд которые я понимаю:\n/help - Вы можете узнать дополнительную информацию о боте,\n/no - yes,\n/weather - Узнайте о погоде,\n/film - Раздел с фильмами,\n/profile - ваш профиль,\n/calc - Калькулятор")
        
    elif message.text.lower() == '/no':
        bot.send_message(message.chat.id, "yes")
   
    elif message.text.lower() == '/film':
        bot.send_message(message.chat.id, "Вы попали на раздел с фильмами")
        bot.send_message(message.chat.id, "Какой фильм хотите посмотреть?")
        bot.register_next_step_handler(message, film_menu)

    elif message.text.lower() == '/weather':
        bot.send_message(message.chat.id, "Раздел погоды")
        bot.send_message(message.chat.id, "Введите название города")
        bot.register_next_step_handler(message, weather_menu)
        
    elif message.text.lower() == '/profile':
        bot.send_message(message.chat.id, "Вы попали на ваш профиль!")
        bot.send_message(message.chat.id, "Ваше имя:")
        bot.register_next_step_handler(message, entry_name)
        
    elif message.text.lower() == '/calc':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Сумма')
        btn2 = types.KeyboardButton('Минус')
        btn3 = types.KeyboardButton('Умножение')
        btn4 = types.KeyboardButton('Деление')
        keyboard.add(btn1,btn2)
        keyboard.add(btn3,btn4)
        
        bot.send_message(message.chat.id, "Калькулятор")
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)
        bot.register_next_step_handler(message, calc_start)

def calc_start(message):
    bot.send_message(message.chat.id, "Введите два числа через пробел")
    if message.text == 'Сумма':
        bot.register_next_step_handler(message, calc_sum)
    elif message.text == 'Минус':
        bot.register_next_step_handler(message, calc_min)
    elif message.text == 'Умножение':
        bot.register_next_step_handler(message, calc_umn)
    elif message.text == 'Деление':
        bot.register_next_step_handler(message, calc_del)

def calc_min(message):        
    nums = message.text.split()
    num1 = int(nums[0])
    num2 = int(nums[1])
    bot.send_message(message.chat.id, f"Ответ: {num1 - num2}")
        
def calc_sum(message):        
    nums = message.text.split()
    num1 = int(nums[0])
    num2 = int(nums[1])
    bot.send_message(message.chat.id, f"Ответ: {num1 + num2}")
        
def calc_umn(message):
    nums = message.text.split()
    num1 = int(nums[0])
    num2 = int(nums[1])
    bot.send_message(message.chat.id, f"Ответ: {num1 * num2}")
    
def calc_del(message):
    nums = message.text.split()
    num1 = int(nums[0])
    num2 = int(nums[1])
    bot.send_message(message.chat.id, f"Ответ: {num1 / num2}")
        

        
        
def entry_name(message):
    name = message.text
    bot.send_message(message.chat.id, f"Ваше имя: {name}")
    bot.send_message(message.chat.id, f"Хорошо {name}, а теперь назовите свой возраст")
    bot.register_next_step_handler(message, entry_age)
    
def entry_age(message):
    age = message.text
    bot.send_message(message.chat.id, f"Ваш возраст: {age}")
    bot.send_message(message.chat.id, "Назовите свой номер телефона")
    bot.register_next_step_handler(message, entry_num)

def entry_num(message):
    num = message.text
    bot.send_message(message.chat.id, f"Ваш номер телефона: {num}")
    bot.send_message(message.chat.id, f"Добро пожаловать! /help для того что-бы узнать дополнительную информацию про бота*") 
    
    
@bot.message_handler(content_type=['text'])
def film_menu(message):
    film = message.text
    bot.send_message(message.chat.id, f"Вы хотите посмотреть фильм {film}?")
    bot.send_message(message.chat.id, f"Неплохой выбор!") 
    
@bot.message_handler(content_type=['text'])
def weather_menu(message):
    city = message.text
    API_URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_TOKEN}'
    r = requests.get(API_URL)
    w = r.json()
    
    print(r.text)
    
    bot.send_message(message.chat.id, f"Вы ввели город {city}!")
    bot.send_message(message.chat.id, f"Ищем температуру для города...")
    
    
    bot.send_message(message.chat.id,
f'''В городе {w['name']}\n
Температура: {round(w['main']['temp'] - 273.15)} С°\n
Температура чувствуется как: {round(w['main']['feels_like'] - 273.15)} С°\n
Ветер: {round(w['wind']['speed'])} м/с\n
Влажность: {round(w['main']['humidity'])}% \n
Давление:{round(w['main']['pressure'])} гПа
''')



bot.polling()
























































































