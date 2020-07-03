import telebot

from telebot import types

from urllib.request import urlopen

import json


def get_jsonparset_data(uri):
    response = urlopen(uri)
    data = response.read().decode("utf-8")
    return json.loads(data)


weather_dictionary = {"Snow": "снег", "Sleet": "дождь со снегом", "Hail": "град", "Thunderstorm": "гроза",
                      "Heavy Rain": "сильный дождь", "Light Rain": "лёгкий дождь", "Showers": "ливни",
                      "Heavy Cloud": "пасмурно", "Light Cloud": "облачно", "Clear": "солнечно"}

itembtn_mega = []

url = "https://www.metaweather.com/api/location/44418/"
url1 = "https://www.metaweather.com/api/location/2122265/"
url2 = "https://www.metaweather.com/api/location/638242/"
wealondon = get_jsonparset_data(url)
wemoscow = get_jsonparset_data(url1)
weberlin = get_jsonparset_data(url2)
london = weather_dictionary[wealondon['consolidated_weather'][0]['weather_state_name']]
moscow = weather_dictionary[wemoscow['consolidated_weather'][0]['weather_state_name']]
berlin = weather_dictionary[weberlin['consolidated_weather'][0]['weather_state_name']]
london1 = str(int(wealondon['consolidated_weather'][0]['min_temp'])) + '°C', str(
    int(wealondon['consolidated_weather'][0]['max_temp'])) + '°C'
moscow1 = str(int(wemoscow['consolidated_weather'][0]['min_temp'])) + '°C', str(
    int(wemoscow['consolidated_weather'][0]['max_temp'])) + '°C'
berlin1 = str(int(weberlin['consolidated_weather'][0]['min_temp'])) + '°C', str(
    int(weberlin['consolidated_weather'][0]['max_temp'])) + '°C'
word_weather = {"снег": "Я б сходил погулять, сыграть в снежки, или слепить снеговика!",
                "дождь со снегом": "что-то погода не очень, советую остаться дома.",
                "град": "вот сейчас точно не стоит выходить из дома - ЭТО ОПАСНО!",
                "гроза": "люблю смотреть на грозу, но только если я при этом в доме, советую тебе поступить так же!",
                "сильный дождь": "если хочешь промокнуть насквозь, то срочно беги на улицу",
                "лёгкий дождь": "думаю он скоро закончится, и после него будет прекрасная свежесть на улице",
                "ливни": "если хотел идти гулять, пора менять планы",
                "пасмурно": "я бы остался дома, но если хочется гулять, я думаю можно сходить",
                "облачно": "хороший повод пойти гулять",
                "солнечно": "прекрасная погода, чтобы пойти гулять, советую так и поступить!"}
cities = {"лондон": "Лондон\nТемпература: " + str(london1[0]) + "-" + str(london1[1]) + "\n" + london + ",\n" +
                    word_weather[london],
          "москв": "Москва\nТемпература: " + str(moscow1[0]) + "-" + str(moscow1[1]) + "\n" + moscow + ",\n" +
                   word_weather[moscow],
          "берлин": "Берлин\nТемпература: " + str(berlin1[0]) + "-" + str(berlin1[1]) + "\n" + berlin + ",\n" +
                    word_weather[berlin]}
very_famous = {}
very_famous1 = {}
very_famous2 = {}
very_famous3 = {}
cities_spisok = ["не нужный", "москв", "лондон", "берлин"]

bot = telebot.TeleBot('token')

markup = types.ReplyKeyboardMarkup()
itembtn = ["Москва", "Лондон", "Берлин"]
for l in range(len(itembtn)):
    markup.add(types.KeyboardButton(itembtn[l]))


@bot.message_handler(content_types=["text"])
def handle_text(message):
    o = []
    for i in range(len(cities_spisok)):
        if cities_spisok[i] in message.text.lower():
            bot.send_message(message.chat.id, cities[cities_spisok[i]])
    for q in range(len(cities_spisok)):
        o.append(cities_spisok[q] not in message.text.lower() and "погод" in message.text.lower())
    if all(o) == True:
        bot.send_message(message.chat.id, "В каком городе нужна погода?", reply_markup=markup)
    else:
        None
    if message.text == "/start":
        bot.send_message(message.chat.id,
                         'Привет я умею:\n  1) показывать погоду,\nдля этого спроси меня о погоде\n  2) показывать погоду там где тебе нужно, если этого города нет в моих вариантах,\nдля этого напиши мне команду: "свой город"\n 3) предсказывать будущее! Для этого просо введи команду /предсказатель \n захочешь закончить предсказания, напиши /стоп')
    elif message.text.lower() == "свой город":
        bot.send_message(message.chat.id,
                         "Напиши название города, который хочешь добавить. Будь внимателен, нужно написать только название города и только на английском")
        bot.register_next_step_handler(message, new_city)
    elif message.text.lower() == "/предсказатель":
        bot.send_message(message.chat.id, "спроси у меня что-то, на что хочешь получить утвердительный ответ")


def new_city(message):
    if " " not in message.text.lower():
        new_url = ("https://www.metaweather.com/api/location/search/?query=" + message.text.lower())
    elif " " in message.text.lower():
        new_url = ("https://www.metaweather.com/api/location/search/?query=" + message.text.lower()[
                                                                              message.text.index(" ") + 1:])
    try:
        city_url = "https://www.metaweather.com/api/location/" + str(get_jsonparset_data(new_url)[0]['woeid']) + "/"
        wenew = get_jsonparset_data(city_url)
        new = weather_dictionary[wenew['consolidated_weather'][0]['weather_state_name']]
        new1 = str(int(wenew['consolidated_weather'][0]['min_temp'])) + '°C', str(
            int(wenew['consolidated_weather'][0]['max_temp'])) + '°C'
        bot.send_message(message.chat.id,
                         message.text + "\nТемпература: " + str(new1[0]) + "-" + str(new1[1]) + "\n" + new + ",\n" +
                         word_weather[new])
        if message.text.lower() not in itembtn_mega and message.text.lower() != "moscow" and message.text.lower() != "berlin" and message.text.lower() != "london":
            cities_spisok.append(message.text.lower())
            very_famous[message.text.lower()] = "https://www.metaweather.com/api/location/" + str(
                get_jsonparset_data(new_url)[0]['woeid']) + "/"
            very_famous1[message.text.lower()] = get_jsonparset_data(very_famous[message.text.lower()])
            very_famous2[message.text.lower()] = weather_dictionary[
                very_famous1[message.text.lower()]['consolidated_weather'][0]['weather_state_name']]
            very_famous3[message.text.lower()] = str(
                int(very_famous1[message.text.lower()]['consolidated_weather'][0]['min_temp'])) + '°C', str(
                int(very_famous1[message.text.lower()]['consolidated_weather'][0]['max_temp'])) + '°C'
            cities[message.text.lower()] = message.text + "\nТемпература: " + str(
                very_famous3[message.text.lower()][0]) + "-" + str(very_famous3[message.text.lower()][1]) + "\n" + \
                                           very_famous2[message.text.lower()] + ",\n" + str(
                word_weather[very_famous2[message.text.lower()]])
            itembtn.append(message.text)
            markup.add(types.KeyboardButton(itembtn[-1]))
            for y in range(len(itembtn)):
                itembtn_mega.append(itembtn[y].lower())
        else:
            print(message.text in itembtn)

    except UnicodeEncodeError:
        bot.send_message(message.chat.id,
                         "Я не могу найти этот город, проверь написание, если не поможет значит его нет в базе данных")
    except IndexError:
        bot.send_message(message.chat.id,
                         "Я не могу найти этот город, проверь написание, если не поможет значит его нет в базе данных")


if __name__ == '__main__':
    bot.polling(none_stop=True)
