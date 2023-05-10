import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CriptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help (message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате: \n <имя валюты> \
<в какую валюту нужно перевести> \
<количество переводимой валюты>\n увидеть список доступных валют:/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные вылюты:'
    for key in keys.keys():
        text ='\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('должно быть три параметра.')

        qoute, base, amount = values
        total_base = CriptoConverter.convert(qoute, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду \n{e}')

    else:
        text = f'Цена {amount} {qoute} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()





