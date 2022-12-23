import telebot
import json
import urllib
from telebot import types
import random


def main(token):
    bot = telebot.TeleBot(token)
    password = "password"
    modes = ["Get some quotes", "Get some cool pics", "Bof"]
    editing = ["Add characters", "Add quotes", "Add pics", "Finish editing"]
    bot.characters = None
    bot.pics = None
    bot.quotes = None
    bot.mode = None
    bot.character = None
    bot.current_data = None
    bot.editor_mode = "not editing"

    @bot.message_handler(commands=['start', 'help'])
    def start_message(message):
        with open("data/tgbot/data.json", "r") as read_file:
            bot.current_data = json.load(read_file)
        bot.characters = bot.current_data["characters"]
        bot.pics = bot.current_data["pics"]
        bot.quotes = bot.current_data["quotes"]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        items = []
        for possible_mode in modes:
            items.append(types.KeyboardButton(possible_mode))
            markup.add(items[-1])
        item = types.KeyboardButton("*EDITOR MODE*")
        markup.add(item)
        bot.send_message(message.chat.id, 'What do you want to do?',
                         reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def message_reply(message):
        try:
            if bot.editor_mode == "waiting for password":
                if message.text != password:
                    bot.send_message(message.chat.id,
                                     "Wrong password")
                    bot.editor_mode = "not editing"
                    start_message(message)
                else:
                    bot.editor_mode = "editing"
                    bot.character = None
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    items = []
                    for possible_editing in editing:
                        items.append(types.KeyboardButton(possible_editing))
                        markup.add(items[-1])
                    bot.send_message(message.chat.id,
                                     "you are in editing mode",
                                     reply_markup=markup)

            elif bot.editor_mode == "editing":
                if message.text == "Finish editing":
                    with open("data/tgbot/data.json", "w") as write_file:
                        json.dump(bot.current_data, write_file)

                    bot.send_message(message.chat.id,
                                     "changes applied")
                    bot.editor_mode = "not editing"
                    start_message(message)
                elif message.text == "Add characters":
                    bot.editor_mode = "adding characters"
                    bot.send_message(message.chat.id,
                                     "type the character name")
                else:
                    if message.text == "Add quotes":
                        bot.editor_mode = "adding quotes"
                    elif message.text == "Add pics":
                        bot.editor_mode = "adding pics"
                    markup = types.ReplyKeyboardMarkup(
                        resize_keyboard=True)
                    items = []
                    for possible_character in bot.characters:
                        items.append(
                            types.KeyboardButton(possible_character))
                        markup.add(items[-1])
                    bot.send_message(message.chat.id,
                                     "choose the character",
                                     reply_markup=markup)


            elif bot.editor_mode == "adding characters":
                bot.current_data["characters"].append(message.text)
                bot.editor_mode = "editing"
                bot.send_message(message.chat.id,
                                 "character added")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                items = []
                for possible_editing in editing:
                    items.append(types.KeyboardButton(possible_editing))
                    markup.add(items[-1])
                bot.send_message(message.chat.id,
                                 "you are in editing mode",
                                 reply_markup=markup)

            elif bot.editor_mode == "adding quotes" or bot.editor_mode == "adding pics" and message.text in bot.characters:
                bot.editor_mode = bot.editor_mode[7:]
                bot.character = message.text
                bot.send_message(message.chat.id, "Now enter the info")

            elif bot.editor_mode == "quotes" or bot.editor_mode == "pics" and bot.character is not None:
                bot.current_data[bot.editor_mode][bot.character] = bot.current_data[bot.editor_mode].get(bot.character, [])
                bot.current_data[bot.editor_mode][bot.character].append(message.text)
                bot.send_message(message.chat.id, bot.editor_mode[:-1] + " added")
                bot.editor_mode = "editing"
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                items = []
                for possible_editing in editing:
                    items.append(types.KeyboardButton(possible_editing))
                    markup.add(items[-1])
                bot.send_message(message.chat.id,
                                 "you are in editing mode",
                                 reply_markup=markup)

            elif message.text == "*EDITOR MODE*":
                bot.editor_mode = "waiting for password"
                bot.send_message(message.chat.id,
                                 "Enter the password")

            elif bot.editor_mode != "not editing":
                bot.send_message(message.chat.id,
                                 "Try again later")
                bot.mode = None
                bot.character = None
                start_message(message)

            elif message.text in modes:
                bot.mode = message.text
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                items = []
                for possible_character in bot.characters:
                    items.append(types.KeyboardButton(possible_character))
                    markup.add(items[-1])
                bot.send_message(message.chat.id,
                                 "Great! Choose the character now",
                                 reply_markup=markup)
            elif bot.mode is not None and message.text in bot.characters:
                bot.character = message.text
                bot.send_message(message.chat.id, "Cool beans")
                send_stuff(message)
            else:
                bot.send_message(message.chat.id,
                                 "Sorry, can't understand you")
                start_message(message)
        except:
            bot.send_message(message.chat.id,
                             "Something went wrong, try again")
            bot.mode = None
            bot.character = None
            start_message(message)

    def send_stuff(message):
        if bot.mode is None or bot.character is None:
            bot.send_message(message.chat.id,
                             "Something went wrong, try again")
        else:
            try:
                if bot.mode != "Get some quotes":
                    if bot.character not in bot.pics.keys():
                        bot.send_message(message.chat.id,
                                         "Don't have any pictures :(")
                    else:
                        index_max = len(bot.pics[bot.character]) - 1
                        index = random.randint(0, index_max)
                        url = bot.pics[bot.character][index]
                        f = open('out.jpg', 'wb')
                        f.write(urllib.request.urlopen(url).read())
                        f.close()
                        img = open('out.jpg', 'rb')
                        bot.send_photo(message.chat.id, img)
                        img.close()
                if bot.mode != "Get some cool pics":
                    if bot.character not in bot.quotes.keys():
                        bot.send_message(message.chat.id,
                                         "Don't have any quotes :(")
                    else:
                        index_max = len(bot.quotes[bot.character]) - 1
                        index = random.randint(0, index_max)
                        bot.send_message(message.chat.id,
                                         bot.quotes[bot.character][index],
                                         parse_mode='Markdown')
            except:
                bot.send_message(message.chat.id,
                                 "Something went wrong, try again")
        bot.mode = None
        bot.character = None
        start_message(message)

    bot.polling()


if __name__ == "__main__":
    token = '2093628773:AAF1tyeJ5dP8ZEbiRPXLFR3uNqYHe5hDgvg'
    main(token)
