from telebot import TeleBot
import requests

TOKEN = "5565566607:AAFhS8jEqHOvy8jyWvyoK0RdXgpIzvAchbI"
MIN_CHAR_COUNT = 20

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
'''Hi! I\'m the News Categorizer Bot.\n\nSend me a news headline and I will tell you, what category such a news belongs to.

I know 15 news categories:
\nACTIVISM & EQUALITY\nCRIME\nCULTURE\nECONOMY\nENTERTAINMENT\nFOOD & DRINK\nHEALTH\nLIFESTYLE\nMISCELLANEOUS\nPOLITICS\nSCIENCE & TECH\nSPORTS\nSTYLE & BEAUTY\nTRAVEL\nWORLD NEWS

Keep in mind that the news I\'ve been trained on were written in the US from 2012 to 2022. I may missenterpret cultural differences and have limited world knowledge. Beware that no AI is 100 percent accurate.

I\'ve been trained on this dataset of over 200.000 real news articles: https://www.kaggle.com/datasets/rmisra/news-category-dataset''')


@bot.message_handler(content_types=["text"])
def send_text(message):
    text = message.text.replace("\n", " ")

    if len(text) > MIN_CHAR_COUNT:
        category = get_predicted_category(text)
        bot.send_message(message.chat.id, f'Category: {category}')
    else:
        bot.send_message(message.chat.id, f'Headline must contain at least {MIN_CHAR_COUNT} characters in order to make a prediction.')


def get_predicted_category(headline):
    # Make API request
    response = requests.post(url=f'https://news-category-app.azurewebsites.net/api/predict?headline={headline}')
    if response.status_code == 200:
        category = response.text
        return category
    else:
        return 'Error: Failed to call API. Please try again later.'


bot.polling(none_stop=True)