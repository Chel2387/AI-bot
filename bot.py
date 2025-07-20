import telebot
import os
import random
from bot_logic import gen_pass
from model import get_class

text_messages = {
    'info':
        u'Привет, Я твой бот Бро,\n'
        u'У меня есть кучу команд.\n'
        u'Вот они: '
        u'start, hello, bye, password, heh, help/info, mem, eco, why need eco?'
}


# Замени 'TOKEN' на токен твоего бота
# Этот токен ты получаешь от BotFather, чтобы бот мог работать
bot = telebot.TeleBot("TOKEN")
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Бот, приятно видеть тебя :)")
    
@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")
    
@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['password'])
def send_bye(gen_pass):
    bot.reply_to(gen_pass())

# Обработчик команды '/heh'
@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)
    
@bot.message_handler(commands=['info', 'help'])
def on_info(message):
    bot.reply_to(message, text_messages['info'])

@bot.message_handler(commands=['mem'])
def send_mem(message):
    file_list = os.listdir("images")
    img_name = random.choice(file_list)
    with open(f'images/{img_name}', 'rb') as f:  
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=['eco'])
def send_eco(message):
    file_list = os.listdir("images_eco")
    name = random.choice(file_list)
    with open(f'images_eco/{name}', 'rb') as a:  
        bot.send_photo(message.chat.id, a)

@bot.message_handler(commands=['why need eco?'])
def send_bye(message):
    bot.reply_to(message, "Если мы не будем беречь природу, то тогда мы все умрём :)")

@bot.message_handler(commands=['trash'])
def send_bye(message):
    bot.reply_to(message, "Стекло - зелёный бак, Пластик - красный бак, Метал - жёлтый бак, Бумага - синий бак")

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    if not message.photo:
        return bot.send_photo(message.chat.id, "Ты не загрузил фото")

    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]

    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Картинка сохранена")

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    if not message.photo:
        return bot.send_photo(message.chat.id, "Ты не загрузил фото")
    
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]

    result = get_class(file_name)
    if result == "Стакан":
        bot.reply_to(message, "На изображении стакан, в отличии от кружки, у него нету ручки и чаще всего стакан прозрачный")
    if result == "Кружка":
        bot.reply_to(message, "На изображении кружка, в отличии от стакана, у кружки есть ручка")
    

    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    
bot.polling()
