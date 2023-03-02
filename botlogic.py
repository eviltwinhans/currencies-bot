import telebot
from config import TOKEN, currency_codes
from utils import ConversionException, MoneyConverter
# import redis


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    text = f"Hello, _{message.from_user.first_name} {message.from_user.last_name}_!\n" \
           f"Send '/help' to get instructions on how to use this bot."
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=['help'])
def send_instructions(message: telebot.types.Message):
    text = "Send the bot '*<amount> <current currency> <resulting currency>*' " \
           "to see the result of converting the first currency's amount into the second one.\n" \
           "Example: `100 usd eur`.\n" \
           "Send '/currencies' to get the list of available currencies to use with the main request."
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=['currencies'])
def send_currencies(message: telebot.types.Message):
    text = "Available currencies are: "
    for key, value in currency_codes.items():
        text = '\n'.join((text, f"\* {key}: *{value}*",))
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(content_types=['photo'])
def handle_photos(message: telebot.types.Message):
    bot.reply_to(message, "OK, sure...")
    bot.send_message(message.chat.id, "That's still a nice picture, dude =)")


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        query_parameters = message.text.split()

        if len(query_parameters) != 3:
            raise ConversionException('Incorrect format of request. Please send exactly 3 parameters.')

        amount, convert_from_code, convert_to_code = query_parameters
        convert_from_code = convert_from_code.upper()
        convert_to_code = convert_to_code.upper()
        total = MoneyConverter.convert(amount, convert_from_code, convert_to_code)
    except ConversionException as e:
        bot.reply_to(message, f"Incorrect request.\n{e}", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"Failed to process the request.\n{e}", parse_mode='Markdown')
    else:
        text = f"The cost of {amount} {convert_from_code} in {convert_to_code} today is *{total}*."
        bot.send_message(message.chat.id, text, parse_mode='Markdown')


bot.polling()
